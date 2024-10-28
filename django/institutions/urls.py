from django.urls import path

from .views import DetailInstitutionView, HomeView, InstitutionListView, TermsOfUseView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("institutions/", InstitutionListView.as_view(), name="institutions"),
    path(
        "institutions/<str:cnpj>/", DetailInstitutionView.as_view(), name="institution"
    ),
    path("terms-of-use/", TermsOfUseView.as_view(), name="terms_of_use"),
]
