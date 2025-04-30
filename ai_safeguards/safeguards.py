import re
import json
from typing import List, Dict, Any, Optional
import numpy as np
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity

from .prompts import CLAIM_EXTRACTOR_PROMPT, FACTUALITY_EVALUATOR_PROMPT
from .agents import GPTAgent, gpt_claims_settings, gpt_factuality_settings
from .embedders import Embedder



class Safeguards:
    """A class to run RAG metrics
    
    ### Attributes:
        - model_name (str): LLM model name (currently only GPT models are avaiable).
        - api_key (str): LLM provider API Key.
    
    ### Methods:
        - extract_claims: extract the claims/statements from a given text.
    """
    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: Optional[str] = None,
        embedder_model_name: Optional[str] = None,
    ) -> None:
        self.api_key = api_key
        self.model_name = model_name
        self.embedder_model_name = embedder_model_name
        
    def extract_claims(
        self, 
        text: str, 
        extraction_method: str = 'llm'
    ) -> List[str]:
        """Split a paragraph into claims.

        ### Args
            - text (str): text paragraph to be splitted by sentences (claims).
            - extraction_method (str): how the claims will be extracted (llm, regex).
        
        ### Returns:
            - (List[str]): a list of sentences (claims).

        ### NOTE:
            The Regex pattern aims to finds a whitespace that:
            - is preceded by a period, exclamation or interrogation;
            - is not preceded by the pattern word.word.character;
            - is not predece by abreviation like 'Dr.'.
        """
        if extraction_method == "regex":
            ending_patterns = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s'
            claims = re.split(ending_patterns, text.strip())

            return claims
        
        if extraction_method == "llm":
            # TODO: create a Gemini API call and a sigle Agent class for all LLM calls
            agent = GPTAgent(
                api_key=self.api_key,
                model_name=self.model_name,
                input_text=text,
                instructions_prompt=CLAIM_EXTRACTOR_PROMPT,
                model_settings=gpt_claims_settings
            )
            llm_output = agent()
            claims = llm_output['claims']

            return claims

    # NOTE: compute_cosine_similarity is not working yet
    # def compute_cosine_similarity(
    #     self, 
    #     claims: List[str], 
    #     context: str
    # ) -> float:
    #     """Computes the cosine similarity for claims and context embeddings.

    #     ### Args
    #         - claims (List[str]): claims extracted from LLM agent response.
    #         - context (str): retrived context to support or refute the extracted claims.

    #     ### Returns:
    #         - (float): computed cosine similarity.
    #     """
    #     embedder = Embedder(
    #         api_key=self.api_key, 
    #         model_name=self.embedder_model_name,
    #         input_texts=[claims, context]
    #     )
    #     embeddings = embedder()

    #     cos_sim = []
    #     context_array = np.array(embeddings[1]).reshape(1, -1)
    #     for c in embeddings:
    #         claim_array = np.array(c).reshape(1, -1)
    #         cos_sim.append(cosine_similarity(claim_array, context_array)[0][0])
        
    #     return cos_sim 

    def eval_factuality(
        self, 
        claims: List[str], 
        context: str
    ) -> Dict[str, List[str]]:
        """Evaluates claims factuality based on the given context.

        ### Args:
            - claims (List[str]): claims extracted from LLM agent response.
            - context (str): retrived context to support or refute the extracted claims.

        ### Returns:
            - (dict): supported claims and unsupported claims.
        """
        agent = GPTAgent(
                api_key=self.api_key,
                model_name=self.model_name,
                input_text="\n> ".join(claims),
                instructions_prompt=FACTUALITY_EVALUATOR_PROMPT.format(context=context),
                model_settings=gpt_factuality_settings
            )
        llm_output = agent()
        factuality = llm_output

        return factuality  
    
    # TODO: implements the methods bellow
    def faithfulness(self):
        """How much the answer is grounded in the context."""
        pass

    def answer_relevancy(self):
        """How much the answer is relevant to the query/input."""
        pass

    def contextual_relevancy(self):
        """How much the retrieved context is relevant to the query/input."""
        pass