import pytest
from unittest.mock import MagicMock
from src.models.sqlite.settings.connection import db_connection_handler
from src.models.sqlite.entities.pessoa_fisica import PessoaFisicaTable
from src.models.sqlite.repositories.pf_repository import PFRepository
from sqlalchemy.orm.exc import NoResultFound

db_connection_handler.connect_to_db()

@pytest.fixture
def mock_db():
    # Mock da conexão com o banco de dados
    mock_db_connection = MagicMock()
    return mock_db_connection


@pytest.fixture
def pf_repository(mock_db):
    
   pf_repository = PFRepository(mock_db) # Instância do repositório com a conexão mockada


def test_create(pf_repository, mock_db):
    # Teste para o método create
    mock_db.__enter__.return_value.session.add = MagicMock()
    mock_db.__enter__.return_value.session.commit = MagicMock()

    pf_repository.create(
        nome_completo="João da Silva",
        idade=30,
        celular="999999999",
        email="joao@teste.com",
        categoria="Categoria1",
        saldo=1000.0,
        renda_mensal=5000.0
    )

    mock_db.__enter__.return_value.session.add.assert_called_once()
    mock_db.__enter__.return_value.session.commit.assert_called_once()


def test_get_found(pf_repository, mock_db):
    
    mock_person = MagicMock(PessoaFisicaTable)
    mock_person.id = 1
    mock_person.nome_completo = "João da Silva"
    mock_db.__enter__.return_value.session.query.return_value.filter.return_value.one.return_value = mock_person
    result = pf_repository.get(1)
    
    assert result == mock_person


def test_get_not_found(pf_repository, mock_db):

    mock_db.__enter__.return_value.session.query.return_value.filter.return_value.one.side_effect = NoResultFound
    result = pf_repository.get(1)

    assert result is None


def test_sacar_sucesso(pf_repository, mock_db):
    # Teste para o método sacar (caso o saque seja bem-sucedido)

    mock_db.fetch_one.return_value = (1000.0,)  # seta saldo = 1000
    mock_db.execute = MagicMock() # Mock do método execute
    
    result = pf_repository.sacar(1, 500.0) # Testa o saque
    
    assert result == True
    mock_db.execute.assert_called_once_with("UPDATE pessoas_fisicas SET saldo = ? WHERE id = ?", (500.0, 1))
    


def test_sacar_erro_saldo_insuficiente(pf_repository, mock_db):
    # Teste para o método `sacar` (caso o saldo seja insuficiente)
    mock_db.fetch_one.return_value = (100.0,)  
    result = pf_repository.sacar(1, 500.0)

    assert result == False
    mock_db.execute.assert_not_called()

def test_extrato(pf_repository, mock_db):
    # Teste para o método extrato
    mock_db.fetch_all.return_value = [
        {"tipo": "Saque", "valor": 100.0, "data": "2025-03-01"},
        {"tipo": "Depósito", "valor": 200.0, "data": "2025-03-02"}
    ]

    result = pf_repository.extrato(1) # Testa o extrato

    # Verifica se as transações foram retornadas corretamente
    assert len(result) == 2
    assert result[0]["tipo"] == "Saque"
    assert result[1]["valor"] == 200.0
