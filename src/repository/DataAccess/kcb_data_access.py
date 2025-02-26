from src.repository.DataAccess.base_exec_sp import SPExecutor
from src.repository.DataAccess.Model.SPU_AIML.SPU_AIML_KCB_UserFeedback_Get_Feedback import SPU_AIML_KCB_UserFeedback_Get_Feedback
from src.repository.DataAccess.Model.SPU_AIML.SPU_AIML_KCB_UserFeedback_Insert_Feedback import SPU_AIML_KCB_UserFeedback_Insert_Feedback

class WasaAimlKCBSPExecutor(SPExecutor):
    
    def get_feedback(self):
        sp_result = self.manage_sp_operation(
            "SPU_AIML_KCB_UserFeedback_Get_Feedback", 
            lambda: SPU_AIML_KCB_UserFeedback_Get_Feedback()
        )
        
        return sp_result
    
    def insert_feedback(self, ip_ServiceID, ip_Feedback):
        self.manage_sp_operation(
            "SPU_AIML_KCB_UserFeedback_Insert_Feedback", 
            lambda: SPU_AIML_KCB_UserFeedback_Insert_Feedback(
                ip_ServiceID, 
                ip_Feedback
            )
        )

