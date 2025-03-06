from typing import Dict
import re
from .interfaces.pj_controller_interface import PJControllerInterface
from src.models.sqlite.interfaces.pj_repository_interface import PJRepositoryInterface

class PJController(PJControllerInterface):
    def __init__(self, pj_repository: PJRepositoryInterface) -> None:
        self.__pj_repository = pj_repository # Injeção de dependencia do repositorio
    
    def create(self, pf_info: Dict) -> Dict:
        nome_fantasia = pf_info['nome_fantasia']
        idade = pf_info['idade']
        celular = pf_info['celular']
        email_corporativo = pf_info['email_corporativo']
        categoria = pf_info['categoria']
        saldo = pf_info['saldo']
        faturamento = pf_info['faturamento']
    
        
    
   