import json
class SPU_AIML_KCB_UserFeedback_Insert_Feedback(object):
    def __init__(self,*args):
        self.ip_Feedback: json = args[0]
        self.op_ErrorMessage = None
        
    def __call__(self):
        return [self.ip_Feedback, self.op_ErrorMessage]
