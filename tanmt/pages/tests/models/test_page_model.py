from django.core.exceptions import ValidationError
from django.test import TestCase

from ..factories import PageFactory


class TestPageModel(TestCase):
    def test_page_url(self):
        """
        Get the URL for the Page instance - via the sluggified title
        """
        page = PageFactory(title='this? is& a! (test*)')
        self.assertEqual(page.slug, '/this-is-a-test/')

    def test_second_level_page_url(self):
        """
        Get the URL for a second-level page - via the sluggified title
        """
        parent_page = PageFactory(title='this? is& a! (test*)')
        child_page = PageFactory(title='child page', parent=parent_page)

        self.assertEqual(child_page.slug, '/this-is-a-test/child-page/')

    def test_third_level_page_url(self):
        """
        Get the URL for a third-level page - via the sluggified title
        """
        parent_page = PageFactory(title='this? is& a! (test*)')
        child_page = PageFactory(title='child page', parent=parent_page)
        grandchild = PageFactory(title='grand child page', parent=child_page)

        self.assertEqual(grandchild.slug,
                         '/this-is-a-test/child-page/grand-child-page/')

    def test_validation_fail(self):
        """
        Ensure a page can't be set as its own parent
        """
        parent_page = PageFactory(title='this? is& a! (test*)')

        def update_parent_to_self(page):
            page.parent = page
            page.clean()

        self.assertRaises(ValidationError, update_parent_to_self, parent_page)
