from django.test import TestCase

from ..factories import PageFactory


class TestPageModel(TestCase):
    def test_page_url(self):
        """
        Get the URL for the Page instance - via the sluggified title
        """
        page = PageFactory(title='this? is& a! (test*)')
        self.assertEqual(page.slug, 'this-is-a-test')
