from abc import ABC, abstractmethod
from url import URL
import html
import socket
import ssl

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
    
class UrlDataStrategy(SchemeStrategy):
    def request(url: URL) -> str:
        if url.mime_type == "text/html":
            return url.data
        
        return "This mime type is not supported."
    
class HttpStrategy(SchemeStrategy):
    def request(url: URL) -> str:
        #Create socket
        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP,
        )
        #Connect to server        
        s.connect((url.host, url.port))
        
        #Wrap socket with ctx if host == "https"
        if url.scheme == "https":
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=url.host)
        
        #Create request
        request = f"GET {url.path} HTTP/1.1\r\n"
        request += f"HOST: {url.host}\r\n"
        request += "Connection: close\r\n"
        request += f"USER-AGENT: PyBrowser/1.0\r\n"
        request += "\r\n"
        
        #Send request
        s.send(request.encode("utf-8"))  

        #Get response
        response = s.makefile("r", encoding="utf8", newline="\r\n")
        status_line = response.readline()
        version, status, explanation = status_line.split(" ", 2)
        
        #Get headers from response
        response_headers = {}
        while True:
            line = response.readline()
            if line == "\r\n": break
            
            header, value = line.split(":", 1)
            response_headers[header.casefold()] = value.strip()
            
        assert "transfer-encoding" not in response_headers
        assert "content-encoding" not in response_headers
        
        #Get body from response
        content = response.read()
        s.close()
        
        return content