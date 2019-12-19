from django.test import TestCase

from ...models import GlobalTags
from ..factories import PictureFactory, TagFactory


class TestPictureModel(TestCase):
    def test_get_tags_all(self):
        """
        Check tag string is generated as expected
        """
        global_tags = GlobalTags(tags='#GlobalTag #AnotherGlobalTag')
        global_tags.save()

        tag = TagFactory(
            tag='Lorem Ipsum',
            extra_tags='#TagExtraTag #AnotherTagExtraTag',
        )
        tag_two = TagFactory(tag='_This is _a_ -te*s\'t /blah yeah? yo!')

        picture = PictureFactory(
            extra_tags='#PictureExtraTag #AnotherPictureExtraTag')

        picture.tags.add(tag, tag_two)

        self.assertEqual(
            picture.get_tags(), '#LoremIpsum #ThisIsATestBlahYeahYo '
            '#TagExtraTag #AnotherTagExtraTag '
            '#PictureExtraTag #AnotherPictureExtraTag '
            '#GlobalTag #AnotherGlobalTag')

    def test_get_tags_picture_only(self):
        """
        Check tag string is generated as expected
        """
        picture = PictureFactory(
            extra_tags='#PictureExtraTag #AnotherPictureExtraTag')

        self.assertEqual(picture.get_tags(),
                         '#PictureExtraTag #AnotherPictureExtraTag')

    def test_get_tags_tags_only(self):
        """
        Check tag string is generated as expected
        """
        tag = TagFactory(tag='Lorem Ipsum', )
        tag_two = TagFactory(tag='_This is _a_ -te*s\'t /blah yeah? yo!')

        picture = PictureFactory()

        picture.tags.add(tag, tag_two)

        self.assertEqual(picture.get_tags(),
                         '#LoremIpsum #ThisIsATestBlahYeahYo')

    def test_get_tags_with_tags_and_extra_tags_only(self):
        """
        Check tag string is generated as expected
        """
        tag = TagFactory(
            tag='Lorem Ipsum',
            extra_tags='#TagExtraTag #AnotherTagExtraTag',
        )
        tag_two = TagFactory(tag='_This is _a_ -te*s\'t /blah yeah? yo!')

        picture = PictureFactory()

        picture.tags.add(tag, tag_two)

        self.assertEqual(
            picture.get_tags(), '#LoremIpsum #ThisIsATestBlahYeahYo '
            '#TagExtraTag #AnotherTagExtraTag')

    def test_get_tags_global_only(self):
        """
        Check tag string is generated as expected
        """
        global_tags = GlobalTags(tags='#GlobalTag #AnotherGlobalTag')
        global_tags.save()

        picture = PictureFactory()

        self.assertEqual(picture.get_tags(), '#GlobalTag #AnotherGlobalTag')
