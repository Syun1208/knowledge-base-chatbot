import dataclasses
from typing import List

@dataclasses.dataclass
class SearchingInformation:
    scores: List[float]
    urls: List[str]
    contexts: List[str]
    indices: List[str]
