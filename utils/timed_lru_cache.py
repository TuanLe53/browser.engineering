from functools import lru_cache, wraps
from datetime import datetime, timedelta

def timed_lru_cache(minutes: int, maxsize: int = 128):
    def wrapper_cache(func):
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(minutes=minutes)
        func.expiration = datetime.now() - func.lifetime
        
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if datetime.now() >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.now() + func.lifetime
            
            return func(*args, **kwargs)
        
        return wrapped_func
    
    return wrapper_cache