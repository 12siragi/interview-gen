"""
Custom exceptions for the questions app.

Keeping exceptions in their own module avoids circular imports
and makes it easy to catch specific errors across the codebase.
"""


class InvalidJobTitleError(ValueError):
    """
    Raised when the input is not a real job title.
    Caught separately in views.py to return a 400 instead of 500.
    """
    pass