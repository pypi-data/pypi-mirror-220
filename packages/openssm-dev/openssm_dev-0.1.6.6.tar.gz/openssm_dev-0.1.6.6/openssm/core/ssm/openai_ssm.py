"""OpenAI-based SSMs."""


from typing import Optional
from openssm.core.ssm.base_ssm import BaseSSM
from openssm.core.slm.openai_slm import GPT3CompletionSLM
from openssm.core.slm.openai_slm import GPT3ChatCompletionSLM
from openssm.core.adapter.abstract_adapter import AbstractAdapter
from openssm.core.backend.abstract_backend import AbstractBackend


class GPT3CompletionSSM(BaseSSM):
    """GPT3-based Completion SSMs."""

    def __init__(self,
                 adapter: Optional[AbstractAdapter] = None,
                 backends: Optional[list[AbstractBackend]] = None):
        super().__init__(GPT3CompletionSLM(), adapter, backends)

    def __repr__(self) -> str:
        """Return SSM instance's string representation."""
        return (f'GPT3CompletionSSM[adapter: {self.get_adapter()} | '
                f'backends: {self.get_backends()}]')


class GPT3ChatCompletionSSM(BaseSSM):
    """GPT3-based Chat Completion SSMs."""

    def __init__(self,
                 adapter: Optional[AbstractAdapter] = None,
                 backends: Optional[list[AbstractBackend]] = None):
        super().__init__(GPT3ChatCompletionSLM(), adapter, backends)

    def __repr__(self) -> str:
        """Return SSM instance's string representation."""
        return (f'GPT3ChatCompletionSSM[adapter: {self.get_adapter} | '
                f'backends: {self.get_backends}]')
