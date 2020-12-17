# -*- coding: utf-8 -*-
from collections import namedtuple
from functools import partial, wraps
from inspect import isawaitable

from sanic import response

__version__ = '0.3.0'

__all__ = ['Auth', 'User']


#: A User proxy type, used by default implementation of :meth:`Auth.load_user`
User = namedtuple('User', 'id name'.split())


class Auth:
    """Authentication Manager."""
    def __init__(self, app=None):
        self.app = None
        if app is not None:
            self.setup(app)

    def setup(self, app):
        """Setup with application's configuration.

        This method be called automatically if the application is provided
        upon initialization
        """
        if self.app is not None:
            raise RuntimeError('already initialized with an application')
        self.app = app
        get = app.config.get
        self.login_endpoint = get('AUTH_LOGIN_ENDPOINT', 'auth.login')
        self.login_url = get('AUTH_LOGIN_URL', None)
        session = get('AUTH_SESSION_NAME', get('SESSION_NAME', 'session'))
        self.session_name = session
        self.auth_session_key = get('AUTH_TOKEN_NAME', '_auth')

    def login_user(self, request, user):
        """Log in a user.

        The user object will be serialized with :meth:`Auth.serialize` and the
        result, usually a token representing the logged in user, will be
        placed into the request session.
        """
        self.get_session(request)[self.auth_session_key] = self.serialize(user)

    def logout_user(self, request):
        """Log out any logged in user in this session.

        Return the user token or :code:`None` if no user logged in.
        """
        return self.get_session(request).pop(self.auth_session_key, None)

    def current_user(self, request):
        """Get the current logged in user.

        Return :code:`None` if no user logged in.
        """
        token = self.get_session(request).get(self.auth_session_key, None)
        if token is not None:
            return self.load_user(token)

    def login_required(self, route=None, *, user_keyword=None,
                       handle_no_auth=None):
        """Decorator to make routes only accessible with authenticated user.

        Redirect visitors to login view if no user logged in.

        :param route:
            the route handler to be protected
        :param user_keyword:
            keyword only arugment, if it is not :code:`None`, and set to a
            string representing a valid python identifier, a user object
            loaded by :meth:`load_user` will be injected into the route
            handler's arguments.  This is to save from loading the user twice
            if the current user object is going to be used inside the route
            handler.
        :param handle_no_auth:
            keyword only arugment, if it is not :code:`None`, and set to a
            function this will be used to handle an unauthorized request.
        """
        if route is None:
            return partial(self.login_required, user_keyword=user_keyword,
                           handle_no_auth=handle_no_auth)

        if handle_no_auth is not None:
            assert callable(handle_no_auth), 'handle_no_auth must be callable'

        @wraps(route)
        async def privileged(request, *args, **kwargs):
            user = self.current_user(request)
            if isawaitable(user):
                user = await user

            if user is None:
                if handle_no_auth:
                    resp = handle_no_auth(request)
                else:
                    resp = self.handle_no_auth(request)
            else:
                if user_keyword is not None:
                    if user_keyword in kwargs:
                        raise RuntimeError(
                            'override user keyword %r in route' % user_keyword)
                    kwargs[user_keyword] = user
                resp = route(request, *args, **kwargs)

            if isawaitable(resp):
                resp = await resp
            return resp

        return privileged

    def serialize(self, user):
        """Serialize the user, returns a token to be placed into session"""
        return {'uid': user.id, 'name': user.name}

    def serializer(self, user_serializer):
        """Decorator to set a custom user serializer"""
        self.serialize = user_serializer
        return user_serializer

    def load_user(self, token):
        """Load user with token.

        Return a User object, the default implementation use a proxy object of
        :class:`User`, Sanic-Auth can be remain backend agnostic this way.

        Override this with routine that loads user from database if needed.
        """
        if token is not None:
            return User(id=token['uid'], name=token['name'])

    def user_loader(self, load_user):
        """Decorator to set a custom user loader that loads user with token"""
        self.load_user = load_user
        return load_user

    def get_session(self, request):
        """Get the session object associated with current request"""
        return request.ctx.session

    def handle_no_auth(self, request):
        """Handle unauthorized user"""
        u = self.login_url or request.app.url_for(self.login_endpoint)
        return response.redirect(u)

    def no_auth_handler(self, handle_no_auth):
        """Decorator to handle an unauthorized request"""
        self.handle_no_auth = handle_no_auth
        return handle_no_auth
