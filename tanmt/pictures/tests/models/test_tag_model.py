from django.test import TestCase

from ..factories import TagFactory


class TestTagModel(TestCase):
    def test_custom_slug_creation(self):
        """
        Check slugs are generated as expected
        """
        tag = TagFactory(tag='Lorem Ipsum')
        tag_two = TagFactory(tag='_This is _a_ -te*s\'t /blah yeah? yo!')
        self.assertEqual(tag.slug, 'LoremIpsum')
        self.assertEqual(tag_two.slug, 'ThisIsATestBlahYeahYo')
