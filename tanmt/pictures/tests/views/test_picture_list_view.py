from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from ..factories import PictureFactory, TagFactory


class TestPictureListView(TestCase):

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
        """ "
        URL resolves as expected
        """
        url = reverse("picture-list")

        self.assertEqual(url, "/picture/")

    def test_get(self):
        """ "
        GET request uses template
        """
        url = reverse("picture-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pictures/picture-list.html")

    def test_picture_content(self):
        """
        View returns content to view as expected
        """
        first_picture = self.create_published_picture(1)
        self.create_published_picture(2)
        third_picture = self.create_published_picture(3, 3)
        PictureFactory()  # unpublished picture

        url = reverse("picture-list")

        response = self.client.get(url)

        self.assertEqual(response.context["pictures"].count(), 3)
        self.assertEqual(response.context["pictures"].first(), third_picture)
        self.assertEqual(response.context["pictures"].last(), first_picture)
        self.assertEqual(response.context["pictures"].first().tags.count(), 3)
