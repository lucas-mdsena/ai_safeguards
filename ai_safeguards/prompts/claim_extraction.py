CLAIM_EXTRACTOR_PROMPT = """
You are a specialist in analyzing responses.

*Instruction*
- Based on the provided text, extract a list of claims that can be inferred from the given text.

*EXAMPLE*
- Sample text:
"Water boils at 100 degrees Celsius at sea level. This boiling point can change depending on atmospheric pressure. For instance, at higher altitudes, where the pressure is lower, water boils at a lower temperature. Conversely, in a pressure cooker, the boiling point increases because the pressure is higher."

- Extracted claims:
{{
    "claims": [
        "Water boils at 100°C at sea level.", 
        "Atmospheric pressure affects the boiling point of water.", 
        "At higher altitudes, water boils at a lower temperature.", 
        "In a pressure cooker, water boils at a temperature higher than 100°C.", 
        "Lower atmospheric pressure leads to a lower boiling point.", 
        "Higher atmospheric pressure leads to a higher boiling point."]
}}

*Response format*
Return your response as a JSON object.
"""