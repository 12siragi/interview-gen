from django.urls import path, include
from django.http import JsonResponse


def home(request):
    return JsonResponse({"status": "ok"})


def health(request):
    """
    Dedicated health check endpoint.

    Used by load balancers, uptime monitors, and deployment platforms
    to verify the service is running.

    Future improvement: extend this to report circuit breaker state
    and cache hit rate per provider so ops can see provider health
    without digging through logs.
    """
    return JsonResponse({
        "status": "ok",
        "version": "1.0.0",
    })


urlpatterns = [
    path("", home),
    path("api/health/", health),
    path("api/questions/", include("questions.urls")),
]