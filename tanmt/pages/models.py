import logging

from components.models import (
    AbstractEditorial,
    AbstractEmbed,
    AbstractImage,
    AbstractImageWithText,
    AbstractQuote,
    AbstractTable,
)
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField

logger = logging.getLogger(__name__)


def generate_slug(str):
    # keep for legacy reasons - used in migrations
    return str


class Page(models.Model):
    display_in_header = models.BooleanField(
        default=False, help_text='(Applicable to top-level pages only)')
    display_in_footer = models.BooleanField(
        default=False, help_text='(Applicable to top-level pages only)')
    title = models.CharField(max_length=200)
    slug = AutoSlugField(help_text='This will be the URL for this page',
                         unique=True,
                         overwrite=True,
                         populate_from='title')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User,
        models.SET_NULL,
        blank=True,
        null=True,
    )
    order = models.PositiveIntegerField(
        default=1,
        help_text=(
            'The lower the number, the closer to the start this appears'))

    # Metadata
    class Meta:
        ordering = ['order', 'title']

    # Methods
    def get_absolute_url(self):
        return reverse('page-detail', kwargs={'slug': self.get_slug()})

    # strip tags from slug before returning
    def get_slug(self):
        return self.slug.lstrip('/').rstrip('/')

    def __str__(self):
        return self.title


class Component(models.Model):
    order = models.IntegerField(
        blank=True,
        null=True,
        default=0,
    )
    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name='components',
    )

    # Metadata
    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"#{self.order + 1}"


class Editorial(AbstractEditorial):
    component = models.OneToOneField(
        Component,
        on_delete=models.CASCADE,
        related_name='editorial',
    )


class Embed(AbstractEmbed):
    component = models.OneToOneField(
        Component,
        on_delete=models.CASCADE,
        related_name='embed',
    )


class Image(AbstractImage):

    def get_upload_path(self, filename):
        id = self.component.page_id
        return f"page/{id}/image/{filename}"

    component = models.OneToOneField(
        Component,
        on_delete=models.CASCADE,
        related_name='image',
    )
    image = models.ImageField(upload_to=get_upload_path)


class ImageWithText(AbstractImageWithText):

    def get_upload_path(self, filename):
        id = self.component.page_id
        return f"page/{id}/image-with-text/{filename}"

    component = models.OneToOneField(
        Component,
        on_delete=models.CASCADE,
        related_name='image_with_text',
    )
    image = models.ImageField(upload_to=get_upload_path, blank=True)


class Quote(AbstractQuote):
    component = models.OneToOneField(
        Component,
        on_delete=models.CASCADE,
        related_name='quote',
    )


class Table(AbstractTable):
    component = models.OneToOneField(
        Component,
        on_delete=models.CASCADE,
        related_name='table',
    )
