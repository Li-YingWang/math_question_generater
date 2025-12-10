from abc import ABC, abstractmethod

class BasePlugin(ABC):
    @abstractmethod
    def get_name(self) -> str:
        """回傳題型名稱"""
        pass

    @abstractmethod
    def generate(self, count: int) -> list[tuple[str, str]]:
        """產生指定數量的題目與解答，回傳 (question, answer) 的 list"""
        pass
