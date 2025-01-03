import dataclasses
from typing import List

@dataclasses.dataclass
class SearchingInfo:
    scores: List[float]
    contexts: List[str]
    indices: List[str]