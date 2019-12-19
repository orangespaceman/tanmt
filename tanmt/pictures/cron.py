import logging

from django.utils import timezone
from django_cron import CronJobBase, Schedule

from .services import SocialService

logger = logging.getLogger(__name__)


class SocialCronPost(CronJobBase):
    RUN_AT_TIMES = [
        '10:30',
    ]
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'tanmt.pictures.social_cron_post'

    def do(self):
        today = timezone.localtime(timezone.now()).weekday()
        if today == 1 or today == 4:  # 1 == Tuesday, 4 == Friday
            logger.info('Tuesday/Friday, running SocialCronPost cron')
            social_service = SocialService()
            social_service.post()
        else:
            logger.info('Not Tuesday/Friday, skipping SocialCronPost cron')
