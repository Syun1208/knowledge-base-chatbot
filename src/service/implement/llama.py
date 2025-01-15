import transformers
import torch

from src.service.interface.llm import LLM

class Llama(LLM):
    
    def __init__(
        self,
        model_id: str,
        token: str
    ):
        super(Llama, self).__init__()

        self.pipeline = transformers.pipeline(
            "text-generation", 
            model=model_id, 
            model_kwargs={"torch_dtype": torch.bfloat16}, 
            device_map="auto", 
            token=token
        )

    def generate(self, prompt):
        assistant = self.pipeline(prompt)
        return assistant