from django.urls import path, include

urlpatterns = [
    path("", include("institutions.urls")),
    path("", include("bot.urls")),
]
