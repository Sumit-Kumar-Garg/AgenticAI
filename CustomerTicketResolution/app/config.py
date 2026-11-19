"""Edit this file to match your team. Everything tunable lives here."""

CATEGORIES = ["billing", "bug", "access", "how_to", "feature_request", "other"]
PRIORITIES = ["P1", "P2", "P3", "P4"]
SENTIMENTS = ["calm", "frustrated", "angry"]

# Replace with your real queues / pods.
TEAMS = ["Billing", "Technical Support", "Account & Access", "Product Experts", "General"]
DEFAULT_TEAM = "General"

# Tickets below this confidence go to a human.
CONFIDENCE_THRESHOLD = 0.75

# Priorities that always get a human look (start strict, relax with eval data).
ALWAYS_REVIEW_PRIORITIES = {"P1"}

# Any of these words in a ticket forces human review.
ESCALATION_KEYWORDS = [
    "lawyer", "legal", "lawsuit", "sue", "chargeback", "fraud",
    "data breach", "hacked", "gdpr", "cancel my contract",
]

KB_PATH = "data/resolved_tickets.csv"
SIMILAR_K = 3
SIMILAR_MIN_SCORE = 0.15
