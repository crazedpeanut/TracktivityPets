import logging
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from fitbit import Fitbit

from . import defaults
from .models import UserFitbit

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
hdlr = logging.FileHandler('./tracktivitypets_fitapp_utils.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.DEBUG)


def create_fitbit(consumer_key=None, consumer_secret=None, **kwargs):
    """Shortcut to create a Fitbit instance.

    If consumer_key or consumer_secret are not provided, then the values
    specified in settings are used.
    """
    if consumer_key is None:
        consumer_key = get_setting('FITAPP_CONSUMER_KEY')
    if consumer_secret is None:
        consumer_secret = get_setting('FITAPP_CONSUMER_SECRET')

    if consumer_key is None or consumer_secret is None:
        raise ImproperlyConfigured("Consumer key and consumer secret cannot "
                "be null, and must be explicitly specified or set in your "
                "Django settings")

    return Fitbit(consumer_key, consumer_secret, **kwargs)


def is_integrated(user):
    """Returns ``True`` if we have Oauth info for the user.

    This does not require that the token and secret are valid.

    :param user: A Django User.
    """
    if user.is_authenticated() and user.is_active:
        return UserFitbit.objects.filter(user=user).exists()
    return False


def get_valid_periods():
    """Returns list of periods for which one may request time series data."""
    return ['1min', '15min','1d', '7d', '30d', '1w', '1m', '3m', '6m', '1y', 'max']


def get_fitbit_data(fbuser, resource_type, base_date=None, period=None,
        end_date=None):
    """Creates a Fitbit API instance and retrieves step data for the period.

    Several exceptions may be thrown:
        TypeError           - Either end_date or period must be specified, but
                              not both.
        ValueError          - Invalid argument formats.
        HTTPUnauthorized    - 401 - fbuser has bad authentication credentials.
        HTTPForbidden       - 403 - This isn't specified by Fitbit, but does
                                 appear in the Python Fitbit library.
        HTTPNotFound        - 404 - The specific resource doesn't exist.
        HTTPConflict        - 409 - HTTP conflict
        HTTPTooManyRequests - 429 - Hitting the rate limit
        HTTPServerError     - >=500 - Fitbit server error or maintenance.
        HTTPBadRequest      - >=400 - Bad request.
    """
    fb = create_fitbit(**fbuser.get_user_data())
    resource_path = resource_type.path()
    
    logger.debug("Detail level: %s, startTime: %s, endTime: %s", period, str(base_date), str(end_date))
    '''
    data = fb.intraday_time_series(resource_path, start_time=base_date, end_time=end_date)
    '''
    data = fb.time_series(resource_path, user_id=fbuser.fitbit_user,
                              period=period, base_date=base_date,
                              end_date=end_date)


    if('HTTP Error 500' in data[resource_path.replace('/', '-')]):
        logger.error('HTTPServerError - >=500 - Fitbit server error or maintenance.')
    
    return data[resource_path.replace('/', '-')]


def get_setting(name, use_defaults=True):
    """Retrieves the specified setting from the settings file.

    If the setting is not found and use_defaults is True, then the default
    value specified in defaults.py is used. Otherwise, we raise an
    ImproperlyConfigured exception for the setting.
    """
    if hasattr(settings, name):
        return getattr(settings, name)
    if use_defaults:
        if hasattr(defaults, name):
            return getattr(defaults, name)
    msg = "{0} must be specified in your settings".format(name)
    raise ImproperlyConfigured(msg)
