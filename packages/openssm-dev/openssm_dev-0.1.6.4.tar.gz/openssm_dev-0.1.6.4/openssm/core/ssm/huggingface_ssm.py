"""Falcon SSMs."""


from typing import Optional
from openssm.core.ssm.base_ssm import BaseSSM
from openssm.core.adapter.abstract_adapter import AbstractAdapter
from openssm.core.backend.abstract_backend import AbstractBackend
from openssm.core.slm.huggingface_slm import Falcon7bSLM
from openssm.core.slm.huggingface_slm import Falcon7bSLMLocal


class Falcon7bSSM(BaseSSM):
    """Falcon 7-billion-parameter SSM."""

    def __init__(self,
                 adapter: Optional[AbstractAdapter] = None,
                 backends: Optional[list[AbstractBackend]] = None):
        super().__init__(Falcon7bSLM(), adapter, backends)

    def __repr__(self) -> str:
        """Return SSM instance's string representation."""
        return (f'Falcon7bSSM[adapter: {self.get_adapter()} | '
                f'backends: {self.get_backends()}]')


class Falcon7bSSMLocal(BaseSSM):
    """Falcon 7-billion-parameter SSM locally deployed."""

    def __init__(self,
                 adapter: Optional[AbstractAdapter] = None,
                 backends: Optional[list[AbstractBackend]] = None):
        super().__init__(Falcon7bSLMLocal(), adapter, backends)

    def __repr__(self) -> str:
        """Return SSM instance's string representation."""
        return (f'Falcon7bSSMLocal[adapter: {self.get_adapter()} | '
                f'backends: {self.get_backends()}]')
