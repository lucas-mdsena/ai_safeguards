# AISafeguards

AISafeguards is a Python package providing easy-to-use metrics for Retrieval-Augmented Generation (RAG) pipelines, including claim extraction and factuality evaluation.

## Installation

```sh
pip install ai-safeguards
```

## Features

- **Claim Extraction:** Extracts factual claims from text using LLMs or regex.
- **Factuality Evaluation:** Assesses if claims are supported by a given context.
- **Embeddings Support:** (Planned) Compute cosine similarity between claims and context.
- Extensible for additional RAG metrics.

## Quick Start

```python
from ai_safeguards import Safeguards

safeguards = Safeguards(
    api_key='YOUR_OPENAI_API_KEY',
    model_name='gpt-4o-mini'
)

text = "Water boils at 100 degrees Celsius at sea level. At higher altitudes, water boils at a lower temperature."
claims = safeguards.extract_claims(text, extraction_method='llm')
print("Extracted claims:", claims)

context = "At sea level, water boils at 100°C. At higher altitudes, the boiling point decreases."
factuality = safeguards.eval_factuality(claims, context)
print("Factuality evaluation:", factuality)
```

## API Reference

### `Safeguards` ([ai_safeguards/safeguards.py](ai_safeguards/safeguards.py))

#### Initialization

```python
Safeguards(api_key: str, model_name: str, embedder_model_name: str = None)
```

#### Methods

- `extract_claims(text: str, extraction_method: str = 'llm') -> List[str]`  
  Extracts claims from text using LLM or regex.

- `eval_factuality(claims: List[str], context: str) -> Dict[str, List[str]]`  
  Evaluates which claims are supported by the context.

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