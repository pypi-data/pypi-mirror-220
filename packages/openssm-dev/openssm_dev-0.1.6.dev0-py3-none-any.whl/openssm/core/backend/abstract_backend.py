from abc import ABC, abstractmethod
from openssm.core.inferencer.abstract_inferencer import AbstractInferencer


# pylint: disable=duplicate-code
class AbstractBackend(ABC):
    @abstractmethod
    def query(self, conversation_id: str, user_input: str) -> list[dict]:
        pass

    @abstractmethod
    def load_all(self):
        """
        Loads all facts, inferencers, and heuristics,
        if appropriate. Some backends may not need to,
        and only load on demand (e.g., a database backend).
        """
        pass

    @abstractmethod
    def add_fact(self, fact: str):
        pass

    @abstractmethod
    def add_inferencer(self, inferencer: AbstractInferencer):
        pass

    @abstractmethod
    def add_heuristic(self, heuristic: str):
        pass

    @abstractmethod
    def list_facts(self):
        pass

    @abstractmethod
    def list_inferencers(self):
        pass

    @abstractmethod
    def list_heuristics(self):
        pass

    @abstractmethod
    def select_facts(self, criteria):
        pass

    @abstractmethod
    def select_inferencers(self, criteria):
        pass

    @abstractmethod
    def select_heuristics(self, criteria):
        pass
