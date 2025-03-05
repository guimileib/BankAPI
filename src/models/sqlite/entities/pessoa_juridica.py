from sqlalchemy import Column, BIGINT, REAL, String
from src.models.sqlite.settings.base import Base

class PessoaJuridicaTable(Base):
    __tablename__ = 'pessoa_juridica'
    
    id = Column(BIGINT, primary_key=True)
    faturamento = Column(REAL, nullable=False)
    idade = Column(BIGINT, nullable=False)
    nome_fantasia = Column(String, nullable=False)
    celular = Column(String, nullable=False)
    email_corporativo = Column(String, nullable=False)
    categoria = Column(String, nullable=False)
    saldo = Column(REAL, nullable=False)
    
    def sacar(self, valor):
        limite_saque = 5000  # Limite maior para Pessoa Jurídica
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
        return f'PessoaJuridica [nome_fantasia={self.nome_fantasia}, idade={self.idade}, celular={self.celular}, email_corporativo={self.email_corporativo}, categoria={self.categoria}, saldo={self.saldo}]'
    