from sanic_auth import Auth

# This Auth object is shared by all blueprints
auth = Auth()

# This is also a good place for other shared objects, such as SQLalchemy-style
# database engine object.

# Some people use the root __init__.py file of the web application package for
# this purpose, as long as the package structure does not cause circular
# import, you are good to go.
