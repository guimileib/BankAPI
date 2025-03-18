from unittest import mock
import pytest
from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from sqlalchemy.orm.exc import NoResultFound

from src.models.sqlite.entities.pessoa_juridica import PessoaJuridicaTable
from src.models.sqlite.repositories.pj_repository import PJRepository


class MockConnection:
    def __init__(self) -> None:
        self.session = UnifiedAlchemyMagicMock(
            data=[
                (
                    [mock.call.query(PessoaJuridicaTable)], 
                    [
                        PessoaJuridicaTable(
                            id=1,
                            nome_fantasia="Empresa A",
                            faturamento=100000.0,
                            idade=5,
                            celular="11999999999",
                            email_corporativo="empresa.a@email.com",
                            categoria="MEI",
                            saldo=5000.0
                        ),
                        PessoaJuridicaTable(
                            id=2,
                            nome_fantasia="Empresa B",
                            faturamento=500000.0,
                            idade=10,
                            celular="11888888888",
                            email_corporativo="empresa.b@email.com",
                            categoria="EPP",
                            saldo=25000.0
                        )
                    ]  # resultado
                ),
                (
                    [mock.call.query(PessoaJuridicaTable),
                     mock.call.filter(PessoaJuridicaTable.id == 1)],
                    [
                        PessoaJuridicaTable(
                            id=1,
                            nome_fantasia="Empresa A",
                            faturamento=100000.0,
                            idade=5,
                            celular="11999999999",
                            email_corporativo="empresa.a@email.com",
                            categoria="MEI",
                            saldo=5000.0
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
        
        self.fetch_one = mock.MagicMock(return_value=(5000.0,))
        self.fetch_all = mock.MagicMock(return_value=[
            ("Depósito", 5000.0, "2024-03-01"),
            ("Saque", 1000.0, "2024-03-05")
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
        self.fetch_one = mock.MagicMock(return_value=(500.0,))
        self.execute = mock.MagicMock()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class TestPJRepository:

    def test_create_success(self):
        mock_connection = MockConnection()
        repo = PJRepository(mock_connection)
        
        repo.create(
            nome_fantasia="Empresa Teste",
            faturamento=200000.0,
            idade=3,
            celular="11977777777",
            email_corporativo="empresa.teste@email.com",
            categoria="ME",
            saldo=10000.0
        )
        
        mock_connection.session.add.assert_called_once()
        mock_connection.session.commit.assert_called_once()
        
        # Verifica o objeto adicionado
        added_obj = mock_connection.session.add.call_args[0][0]
        assert isinstance(added_obj, PessoaJuridicaTable)
        assert added_obj.nome_fantasia == "Empresa Teste"
        assert added_obj.faturamento == 200000.0
        assert added_obj.idade == 3
        assert added_obj.celular == "11977777777"
        assert added_obj.email_corporativo == "empresa.teste@email.com"
        assert added_obj.categoria == "ME"
        assert added_obj.saldo == 10000.0

    def test_create_exception(self):
        mock_connection = MockConnection()
        # Configurar o mock para lançar uma exceção no commit
        mock_connection.session.commit.side_effect = Exception("Erro ao salvar")
        repo = PJRepository(mock_connection)
        
        with pytest.raises(Exception):
            repo.create(
                nome_fantasia="Empresa Teste",
                faturamento=200000.0,
                idade=3,
                celular="11977777777",
                email_corporativo="empresa.teste@email.com",
                categoria="ME",
                saldo=10000.0
            )
        
        mock_connection.session.rollback.assert_called_once()

    def test_get_success(self):
        mock_connection = MockConnection()
        repo = PJRepository(mock_connection)
        
        result = repo.get(1)
        
        mock_connection.session.query.assert_called_with(PessoaJuridicaTable)
        assert isinstance(result, PessoaJuridicaTable)
        assert result.id == 1
        assert result.nome_fantasia == "Empresa A"

    def test_get_not_found(self):
        mock_connection = MockConnectionNoResult()
        repo = PJRepository(mock_connection)
        
        result = repo.get(999)
        
        mock_connection.session.query.assert_called_with(PessoaJuridicaTable)
        assert result is None

    def test_sacar_success(self):
        mock_connection = MockConnectionSaldoSuficiente()
        repo = PJRepository(mock_connection)
        
        result = repo.sacar(1, 1000.0)
        
        mock_connection.fetch_one.assert_called_once_with(
            "SELECT saldo FROM pessoas_juridicas WHERE id = ?", 
            (1,)
        )
        mock_connection.execute.assert_called_once_with(
            "UPDATE pessoas_juridicas SET saldo = ? WHERE id = ?", 
            (4000.0, 1)
        )
        assert result is True

    def test_sacar_saldo_insuficiente(self):
        mock_connection = MockConnectionSaldoInsuficiente()
        repo = PJRepository(mock_connection)
        
        result = repo.sacar(1, 1000.0)
        
        mock_connection.fetch_one.assert_called_once_with(
            "SELECT saldo FROM pessoas_juridicas WHERE id = ?", 
            (1,)
        )
        mock_connection.execute.assert_not_called()
        assert result is False

    def test_sacar_conta_inexistente(self):
        """Testa saque de conta inexistente"""
        mock_connection = MockConnectionNoResult()
        repo = PJRepository(mock_connection)
        
        result = repo.sacar(999, 1000.0)
        
        mock_connection.fetch_one.assert_called_once_with(
            "SELECT saldo FROM pessoas_juridicas WHERE id = ?", 
            (999,)
        )
        mock_connection.execute.assert_not_called()
        assert result is False

    def test_extrato(self):
        mock_connection = MockConnectionSaldoSuficiente()
        repo = PJRepository(mock_connection)
        
        result = repo.extrato(1)
        
        mock_connection.fetch_all.assert_called_once_with(
            "SELECT tipo, valor, data FROM transacoes WHERE id = ? ORDER BY data DESC",
            (1,)
        )
        assert len(result) == 2
        assert result[0][0] == "Depósito"
        assert result[0][1] == 5000.0
        assert result[1][0] == "Saque"
        assert result[1][1] == 1000.0