from factory import Sequence
from factory.django import ImageField
from factory.fuzzy import FuzzyChoice, FuzzyText
from factory_djoy import CleanModelFactory

from components.models import ALIGNMENT_CHOICES, BACKGROUND_CHOICES

from ..models import (
    Component,
    Editorial,
    Embed,
    Image,
    ImageWithText,
    Page,
    Quote,
    Table,
)


class PageFactory(CleanModelFactory):
    title = FuzzyText()

    class Meta:
        model = Page


class ComponentFactory(CleanModelFactory):
    order = Sequence(lambda n: n)

    class Meta:
        model = Component


class EditorialFactory(CleanModelFactory):
    title = FuzzyText()
    content = FuzzyText()

    class Meta:
        model = Editorial


class EmbedFactory(CleanModelFactory):
    title = FuzzyText()
    content = FuzzyText()

    class Meta:
        model = Embed


class ImageFactory(CleanModelFactory):
    caption = FuzzyText()
    image = ImageField()

    class Meta:
        model = Image


class ImageWithTextFactory(CleanModelFactory):
    title = FuzzyText()
    content = FuzzyText()
    image = ImageField()
    background = FuzzyChoice([i[0] for i in BACKGROUND_CHOICES])
    align = FuzzyChoice([i[0] for i in ALIGNMENT_CHOICES])

    class Meta:
        model = ImageWithText


class QuoteFactory(CleanModelFactory):
    quote = FuzzyText()
    author = FuzzyText()
    background = FuzzyChoice([i[0] for i in BACKGROUND_CHOICES])

    class Meta:
        model = Quote


class TableFactory(CleanModelFactory):
    title = FuzzyText()
    content = FuzzyText()

    class Meta:
        model = Table
