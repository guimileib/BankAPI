from abc import ABC, abstractmethod
from src.models.sqlite.entities.pessoa_juridica import PessoaJuridicaTable

class PJRepositoryInterface(ABC):
    
    @abstractmethod
    def create_pj(self, nome: str, idade: int, celular: str, email: str, saldo: float) -> None:
        pass
    
    @abstractmethod
    def get_pj(self, pf_id: int) -> PessoaJuridicaTable:
        pass