from sanic import Blueprint, response

from core import auth

project = Blueprint('project')


INDEX_PAGE = '''
You have no projects.
<a href="/">go back home</a>
'''


@project.route('/')
@auth.login_required
async def index(request):
    return response.html(INDEX_PAGE)
