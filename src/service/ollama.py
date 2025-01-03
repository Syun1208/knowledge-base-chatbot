import requests
from typing import List
import sys
sys.path.append('D:\Desktop\chatbot4group')
from src.interface.llm import LLM


class Ollama(LLM):
    def __init__(self) -> None:
        super(Ollama, self).__init__()
        self.url = 'http://localhost:5000/api/generate'

    def generate(self, prompt: str, conversation: List[str]) -> str:
        response = requests.post(
            self.url,
            json={
                'prompt': prompt,
                'context': conversation,
            },
            stream=True
        )
        response.raise_for_status()

        return response
        
#         new_context = conversation
#         for line in response.iter_lines():
#             body = json.loads(line)
#             response_part = body.get('response', '')
#             print(response_part, end='', flush=True)

#             if 'error' in body:
#                 raise Exception(body['error'])

#             if body.get('done', False):
#                 new_context = body['context']
#                 break

#         return new_context


def main():
    model_name = 'llama3.2'
    ollama = Ollama()
 
        
    next_context = []
    while True:
        user_input = input("Enter a prompt: ")
        if not user_input:
            exit()
        print()
        response = ollama.generate(user_input, next_context)
        print(response)
        print()


if __name__ == "__main__":
    main()
