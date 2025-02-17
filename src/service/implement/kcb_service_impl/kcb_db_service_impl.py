import os
import json
import time
import glob
import pandas as pd
from typing import Optional
from src.utils.constants import DBModel as db
from src.repository.DataAccess.data_access_connection import BaseRepository
from src.repository.DataAccess.kcb_data_access import WasaAimlKCBSPExecutor
from src.service.interface.kcb_service.kcb_db_service import DataService
from src.utils.constants import DBModel as db
class KCBDataServiceImpl(DataService):
    def __init__(
        self,
        wasa_aiml_connector: BaseRepository):
        self.wasa_aiml_executor = WasaAimlKCBSPExecutor(wasa_aiml_connector)

    def get_feedback(self) -> pd.DataFrame:
        dba_result = self.wasa_aiml_executor.get_feedback()
        if (dba_result is None):
            return pd.DataFrame()
        else:
            table = [tuple(record) for record in dba_result[0]]
            feedback_df = pd.DataFrame(table, columns=db.KCB_USER_FEEDBACK_COLS)
            return feedback_df
        
    def insert_feedback(self, question: str, answer:str, feedback:str) -> None:
        try:
            ip_Feedback = json.dumps([{
                db.KCB_USER_FEEDBACK[db.QUESTION]: question,
                db.KCB_USER_FEEDBACK[db.ANSWER]: answer,
                db.KCB_USER_FEEDBACK[db.FEEDBACK]: feedback
            }])
            self.wasa_aiml_executor.insert_feedback(ip_Feedback)
        except Exception as e:
            raise ValueError(e)
