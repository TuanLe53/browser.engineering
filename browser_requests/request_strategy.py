from abc import ABC, abstractmethod
from url import URL

class SchemeStrategy(ABC):
    @abstractmethod
    def request(url: URL) -> str:
        pass
    
