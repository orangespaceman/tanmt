from components.models import COMPONENT_TYPES
from django.shortcuts import get_object_or_404
from django.views import generic

from .models import Component, Page


class PageView(generic.TemplateView):
    template_name = "pages/page.html"

    def get_context_data(self, **kwargs):
        context = super(PageView, self).get_context_data(**kwargs)

        print('page slug', kwargs['slug'])

        page = get_object_or_404(Page, slug=kwargs['slug'])
        context['page'] = page
        context['page_title'] = page.title
        context['components'] = Component.objects.select_related(
            *COMPONENT_TYPES).filter(page_id=page.id)

        return context
