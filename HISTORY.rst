=======
History
=======

0.6.1 (2019-03-17)

* Added health-check for celery and celery beat. Thanks @iharthi

0.6.0 (2019-03-21)
------------------

* Added health-check helpers. Thanks @iharthi

0.5.0 (2019-02-07)
------------------

* Added locking decorator. Thanks @iharthi

0.4.0 (2019-02-07)
------------------

* Supported Django and Python versions are listed below

===============  ==================
Django version   Python versions
---------------  ------------------
Django 1.8       3.4, 3.5, 3.6
Django 1.11      3.4, 3.5, 3.6
Django 2.0       3.4, 3.5, 3.6, 3.7
Django 2.1       3.5, 3.6, 3.7
===============  ==================


0.3.0 (2018-03-12)
------------------

* Supported Django versions are now 1.8, 1.11, and 2.0.
  `ClosableModel.created_by` and `closed_by` now have `on_delete=models.SET_NULL` attribute.
* Supported Python versions are now 3.4, 3.5, and 3.6.


0.2.0 (2016-01-27)
------------------

* Rename `tg_utils.yuglify` module to `tg_utils.compressor_filters` and
  added new filters for using UglifyJS 2 and clean-css.
* Added docs for `tg_utils.compressor_filters` module.


0.1.1 (2016-01-11)
------------------

* First release on PyPI.
