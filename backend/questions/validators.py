"""
Validators for the questions app.

Runs BEFORE any AI API call — no tokens wasted on gibberish input.
The AI prompt acts as a second layer for anything more subtle.

Design decisions:
  - Pure Python, no external dependencies — fast and testable
  - Raises InvalidJobTitleError so views.py can return a clean 400
  - Intentionally permissive — only rejects what we are confident
    is not a job title. Edge cases go through to the AI.
"""

from .constants import ALLOWED_ABBREVIATIONS, BLOCKED_WORDS
from .exceptions import InvalidJobTitleError


def validate_job_title(job_title: str) -> None:
    """
    Validate the job title against the local blocklist.

    Checks (in order):
      1. Empty or whitespace-only → invalid
      2. Known role abbreviation → always valid, return early
      3. Blocked word list → invalid
      4. Everything else → valid (AI handles deeper validation)

    Raises:
      InvalidJobTitleError — if the input is clearly not a job title
    """
    normalised = job_title.strip().lower()

    if not normalised:
        raise InvalidJobTitleError("Job title cannot be blank.")

    # Always allow known short-form role abbreviations
    if normalised in ALLOWED_ABBREVIATIONS:
        return

    # Reject known non-job words
    if normalised in BLOCKED_WORDS:
        raise InvalidJobTitleError("Input is not a recognised job title.")