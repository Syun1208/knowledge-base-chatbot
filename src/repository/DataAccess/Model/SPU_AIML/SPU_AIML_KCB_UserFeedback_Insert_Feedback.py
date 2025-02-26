from typing import Dict
class SPU_AIML_KCB_UserFeedback_Insert_Feedback(object):
    def __init__(self,*args):
        print(args)
        self.ip_ServiceID: int = args[0]
        self.ip_Feedback: Dict[str, str] = args[1]
        self.op_ErrorMessage = None
        
    def __call__(self):
        return [
            self.ip_ServiceID,
            self.ip_Feedback, 
            self.op_ErrorMessage
        ]
