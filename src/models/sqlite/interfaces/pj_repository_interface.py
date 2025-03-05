from typing import List, Dict
from abc import ABC, abstractmethod
from src.models.sqlite.entities.pessoa_juridica import PessoaJuridicaTable

class PJRepositoryInterface(ABC):
    
    @abstractmethod
    def create(self, nome: str, idade: int, celular: str, email: str, saldo: float) -> None:
        pass
    
    @abstractmethod
    def get(self, pf_id: int) -> PessoaJuridicaTable:
        pass
    
    @abstractmethod
    def sacar(self, pf_id: int, valor: float) -> bool:
        pass
    
    @abstractmethod
    def extrato(self, pf_id: int) -> List[Dict]:
        pass