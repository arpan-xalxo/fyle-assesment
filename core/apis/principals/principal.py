from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.principals import Principal  



from .schema import PrincipalSchema
principal_resources = Blueprint('principal_resources', __name__)


@principal_resources.route('/principals', methods=['GET'])
@decorators.authenticate_principal
def list_principals(p):
    """Returns list of all principals"""
    principals = Principal.query.all()
    principals_dump = PrincipalSchema().dump(principals, many=True)
    return APIResponse.respond(data=principals_dump)
