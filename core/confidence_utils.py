# core/confidence_utils.py

# 🔹NEW FEATURE 3: Confidence-Aware Sentiment Output
# Raw model confidence scores are mapped into interpretable bands
# (HIGH / MEDIUM / LOW) to support downstream decision-making and monitoring.

def confidence_level(confidence: float) -> str:
    if confidence >= 0.85:
        return "HIGH"
    elif confidence >= 0.65:
        return "MEDIUM"
    return "LOW"
