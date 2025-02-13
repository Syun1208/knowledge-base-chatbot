CREATE DEFINER=`AIMLOwner`@`%` PROCEDURE `SPU_AIML_KCB_UserFeedback_Get_Feedback`(    
    OUT op_ErrorMessage     VARCHAR(200)
)
    SQL SECURITY INVOKER
BEGIN
    /*
        Created:    20250601@Hani.Nguyen
        Task:       Get Feedback [Redmine ID: #0000]
        DB:         SPU_AIML
        Original: 

        Revisions:
            - 20250601@Hani.Nguyen: Created [Redmine ID: #0000]
            
        Example:call SPU_AIML.SPU_AIML_KCB_UserFeedback_Get_Feedback(@msg);    
            
    */ 

    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN         
        GET DIAGNOSTICS CONDITION 1 op_ErrorMessage = MESSAGE_TEXT;
    END;

    SELECT
		p.RequestID,
		p.Question,
        p.Answer,
		p.Feedback,
        p.CreatedDate
    FROM SPU_AIML.KCB_UserFeedback AS p;
END
