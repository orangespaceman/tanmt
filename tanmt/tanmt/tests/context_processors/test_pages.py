from django.test import TestCase

from pages.tests.factories import PageFactory

from ...context_processors.pages import footer_pages, header_pages


class TestContextProcessorPages(TestCase):
    def test_header_pages(self):
        """
        Return top level pages that should be in the header
        """
        PageFactory()
        header_page = PageFactory(display_in_header=True)

        context = header_pages({})
        self.assertEqual(len(context['header_pages']), 1)
        self.assertTrue(header_page in context['header_pages'])

    def test_header_pages_empty(self):
        """
        Return analytics settings in config object
        """
        context = header_pages({})
        self.assertEqual(len(context['header_pages']), 0)

    def test_footer_pages(self):
        """
        Return top level pages that should be in the footer
        """
        PageFactory()
        footer_page = PageFactory(display_in_footer=True)

        context = footer_pages({})
        self.assertEqual(len(context['footer_pages']), 1)
        self.assertTrue(footer_page in context['footer_pages'])

    def test_footer_pages_empty(self):
        """
        Return analytics settings in config object
        """
        context = footer_pages({})
        self.assertEqual(len(context['footer_pages']), 0)
