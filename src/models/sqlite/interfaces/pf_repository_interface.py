from typing import List, Dict
from abc import ABC, abstractmethod
from src.models.sqlite.entities.pessoa_fisica import PessoaFisicaTable

class PFRepositoryInterface(ABC):
    
    @abstractmethod
    def create(self, nome: str, idade: int, celular: str, email: str, saldo: float) -> None:
        pass
    
    @abstractmethod
    def get(self, pf_id: int) -> PessoaFisicaTable:
        pass
    
    @abstractmethod
    def sacar(self, pj_id: int, valor: float) -> bool:
        pass
    
    @abstractmethod
    def extrato(self, pj_id: int) -> List[Dict]:
        pass