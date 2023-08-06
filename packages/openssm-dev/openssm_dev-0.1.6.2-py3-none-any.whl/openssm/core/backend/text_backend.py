"""Text backend."""


from openssm.core.inferencer.abstract_inferencer import AbstractInferencer
from openssm.core.backend.base_backend import BaseBackend


class TextBackend(BaseBackend):
    """Text backend."""

    def __init__(self):
        super().__init__()
        self.texts = set()

    def __repr__(self) -> str:
        """Return Backend instance's string representation."""
        return 'TextBackend'

    # pylint: disable=unused-argument
    def query(self, conversation_id: str, user_input: str) -> list[dict]:
        responses = [{"item": text} for text in self.texts]
        return responses

    def all_texts(self):
        return self.texts

    def add_fact(self, fact: str):
        super().add_fact(fact)
        self.texts.add(f"fact: {fact}")

    def add_inferencer(self, inferencer: AbstractInferencer):
        super().add_inferencer(inferencer)
        self.texts.add(f"inferencer: {inferencer}")

    def add_heuristic(self, heuristic: str):
        super().add_heuristic(heuristic)
        self.texts.add(f"heuristic: {heuristic}")
