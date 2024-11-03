from app import settings
from django.shortcuts import render
from django.views.generic import TemplateView, View

from .utils import get_endpoint_data


class HomeView(TemplateView):
    """
    View responsible for rendering the homepage template
    """

    template_name = "base.html"


class InstitutionListView(View):
    """
    View responsible for displaying all institutions registered at the
    specified endpoint.
    """

    def get(self, request):
        endpoint = settings.GET_INSTITUTIONS

        institutions = get_endpoint_data(endpoint)[:12]
        return render(request, "institutions.html", {"institutions": institutions})


class DetailInstitutionView(View):
    """
    View responsible for displaying the detailed data of an institution
    obtained through the specified endpoint.
    """

    def get(self, request, cnpj):
        endpoint = settings.GET_INSTITUTION.format(cnpj=cnpj)

        institution = get_endpoint_data(endpoint)

        return render(request, "detail_institution.html", {"institution": institution})


class TermsOfUseView(TemplateView):
    """
    View responsible for rendering the terms_of_use template
    """

    template_name = "terms_of_use.html"
