from factory import RelatedFactory
from factory.django import ImageField
from factory.fuzzy import FuzzyText
from factory_djoy import CleanModelFactory

from ..models import Image, Picture, Tag


class TagFactory(CleanModelFactory):
    tag = FuzzyText()

    class Meta:
        model = Tag


class ImageFactory(CleanModelFactory):
    image = ImageField()

    class Meta:
        model = Image


class PictureFactory(CleanModelFactory):
    title = FuzzyText()

    RelatedFactory(ImageFactory, 'picture')

    class Meta:
        model = Picture
