from dataclasses import dataclass
from typing import Callable, Protocol

class VerifyFn(Protocol):
    def __call__(self, password: str, hashed: str, /) -> bool: ...

@dataclass
class HashService:
    hash_fun: Callable[[str], str]
    
    verify: VerifyFn
