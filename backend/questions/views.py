"""
Views for the questions app.

Design principle: keep views THIN.
  - Validation  → serializer handles it
  - AI logic    → ai_service handles it
  - The view only coordinates between them

This makes each layer independently testable.
"""
import logging

import requests
from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .ai_service import generate_interview_questions
from .exceptions import InvalidJobTitleError
from .serializers import QuestionRequestSerializer

logger = logging.getLogger(__name__)

# Rate limit: max requests per IP per window.
# Prevents a single client from burning the entire AI provider quota.
RATE_LIMIT_MAX    = 20   # requests allowed
RATE_LIMIT_WINDOW = 60   # seconds per window


class GenerateQuestionsView(APIView):
    """
    POST /api/questions/generate/

    Accepts:  { "job_title": "Customer Success Manager" }
    Returns:  { "questions": ["Q1?", "Q2?", "Q3?"] }

    Error responses:
      400 — invalid input (blank, too short, too long, not a real job title)
      429 — rate limit exceeded (too many requests from this IP)
      500 — AI provider error or parse failure
    """

    def post(self, request):
        # ── Step 1: Validate input ────────────────────────────────────────────
        serializer = QuestionRequestSerializer(data=request.data)

        if not serializer.is_valid():
            # 400 errors are descriptive — help the user fix their input
            logger.warning("Invalid request: %s", serializer.errors)
            return Response(
                {"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        job_title = serializer.validated_data["job_title"]

        # X-Forwarded-For can be a comma-separated chain (client, proxy1, proxy2)
        # when behind a load balancer — take the first value only.
        # Fall back to REMOTE_ADDR when the header is absent.
        forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        client_ip = (
            forwarded_for.split(",")[0].strip()
            if forwarded_for
            else request.META.get("REMOTE_ADDR", "unknown")
        )

        logger.info(
            "generate_request ip=%s title_length=%d", client_ip, len(job_title)
        )

        # ── Step 2: Rate limiting ─────────────────────────────────────────────
        # Check before any AI call so quota is never burned by a single abusive IP.
        # Window resets every RATE_LIMIT_WINDOW seconds per IP.
        rate_key = f"rate:{client_ip}"
        count = cache.get(rate_key, 0)

        if count >= RATE_LIMIT_MAX:
            logger.warning(
                "Rate limit exceeded ip=%s count=%d", client_ip, count
            )
            return Response(
                {"error": "Too many requests. Please wait a moment and try again."},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        cache.set(rate_key, count + 1, timeout=RATE_LIMIT_WINDOW)

        # ── Step 3: Generate questions ────────────────────────────────────────
        try:
            questions = generate_interview_questions(job_title)

            logger.info("Successfully generated questions for '%s'", job_title)

            return Response(
                {"questions": questions},
                status=status.HTTP_200_OK,
            )

        except InvalidJobTitleError:
            # Raised by validators.py (local check) or ai_service.py (AI check)
            # This is a user error — return 400 with a helpful message
            logger.warning("Invalid job title rejected: '%s'", job_title)
            return Response(
                {"error": "Please enter a valid job title (e.g. Software Engineer, Nurse, CEO)."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except ValueError as exc:
            # Configuration error or parse failure — not the user's fault
            # Log full detail — return safe message to client
            logger.error(
                "ValueError generating questions for '%s': %s", job_title, exc
            )
            return Response(
                {"error": "Failed to generate questions. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        except (requests.HTTPError, RuntimeError) as exc:
            # requests.HTTPError — AI provider returned a non-200 status
            # RuntimeError     — all providers exhausted (circuit breakers open)
            # Log full detail — return safe message to client
            logger.error(
                "AI provider error for '%s': %s", job_title, exc
            )
            return Response(
                {"error": "AI provider error. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        except Exception:
            # Catch-all — unexpected failures
            # logger.exception() captures the full traceback automatically
            # Never expose internal error details to the client
            logger.exception(
                "Unexpected error generating questions for '%s'", job_title
            )
            return Response(
                {"error": "An unexpected error occurred. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )