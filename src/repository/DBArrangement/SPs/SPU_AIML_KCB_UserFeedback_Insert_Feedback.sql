DELIMITER $$
USE SPU_AIML $$
DROP PROCEDURE IF EXISTS `SPU_AIML`.`SPU_AIML_KCB_UserFeedback_Insert_Feedback`$$

CREATE DEFINER=`AIMLOwner`@`%` PROCEDURE `SPU_AIML_KCB_UserFeedback_Insert_Feedback`(
	IN 	ip_Feedback 		JSON,
    OUT op_ErrorMessage 	VARCHAR(200)
)
    SQL SECURITY INVOKER
BEGIN
	/*
		Created:	20251202@Hani.Nguyen
		Task:		Insert Predict Info [Redmine ID: #0000]
		DB:			SPU_AIML
		Original: 

		Revisions:
			- 20251202@Hani.Nguyen: Created [Redmine ID: #0000]
            
		Example:
			CALL SPU_AIML.SPU_AIML_KCB_UserFeedback_Insert_Feedback ('[{"Q":"What is AI?", "A":"Artificial Intelligence is...", "F":"Positive"}]','20230509',@msg);    
	*/ 

    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN         
        GET DIAGNOSTICS CONDITION 1 op_ErrorMessage = MESSAGE_TEXT;
    END;

	INSERT INTO SPU_AIML.KCB_UserFeedback(Question, Answer, Feedback, CreatedDate)
    SELECT  
        tmpTable.Question,
        tmpTable.Answer,
        tmpTable.Feedback,
        CURRENT_TIMESTAMP 
	FROM JSON_TABLE(ip_Feedback,
        "$[*]" COLUMNS(
            Question TEXT PATH "$.Q",
            Answer   TEXT PATH "$.A",
            Feedback TEXT PATH "$.F"
        )
    ) AS tmpTable;
    
END$$
DELIMITER ;


