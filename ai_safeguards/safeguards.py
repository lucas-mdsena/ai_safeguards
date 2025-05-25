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
        # embedder_model_name: Optional[str] = None, # not working yet
    ) -> None:
        self.api_key = api_key
        self.model_name = model_name
        # self.embedder_model_name = embedder_model_name # not working yet
        
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
 
    def faithfulness(
        self,
        response: str,
        context: str,
        claim_extraction_method: str,
    ) -> Dict[str, Any]:
        """
        Evaluates how much of the answer is grounded within the provided context.

        ### Args:
            - response (str): llm generated answer or output to be evaluated.
            - context (str): retrieved context to support or refute the claims in the response.
            - claim_extraction_method (str): method to extract claims from the response ('llm' or 'regex').

        ### Returns:
            - (dict): contains the faithfulness score, supported claims, and non-supported claims.
        """
        response_claims = self.extract_claims(text=response, extraction_method=claim_extraction_method)
        results = self.eval_factuality(claims=response_claims, context=context)
        faithfulness_score = len(results["supported_claims"]) / len(response_claims)

        return {
            "faithfulness_score": faithfulness_score,
            "supported_claims": results["supported_claims"],
            "non_supported_claims": results["non_supported_claims"]
        }

    def answer_relevancy(
        self,
        response: str,
        query: str,
        claim_extraction_method: str,
    ) -> Dict[str, Any]:
        """
        Evaluates how much the of the answer is relevant to the query/input.

        ### Args:
            - response (str): llm generated answer or output to be evaluated.
            - query (str): user query to it's RAG pipeline, used to support or refute the claims in the response.
            - claim_extraction_method (str): method to extract claims from the response ('llm' or 'regex').

        ### Returns:
            - (dict): contains the answer relevancy score, supported claims, and non-supported claims.
        """
        response_claims = self.extract_claims(text=response, extraction_method=claim_extraction_method)
        results = self.eval_factuality(claims=response_claims, context=query)
        answer_relevancy_score = len(results['supported_claims']) / len(response_claims)

        return {
            "answer_relevancy_score": answer_relevancy_score,
            "supported_claims": results["supported_claims"],
            "non_supported_claims": results["non_supported_claims"]
        }

    def contextual_relevancy(
        self,
        context: str,
        query: str,
        claim_extraction_method: str,
    ) -> Dict[str, Any]:
        """
        Evaluates how much the of the retrieved context is relevant to the query/input.

        ### Args:
            - context (str): retrieved context from user's RAG pipeline.
            - query (str): user query to it's RAG pipeline, used to support or refute the claims in the context.
            - claim_extraction_method (str): method to extract claims from the context ('llm' or 'regex').

        ### Returns:
            - (dict): contains the context relevancy score, supported claims, and non-supported claims.
        """
        context_claims = self.extract_claims(text=context, extraction_method=claim_extraction_method)
        results = self.eval_factuality(claims=context_claims, context=query)
        contextual_relevancy_score = len(results['supported_claims']) / len(context_claims)

        return {
            "contextual_relevancy_score": contextual_relevancy_score,
            "supported_claims": results["supported_claims"],
            "non_supported_claims": results["non_supported_claims"]
        }

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
