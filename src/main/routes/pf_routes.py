from flask import Blueprint, request, jsonify
from src.views.http_types.http_request  import HttpRequest

from src.main.composer.pf_composer import pf_composer

pf_view = pf_composer()

pf_routes = Blueprint('pj_routes', __name__)

@pf_routes.route('/pessoa-fisica', methods=['POST'])
def create_pf():
    http_request = HttpRequest(
        body=request.json
    )
    response = pf_view.create(http_request)
    return jsonify(response.body), response.status_code

@pf_routes.route('/pessoa-fisica/<int:pf_id>', methods=['GET'])
def get_pf(pf_id):
    http_request = HttpRequest(
        param={"id": pf_id}
    )
    response = pf_view.get(http_request)
    return jsonify(response.body), response.status_code

@pf_routes.route('/pessoa-fisica/<int:pf_id>/sacar', methods=['POST'])
def sacar_pf(pf_id):
    http_request = HttpRequest(
        param={"id": pf_id},
        body=request.json
    )
    response = pf_view.sacar(http_request)
    return jsonify(response.body), response.status_code

@pf_routes.route('/pessoa-fisica/<int:pf_id>/extrato', methods=['GET'])
def extrato_pf(pf_id):
    http_request = HttpRequest(
        param={"id": pf_id}
    )
    response = pf_view.extrato(http_request)
    return jsonify(response.body), response.status_code