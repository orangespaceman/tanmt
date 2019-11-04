from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from ..factories import PictureFactory, TagFactory


class TestHomeView(TestCase):
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
        self.create_published_picture()
        url = reverse('picture-home')

        self.assertEqual(url, '/')

    def test_get(self):
        """"
        GET request uses template
        """
        self.create_published_picture()
        url = reverse('picture-home')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pictures/picture.html')

    def test_home_content(self):
        """
        Home view returns content to view as expected
        """
        self.create_published_picture(1)
        self.create_published_picture(2)
        third_picture = self.create_published_picture(3, 3)
        PictureFactory()  # unpublished picture

        url = reverse('picture-home')

        response = self.client.get(url)

        self.assertEqual(response.context['picture'], third_picture)
        self.assertEqual(response.context['picture'].tags.count(), 3)
