from .things import ThingsResource, SmallThingsResource
from .products import ProductResource
"""
from .users import UsersResource
from .authentication import AuthResource"""



def apply_routes(app):
    app.add_route('/things',ThingsResource())
    app.add_route('/things/{name}',SmallThingsResource())
    app.add_route('/products',ProductResource())
    #app.add_route('/users',UsersResource())
    #app.add_route('/authentication',AuthResource())