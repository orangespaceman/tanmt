import logging
import os

from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from easy_thumbnails.files import get_thumbnailer
from twitter import OAuth, Twitter

from .models import Picture

logger = logging.getLogger(__name__)


class SocialService():
    def post(self):
        model = Picture.objects.filter(
            published_date__isnull=True).order_by('order')[:1].first()

        if model:
            model.published_date = timezone.now()
            previous_picture = Picture.published_pictures.first()

            if previous_picture:
                model.published_id = previous_picture.published_id + 1
            else:
                model.published_id = 1

            model.save()

            url = self.get_url(model)
            tags = self.get_tags(model)
            image = self.get_image(model)

            self.post_to_twitter(model, image.path, tags, url)
            self.post_to_instagram(model, image.path, tags)

    def repost_twitter(self):
        model = Picture.published_pictures.first()
        if model:
            url = self.get_url(model)
            tags = self.get_tags(model)
            image = self.get_image(model)
            self.post_to_twitter(model, image.path, tags, url)

    def repost_instagram(self):
        model = Picture.published_pictures.first()
        if model:
            tags = self.get_tags(model)
            image = self.get_image(model)
            self.post_to_instagram(model, image.path, tags)

    def get_url(self, model):
        return reverse('picture-slug',
                       kwargs={
                           'id': model.published_id,
                           'slug': model.slug,
                       })

    def get_tags(self, model):
        return " ".join(f"#{tag.slug}" for tag in model.tags.all())

    def get_image(self, model):
        # generate a smaller image to avoid Twitter 5mb file limit
        thumbnailer = get_thumbnailer(model.image.image)
        thumbnail_options = {'size': (2000, 2000)}
        return thumbnailer.get_thumbnail(thumbnail_options,
                                         save=True,
                                         generate=True)

    def post_to_twitter(self, model, image_path, tags, url):
        if hasattr(settings, 'TWITTER'):
            try:
                message = (f"{model.title}\n\n"
                           f"{settings.SITE_URL}{url}\n\n{tags}")

                with open(image_path, "rb") as imagefile:
                    imagedata = imagefile.read()

                t = Twitter(auth=OAuth(settings.TWITTER['oauth_token'],
                                       settings.TWITTER['oauth_secret'],
                                       settings.TWITTER['consumer_key'],
                                       settings.TWITTER['consumer_secret']))

                t_upload = Twitter(domain='upload.twitter.com',
                                   auth=OAuth(
                                       settings.TWITTER['oauth_token'],
                                       settings.TWITTER['oauth_secret'],
                                       settings.TWITTER['consumer_key'],
                                       settings.TWITTER['consumer_secret']))

                id_img = t_upload.media.upload(
                    media=imagedata)["media_id_string"]

                t.statuses.update(status=message, media_ids=id_img)

            except Exception as e:
                logger.error(e)

    def post_to_instagram(self, model, image_path, tags):
        if hasattr(settings, 'INSTAGRAM'):
            try:
                cmd = (f"php ../insta/upload.php "
                       f"'{image_path}' '{model.title}' '{tags}' "
                       f"'{settings.INSTAGRAM['username']}' "
                       f"'{settings.INSTAGRAM['password']}'")

                output = os.popen(cmd).read()
                if "error" in output:
                    logger.error(output)
                else:
                    logger.info(output)

            except Exception as e:
                logger.error(e)
