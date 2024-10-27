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

        institutions = get_endpoint_data(endpoint)
        return render(request, "institutions.html", {"institutions": institutions})
