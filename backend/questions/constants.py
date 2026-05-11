"""
Constants for the questions app.

Keeping static data here (blocklists, allowlists) means:
  - ai_service.py stays focused on AI logic
  - validators.py stays focused on validation logic
  - Lists can be updated without touching any logic
"""

# Maximum characters accepted for a job title.
# Prevents oversized input reaching build_prompt() and reduces
# the prompt-injection surface area.
# Must match max_length in QuestionRequestSerializer — the serializer
# imports this value directly so they are always in sync.
MAX_JOB_TITLE_LENGTH = 120

# Short role abbreviations that are valid job titles despite being <= 3 characters.
# Checked BEFORE BLOCKED_WORDS — if a term appears here it is always accepted.
ALLOWED_ABBREVIATIONS = {
    "ceo", "cto", "cfo", "coo", "cmo", "cio",
    "vp", "hr", "qa", "pm", "ta", "pa", "md",
}

# Common English words that are never job titles.
# IMPORTANT: only applied to single-word inputs — see validators.py.
# Focused on short words the AI tends to let through — verbs, articles, slang.
BLOCKED_WORDS = {
    # Verbs
    "be", "do", "go", "run", "get", "set", "let", "put",
    "use", "try", "say", "see", "ask", "add", "end", "fix",
    "buy", "cut", "hit", "sit", "win", "fly", "cry", "eat",
    # Articles / prepositions / conjunctions
    "the", "and", "but", "for", "nor", "yet", "so", "or",
    "a", "an", "in", "on", "at", "to", "of", "up", "by",
    # Common adjectives
    "new", "old", "big", "bad", "hot", "top", "raw", "key",
    # Gibberish / slang
    "lol", "wtf", "omg", "asdf", "zzz", "hey", "yep", "nah",
    "ok", "hi", "yes", "no", "wow", "hmm", "meh",
}

# Catch accidental overlaps between the two sets at import time.
# ALLOWED_ABBREVIATIONS wins over BLOCKED_WORDS (checked first in validators.py),
# but an overlap is almost certainly a mistake — surface it immediately at startup.
assert not (ALLOWED_ABBREVIATIONS & BLOCKED_WORDS), (
    "Overlap between ALLOWED_ABBREVIATIONS and BLOCKED_WORDS: "
    f"{ALLOWED_ABBREVIATIONS & BLOCKED_WORDS}"
)