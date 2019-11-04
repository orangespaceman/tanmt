from django.shortcuts import get_object_or_404
from django.views import generic

from components.models import COMPONENT_TYPES

from .models import Component, Page


class PageView(generic.TemplateView):
    template_name = "pages/page.html"

    def get_context_data(self, **kwargs):
        context = super(PageView, self).get_context_data(**kwargs)

        slug = f"/{kwargs['slug']}"
        if not slug.endswith('/'):
            slug = f"{slug}/"

        page = get_object_or_404(Page, slug=slug)
        context['page'] = page
        context['page_title'] = page.title
        context['components'] = Component.objects.select_related(
            *COMPONENT_TYPES).filter(page_id=page.id)

        return context
