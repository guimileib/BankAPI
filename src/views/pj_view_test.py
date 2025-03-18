import pytest
from unittest.mock import MagicMock
from src.views.pj_view import PJView
from src.controllers.interfaces.pj_controller_interface import PJControllerInterface
from src.views.http_types.http_request import HttpRequest
from src.views.http_types.http_response import HttpResponse

def test_create_success():
    controller_mock = MagicMock(spec=PJControllerInterface)
    controller_mock.create.return_value = {"id": 1, "nome": "Empresa X"}
    view = PJView(controller_mock)
    
    request = HttpRequest(body={"nome": "Empresa X"})
    response = view.create(request)
    
    assert response.status_code == 201
    assert response.body == {"id": 1, "nome": "Empresa X"}
    controller_mock.create.assert_called_once_with({"nome": "Empresa X"})

def test_create_value_error():
    controller_mock = MagicMock(spec=PJControllerInterface)
    controller_mock.create.side_effect = ValueError("Dados inválidos")
    view = PJView(controller_mock)
    
    request = HttpRequest(body={})
    response = view.create(request)
    
    assert response.status_code == 400
    assert response.body == {"error": {"message": "Dados inválidos"}}

def test_get_success():
    controller_mock = MagicMock(spec=PJControllerInterface)
    controller_mock.get.return_value = {"id": 1, "nome": "Empresa X"}
    view = PJView(controller_mock)
    
    request = HttpRequest(param={"id": "1"})
    response = view.get(request)
    
    assert response.status_code == 200
    assert response.body == {"id": 1, "nome": "Empresa X"}
    controller_mock.get.assert_called_once_with(1)

def test_get_not_found():
    controller_mock = MagicMock(spec=PJControllerInterface)
    controller_mock.get.side_effect = ValueError("Empresa não encontrada")
    view = PJView(controller_mock)
    
    request = HttpRequest(param={"id": "999"})
    response = view.get(request)
    
    assert response.status_code == 404
    assert response.body == {"error": {"message": "Empresa não encontrada"}}

def test_sacar_success():
    controller_mock = MagicMock(spec=PJControllerInterface)
    controller_mock.sacar.return_value = "Saque realizado com sucesso"
    view = PJView(controller_mock)
    
    request = HttpRequest(param={"id": "1"}, body={"valor": "100.00"})
    response = view.sacar(request)
    
    assert response.status_code == 200
    assert response.body == {"data": "Saque realizado com sucesso"}
    controller_mock.sacar.assert_called_once_with(1, 100.00)

def test_sacar_valor_negativo():
    controller_mock = MagicMock(spec=PJControllerInterface)
    view = PJView(controller_mock)
    
    request = HttpRequest(param={"id": "1"}, body={"valor": "-50.00"})
    response = view.sacar(request)
    
    assert response.status_code == 400
    assert response.body == {"error": {"message": "Valor de saque deve ser positivo"}}

def test_extrato_success():
    controller_mock = MagicMock(spec=PJControllerInterface)
    controller_mock.extrato.return_value = [{"tipo": "crédito", "valor": 200.00, "data": "2025-03-18"}]
    view = PJView(controller_mock)
    
    request = HttpRequest(param={"id": "1"})
    response = view.extrato(request)
    
    assert response.status_code == 200
    assert response.body == {"data": {"transacoes": [{"tipo": "crédito", "valor": 200.00, "data": "2025-03-18"}]}}
    controller_mock.extrato.assert_called_once_with(1)
