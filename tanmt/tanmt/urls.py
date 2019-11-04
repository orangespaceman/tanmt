from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.urls import path, re_path

from error.views import Error400View, Error403View, Error404View, error_500

from .admin import tanmt_admin

urlpatterns = [
    # app
    path('admin/', tanmt_admin.urls),
    path('', include('pictures.urls')),

    # third-party
    re_path(r'^_nested_admin/', include('nested_admin.urls')),

    # pages - must be last
    re_path(r'^(?P<slug>.*)/', include('pages.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = Error400View.as_view()
handler403 = Error403View.as_view()
handler404 = Error404View.as_view()
handler500 = error_500

# debug toolbar
if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns = [
            re_path(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass
