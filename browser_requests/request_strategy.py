from abc import ABC, abstractmethod
from url import URL

class SchemeStrategy(ABC):
    @abstractmethod
    def request(url: URL) -> str:
        pass
    
class LocalFileStrategy(SchemeStrategy):
    def request(url: URL) -> str:
        #Get file extension
        extension: str = url.path.split(".")[-1]
        
        if extension == "txt":
            with open(url.path[1:], "r") as f:
                content = f.read()
                return content
            
        return "This file extension is not supported yet."