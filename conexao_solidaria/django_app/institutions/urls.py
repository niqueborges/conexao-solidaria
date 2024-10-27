from django.urls import path

from .views import HomeView, InstitutionListView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("institutions/", InstitutionListView.as_view(), name="institutions"),
]
