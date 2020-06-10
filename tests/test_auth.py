# -*- coding: utf-8 -*-
import pytest

from sanic import response
from sanic_auth import Auth, User


def test_login(app):
    auth = Auth(app)

    @app.post('/login')
    async def login(request):
        name = request.form.get('name')
        password = request.form.get('password')
        if name == 'demo' and password == '1234':
            auth.login_user(request, User(id=1, name=name))
            return response.text('okay')
        return response.text('failed')

    @app.route('/user')
    async def user(request):
        user = auth.current_user(request)
        if user is not None:
            return response.text(user.name)
        return response.text('')

    payload = {}
    req, resp = app.test_client.post('/login', data=payload)
    assert resp.status == 200 and resp.text == 'failed'
    req, resp = app.test_client.get('/user')
    assert resp.status == 200 and resp.text == ''

    payload = {'user': 'demo'}
    req, resp = app.test_client.post('/login', data=payload)
    assert resp.status == 200 and resp.text == 'failed'
    req, resp = app.test_client.get('/user')
    assert resp.status == 200 and resp.text == ''

    payload = {'name': 'demo', 'password': '4321'}
    req, resp = app.test_client.post('/login', data=payload)
    assert resp.status == 200 and resp.text == 'failed'
    req, resp = app.test_client.get('/user')
    assert resp.status == 200 and resp.text == ''

    payload = {'name': 'demo', 'password': '1234'}
    req, resp = app.test_client.post('/login', data=payload)
    assert resp.status == 200 and resp.text == 'okay'
    req, resp = app.test_client.get('/user')
    assert resp.status == 200 and resp.text == 'demo'


def test_logout(app):
    auth = Auth(app)

    @app.post('/login')
    async def login(request):
        name = request.form.get('name')
        password = request.form.get('password')
        if name == 'demo' and password == '1234':
            auth.login_user(request, User(id=1, name=name))
            return response.text('okay')
        return response.text('failed')

    @app.route('/logout')
    async def logout(request):
        auth.logout_user(request)
        return response.redirect('/user')

    @app.route('/user')
    async def user(request):
        user = auth.current_user(request)
        if user is not None:
            return response.text(user.name)
        return response.text('')

    payload = {'name': 'demo', 'password': '1234'}
    req, resp = app.test_client.post('/login', data=payload)
    assert resp.status == 200 and resp.text == 'okay'
    req, resp = app.test_client.get('/user')
    assert resp.status == 200 and resp.text == 'demo'

    req, reps = app.test_client.get('/logout')
    assert resp.status == 200 and resp.text == 'demo'
    req, resp = app.test_client.get('/user')
    assert resp.status == 200 and resp.text == ''

    req, reps = app.test_client.get('/logout')
    assert resp.status == 200 and resp.text == ''
    req, resp = app.test_client.get('/user')
    assert resp.status == 200 and resp.text == ''


def test_login_required(app):
    # the default is 'auth.login', change to 'login' to avoid using blueprint
    app.config.AUTH_LOGIN_ENDPOINT = 'login'
    auth = Auth(app)

    @app.post('/login')
    async def login(request):
        name = request.form.get('name')
        password = request.form.get('password')
        if name == 'demo' and password == '1234':
            auth.login_user(request, User(id=1, name=name))
            return response.text('okay')
        return response.text('failed')

    @app.route('/logout')
    @auth.login_required
    async def logout(request):
        auth.logout_user(request)
        return response.redirect('/user')

    @app.route('/user')
    @auth.login_required(user_keyword='user')
    async def user(request, user):
        return response.text(user.name)

    payload = {'name': 'demo', 'password': '1234'}
    req, resp = app.test_client.get('/user', allow_redirects=False)
    assert resp.status == 302
    assert resp.headers['Location'] == app.url_for('login')

    payload = {'name': 'demo', 'password': '1234'}
    req, resp = app.test_client.post('/login', data=payload)
    assert resp.status == 200 and resp.text == 'okay'
    req, resp = app.test_client.get('/user')
    assert resp.status == 200 and resp.text == 'demo'


