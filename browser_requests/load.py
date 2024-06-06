from url import URL
import html
from browser_requests.request_strategy import LocalFileStrategy, UrlDataStrategy, HttpStrategy, ViewSourceStrategy

def show(body: str) -> None:
    in_tag: bool = False
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            print(c, end="")
            
def show_source(body: str) -> None:
    decoded_body = html.unescape(body)
    for c in decoded_body:
        print(c, end="")

def load(url: URL) -> None:
    if url.scheme in ["http", "https", "file"]:
        if url.scheme == "http" or url.scheme == "https":
            body = HttpStrategy.request(url)
        elif url.scheme == "file":
            body = LocalFileStrategy.request(url)
        show(body)
    
    elif url.scheme in ["data", "view-source"]:
        if url.scheme == "data":
            body = UrlDataStrategy.request(url)
        elif url.scheme == "view-source":
            body = ViewSourceStrategy.request(url)
        show_source(body)