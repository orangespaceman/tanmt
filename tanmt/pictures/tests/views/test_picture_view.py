from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from ..factories import PictureFactory, TagFactory


class TestPictureView(TestCase):
    def create_published_picture(self, published_id=1, tag_count=0):
        past_date = timezone.now() - timezone.timedelta(days=1)
        tags = TagFactory.create_batch(tag_count)
        picture = PictureFactory(
            published_id=published_id,
            published_date=past_date,
        )
        picture.tags.add(*tags)
        return picture

    def test_url_resolves(self):
        """"
        URL resolves as expected
        """
        picture = self.create_published_picture()
        url = reverse('picture-slug',
                      kwargs={
                          'id': picture.published_id,
                          'slug': picture.slug
                      })

        self.assertEqual(url, f"/picture/1/{picture.slug}/")

    def test_get(self):
        """"
        GET request uses template
        """
        picture = self.create_published_picture()
        url = reverse('picture-slug',
                      kwargs={
                          'id': picture.published_id,
                          'slug': picture.slug
                      })

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pictures/picture.html')

    def test_get_missing(self):
        """"
        GET request can't find picture
        """
        url = reverse('picture-slug', kwargs={'id': 9, 'slug': 'blah'})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'error/error.html')

    def test_picture_content(self):
        """
        View returns content to view as expected
        """
        picture = self.create_published_picture(3, 3)

        url = reverse('picture-slug',
                      kwargs={
                          'id': picture.published_id,
                          'slug': picture.slug
                      })

        response = self.client.get(url)

        self.assertEqual(response.context['picture'], picture)
        self.assertEqual(response.context['picture'].tags.count(), 3)
