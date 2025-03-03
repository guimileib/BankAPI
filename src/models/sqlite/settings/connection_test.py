import pytest
from sqlalchemy.engine import Engine
from .connection import db_connection_handler

#3@pytest.mark.skip(reason="interação com banco de dados") # Ignora o teste
def test_connect_to_db():
    assert db_connection_handler.get_engine() is None # Verifica se é None

    db_connection_handler.connect_to_db()
    db_engine = db_connection_handler.get_engine()

    assert db_engine is not None # Verifica se não é None
    assert isinstance(db_engine, Engine) # Verifica se é uma instância de Engine
