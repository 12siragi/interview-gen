"""
Validators for the questions app.

Runs BEFORE any AI API call — no tokens wasted on gibberish input.
The AI prompt acts as a second layer for anything more subtle.

Design decisions:
  - Pure Python, no external dependencies — fast and testable
  - Raises InvalidJobTitleError so views.py can return a clean 400
  - Intentionally permissive — only rejects what we are confident
    is not a job title. Edge cases go through to the AI.
  - Blocklist only applies to single-word inputs — multi-word phrases
    like "no code engineer" or "go developer" go straight to the AI
    because single-word blocklists don't compose well with phrases.
"""

from .constants import ALLOWED_ABBREVIATIONS, BLOCKED_WORDS, MAX_JOB_TITLE_LENGTH
from .exceptions import InvalidJobTitleError


def validate_job_title(job_title: str) -> None:
    """
    Validate the job title against the local blocklist.

    Checks (in order):
      1. Empty or whitespace-only              → invalid
      2. Exceeds max length                    → invalid
      3. Contains no letters at all            → invalid
      4. Multi-word input                      → valid, return early (AI handles it)
      5. Known role abbreviation (single word) → always valid, return early
      6. Single-word blocked term              → invalid
      7. Everything else                       → valid (AI handles deeper validation)

    Raises:
      InvalidJobTitleError — if the input is clearly not a job title
    """
    normalised = job_title.strip().lower()

    # 1. Blank input
    if not normalised:
        raise InvalidJobTitleError("Job title cannot be blank.")

    # 2. Length guard — prevents oversized input reaching build_prompt()
    #    and reduces prompt-injection surface area
    if len(normalised) > MAX_JOB_TITLE_LENGTH:
        raise InvalidJobTitleError("Job title is too long.")

    # 3. No letters at all — "12345", "!!!" — no real job title is letter-free
    if not any(c.isalpha() for c in normalised):
        raise InvalidJobTitleError("Input is not a recognised job title.")

    # 4. Multi-word inputs skip the blocklist entirely and go to the AI.
    #    "no code engineer" contains "no" which is blocked, but it's a real niche.
    #    "go developer" contains "go" which is blocked, but it's a real language.
    tokens = normalised.split()
    if len(tokens) > 1:
        return

    # 5. Single-word path: allowlist checked before blocklist (order matters)
    if normalised in ALLOWED_ABBREVIATIONS:
        return

    # 6. Single-word blocked term
    if normalised in BLOCKED_WORDS:
        raise InvalidJobTitleError("Input is not a recognised job title.")