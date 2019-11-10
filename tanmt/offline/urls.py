from django.urls import path

from . import views

urlpatterns = [
    path('offline/', views.OfflineView.as_view(), name='offline-index'),
    path('service-worker.js',
         views.ServiceWorkerView.as_view(),
         name='offline-service-worker'),
]
