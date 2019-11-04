from pages.models import Page


def header_pages(request):
    header_pages = Page.objects.filter(parent=None, display_in_header=True)
    context = {'header_pages': header_pages}
    return context


def footer_pages(request):
    footer_pages = Page.objects.filter(parent=None, display_in_footer=True)
    context = {'footer_pages': footer_pages}
    return context
