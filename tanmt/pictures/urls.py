from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='picture-home'),
    path('picture/', views.PictureListView.as_view(), name='picture-list'),
    path('picture/<int:id>/<slug:slug>/',
         views.PictureView.as_view(),
         name='picture-slug'),
    path('picture/random/',
         views.PictureRandomView.as_view(),
         name='picture-random'),
    path('picture/latest/',
         views.PictureLatestView.as_view(),
         name='picture-latest'),
    path('collections/', views.TagsView.as_view(), name='tags-list'),
    path('collections/<slug:tag>/',
         views.TagView.as_view(),
         name='tags-detail'),
]
