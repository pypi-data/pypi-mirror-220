from flask import Blueprint, jsonify

from foobar.core import doc


bp = Blueprint('home', __name__)


@doc(tags=['Home'], description='home',
     responses={'200': {
         'description': 'success',
         'schema': {
             'type': 'object',
             'properties': {
                 'message': {'type': 'string'}
             }
         }
     }})
@bp.route('', methods=('GET', ), provide_automatic_options=False)
def home():
    return jsonify({
        'message': 'Hello visitor, Welcome to TestFromLocal_Json_App_0!'
    })
