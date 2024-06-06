from typing import List

schemes: List[str] = ["http", "https", "file", "data", "view-source"]
#view-source:https://example.com/
class URL:
    def __init__(self, url: str) -> None:
        if url.startswith("data:") or url.startswith("view-source:"):
            self.scheme, url = url.split(":", 1)
        else:
            self.scheme, url = url.split("://", 1)
        assert self.scheme in schemes
        
        if self.scheme == "data":
            self.mime_type, self.data = url.split(",", 1)
        elif self.scheme == "view-source":
            self.source_scheme, url = url.split("://", 1)
            if self.source_scheme == "http":
                self.port: int = 80
            elif self.source_scheme == "https":
                self.port: int = 443
            
            if "/" not in url:
                url = url + "/"
            self.host, url = url.split("/", 1)
            self.path = "/" + url
            
            if ":" in self.host:
                self.host, port = self.host.split(":", 1)
                self.port: int = int(port)
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