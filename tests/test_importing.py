# flake8: noqa


def test_imports():
    """ Ensures all submodules are importable

    Acts as a simple smoketest.
    """
    from tg_utils import admin
    from tg_utils import checks
    from tg_utils import compressor_filters
    from tg_utils import email
    from tg_utils import files
    from tg_utils import hashmodels
    from tg_utils import lock
    from tg_utils import managers
    from tg_utils import mixins
    from tg_utils import models
    from tg_utils import profiling
    from tg_utils import signals
    from tg_utils import uuid
