from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from ..factories import PictureFactory, TagFactory


class TestRandomPictureView(TestCase):

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
        url = reverse('picture-random')

        self.assertEqual(url, "/picture/random/")

    def test_get(self):
        """"
        GET request uses template
        """
        self.create_published_picture(1)
        url = reverse('picture-random')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_get_follow_redirect(self):
        """
        View returns content to view as expected
        """
        picture = self.create_published_picture(1, 3)
        PictureFactory()

        url = reverse('picture-random')

        response = self.client.get(url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pictures/picture.html')

        self.assertEqual(response.context['picture'], picture)
        self.assertEqual(response.context['picture'].tags.count(), 3)
