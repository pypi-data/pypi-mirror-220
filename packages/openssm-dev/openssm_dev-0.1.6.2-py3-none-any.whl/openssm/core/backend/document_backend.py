"""Backend for knowledge stored in documents."""


from collections.abc import Iterable, Sequence
from pathlib import Path

from openssm.core.backend.base_backend import BaseBackend


__all__: Sequence[str] = ('DocumentBackend',)


class DocumentBackend(BaseBackend):
    """Backend for knowledge stored in documents."""

    def __init__(self, document_paths: Iterable[str | Path]):
        """
        Initialize backend with a collection of document paths.
        Local paths and S3 paths are currently supported.
        """
        super().__init__()
        self.document_paths: set[str | Path] = set(document_paths)

    def __repr__(self) -> str:
        """Return Backend instance's string representation."""
        return f'DocumentBackend[{len(self.document_paths)} docs]'
