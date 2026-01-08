# core/healing_engine.py

# 🔹NEW FEATURE 2: Healing History Per Record
# Each review output explicitly records whether healing was applied,
# the detected error type, and the corrective action taken,
# enabling per-record auditability and traceability.

import re
from datetime import datetime
from core.healing_rules import HealingRules

def heal_review(review: dict, max_length: int) -> dict:
    text = review.get("text")

    result = {
        "review_id": review.get("review_id"),
        "business_id": review.get("business_id"),
        "stars": review.get("stars", 0),
        "original_text": text,
        "healed_text": None,
        "error_type": None,
        "action_taken": None,
        "was_healed": False,
        "healing_history": [],
        "metadata": {
            "user_id": review.get("user_id"),
            "date": review.get("date"),
            "useful": review.get("useful", 0),
            "funny": review.get("funny", 0),
            "cool": review.get("cool", 0),
        }
    }

    def record(error_type, action):
        result["healing_history"].append({
            "error_type": error_type,
            "action": action,
            "timestamp": datetime.now().isoformat()
        })

    rules = HealingRules.RULES

    if text is None:
        rule = rules["missing_text"]
        result["healed_text"] = rule["placeholder"]
        result["error_type"] = "missing_text"
        result["action_taken"] = rule["action"]
        result["was_healed"] = True
        record("missing_text", rule["action"])

    elif not isinstance(text, str) or not text.strip():
        rule = rules["empty_text"]
        result["healed_text"] = rule["placeholder"]
        result["error_type"] = "empty_text"
        result["action_taken"] = rule["action"]
        result["was_healed"] = True
        record("empty_text", rule["action"])

    elif not re.search(r"[a-zA-Z0-9]", text):
        rule = rules["special_characters_only"]
        result["healed_text"] = rule["placeholder"]
        result["error_type"] = "special_characters_only"
        result["action_taken"] = rule["action"]
        result["was_healed"] = True
        record("special_characters_only", rule["action"])

    elif len(text) > max_length:
        rule = rules["too_long"]
        half = max_length // 2
        result["healed_text"] = text[:half] + "..." + text[-half:]
        result["error_type"] = "too_long"
        result["action_taken"] = rule["action"]
        result["was_healed"] = True
        record("too_long", rule["action"])

    else:
        result["healed_text"] = text.strip()

    return result
