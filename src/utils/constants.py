from pathlib import Path
HEADERS_TO_SPLIT_ON = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
    ("####", "Header 4"),
    ("#####", "Header 5"),
]
FILE = Path(__file__).resolve()
WORK_DIR = FILE.parents[2]
