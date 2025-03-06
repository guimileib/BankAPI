from typing import Dict
import re
from .interfaces.pf_controller_interface import PFControllerInterface
from src.models.sqlite.interfaces.pf_repository_interface import PFRepositoryInterface

class PFController(PFControllerInterface):
    def __init__(self, pf_repository: PFRepositoryInterface) -> None:
        self.__pf_repository = pf_repository # Injeção de dependencia do repositorio
    
    def create(self, pf_info: Dict) -> Dict:
        nome_completo = pf_info['nome_completo']
        idade = pf_info['idade']
        celular = pf_info['celular']
        email = pf_info['email']
        categoria = pf_info['categoria']
        saldo = pf_info['saldo']
        renda_mensal = pf_info['renda_mensal']
        
        self.__validate_first_and_last_name(nome_completo)
        self.__insert_person_in_db(nome_completo, idade, celular, email, categoria, saldo, renda_mensal)
        formated_response = self.__format_response(pf_info)
        return formated_response
    
    def __validate_first_and_last_name(self, nome_completo: str) -> None:
        non_valid_caracteres = re.compile(r'[^a-zA-Z]')  # Expressão regular para encontrar caracteres não alfabéticos
        
        if non_valid_caracteres.search(nome_completo):
            raise ValueError("Nome completo deve conter apenas letras.")
        
    def __insert_person_in_db(self, nome_completo: str, idade: int, celular: str, email: str, categoria: str, saldo: float, renda_mensal: float) -> None:
        self.__pf_repository.create(nome_completo, idade, celular, email, categoria, saldo, renda_mensal)
    
    def __format_response(self, nome_completo: str, idade: int, celular: str, email: str, categoria: str, saldo: float, renda_mensal: float) -> Dict:
        return {
            "data":{
                'nome_completo': nome_completo,
                'idade': idade,
                'celular': celular,
                'email': email,
                'categoria': categoria,
                'saldo': saldo,
                'renda_mensal': renda_mensal
            }
        }
        
    