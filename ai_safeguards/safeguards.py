import re
import json
from typing import List, Dict, Any

import numpy as np
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity

from prompts import CLAIM_EXTRACTOR_PROMPT



class Safeguards:
    """A class to run RAG metrics
    
    ### Attributes:
        - model_name (str): LLM model name (currently only GPT models are avaiable)
        - api_key (str): LLM provider API Key
    
    ### Methods:
        - extract_claims: extract the claims/statements from a given text.
    """
    def __init__(
        self,
        model_name: str,
        api_key: str
    ) -> None: 
        self.model_name = model_name
        self.api_key = api_key

    def extract_claims(
        self, 
        text: str, 
        extraction_method: str
    ) -> List[str]:
        """Split a paragraph into claims.

        ### Args
            - text (str): text paragraph to be splitted by sentences (claims)
            - extraction_method (str): how the claims will be extracted (llm, regex)
        
        ### Returns:
            - (List[str]): a list of sentences (claims)

        ### Note:
            The Regex pattern aims to finds a whitespace that:
            - is preceded by a period, exclamation or interrogation
            - is not preceded by the pattern word.word.character
            - is not predece by abreviation like 'Dr.'
        """
        if extraction_method == "regex":
            ending_patterns = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s'
            claims = re.split(ending_patterns, text.strip())

            return claims
        
        if extraction_method == "llm":

            # to-do: import this from a module
            # to-do: create a Gemini API call
            openai_client = OpenAI(api_key=self.api_key)
            llm_output = openai_client.responses.create(
                model=self.model_name,
                instructions=CLAIM_EXTRACTOR_PROMPT,
                input=text,
                temperature=0,
                text={
                    "format": {
                        "type": "json_schema",
                        "name": "claims_list",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "claims": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                }
                            },
                            "required": ["claims"],
                            "additionalProperties": False
                        },
                        "strict": True
                    }
                }
            )
            claims = json.loads(llm_output.output_text)['claims']
            
            return claims