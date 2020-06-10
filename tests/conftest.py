# -*- coding: utf-8 -*-
import pytest

from sanic import Sanic
from sanic.request import Request


@pytest.fixture(scope='function')
def app():
    test_app = Sanic('test_app')
    session = {}

    @test_app.middleware('request')
    async def add_session(request: Request):
        request.ctx.session = session

    return test_app
