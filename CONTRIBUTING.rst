.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/thorgate/tg-utils/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "feature"
is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

tg-utils could always use more documentation, whether as part of the
official tg-utils docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/thorgate/tg-utils/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `tg-utils` for local development.

1. Fork the `tg-utils` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/tg-utils.git

3. [Install poetry](https://python-poetry.org/docs/#installation)

4. Install dependencies::

    $ poetry install

5. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

Now you can make your changes locally.

6. When you're done making changes, check that your changes pass linters and the tests, including testing other Python versions with tox::

    $ poetry run make lint
    $ poetry run make test
    $ poetry run make test-all

7. Commit your changes and push your branch to GitHub::

    git add .
    git commit -m "Your detailed description of your changes."
    git push origin name-of-your-bugfix-or-feature

8. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst. You should also update the documentation
   source files via::

    poetry run make docs

3. If the pull request modifies/adds translations don't forget to run::

    poetry run make update-messages

4. The pull request should work for Python 3.7, 3.8, 3.9 and 3.10. Check
   https://github.com/thorgate/tg-utils/actions and make sure that the tests
   pass for all supported Python versions.

Tips
----

Run full test suite via tox (all python and django version combinations)::

    poetry run make test-all

To run a subset of tests::

    poetry run pytest tests.test_tg_utils

Update documentation source files and generate it::

    poetry run make docs

To see all make commands::

    poetry run make help
