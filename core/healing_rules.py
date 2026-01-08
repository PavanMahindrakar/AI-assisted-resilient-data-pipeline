# core/healing_rules.py

# 🔹NEW FEATURE 1: Config-Driven Healing Rules
# Incoming reviews are automatically validated and healed using configurable rules
# (e.g., missing text, empty text, special characters, overly long reviews)
# before being sent to the LLM for sentiment analysis.

class HealingRules:
    RULES = {
        "missing_text": {
            "action": "filled_with_placeholder",
            "placeholder": "No review text provided."
        },
        "empty_text": {
            "action": "filled_with_placeholder",
            "placeholder": "No review text provided."
        },
        "special_characters_only": {
            "action": "replaced_special_characters",
            "placeholder": "[Non-text content]"
        },
        "too_long": {
            "action": "truncated_text",
            "strategy": "head_tail"
        }
    }
