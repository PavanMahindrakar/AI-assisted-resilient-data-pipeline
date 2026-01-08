# core/response_parser.py

# 🔹 SUPPORTING MODULE: LLM Response Normalization
# Centralizes parsing and validation of raw LLM responses into a consistent
# sentiment + confidence schema. Ensures resilience against malformed or
# non-JSON model outputs while keeping parsing logic decoupled from the DAG
# and LLM engine implementation.

import json

def parse_ollama_response(response_text: str) -> dict:
    """
    Safely parse Ollama LLM response into sentiment + confidence.
    Falls back gracefully if model output is malformed.
    """
    try:
        clean_text = response_text.strip()

        # Handle ```json blocks
        if clean_text.startswith("```"):
            lines = clean_text.split("\n")
            clean_text = "\n".join(lines[1:-1])

        parsed = json.loads(clean_text)

        sentiment = parsed.get("sentiment", "NEUTRAL").upper()
        confidence = float(parsed.get("confidence", 0.0))

        if sentiment not in {"POSITIVE", "NEGATIVE", "NEUTRAL"}:
            sentiment = "NEUTRAL"

        return {
            "label": sentiment,
            "score": max(0.0, min(confidence, 1.0))
        }

    except Exception:
        upper = response_text.upper()
        if "POSITIVE" in upper:
            return {"label": "POSITIVE", "score": 0.75}
        if "NEGATIVE" in upper:
            return {"label": "NEGATIVE", "score": 0.75}
        return {"label": "NEUTRAL", "score": 0.5}
