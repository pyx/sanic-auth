============================================
Sanic-Auth - Simple Authentication for Sanic
============================================

Sanic-Auth implements a minimal backend agnostic session-based user
authentication mechanism for `Sanic`_.


.. _Sanic: https://github.com/channelcat/sanic


Quick Start
===========


Installation
------------

.. code-block:: sh

  pip install --upgrade Sanic-Auth


How to use it
-------------

.. code-block:: python

  from sanic_auth import Auth
  from sanic import Sanic, response


  app = Sanic(__name__)
  app.config.AUTH_LOGIN_ENDPOINT = 'login'


  @app.middleware('request')
  async def add_session_to_request(request):
      # setup session

  auth = Auth(app)

  @app.route('/login', methods=['GET', 'POST'])
  async def login(request):
      message = ''
      if request.method == 'POST':
          username = request.form.get('username')
          password = request.form.get('password')
          # fetch user from database
          user = some_datastore.get(name=username)
          if user and user.check_password(password):
              auth.login_user(request, user)
              return response.redirect('/profile')
      return response.html(HTML_LOGIN_FORM)


  @app.route('/logout')
  @auth.login_required
  async def logout(request):
      auth.logout_user(request)
      return response.redirect('/login')


  @app.route('/profile')
  @auth.login_required(user_keyword='user')
  async def profile(request, user):
      return response.json({'user': user})


For more details, please see documentation.


License
=======

BSD New, see LICENSE for details.


Links
=====

- `Documentation <http://sanic-auth.readthedocs.org/>`_

- `Issue Tracker <https://github.com/pyx/sanic-auth/issues/>`_

- `Source Package @ PyPI <https://pypi.python.org/pypi/sanic-auth/>`_

- `Git Repository @ Github
  <https://github.com/pyx/sanic-auth/>`_

- `Git Repository @ Gitlab
  <https://gitlab.com/pyx/sanic-auth/>`_

- `Development Version
  <http://github.com/pyx/sanic-auth/zipball/master#egg=sanic-auth-dev>`_
