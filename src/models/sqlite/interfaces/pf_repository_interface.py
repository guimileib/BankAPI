from abc import ABC, abstractmethod
from src.models.sqlite.entities.pessoa_fisica import PessoaFisicaTable

class PFRepositoryInterface(ABC):
    
    @abstractmethod
    def create_pf(self, nome: str, idade: int, celular: str, email: str, saldo: float) -> None:
        pass
    
    @abstractmethod
    def get_pf(self, pf_id: int) -> PessoaFisicaTable:
        pass