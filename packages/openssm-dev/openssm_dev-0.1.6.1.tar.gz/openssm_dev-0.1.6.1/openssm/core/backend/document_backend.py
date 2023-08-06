"""Backend for knowledge stored in documents."""


from collections.abc import Iterable, Sequence
from pathlib import Path

from openssm.core.backend.base_backend import BaseBackend


__all__: Sequence[str] = ('DocumentBackend',)


class DocumentBackend(BaseBackend):
    """Backend for knowledge stored in documents."""

    def __init__(self, document_paths: Iterable[str | Path]):
        super().__init__()
        self.document_paths: set[str | Path] = set(document_paths)
