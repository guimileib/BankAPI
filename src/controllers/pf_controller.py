from typing import Dict
import re
from .interfaces.pf_controller_interface import PFControllerInterface
from src.models.sqlite.entities.pessoa_fisica import PessoaFisicaTable
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
        
        self. __validate_name(nome_completo)
        self.__insert_person_in_db(nome_completo, idade, celular, email, categoria, saldo, renda_mensal)
        formated_response = self.__format_response(pf_info)
        return formated_response
    
    def __validate_name(self, nome_completo: str) -> None:
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
    
    def get(self, pf_id:int) -> Dict:
        pf = self.__get_pf_from_db(pf_id)
        response = self.__format_response(pf)
        return response
        
    def __get_pf_from_db(self, pf_id:int) -> PessoaFisicaTable:
        pf = self.__pf_repository.get(pf_id)
        if not pf:
            raise ValueError("Pessoa física não encontrada.")
        return pf
    
    def sacar(self, pf_id: int, valor: float) -> Dict:
        self.__withdraw_money_from_db(pf_id, valor)
        response = self.__format_response_for_withdraw(pf_id, valor)
        return response
    
    def __withdraw_money_from_db(self, pf_id: int, valor: float) -> None:
        if not self.__pf_repository.sacar(pf_id, valor):
            raise ValueError("Saldo insuficiente.")
        
    def __format_response_for_withdraw(self, pf_id: int, valor: float) -> Dict:
        return {
            "data":{
                "id": pf_id,
                "valor_sacado": valor
            }
        }
        