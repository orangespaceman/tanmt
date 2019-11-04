from ckeditor.fields import RichTextField
from django.db import models

COMPONENT_TYPES = [
    'editorial',
    'embed',
    'image',
    'image_with_text',
    'quote',
    'table',
]

ALIGNMENT_CHOICES = (
    ('imageLeft', 'Image left'),
    ('imageRight', 'Image right'),
)

BACKGROUND_CHOICES = (
    ('dark', 'Dark'),
    ('white', 'White'),
)


class AbstractComponent(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AbstractEditorial(AbstractComponent):
    title = models.CharField(max_length=200, blank=True)
    content = RichTextField(config_name='text', )

    class Meta:
        abstract = True

    def __str__(self):
        return 'editorial'


class AbstractEmbed(AbstractComponent):
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField(
        help_text="Careful! Anything you enter here will be embedded "
        "directly in the website...")

    class Meta:
        abstract = True

    def __str__(self):
        return 'embed'


class AbstractImage(AbstractComponent):
    # add image field directly where used:
    # image = models.ImageField(upload_to=get_upload_path)
    image_alt = models.CharField(max_length=200, blank=True)
    caption = models.CharField(max_length=200, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return 'image'


class AbstractImageWithText(AbstractComponent):
    # add image field directly where used:
    # image = models.ImageField(upload_to=get_upload_path, blank=True)
    title = models.CharField(max_length=200)
    content = RichTextField(config_name='text', )
    image_alt = models.CharField(max_length=200, blank=True)
    align = models.CharField(choices=ALIGNMENT_CHOICES, max_length=200)
    background = models.CharField(choices=BACKGROUND_CHOICES, max_length=200)

    class Meta:
        abstract = True

    def __str__(self):
        return 'image_with_text'


class AbstractQuote(AbstractComponent):
    # add image field directly where used:
    # image = models.ImageField(upload_to=get_upload_path, blank=True)
    quote = models.TextField()
    author = models.CharField(max_length=200, blank=True)
    background = models.CharField(choices=BACKGROUND_CHOICES, max_length=200)

    class Meta:
        abstract = True

    def __str__(self):
        return 'quote'


class AbstractTable(AbstractComponent):
    title = models.CharField(max_length=200, blank=True)
    content = RichTextField(config_name='table', )

    class Meta:
        abstract = True

    def __str__(self):
        return 'table'
