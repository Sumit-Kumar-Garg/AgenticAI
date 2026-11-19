import re

_PATTERNS = [
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"), "[EMAIL]"),
    (re.compile(r"\b\d(?:[ -]?\d){12,15}\b"), "[CARD]"),
    (re.compile(r"(?<![\w])\+?\d[\d ()\-]{7,}\d(?![\w])"), "[PHONE]"),
]


def mask_pii(text: str) -> str:
    """Basic regex masking. Good enough to start; review it against your real data."""
    for pattern, token in _PATTERNS:
        text = pattern.sub(token, text)
    return text
