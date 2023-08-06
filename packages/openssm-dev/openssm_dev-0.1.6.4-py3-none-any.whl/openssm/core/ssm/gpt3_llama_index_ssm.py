"""SSM with GPT3-based SLM and LlamaIndex-based adapter."""


from openssm.core.ssm.base_ssm import BaseSSM
from openssm.core.slm.openai_slm import GPT3ChatCompletionSLM
from openssm.core.adapter.llama_index_adapter import LlamaIndexAdapter
from openssm.core.backend.abstract_backend import AbstractBackend


class GPT3LlamaIndexSSM(BaseSSM):
    """SSM with GPT3-based SLM and LlamaIndex-based adapter."""

    def __init__(self, backends: list[AbstractBackend]):
        slm = GPT3ChatCompletionSLM()
        adapter = LlamaIndexAdapter(backends)
        super().__init__(slm, adapter, backends)

    def __repr__(self) -> str:
        """Return SSM instance's string representation."""
        return f'GPT3LlamaIndexSSM[backends: {self.get_backends()}]'
