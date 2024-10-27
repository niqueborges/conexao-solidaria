from django.urls import path

from .views import HomeView, InstitutionListView, DetailInstitutionView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("institutions/", InstitutionListView.as_view(), name="institutions"),
    path(
        "institutions/<str:cnpj>/", DetailInstitutionView.as_view(), name="institution"
    ),
]
