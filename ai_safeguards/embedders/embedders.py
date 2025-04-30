from typing import List
from openai import OpenAI



# TODO: create a Google embedding API call and a sigle Embedder class for all API calls
class Embedder:
    def __init__(
        self,
        api_key: str, 
        model_name: str, 
        input_texts: List[str],
    ) -> None:
        self.api_key = api_key
        self.model_name = model_name
        self.input_texts = input_texts
        self.openai_client = OpenAI(api_key=self.api_key)

    def __call__(self):
        embeddings = {}
        for i, text in enumerate(self.input_texts):
            response = self.openai_client.embeddings.create(
                input=text,
                model=self.model_name
            )
            embeddings[f'embedding_{i}'] = response.data[0].embedding
        
        return embeddings
