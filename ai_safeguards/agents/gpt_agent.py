import json
from typing import Dict, List
from openai import OpenAI



# TODO: create a Gemini API call and a sigle Agent class for all LLM calls
class GPTAgent:
    def __init__(
        self, 
        api_key: str, 
        model_name: str, 
        input_text: str, 
        instructions_prompt: str,
        model_settings: Dict[str, List[str]]
    ) -> None:
        self.api_key = api_key
        self.model_name = model_name
        self.input_text = input_text
        self.instructions_prompt = instructions_prompt
        self.model_settings = model_settings
        self.openai_client = OpenAI(api_key=self.api_key)

    def __call__(self):
        gpt_output = self.openai_client.responses.create(
            model=self.model_name,
            instructions=self.instructions_prompt,
            input=self.input_text,
            temperature=0,
            text=self.model_settings
        )
        return json.loads(gpt_output.output_text)

