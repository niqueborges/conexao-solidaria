from django.core.paginator import Paginator
from django.views.generic import TemplateView, View
from django.shortcuts import render
from utils.http import fetch_data
from app import settings


class HomeView(TemplateView):
    """
    View responsible for rendering the homepage template
    """

    template_name = "home.html"


class InstitutionListView(View):
    """
    View responsible for displaying all institutions registered at the
    specified endpoint.
    """

    def get(self, request):
        endpoint = settings.GET_INSTITUTIONS
        all_institutions = fetch_data(endpoint).get("institutions", [])
        verified_institutions = [
            institution for institution in all_institutions if institution["verified"]
        ]
        paginator = Paginator(verified_institutions, 6)
        page_number = request.GET.get("page", 1)
        page_object = paginator.get_page(page_number)

        return render(request, "institutions.html", {"page_object": page_object})


class DetailInstitutionView(View):
    """
    View responsible for displaying the detailed data of an institution
    obtained through the specified endpoint.
    """

    def get(self, request, cnpj):
        endpoint = settings.GET_INSTITUTION.format(cnpj=cnpj)
        institution = fetch_data(endpoint)

        return render(request, "detail_institution.html", {"institution": institution})


class TermsOfUseView(TemplateView):
    """
    View responsible for rendering the terms_of_use template
    """

    template_name = "terms_of_use.html"


class FilterStateInstitutionView(View):
    def get(self, request):
        paginator = Paginator("change", 6)
        page_number = request.GET.get("page", 1)
        page_object = paginator.get_page(page_number)
        return render(request, "institutions.html", {"page_object": page_object})


class FilterRegionInstitutionView(View):
    def get(self, request):
        paginator = Paginator("change", 6)
        page_number = request.GET.get("page", 1)
        page_object = paginator.get_page(page_number)
        return render(request, "institutions.html", {"page_object": page_object})
