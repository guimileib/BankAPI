from sqlalchemy import Column, String, BIGINT, REAL
from src.models.sqlite.settings.base import Base

class PessoaFisicaTable(Base):
    __tablename__ = 'pessoa_fisica'
    
    id = Column(BIGINT, primary_key=True)
    idade = Column(BIGINT, nullable=False)
    nome_completo = Column(String, nullable=False)
    celular = Column(String, nullable=False)
    categoria = Column(String, nullable=False)
    saldo = Column(REAL, nullable=False)
    
    # Representação de como o objeto será exibido
    def __repr__(self):
        return f'PessoaFisica [nome_completo={self.nome_completo}, idade={self.idade}, celular={self.celular}, categoria={self.categoria}, saldo={self.saldo}]'
    