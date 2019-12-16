import re

from django.db import models
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from easy_thumbnails.files import get_thumbnailer


class Tag(models.Model):
    tag = models.CharField(max_length=200)
    description = models.TextField(
        blank=True,
        null=True,
    )
    slug = AutoSlugField(populate_from='tag',
                         help_text='This is used as the URL for this tag',
                         unique=True,
                         overwrite=True,
                         max_length=200)

    def slugify_function(self, content):
        content = re.sub('[^0-9a-zA-Z ]+', '', content)
        content = content.title()
        content = content.replace(' ', '')
        return content

    def __str__(self):
        return self.tag


class PublishedPictureManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(published_date__isnull=False)


class Picture(models.Model):
    order = models.PositiveIntegerField(
        default=1000,
        help_text=(
            'The lower the number, the sooner this picture will be published'))
    title = models.CharField(max_length=200)
    slug = AutoSlugField(
        populate_from='title',
        help_text='This is used as the URL for this picture',
        max_length=200,
    )
    description = models.TextField(
        blank=True,
        null=True,
    )
    published_id = models.PositiveIntegerField(
        blank=True,
        null=True,
    )
    published_date = models.DateTimeField(
        blank=True,
        null=True,
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
    )
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    # Managers
    objects = models.Manager()
    published_pictures = PublishedPictureManager()

    def get_url(self):
        return reverse(
            'picture-slug',
            kwargs={
                'id': self.published_id,
                'slug': self.slug,
            },
        )

    def get_tags(self):
        return " ".join(f"#{tag.slug}" for tag in self.tags.all())

    def get_image(self):
        # generate a smaller image to avoid Twitter 5mb file limit
        thumbnailer = get_thumbnailer(self.image.image)
        thumbnail_options = {'size': (2000, 2000)}
        return thumbnailer.get_thumbnail(
            thumbnail_options,
            save=True,
            generate=True,
        )

    # Metadata
    class Meta:
        ordering = ['-published_id', 'order']

    def __str__(self):
        return self.title


class Image(models.Model):
    def get_upload_path(self, filename):
        id = self.picture_id
        return f"pictures/{id}/image/{filename}"

    picture = models.OneToOneField(
        Picture,
        on_delete=models.CASCADE,
        related_name='image',
    )
    image = models.ImageField(upload_to=get_upload_path)

    def __str__(self):
        return self.picture.title
