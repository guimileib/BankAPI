import pytest
from unittest.mock import MagicMock
from src.views.pf_view import PFView
from src.controllers.interfaces.pf_controller_interface import PFControllerInterface
from src.views.http_types.http_request import HttpRequest
from src.views.http_types.http_response import HttpResponse

@pytest.fixture
def mock_controller():
    return MagicMock(spec=PFControllerInterface)

@pytest.fixture
def pf_view(mock_controller):
    return PFView(controller=mock_controller)

def test_create_success(pf_view, mock_controller):
    mock_controller.create.return_value = {"id": 1, "nome": "Teste"}
    http_request = HttpRequest(body={"nome": "Teste"})
    response = pf_view.create(http_request)
    
    assert response.status_code == 201
    assert response.body == {"id": 1, "nome": "Teste"}
    mock_controller.create.assert_called_once_with({"nome": "Teste"})

def test_create_invalid_data(pf_view, mock_controller):
    mock_controller.create.side_effect = ValueError("Nome inválido")
    http_request = HttpRequest(body={"nome": "123"})
    response = pf_view.create(http_request)
    
    assert response.status_code == 400
    assert response.body == {"error": {"message": "Nome inválido"}}

def test_get_success(pf_view, mock_controller):
    mock_controller.get.return_value = {"id": 1, "nome": "Teste"}
    http_request = HttpRequest(param={"id": "1"})
    response = pf_view.get(http_request)
    
    assert response.status_code == 200
    assert response.body == {"id": 1, "nome": "Teste"}
    mock_controller.get.assert_called_once_with(1)

def test_get_not_found(pf_view, mock_controller):
    mock_controller.get.side_effect = ValueError("Pessoa não encontrada")
    http_request = HttpRequest(param={"id": "999"})
    response = pf_view.get(http_request)
    
    assert response.status_code == 404
    assert response.body == {"error": {"message": "Pessoa não encontrada"}}

def test_sacar_success(pf_view, mock_controller):
    mock_controller.sacar.return_value = {"id": 1, "valor_sacado": 100.0}
    http_request = HttpRequest(param={"id": "1"}, body={"valor": 100.0})
    response = pf_view.sacar(http_request)
    
    assert response.status_code == 200
    assert response.body == {"data": {"id": 1, "valor_sacado": 100.0}}
    mock_controller.sacar.assert_called_once_with(1, 100.0)

def test_sacar_invalid_value(pf_view, mock_controller):
    http_request = HttpRequest(param={"id": "1"}, body={"valor": -50})
    response = pf_view.sacar(http_request)
    
    assert response.status_code == 400
    assert response.body == {"error": {"message": "Valor de saque deve ser positivo"}}

def test_extrato_success(pf_view, mock_controller):
    mock_controller.extrato.return_value = [{"tipo": "saque", "valor": 50.0, "data": "2025-03-18"}]
    http_request = HttpRequest(param={"id": "1"})
    response = pf_view.extrato(http_request)
    
    assert response.status_code == 200
    assert response.body == {"data": {"transacoes": [{"tipo": "saque", "valor": 50.0, "data": "2025-03-18"}]}}
    mock_controller.extrato.assert_called_once_with(1)

def test_extrato_not_found(pf_view, mock_controller):
    mock_controller.extrato.side_effect = ValueError("Pessoa não encontrada")
    http_request = HttpRequest(param={"id": "999"})
    response = pf_view.extrato(http_request)
    
    assert response.status_code == 404
    assert response.body == {"error": {"message": "Pessoa não encontrada"}}
    