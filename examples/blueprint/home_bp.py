from sanic import Blueprint, response

home = Blueprint('home')


HOME_PAGE = '''
<a href="/user/">My Account</a>
<a href="/project">My Projects</a>
'''


@home.route('/')
async def index(request):
    return response.html(HOME_PAGE)
