import logging
import sys

from celery import shared_task
from celery.exceptions import Ignore, Reject
from dateutil import parser
from django.core.cache import cache
from django.conf import settings
from django.contrib.auth.models import User
from fitapp.models import UserFitbit
from tracktivityPetsWebsite.utils import update_user_fitbit

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
hdlr = logging.FileHandler(settings.LOG_LOCATION + '/tracktivitypets_tasks.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)

from django.core.mail import send_mail

LOCK_EXPIRE = 60 * 5 # Lock expires in 5 minutes

@shared_task
def update_user_with_fitbit(fitbit_user):
    """ Get the user's time series data """

    logger.debug("Updating TracktivityPets local db: %s" % (str(fitbit_user)))

    # Create a lock so we don't try to run the same task multiple times
    lock_id = '{0}-lock-{1}'.format(__name__, fitbit_user)
    if not cache.add(lock_id, 'true', LOCK_EXPIRE):
        logger.debug('Already updating fitbit name: %s' % (fitbit_user))
        raise Ignore()

    fbusers = UserFitbit.objects.filter(fitbit_user=fitbit_user)

    for fbuser in fbusers:
        update_user_fitbit(fbuser.user)

    send_mail("Fitbit update for user: %s" % (fitbit_user), "", "john@johnkendall.net", ["john@johnkendall.net"] )

    #release lock
    cache.delete(lock_id)
