# -*- coding: utf-8 -*-
import pytest

from sanic import Sanic


@pytest.fixture(scope='function')
def app():
    test_app = Sanic('test_app')
    session = {}

    @test_app.middleware('request')
    async def add_session(request):
        name = request.app.config.get('SESSION_NAME', 'session')
        request[name] = session

    return test_app
