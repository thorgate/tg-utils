=====
Usage
=====

To use tg-utils in a project::

    import tg_utils



Django Compressor filters
-------------------------

If you're using `Django Compressor <https://django-compressor.readthedocs.org/en/latest/>`_ for compressing CSS/JS, we have a few filters to use clean-css and Uglify JS 2 for
compression out of the box.

To use them, add to your Django settings::

    COMPRESS_CSS_FILTERS = [
        'compressor.filters.css_default.CssAbsoluteFilter',
        'tg_utils.compressor_filters.CleanCssFilter',
    ]
    COMPRESS_JS_FILTERS = [
        'tg_utils.compressor_filters.UglifyFilter',
    ]

Note that you need to have clean-css and uglify-js npm packages installed and in $PATH.
Django Compressor versions 1.4 to 2.0 (inclusive) are supported.


Health-check endpoint
---------------------

Make sure the extra dependencies are installed (by specifying [health_check] extra when adding tg_utils to project
requirements).

Add health_check app and relevant health-checkers to installed apps::

    INSTALLED_APPS = [
        ...
        'health_check',
        'health_check.db',
        'health_check.cache',
        'health_check.storage',
        'health_check.contrib.psutil',
        'health_check.contrib.celery',
        'tg_utils.health_check.checks.elvis',
        'tg_utils.health_check.checks.phantomjs',
        'tg_utils.health_check.checks.celery_beat',
        ...
    [

Add healthcheck to your urls.py::

    urlpatterns = [
        ...
        url(r'', include('tg_utils.health_check.urls')),
        ...
    ]

or manually, if you desire different urls::

    from tg_utils.health_check.views import HealthCheckViewProtected, HealthCheckViewMinimal

    urlpatterns = [
        ...
        url(r'^health/detail/?$', HealthCheckViewProtected.as_view(), name='health-check-detail'),
        url(r'^health/?$', HealthCheckViewMinimal.as_view(), name='health-check'),
        ...
    ]


Add settings, if required, to settings.py::

    # Settings related to views
    HEALTH_CHECK_ACCESS_TOKEN = 'secret' # Used to access protected detail view
    HEALTH_CHECK_ACCESS_TOKEN_PARAMETER = 'tervisetoken'
    HEALTH_CHECK_ACCESS_TOKEN_HEADER = 'HTTP_X_TERVISETOKEN'

    # Settings related to checkers
    HEALTH_CHECK = {
        # For 'health_check.contrib.psutil'
        'DISK_USAGE_MAX': 90,   # percent
        'MEMORY_MIN': 100,      # in MB

        # For 'tg_utils.health_check.checks.phantomjs'
        'PHANTOMJS_REQUIRES_HEADER_HTML': True,  # Defaults to False, set to true if phantomjs expects header_html data

        # For 'tg_utils.health_check.checks.celery_beat'
        'CELERY_APP': 'my_cool_project.celery.app',  # Celery app instance
        'CELERY_BEAT_CHECK_INTERVAL': 60,            # How frequently to schedule the health check beat, in seconds
        'CELERY_BEAT_DELAY_THRESHOLD': 10,           # Goes to error state if the task does not complete within
                                                     # this number of seconds after it was supposed to be scheduled

    }

To access protected detail view, secret token has to be passed as either a GET parameter or HTTP header.
