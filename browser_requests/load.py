from url import URL

def show(body: str) -> None:
    in_tag: bool = False
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            print(c, end="")
            
def load(url: URL) -> None:
    pass