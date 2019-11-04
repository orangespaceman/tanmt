import nested_admin
from admin_ordering.admin import OrderableAdmin
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path
from django.utils.html import format_html
from easy_thumbnails.files import get_thumbnailer

from tanmt.admin import tanmt_admin

from .models import Image, Picture, Tag
from .services import SocialService


class TagAdmin(admin.ModelAdmin):
    list_display = ['tag', 'slug', 'get_pictures']
    readonly_fields = ('slug', )

    def get_pictures(self, obj):
        return obj.picture_set.count()

    get_pictures.short_description = 'pictures'


class ImageAdmin(nested_admin.NestedStackedInline):
    readonly_fields = ['current_image']
    model = Image
    extra = 1

    def current_image(self, obj):
        if obj.image:
            thumbnailer = get_thumbnailer(obj.image)
            thumbnail_options = {'size': (100, 100)}
            return format_html(
                f'<img src="/media/'
                f'{thumbnailer.get_thumbnail(thumbnail_options)}" />')


class PictureAdmin(OrderableAdmin, nested_admin.NestedModelAdmin):
    change_list_template = "admin/picture_admin.html"

    list_display = [
        'title',
        'current_image',
        'get_tags',
        'published_date',
        'created_date',
        'order',
    ]
    list_editable = ('order', )
    ordering_field = 'order'
    readonly_fields = (
        'order',
        'published_id',
        'published_date',
    )
    inlines = [ImageAdmin]

    def current_image(self, obj):
        if obj.image:
            thumbnailer = get_thumbnailer(obj.image.image)
            thumbnail_options = {'size': (100, 100)}
            return format_html(
                f'<img src="/media/'
                f'{thumbnailer.get_thumbnail(thumbnail_options)}" />')

    def get_tags(self, obj):
        return ', '.join(tag.tag for tag in obj.tags.all())

    get_tags.short_description = 'tags'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('publish/', self.publish),
            path('republish-twitter/', self.republish_twitter),
            path('republish-instagram/', self.republish_instagram),
        ]
        return my_urls + urls

    def publish(self, request):
        model = Picture.objects.filter(
            published_date__isnull=True).order_by('order')[:1].first()

        if model:
            social_service = SocialService()
            social_service.post()
            self.message_user(request, "Picture published")
        else:
            self.message_user(request,
                              "No pictures to publish",
                              level=messages.WARNING)

        return HttpResponseRedirect("../")

    def republish_twitter(self, request):
        model = Picture.published_pictures.first()
        if model:
            social_service = SocialService()
            social_service.repost_twitter()
            self.message_user(request, "Picture republished to Twitter")
        else:
            self.message_user(request,
                              "No pictures to publish",
                              level=messages.WARNING)

        return HttpResponseRedirect("../")

    def republish_instagram(self, request):
        model = Picture.published_pictures.first()
        if model:
            social_service = SocialService()
            social_service.repost_instagram()
            self.message_user(request, "Picture republished to Instagram")
        else:
            self.message_user(request,
                              "No pictures to publish",
                              level=messages.WARNING)

        return HttpResponseRedirect("../")


tanmt_admin.register(Picture, PictureAdmin)
tanmt_admin.register(Tag, TagAdmin)
