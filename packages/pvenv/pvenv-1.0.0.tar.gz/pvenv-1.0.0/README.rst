=================================================
pvenv: Easy python virtual environment management
=================================================

.. image:: https://github.com/spapanik/pvenv/actions/workflows/tests.yml/badge.svg
  :alt: Tests
  :target: https://github.com/spapanik/pvenv/actions/workflows/tests.yml
.. image:: https://img.shields.io/github/license/spapanik/pvenv
  :alt: License
  :target: https://github.com/spapanik/pvenv/blob/main/LICENSE.txt
.. image:: https://img.shields.io/pypi/v/pvenv
  :alt: PyPI
  :target: https://pypi.org/project/pvenv
.. image:: https://pepy.tech/badge/pvenv
  :alt: Downloads
  :target: https://pepy.tech/project/pvenv
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
  :alt: code style: black
  :target: https://github.com/psf/black
.. image:: https://img.shields.io/badge/build%20automation-yamk-success
  :alt: build automation: yam
  :target: https://github.com/spapanik/yamk
.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json
  :alt: Lint: ruff
  :target: https://github.com/charliermarsh/ruff


In a nutshell
-------------

Installation
^^^^^^^^^^^^

The easiest way is to use pipx to install ``pvenv``.

.. code:: console

   $ pipx install pvenv

Please make sure that the correct directory is added to your path. This
depends on the OS.

Run ``pvenv`` to get the path to be sourced in the shell rc:

.. code:: console

   $ pvenv

Usage
^^^^^

You can use the following commands:

* `venv activate` (aliased to `avenv`) to activate a virtual environment
* `venv deactivate` (aliased to `dvenv`) to deactivate a virtual environment
* `venv list` (aliased to `lsvenv`) to list all the virtual environments
* `venv make` (aliased to `mkvenv`) to create a new virtual environment
* `venv rm` (aliased to `rmvenv`) to remove a virtual environment


Links
-----

- `Documentation`_
- `Changelog`_


.. _Changelog: https://github.com/spapanik/pvenv/blob/main/CHANGELOG.rst
.. _Documentation: https://p-venv.readthedocs.io/en/stable/
