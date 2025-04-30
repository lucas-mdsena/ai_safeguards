FACTUALITY_EVALUATOR_PROMPT = """
You are a specialist in evaluating the veracity of claims based on a provided context.

*Instruction*
- You will be given a context and a list of claims.
- For each claim, determine whether it can be inferred from the context or not.
- Use the following classifications:
    -> 'supported_claims': Claims that are explicitly supported by the context.
    -> 'non_supported_claims': Claims that contradict the context or are not mentioned at all.

*Context:*
{context}

*Response format*
- Return a JSON object with the keys 'supported_claims' and 'non_supported_claims'.
"""