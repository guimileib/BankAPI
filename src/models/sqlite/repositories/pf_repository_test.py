from unittest import mock
import pytest
from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from sqlalchemy.orm.exc import NoResultFound

from src.models.sqlite.entities.pessoa_fisica import PessoaFisicaTable
from src.models.sqlite.interfaces.pf_repository_interface import PFRepositoryInterface
from src.models.sqlite.repositories.pf_repository import PFRepository


class MockConnection:
    def __init__(self) -> None:
        self.session = UnifiedAlchemyMagicMock(
            data=[
                (
                    [mock.call.query(PessoaFisicaTable)], 
                    [
                        PessoaFisicaTable(
                            id=1,
                            nome_completo="João Silva",
                            idade=30,
                            celular="11999999999",
                            email="joao@example.com",
                            categoria="Standard",
                            saldo=1000.0,
                            renda_mensal=5000.0
                        ),
                        PessoaFisicaTable(
                            id=2,
                            nome_completo="Maria Souza",
                            idade=35,
                            celular="11888888888",
                            email="maria@example.com",
                            categoria="Premium",
                            saldo=2000.0,
                            renda_mensal=7000.0
                        )
                    ]  # resultado
                ),
                (
                    [mock.call.query(PessoaFisicaTable),
                     mock.call.filter(PessoaFisicaTable.id == 1)],
                    [
                        PessoaFisicaTable(
                            id=1,
                            nome_completo="João Silva",
                            idade=30,
                            celular="11999999999",
                            email="joao@example.com",
                            categoria="Standard",
                            saldo=1000.0,
                            renda_mensal=5000.0
                        )
                    ]
                )
            ]
        )
        
        self.fetch_one = mock.MagicMock()
        self.fetch_all = mock.MagicMock()
        self.execute = mock.MagicMock()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class MockConnectionNoResult:
    def __init__(self) -> None:
        self.session = UnifiedAlchemyMagicMock()
        self.session.query.side_effect = self.__raise_no_result_found  # força a exceção
        self.session.rollback = mock.MagicMock()
        
        self.fetch_one = mock.MagicMock(return_value=None)
        self.fetch_all = mock.MagicMock(return_value=[])
        self.execute = mock.MagicMock()

    def __raise_no_result_found(self, *args, **kwargs):
        raise NoResultFound("No result found")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class MockConnectionSaldoSuficiente:
    def __init__(self) -> None:
        self.session = UnifiedAlchemyMagicMock()
        
        # Para métodos que usam execução SQL direta
        self.fetch_one = mock.MagicMock(return_value=(1000.0,))
        self.fetch_all = mock.MagicMock(return_value=[
            ("Depósito", 2000.0, "2024-03-01"),
            ("Saque", 500.0, "2024-03-05")
        ])
        self.execute = mock.MagicMock()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class MockConnectionSaldoInsuficiente:
    def __init__(self) -> None:
        self.session = UnifiedAlchemyMagicMock()
        
        # Para métodos que usam execução SQL direta
        self.fetch_one = mock.MagicMock(return_value=(200.0,))
        self.execute = mock.MagicMock()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class TestPFRepository:
    def test_create_success(self):
        mock_connection = MockConnection()
        repo = PFRepository(mock_connection)
        
        repo.create(
            nome_completo="Ana Pereira",
            idade=28,
            celular="11977777777",
            email="ana@example.com",
            categoria="Basic",
            saldo=500.0,
            renda_mensal=4000.0
        )
        
        mock_connection.session.add.assert_called_once()
        mock_connection.session.commit.assert_called_once()
        
        # Verifica o objeto adicionado
        added_obj = mock_connection.session.add.call_args[0][0]
        assert isinstance(added_obj, PessoaFisicaTable)
        assert added_obj.nome_completo == "Ana Pereira"
        assert added_obj.idade == 28
        assert added_obj.celular == "11977777777"
        assert added_obj.email == "ana@example.com"
        assert added_obj.categoria == "Basic"
        assert added_obj.saldo == 500.0
        assert added_obj.renda_mensal == 4000.0

    def test_create_exception(self):
        mock_connection = MockConnection()
        # Configurar o mock para lançar uma exceção no commit
        mock_connection.session.commit.side_effect = Exception("Erro ao salvar")
        repo = PFRepository(mock_connection)
        
        with pytest.raises(Exception):
            repo.create(
                nome_completo="Ana Pereira",
                idade=28,
                celular="11977777777",
                email="ana@example.com",
                categoria="Basic",
                saldo=500.0,
                renda_mensal=4000.0
            )
        
        mock_connection.session.rollback.assert_called_once()

    def test_get_success(self):
        mock_connection = MockConnection()
        repo = PFRepository(mock_connection)
        
        result = repo.get(1)

        mock_connection.session.query.assert_called_with(PessoaFisicaTable)
        assert isinstance(result, PessoaFisicaTable)
        assert result.id == 1
        assert result.nome_completo == "João Silva"
        assert result.idade == 30
        assert result.celular == "11999999999"
        assert result.email == "joao@example.com"
        assert result.categoria == "Standard"
        assert result.saldo == 1000.0
        assert result.renda_mensal == 5000.0

    def test_get_not_found(self):
        mock_connection = MockConnectionNoResult()
        repo = PFRepository(mock_connection)
        
        result = repo.get(999)
        
        mock_connection.session.query.assert_called_with(PessoaFisicaTable)
        assert result is None

    def test_sacar_success(self):
        mock_connection = MockConnectionSaldoSuficiente()
        repo = PFRepository(mock_connection)
        repo._PFRepository__db = mock_connection

        result = repo.sacar(1, 500.0)
        
        mock_connection.fetch_one.assert_called_once_with(
            "SELECT saldo FROM pessoas_fisicas WHERE id = ?", 
            (1,)
        )
        mock_connection.execute.assert_called_once_with(
            "UPDATE pessoas_fisicas SET saldo = ? WHERE id = ?", 
            (500.0, 1)
        )
        assert result is True

    def test_sacar_saldo_insuficiente(self):
        mock_connection = MockConnectionSaldoInsuficiente()
        repo = PFRepository(mock_connection)
        
        result = repo.sacar(1, 500.0)
        
        mock_connection.fetch_one.assert_called_once_with(
            "SELECT saldo FROM pessoas_fisicas WHERE id = ?", 
            (1,)
        )
        mock_connection.execute.assert_not_called()
        assert result is False

    def test_sacar_conta_inexistente(self):
        mock_connection = MockConnectionNoResult()
        repo = PFRepository(mock_connection)
        
        result = repo.sacar(999, 500.0)
        
        mock_connection.fetch_one.assert_called_once_with(
            "SELECT saldo FROM pessoas_fisicas WHERE id = ?", 
            (999,)
        )
        mock_connection.execute.assert_not_called()
        assert result is False

    def test_extrato(self):
        mock_connection = MockConnectionSaldoSuficiente()
        repo = PFRepository(mock_connection)
        # Corrigir referência para variável privada
        repo._PFRepository__db = mock_connection
        
        result = repo.extrato(1)
        
        mock_connection.fetch_all.assert_called_once_with(
            "SELECT tipo, valor, data FROM transacoes WHERE id = ? ORDER BY data DESC",
            (1,)
        )
        assert len(result) == 2
        assert result[0][0] == "Depósito"
        assert result[0][1] == 2000.0
        assert result[1][0] == "Saque"
        assert result[1][1] == 500.0
        