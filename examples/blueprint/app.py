from sanic import Sanic

from core import auth

from home_bp import home
from project_bp import project
from user_bp import user


app = Sanic(__name__)
app.config.AUTH_LOGIN_ENDPOINT = 'user.login'
auth.setup(app)

app.blueprint(user, url_prefix='user')
app.blueprint(project, url_prefix='project')
app.blueprint(home)


# NOTE
# For demonstration purpose, we use a mock-up globally-shared session object.
session = {}
@app.middleware('request')
async def add_session(request):
    request.ctx.session = session


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
