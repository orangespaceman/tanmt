from django.test import TestCase
from django.urls import reverse
from factory import SubFactory

from ..factories import (
    ComponentFactory,
    EditorialFactory,
    EmbedFactory,
    ImageFactory,
    ImageWithTextFactory,
    PageFactory,
    QuoteFactory,
    TableFactory,
)


class TestPageView(TestCase):
    def test_url_resolves(self):
        """"
        URL resolves as expected
        """
        page = PageFactory(title='this? is& a! (test*)')
        url = reverse('page-detail', kwargs={'slug': page.get_slug()})

        self.assertEqual(url, '/this-is-a-test/')

    def test_get(self):
        """"
        GET request uses template
        """
        page = PageFactory(title='this? is& a! (test*)')
        url = reverse('page-detail', kwargs={'slug': page.get_slug()})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/page.html')

    def test_get_no_page(self):
        """"
        GET request returns a 404 when no page found
        """
        url = reverse('page-detail', kwargs={'slug': 'this is a test'})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'error/error.html')

    def test_component_editorial(self):
        """"
        GET request returns editorial component as expected
        """
        page = PageFactory()
        editorial = EditorialFactory(title='first editorial block',
                                     component=SubFactory(ComponentFactory,
                                                          page=page))

        url = reverse('page-detail', kwargs={'slug': page.get_slug()})

        response = self.client.get(url)
        component = response.context['components'].first()
        first_editorial = component.editorial
        self.assertEqual(first_editorial, editorial)
        self.assertEqual(first_editorial.title, 'first editorial block')

    def test_component_embed(self):
        """"
        GET request returns embed component as expected
        """
        page = PageFactory()
        embed = EmbedFactory(title='first embed block',
                             component=SubFactory(ComponentFactory, page=page))

        url = reverse('page-detail', kwargs={'slug': page.get_slug()})

        response = self.client.get(url)
        component = response.context['components'].first()
        first_embed = component.embed
        self.assertEqual(first_embed, embed)
        self.assertEqual(first_embed.title, 'first embed block')

    def test_component_image(self):
        """"
        GET request returns image component as expected
        """
        page = PageFactory()
        image = ImageFactory(caption='first image block',
                             component=SubFactory(ComponentFactory, page=page))

        url = reverse('page-detail', kwargs={'slug': page.get_slug()})

        response = self.client.get(url)
        component = response.context['components'].first()
        first_image = component.image
        self.assertEqual(first_image, image)
        self.assertEqual(first_image.caption, 'first image block')

    def test_component_image_with_text(self):
        """"
        GET request returns image with text component as expected
        """
        page = PageFactory()
        image_with_text = ImageWithTextFactory(
            title='first image with text block',
            component=SubFactory(ComponentFactory, page=page))

        url = reverse('page-detail', kwargs={'slug': page.get_slug()})

        response = self.client.get(url)
        component = response.context['components'].first()
        first_image_with_text = component.image_with_text
        self.assertEqual(first_image_with_text, image_with_text)
        self.assertEqual(first_image_with_text.title,
                         'first image with text block')

    def test_component_quote(self):
        """"
        GET request returns quote component as expected
        """
        page = PageFactory()
        quote = QuoteFactory(quote='first quote block',
                             component=SubFactory(ComponentFactory, page=page))

        url = reverse('page-detail', kwargs={'slug': page.get_slug()})

        response = self.client.get(url)
        component = response.context['components'].first()
        first_quote = component.quote
        self.assertEqual(first_quote, quote)
        self.assertEqual(first_quote.quote, 'first quote block')

    def test_component_table(self):
        """"
        GET request returns table component as expected
        """
        page = PageFactory()
        table = TableFactory(title='first table block',
                             component=SubFactory(ComponentFactory, page=page))

        url = reverse('page-detail', kwargs={'slug': page.get_slug()})

        response = self.client.get(url)
        component = response.context['components'].first()
        first_table = component.table
        self.assertEqual(first_table, table)
        self.assertEqual(first_table.title, 'first table block')
