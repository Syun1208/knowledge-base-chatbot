import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from src.service.interface.kcb_supporter.llm import LLM


class ViMistral(LLM):
    
    def __init__(
        self,
        model_id: str,
        token: str
    ) -> None:
        super(ViMistral, self).__init__()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_id, token=token)

        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=torch.bfloat16, # change to torch.float16 if you're using V100
            device=self.device,
            token=token,
            low_cpu_mem_usage=True,
            use_cache=True,
        )
        
    def generate(self, prompt: str) -> str:
        system_prompt = "Bạn là một trợ lí Tiếng Việt nhiệt tình và trung thực. Hãy luôn trả lời một cách hữu ích nhất có thể, đồng thời giữ an toàn.\n"
        system_prompt += "Câu trả lời của bạn không nên chứa bất kỳ nội dung gây hại, phân biệt chủng tộc, phân biệt giới tính, độc hại, nguy hiểm hoặc bất hợp pháp nào. Hãy đảm bảo rằng các câu trả lời của bạn không có thiên kiến xã hội và mang tính tích cực."
        system_prompt += "Nếu một câu hỏi không có ý nghĩa hoặc không hợp lý về mặt thông tin, hãy giải thích tại sao thay vì trả lời một điều gì đó không chính xác. Nếu bạn không biết câu trả lời cho một câu hỏi, hãy trẳ lời là bạn không biết và vui lòng không chia sẻ thông tin sai lệch."
        
        conversation = [{"role": "system", "content": system_prompt }]  
        conversation.append({"role": "user", "content": prompt})
        
        input_ids = self.tokenizer.apply_chat_template(conversation, return_tensors="pt").to(self.device)

        out_ids = self.model.generate(
            input_ids=input_ids,
            max_new_tokens=768,
            do_sample=True,
            top_p=0.95,
            top_k=40,
            temperature=0.1,
            repetition_penalty=1.05
        )
        assistant = self.tokenizer.batch_decode(out_ids[:, input_ids.size(1): ], skip_special_tokens=True)[0].strip()

        return assistant
