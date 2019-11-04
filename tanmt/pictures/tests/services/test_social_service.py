from unittest.mock import Mock, patch

from django.test import TestCase
from django.utils import timezone

from ...services import SocialService
from ..factories import PictureFactory, TagFactory


class TestSocialService(TestCase):
    def generate_pictures(self):
        past_date = timezone.now() - timezone.timedelta(days=1)
        PictureFactory(order=3)
        next_picture = PictureFactory(order=2, title="Picture to publish")
        current_picture = PictureFactory(
            order=1,
            published_id=1,
            published_date=past_date,
            title="Picture published",
        )
        PictureFactory(order=4)
        PictureFactory(order=5)

        tag_lorem = TagFactory(tag='lorem')
        tag_ipsum = TagFactory(tag='Ipsum dolor sit amet')
        TagFactory(tag='foo')
        tag_bar = TagFactory(tag='fo-o! b_ar?')
        current_picture.tags.add(tag_ipsum, tag_bar)
        next_picture.tags.add(tag_lorem, tag_ipsum, tag_bar)

        return current_picture, next_picture

    @patch('pictures.services.SocialService.post_to_instagram')
    @patch('pictures.services.SocialService.post_to_twitter')
    @patch('pictures.services.SocialService.get_image')
    def test_post(self, get_image_mock, post_to_twitter_mock,
                  post_to_instagram_mock):
        """
        Check social service posts as expected
        """
        current_picture, next_picture = self.generate_pictures()

        get_image_mock.return_value = Mock(path='image-path')

        social_service = SocialService()
        social_service.post()

        get_image_mock.assert_called_once_with(next_picture)

        post_to_twitter_mock.assert_called_once_with(
            next_picture,
            'image-path',
            '#Lorem #IpsumDolorSitAmet #FooBar',
            '/picture/2/picture-to-publish/',
        )
        post_to_instagram_mock.assert_called_once_with(
            next_picture,
            'image-path',
            '#Lorem #IpsumDolorSitAmet #FooBar',
        )

    @patch('pictures.services.SocialService.post_to_twitter')
    @patch('pictures.services.SocialService.get_image')
    def test_repost_twitter(self, get_image_mock, post_to_twitter_mock):
        """
        Check social service repost works as expected
        """
        current_picture, next_picture = self.generate_pictures()

        get_image_mock.return_value = Mock(path='image-path')

        social_service = SocialService()
        social_service.repost_twitter()

        get_image_mock.assert_called_once_with(current_picture)

        post_to_twitter_mock.assert_called_once_with(
            current_picture,
            'image-path',
            '#IpsumDolorSitAmet #FooBar',
            '/picture/1/picture-published/',
        )

    @patch('pictures.services.SocialService.post_to_instagram')
    @patch('pictures.services.SocialService.get_image')
    def test_repost_instagram(self, get_image_mock, post_to_instagram_mock):
        """
        Check social service repost works as expected
        """
        current_picture, next_picture = self.generate_pictures()

        get_image_mock.return_value = Mock(path='image-path')

        social_service = SocialService()
        social_service.repost_instagram()

        get_image_mock.assert_called_once_with(current_picture)

        post_to_instagram_mock.assert_called_once_with(
            current_picture,
            'image-path',
            '#IpsumDolorSitAmet #FooBar',
        )
