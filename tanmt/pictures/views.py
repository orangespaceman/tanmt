from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Prefetch, Q
from django.http import Http404, JsonResponse
from django.shortcuts import redirect
from django.views import generic

from .models import Picture, Tag


class NavMixin():
    def generate_nav(self, picture):

        if picture is None:
            return

        first = Picture.published_pictures.last()

        previous = Picture.published_pictures.filter(
            published_date__lt=picture.published_date)[0:1].first()

        next = Picture.published_pictures.filter(
            published_date__gt=picture.published_date).order_by(
                'published_date')[0:1].first()

        latest = Picture.published_pictures.first()

        return {
            'first': first if first != picture else None,
            'previous': previous if previous else None,
            'next': next if next else None,
            'latest': latest if latest != picture else None,
        }


class HomeView(generic.TemplateView, NavMixin):
    template_name = "pictures/picture.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        picture = Picture.published_pictures.first()
        context['picture'] = picture
        context['nav'] = self.generate_nav(picture)

        return context


class PictureListView(generic.TemplateView):
    template_name = "pictures/picture-list.html"

    def get_context_data(self, **kwargs):
        context = super(PictureListView, self).get_context_data(**kwargs)
        pictures = Picture.published_pictures.all()
        context['pictures'] = pictures
        context['title'] = "Pictures"
        return context


class PictureView(generic.TemplateView, NavMixin):
    template_name = "pictures/picture.html"

    def get_context_data(self, **kwargs):
        context = super(PictureView, self).get_context_data(**kwargs)

        id = kwargs.get('id', None)
        slug = kwargs.get('slug', None)

        try:
            picture = Picture.published_pictures.filter(
                published_id=id,
                slug=slug,
            ).get()
        except Picture.DoesNotExist:
            raise Http404("Picture does not exist")

        context['picture'] = picture
        context['title'] = picture.title
        context['nav'] = self.generate_nav(picture)

        return context


class PictureRandomView(generic.View):
    def dispatch(self, request):
        picture = Picture.published_pictures.order_by('?').first()
        if picture is None:
            return redirect('picture-home')

        return redirect('picture-slug',
                        id=picture.published_id,
                        slug=picture.slug)


class PictureLatestView(generic.View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        try:
            picture = Picture.published_pictures.first()
        except ObjectDoesNotExist:
            data = {
                "error": "No pictures published",
            }
            return JsonResponse(data, status=400)

        data = {
            'title': picture.title,
            'description': picture.description,
            'url': f"{settings.SITE_URL}{picture.get_url()}",
            'image': f"{settings.SITE_URL}{picture.get_image().url}",
            'tags': picture.get_tags(),
            'last_modified': picture.modified_date.timestamp()
        }

        return JsonResponse(data)


class TagsView(generic.TemplateView):
    template_name = "pictures/tag-list.html"

    def get_context_data(self, **kwargs):
        context = super(TagsView, self).get_context_data(**kwargs)
        pictures = Picture.published_pictures.all()
        tags = Tag.objects.prefetch_related(
            Prefetch('picture_set', queryset=pictures))
        tags = tags.annotate(picture_count=Count(
            'picture',
            filter=Q(picture__published_date__isnull=False),
        ))
        tags = tags.filter(picture_count__gt=0).order_by('-picture_count')
        context['tags'] = tags
        context['title'] = "Collections"

        return context


class TagView(generic.TemplateView):
    template_name = "pictures/tag.html"

    def get_context_data(self, **kwargs):
        context = super(TagView, self).get_context_data(**kwargs)

        slug = kwargs.get('tag', None)

        try:
            tag = Tag.objects.filter(slug=slug).get()
        except Tag.DoesNotExist:
            raise Http404("Collection does not exist")

        pictures = Picture.published_pictures.filter(tags__in=[tag.pk], ).all()

        context['pictures'] = pictures
        context['tag'] = tag
        context['title'] = (f"#{tag.slug} ({pictures.count()} "
                            f"picture{'' if pictures.count() == 1 else 's'})")

        return context
