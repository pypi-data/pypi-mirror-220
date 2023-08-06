"""Backend for knowledge stored in documents."""


from collections.abc import Iterable, Sequence
import os
from pathlib import Path
from shutil import copyfile
from tempfile import TemporaryDirectory
from typing import Optional
from uuid import uuid4

from llama_index.readers.schema import Document
from llama_hub.file.base import SimpleDirectoryReader

from s3fs import S3FileSystem

from openssm.core.backend.base_backend import BaseBackend


__all__: Sequence[str] = ('DocumentBackend',)


class DocumentBackend(BaseBackend):
    """Backend for knowledge stored in documents."""

    _S3FS: Optional[S3FileSystem] = None

    def __init__(self, document_paths: Iterable[str | Path]):
        """
        Initialize backend with a collection of document paths.
        Local paths and S3 paths are currently supported.
        """
        super().__init__()

        self.document_paths: set[Path | str] = set(document_paths)

        # initialize S3FS if necessary
        if any((isinstance(_, str) and _.startswith('s3://'))
               for _ in self.document_paths):
            self._set_s3fs()

        # TODO: refactor / move this elsewhere to make DocumentBackend adapter-agnostic
        # LlamaIndex-load documents
        self._llama_documents: list[Document] = self._llama_load_documents()

    def __repr__(self) -> str:
        """Return Backend instance's string representation."""
        return (f'DocumentBackend[{len(self.document_paths):,} doc(s): '
                f'{self.document_paths}]')

    @classmethod
    def _set_s3fs(cls):
        if not cls._S3FS:
            cls._S3FS = S3FileSystem(key=os.environ.get('AWS_ACCESS_KEY_ID'),
                                     secret=os.environ.get('AWS_SECRET_ACCESS_KEY'))

    # TODO: refactor / move this elsewhere to make DocumentBackend adapter-agnostic
    def _llama_load_documents(self) -> list[Document]:
        """Load documents with Llama Index."""
        with TemporaryDirectory(suffix=None, prefix=None, dir=None,
                                ignore_cleanup_errors=False) as tmp_dir_path:
            for document_path in self.document_paths:
                # temp file path each document is copied to must retain same extension/suffix
                tmp_file_path: str = os.path.join(tmp_dir_path,
                                                  f'{uuid4()}{Path(document_path).suffix}')

                if isinstance(document_path, str) and document_path.startswith('s3://'):
                    self._S3FS.download(rpath=document_path,
                                        lpath=tmp_file_path,
                                        recursive=False)
                else:
                    copyfile(src=document_path, dst=tmp_file_path,
                             follow_symlinks=True)

            return SimpleDirectoryReader(input_dir=tmp_dir_path,
                                         exclude_hidden=True,
                                         errors='strict',
                                         recursive=True,
                                         required_exts=None,
                                         file_extractor=None,
                                         num_files_limit=None,
                                         file_metadata=None).load_data()
