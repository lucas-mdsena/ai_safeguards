# AISafeguards

AISafeguards is a Python package providing easy-to-use metrics for Retrieval-Augmented Generation (RAG) pipelines, including claim extraction and factuality evaluation.

## Installation

```sh
pip install ai-safeguards
```

## Features

- **Claim Extraction:** Extracts factual claims from text using LLMs or regex.
- **Factuality Evaluation:** Assesses if claims are supported by a given context.
- **Faithfulness:** Evaluates how much the RAG answer is grounded within the retrieved context.
- **Answer Relevancy:** Evaluates how much the RAG answer is relevant to the user's query/input.
- **Contextual Relevancy:** Evaluates how much the RAG retrieved context is relevant to the user's query/input.
- Extensible for additional RAG metrics and evaluation via cosine similarity (embeddings support).

## Quick Start

```python
from ai_safeguards import Safeguards

user_query = "What is the significance of the One Ring in The Lord of the Rings, and who forged it?"
llm_answer = "The One Ring, forged by Sauron in Mount Doom around SA 1600, was made to control the other Rings of Power. It grants invisibility and immense power but corrupts its wearer, like Gollum. Its destruction in Mount Doom defeats Sauron, as it holds his essence. However, the Ring was also crafted with Elven assistance in Eregion and could summon Nazgûl to its wearer instantly."
retrieved_context = "The One Ring was forged solely by the Dark Lord Sauron in the fires of Mount Doom in Mordor, circa SA 1600, during the Second Age. Its purpose was to dominate the bearers of the other Rings of Power, which were crafted by the Elves of Eregion under Sauron’s influence (though the Three Elven Rings were made by Celebrimbor alone). The Ring grants invisibility and amplifies power but corrupts its wearer, as seen with Gollum and Frodo. Sauron infused much of his power into the Ring, tying his fate to it; its destruction in Mount Doom at the end of the Third Age caused his downfall. Only the fires of Mount Doom could destroy the Ring."

safeguards = Safeguards(
    api_key='YOUR_OPENAI_API_KEY',
    model_name='gpt-4o-mini'
)

faithfulness_results = safeguards.faithfulness(
  response=llm_answer,
  context=retrieved_context,
  claim_extraction_method='llm',
)

print(f"Faithfulness score: {faithfulness_results.score}")
print(f"Suported claims: {faithfulness_results.supported_claims}")
print(f"Unsuported claims: {faithfulness_results.non_supported_claims}")
```

```sh
Faithfulness score: 0.7777777777777778
Suported claims: ['The One Ring was forged by Sauron in Mount Doom around SA 1600.', 'The One Ring was made to control the other Rings of Power.', 'The One Ring grants invisibility and immense power.', 'The One Ring corrupts its wearer.', 'Gollum is an example of someone corrupted by the One Ring.', 'The destruction of the One Ring in Mount Doom defeats Sauron.', "The One Ring holds Sauron's essence."]
Unsuported claims: ['The One Ring was crafted with Elven assistance in Eregion.', 'The One Ring can summon Nazgûl to its wearer instantly.']
```

## Project Structure

```
ai_safeguards/
    safeguards.py
    agents/
    embedders/
    prompts/
tests/
README.md
pyproject.toml
```

## Contributing

Contributions are welcome! Please open issues or pull requests on [GitHub](https://github.com/seu-usuario/ai_safeguards).

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.