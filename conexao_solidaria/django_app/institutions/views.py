from django.views.generic import TemplateView


class HomeView(TemplateView):
    """
    View responsible for rendering the homepage template
    """

    template_name = "base.html"
