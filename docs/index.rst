.. include:: ../README.rst


Configuration
=============

================================ =============================================
Option                           Description
================================ =============================================
:code:`AUTH_LOGIN_ENDPOINT`      The name of login endpoint. Default is
                                 :code:`"auth.login"`
:code:`AUTH_LOGIN_URL`           The url of login endpoint, if this is set, it
                                 will take precedence over
                                 :code:`AUTH_LOGIN_ENDPOINT`. Default is
                                 :code:`None`, which means
                                 :code:`AUTH_LOGIN_ENDPOINT` will be used.
:code:`AUTH_SESSION_NAME`        The name of session to store the auth token,
                                 if it is not set, value of
                                 :code:`SESSION_NAME` will be used, if that is
                                 not set either, the default key name
                                 :code:`"session"` will be used.
:code:`AUTH_TOKEN_NAME`          The name of the key used in session to store
                                 user token.  Default is :code:`"_auth"`
================================ =============================================


API
===

.. automodule:: sanic_auth
  :members:


Full Example
============

.. literalinclude:: ../examples/note.py


Changelog
=========

- 0.3.0

  - Support Sanic 20.3.0
  - Drop python 3.5 support.

- 0.2.0

  - Handling of unauthorized request can be customized.
  - Properly handle async user loader.


- 0.1.0

  First public release.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
