from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from ..factories import PictureFactory, TagFactory


class TestPictureNav(TestCase):

    def create_published_picture(self, published_id=1, tag_count=0):
        past_date = timezone.now() - timezone.timedelta(days=1)
        tags = TagFactory.create_batch(tag_count)
        picture = PictureFactory(
            published_id=published_id,
            published_date=past_date,
        )
        picture.tags.add(*tags)
        return picture

    def test_nav(self):
        """
        View returns content to view as expected
        """
        PictureFactory()
        first_picture = self.create_published_picture(1, 1)
        second_picture = self.create_published_picture(2, 2)
        third_picture = self.create_published_picture(3, 3)
        PictureFactory()
        fourth_picture = self.create_published_picture(4, 4)
        latest_picture = self.create_published_picture(5, 5)
        PictureFactory()

        url = reverse('picture-slug',
                      kwargs={
                          'id': third_picture.published_id,
                          'slug': third_picture.slug
                      })

        response = self.client.get(url)

        self.assertEqual(response.context['picture'], third_picture)

        self.assertEqual(response.context['nav']['first'], first_picture)
        self.assertEqual(response.context['nav']['latest'], latest_picture)
        self.assertEqual(response.context['nav']['previous'], second_picture)
        self.assertEqual(response.context['nav']['next'], fourth_picture)
