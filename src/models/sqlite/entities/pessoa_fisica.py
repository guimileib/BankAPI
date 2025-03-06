from sqlalchemy import Column, String, BIGINT, REAL
from src.models.sqlite.settings.base import Base

class PessoaFisicaTable(Base):
    __tablename__ = 'pessoa_fisica'
    
    id = Column(BIGINT, primary_key=True)
    idade = Column(BIGINT, nullable=False)
    nome_completo = Column(String, nullable=False)
    celular = Column(String, nullable=False)
    email = Column(String, nullable=False)
    categoria = Column(String, nullable=False)
    saldo = Column(REAL, nullable=False)
    renda_mensal = Column(REAL, nullable=False)
    
    def sacar(self, valor):
        limite_saque = 1000  # Limite menor para Pessoa Física
        if valor > self.saldo:
            raise ValueError("Saldo insuficiente.")
        if valor > limite_saque:
            raise ValueError(f"Limite de saque excedido! O máximo permitido é R$ {limite_saque}.")
        
        self.saldo -= valor
        return f"Saque de R$ {valor} realizado. Novo saldo: R$ {self.saldo:.2f}"

    def extrato(self):
        return f"Saldo atual: R$ {self.saldo:.2f}"
    
    # Representação de como o objeto será exibido
    def __repr__(self):
        return f'PessoaFisica [nome_completo={self.nome_completo}, idade={self.idade}, celular={self.celular}, email={self.email},categoria={self.categoria}, saldo={self.saldo}, renda_mensal={self.renda_mensal}]'
    