import dataclasses
from typing import List

@dataclasses.dataclass
class SearchingInfo:
    scores: List[float]
    urls: List[str]
    contexts: List[str]
    indices: List[str]