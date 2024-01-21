FediBlog
========

FediBlog is a simple demo of a ActivityPub-enabled federated blog built with
FediKit.


Prerequisites
-------------

FediBlog requires Python 3.12 or later.  All dependencies are managed via
Poetry_.  To install Poetry, follow the `instructions on the Poetry website`__.

Then, install the dependencies::

    poetry install

.. _Poetry: https://python-poetry.org/
__ https://python-poetry.org/docs/#installation


Configuration
-------------

FediBlog is configured via environment variables:

``QUART_APP``
   The entry point for Quart_.  This should be set to ``fediblog.app:app``.

``FEDIBLOG_DATABASE_PATH``
   A path to a SQLite database file.  If the file does not exist, it will be
   created.  If the file exists, it will be used as-is.

``FEDIBLOG_DEBUG``
   Turn on debug mode if set to ``true``.

See also the `.env.sample` file.  Note that it automatically loads the `.env`
file if it exists.

.. _Quart: https://quart.palletsprojects.com/


Running
-------

FediBlog is a Quart_ app, so it can be run with the ``quart run`` command::

    poetry run quart run

It will be available at http://127.0.0.1:5000/ by default.
