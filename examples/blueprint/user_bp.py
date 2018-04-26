from sanic import Blueprint, response

from sanic_auth import User

from core import auth

user = Blueprint('user')


LOGIN_FORM = '''
<h2>Please sign in, you can try:</h2>
<dl>
<dt>Username</dt> <dd>demo</dd>
<dt>Password</dt> <dd>1234</dd>
</dl>
<p>{}</p>
<form action="" method="POST">
  <input class="username" id="name" name="username"
    placeholder="username" type="text" value=""><br>
  <input class="password" id="password" name="password"
    placeholder="password" type="password" value=""><br>
  <input id="submit" name="submit" type="submit" value="Sign In">
</form>
'''


@user.route('/login', methods=['GET', 'POST'])
async def login(request):
    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # for demonstration purpose only, you should use more robust method
        if username == 'demo' and password == '1234':
            # use User proxy in sanic_auth, this should be some ORM model
            # object in production, the default implementation of
            # auth.login_user expects User.id and User.name available
            user = User(id=1, name=username)
            auth.login_user(request, user)
            return response.redirect('/')
        message = 'invalid username or password'
    return response.html(LOGIN_FORM.format(message))


@user.route('/logout')
@auth.login_required
async def logout(request):
    auth.logout_user(request)
    return response.redirect('/')


@user.route('/')
@auth.login_required(user_keyword='user')
async def profile(request, user):
    text = '<a href="/user/logout">Logout</a><p>Welcome, %s</p>' % user.name
    return response.html(text)
