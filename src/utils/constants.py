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

class DBModel:
    REQUEST_ID = 'request_id'
    QUESTION = "question"
    ANSWER = "answer"
    FEEDBACK = "feedback"
    CREATED_DATE = "created_date"
    KCB_USER_FEEDBACK_COLS = [REQUEST_ID, QUESTION, ANSWER, FEEDBACK, CREATED_DATE]
    KCB_USER_FEEDBACK = {
        QUESTION: "Q",
        ANSWER: "A",
        FEEDBACK: "F"
    }
