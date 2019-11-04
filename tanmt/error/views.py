from django.shortcuts import render
from django.views.generic import TemplateView


class ErrorAbstractView(TemplateView):
    template_name = 'error/error.html'

    def get_status(self):
        return 200

    def get(self, request, *args, **kwargs):
        response = super(ErrorAbstractView, self).get(request, *args, **kwargs)
        response.status_code = self.get_status()
        return response

    def get_context_data(self, **kwargs):
        context = super(ErrorAbstractView, self).get_context_data(**kwargs)
        context['status'] = self.get_status()
        context['error'] = self.get_error_message()
        return context

    class Meta:
        abstract = True


class Error400View(ErrorAbstractView):
    def get_status(self):
        return 400

    def get_error_message(self):
        return 'Sorry, we encountered an error with that request'


class Error403View(ErrorAbstractView):
    def get_status(self):
        return 403

    def get_error_message(self):
        return 'Sorry, you can\'t access that page'


class Error404View(ErrorAbstractView):
    def get_status(self):
        return 404

    def get_error_message(self):
        return 'Sorry, we couldn\'t find that page'


# 500 error isn't a class-based view due to different call signature required
def error_500(request):
    context = {
        'error': 'Sorry, we encountered an error with that request',
        'status': 500
    }
    return render(request, 'error/error.html', context, status=500)
