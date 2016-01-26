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
