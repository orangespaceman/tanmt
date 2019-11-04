from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from ..factories import PictureFactory, TagFactory


class TestTagListView(TestCase):
    def create_published_picture(self, published_id=1, tags=[]):
        past_date = timezone.now() - timezone.timedelta(days=1)
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
        url = reverse('tags-list')

        self.assertEqual(url, "/tags/")

    def test_get(self):
        """"
        GET request uses template
        """
        url = reverse('tags-list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pictures/tag-list.html')

    def test_tags_content(self):
        """
        View returns content to view as expected
        """
        tag_lorem = TagFactory(tag='lorem')
        tag_ipsum = TagFactory(tag='Ipsum')
        TagFactory(tag='foo')
        tag_bar = TagFactory(tag='bar')

        self.create_published_picture(1, [tag_lorem, tag_ipsum])
        self.create_published_picture(2, [tag_ipsum])
        pic = self.create_published_picture(3, [tag_lorem, tag_ipsum, tag_bar])
        self.create_published_picture(4)

        url = reverse('tags-list')
        response = self.client.get(url)

        self.assertEqual(response.context['tags'].count(), 3)
        self.assertEqual(response.context['tags'].first().picture_count, 3)
        self.assertEqual(response.context['tags'].first().tag, 'Ipsum')
        self.assertEqual(response.context['tags'].last().tag, 'bar')
        self.assertEqual(response.context['tags'].last().picture_count, 1)
        self.assertEqual(response.context['tags'].last().picture_set.first(),
                         pic)
