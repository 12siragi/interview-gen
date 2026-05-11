from django.urls import path, include
from django.http import JsonResponse


def home(request):
    return JsonResponse({
        "status": "ok",
        "message": "Interview Generator API running"
    })


urlpatterns = [
    path("", home),
    path("api/questions/", include("questions.urls")),
]