from typing import List

schemes: List[str] = ["http", "https", "file", "data"]

class URL:
    def __init__(self, url: str) -> None:
        if url.startswith("data:"):
            self.scheme, url = url.split(":", 1)
        else:
            self.scheme, url = url.split("://", 1)
        assert self.scheme in schemes
        
        if self.scheme == "data":
            self.mime_type, self.data = url.split(",", 1)
        else:
            if self.scheme == "http":
                self.port: int = 80
            elif self.scheme == "https":
                self.port: int = 443
                
            if "/" not in url:
                url = url + "/"
            self.host, url = url.split("/", 1)
            self.path = "/" + url
            
            if ":" in self.host:
                self.host, port = self.host.split(":", 1)
                self.port: int = int(port)