"""
Constants for the questions app.

Keeping static data here (blocklists, allowlists) means:
  - ai_service.py stays focused on AI logic
  - validators.py stays focused on validation logic
  - Lists can be updated without touching any logic
"""

# Short role abbreviations that are valid job titles despite being <= 3 characters
ALLOWED_ABBREVIATIONS = {
    "ceo", "cto", "cfo", "coo", "cmo", "cio",
    "vp", "hr", "qa", "pm", "ta", "pa", "md",
}

# Common English words that are never job titles.
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