def test_user_keyword(app):
    auth = Auth(app)

    @app.post('/login')
    async def login(request):
        name = request.form.get('name')
        password = request.form.get('password')
        if name == 'demo' and password == '1234':
            auth.login_user(request, User(id=1, name=name))
            return response.text('okay')
        return response.text('failed')

    @app.route('/user')
    @auth.login_required(user_keyword='user')
    async def user(request, user):
        return response.text(user.name)

    @app.route('/<user>')
    @auth.login_required(user_keyword='user')
    async def user_id(request, user):
        return response.text(user.id)

    payload = {'name': 'demo', 'password': '1234'}
    req, resp = app.test_client.post('/login', data=payload)
    assert resp.status == 200 and resp.text == 'okay'
    req, resp = app.test_client.get('/user')
    assert resp.status == 200 and resp.text == 'demo'

    req, resp = app.test_client.get(app.url_for('user_id', user=1))
    # RuntimeError being raised because we try to overwrite user parameter
    assert resp.status == 500


def test_decorators(app):
    auth = Auth(app)

    USER_DB = [
        {'id': '1', 'name': 'demo', 'password': '1234'},
        {'id': '2', 'name': 'admin', 'password': 'root'},
    ]

    def find_user(name, password):
        for user in USER_DB:
            if user['name'] == name and user['password'] == password:
                return user

    @auth.serializer
    def serialize(user):
        return user['id']

    @auth.user_loader
    def load_user(token):
        for user in USER_DB:
            if user['id'] == token:
                return user

    @auth.no_auth_handler
    def handle_unauthorized(request):
        return response.text('unauthorized', status=401)

    def handle_no_auth(request):
        return response.text('no_auth', status=403)

    @app.post('/login')
    async def login(request):
        name = request.form.get('name')
        password = request.form.get('password')
        user = find_user(name, password)
        if user is not None:
            auth.login_user(request, user)
            return response.text('okay')
        return response.text('failed')

    @app.route('/user')
    @auth.login_required(user_keyword='user')
    async def user(request, user):
        return response.text(user['name'])

    @app.route('/user/data')
    @auth.login_required(handle_no_auth=handle_no_auth)
    async def user_data(request, user):
        return response.text(user['name'])

    req, resp = app.test_client.get('/user')
    assert resp.status == 401 and resp.text == 'unauthorized'

    req, resp = app.test_client.get('/user/data')
    assert resp.status == 403 and resp.text == 'no_auth'

    payload = {'name': 'noone', 'password': '1234'}
    req, resp = app.test_client.post('/login', data=payload)
    assert resp.status == 200 and resp.text == 'failed'

    payload = {'name': 'demo', 'password': '1234'}
    req, resp = app.test_client.post('/login', data=payload)
    assert resp.status == 200 and resp.text == 'okay'
    req, resp = app.test_client.get('/user')
    assert resp.status == 200 and resp.text == 'demo'


def test_async_user_loader(app):
    auth = Auth(app)

    @auth.user_loader
    async def load_user(token):
        if token == 'root':
            return 'pwned'
        return None

    @auth.serializer
    def serialize(user):
        return 'root'

    @app.post('/login')
    async def login(request):
        auth.login_user(request, user)
        return response.text('All your base are belong to us')

    @app.route('/user')
    @auth.login_required(user_keyword='user')
    async def user(request, user):
        return response.text(user)

    req, resp = app.test_client.post('/login')
    assert resp.status == 200 and resp.text == 'All your base are belong to us'

    req, resp = app.test_client.get('/user')
    assert resp.status == 200 and resp.text == 'pwned'


def test_setup_once(app):
    auth = Auth(app)
    with pytest.raises(RuntimeError):
        auth.setup(app)
