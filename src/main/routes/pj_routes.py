from flask import Blueprint, request, jsonify
from src.views.http_types.http_request  import HttpRequest

from src.main.composer.pj_composer import pj_composer

pj_view = pj_composer()

pj_routes = Blueprint('pj_routes', __name__)

@pj_routes.route('/pessoa-juridica', methods=['POST'])
def create_pj():
    http_request = HttpRequest(
        body=request.json
    )
    response = pj_view.create(http_request)
    return jsonify(response.body), response.status_code

@pj_routes.route('/pessoa-juridica/<int:pj_id>', methods=['GET'])
def get_pj(pj_id):
    http_request = HttpRequest(
        param={"id": pj_id}
    )
    response = pj_view.get(http_request)
    return jsonify(response.body), response.status_code

@pj_routes.route('/pessoa-juridica/<int:pj_id>/sacar', methods=['POST'])
def sacar_pj(pj_id):
    http_request = HttpRequest(
        param={"id": pj_id},
        body=request.json
    )
    response = pj_view.sacar(http_request)
    return jsonify(response.body), response.status_code

@pj_routes.route('/pessoa-juridica/<int:pj_id>/extrato', methods=['GET'])
def extrato_pj(pj_id):
    http_request = HttpRequest(
        param={"id": pj_id}
    )
    response = pj_view.extrato(http_request)
    return jsonify(response.body), response.status_code
