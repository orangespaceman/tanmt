from django.views import generic


class OfflineView(generic.TemplateView):
    template_name = "offline/offline.html"


class ServiceWorkerView(generic.TemplateView):
    template_name = "offline/service-worker.js"
    content_type = "application/javascript"
