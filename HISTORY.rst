=======
History
=======

0.3.0 (2018-01-02)
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
