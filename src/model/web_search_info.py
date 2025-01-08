import dataclasses

@dataclasses.dataclass
class WebSearchInfo:
    url: str
    page_content: str
    