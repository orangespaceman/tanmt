from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from ..factories import PictureFactory, TagFactory


class TestTagDetailView(TestCase):
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
        tag = TagFactory(tag='lorem')
        url = reverse('tags-detail', kwargs={'tag': tag.slug})

        self.assertEqual(url, f"/collections/{tag.slug}/")

    def test_get(self):
        """"
        GET request uses template
        """
        tag = TagFactory(tag='lorem')
        url = reverse('tags-detail', kwargs={'tag': tag.slug})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pictures/tag.html')

    def test_get_missing(self):
        """"
        GET request can't find tag
        """
        url = reverse('tags-detail', kwargs={'tag': 'blah'})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'error/error.html')

    def test_tags_detail_content(self):
        """
        View returns content to view as expected
        """
        tag = TagFactory(tag='Lorem Ipsum')

        first = self.create_published_picture(1, [tag])
        self.create_published_picture(2, [tag])
        self.create_published_picture(3)
        PictureFactory()
        latest = self.create_published_picture(4, [tag])

        url = reverse('tags-detail', kwargs={'tag': tag.slug})
        response = self.client.get(url)

        self.assertEqual(response.context['title'],
                         f"#LoremIpsum (3 pictures)")
        self.assertEqual(response.context['pictures'].count(), 3)
        self.assertEqual(response.context['pictures'].first(), latest)
        self.assertEqual(response.context['pictures'].last(), first)
