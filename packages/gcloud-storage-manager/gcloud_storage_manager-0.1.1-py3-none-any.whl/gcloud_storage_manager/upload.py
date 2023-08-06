from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import List, Tuple

from gcloud_storage_manager.base import BaseStorageFileHandler, FileType
from gcloud_storage_manager.std_logging import logging


@dataclass
class UploadResult:
    success_count: int
    failure_count: int
    failed_keys: List[str]
    invalid_keys: List[str] = field(default_factory=list)

    @property
    def has_errors(self):
        return len(self.failed_keys) > 0 or len(self.invalid_keys) > 0


class StorageFileUploader(BaseStorageFileHandler):
    """
    Upload files to cloud storage.

    e.g.
    uploader = StorageFileUploader(
        bucket_name="test_bucket",
        dir_name="test_dir",
        dir_name_child="test_child_dir",
        file_type=FileType(".svg", "image/svg+xml"),
        credentials_path="path/to/creds.json",
    )
    result = uploader.upload_files(validated_files)
    """

    def __init__(
        self,
        bucket_name: str,
        dir_name: str,
        dir_name_child: str,
        file_type: FileType,
        credentials_path: str,
        max_workers=5,
    ):
        super().__init__(
            bucket_name, dir_name, dir_name_child, file_type, credentials_path
        )
        self.max_workers = max_workers

    def upload_files(
        self,
        validated_files: List[Tuple[str, bytes]],  # (file_path, file_content)
        overwrite: bool = False,
    ) -> UploadResult:
        logging.info("Start of uploading files to cloud storage")

        success_count = 0
        failure_count = 0
        failed_keys: List[str] = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures_to_file_paths = {
                executor.submit(
                    self._upload_file, file_path, file_content, overwrite
                ): file_path
                for file_path, file_content in validated_files
            }
            for future in as_completed(futures_to_file_paths):
                file_path = futures_to_file_paths[future]
                try:
                    success = future.result()
                    if success:
                        success_count += 1
                    else:
                        failure_count += 1
                        failed_keys.append(file_path)
                except Exception as e:
                    failure_count += 1
                    failed_keys.append(file_path)
                    logging.info(f"Error uploading '{file_path}': {e}")

        logging.info("End of uploading files to cloud storage")

        return UploadResult(success_count, failure_count, failed_keys)

    def _upload_file(
        self, file_path: str, file_content: bytes, overwrite: bool
    ) -> bool:
        """
        Upload a file to cloud storage.

        e.g.
        file_path = "test_path"
        file_content = b"test_content"
        overwrite = False
        uploader._upload_file(file_path, file_content, overwrite)
        """
        if not self._file_match(file_path):
            return False
        full_file_path = f"{self.storage_base_dir}/{file_path}"

        try:
            blob = self.bucket.blob(full_file_path)
            if blob.exists() and not overwrite:
                return False
            blob.upload_from_string(
                file_content, content_type=self.file_type.content_type
            )
            return True
        except Exception as e:
            logging.info(f"Error uploading '{full_file_path}': {e}")
            return False
