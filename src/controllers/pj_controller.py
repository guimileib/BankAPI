import datetime
from typing import Dict, List
import re
from .interfaces.pj_controller_interface import PJControllerInterface
from src.models.sqlite.entities.pessoa_juridica import PessoaJuridicaTable
from src.models.sqlite.interfaces.pj_repository_interface import PJRepositoryInterface

class PJController(PJControllerInterface):
    def __init__(self, pj_repository: PJRepositoryInterface) -> None:
        self.__pj_repository = pj_repository # Injeção de dependencia do repositorio
    
    def create(self, pj_info: Dict) -> Dict:
        nome_fantasia = pj_info['nome_fantasia']
        idade = pj_info['idade']
        celular = pj_info['celular']
        email_corporativo = pj_info['email_corporativo']
        categoria = pj_info['categoria']
        saldo = pj_info['saldo']
        faturamento = pj_info['faturamento']

        self. __validate_name(nome_fantasia)
        self.__insert_person_in_db(nome_fantasia, idade, celular, email_corporativo, categoria, saldo, faturamento)
        formated_response = self.__format_response(pj_info)
        return formated_response
    
        # Usei a mesma estrutura de Pessoa Física, ja que muda apenas os atributos
    def __validate_name(self, nome_completo: str) -> None:
        non_valid_caracteres = re.compile(r'[^a-zA-Z]')  # Expressão regular para encontrar caracteres não alfabéticos
        
        if non_valid_caracteres.search(nome_completo):
            raise ValueError("Nome completo deve conter apenas letras.")
    
    def __insert_person_in_db(self, nome_fantasia: str, idade: int, celular: str, email_corporativo: str, categoria: str, saldo: float, faturamento: float) -> None:
        self.__pj_repository.create(nome_fantasia, idade, celular, email_corporativo, categoria, saldo, faturamento)
    
    def __format_response(self, nome_fantasia: str, idade: int, celular: str, email_corporativo: str, categoria: str, saldo: float, faturamento: float) -> Dict:
        return {
            "data":{
                'nome_fantasia': nome_fantasia,
                'idade': idade,
                'celular': celular,
                'email_corporativo': email_corporativo,
                'categoria': categoria,
                'saldo': saldo,
                'faturamento': faturamento
            }
        }
    
    def get(self, pj_id:int) -> Dict:
        pj = self.__get_pj_from_db(pj_id)
        response = self.__format_response(pj)
        return response

    def __get_pj_from_db(self, pj_id:int) -> PessoaJuridicaTable:
        pj = self.__pj_repository.get(pj_id)
        if not pj:
            raise ValueError("Pessoa jurídica não encontrada.")
        return pj
    
    def sacar(self, pj_id: int, valor: float) -> Dict:
        self.__withdraw_money_from_db(pj_id, valor)

        transacao = {
            "tipo": "saque",
            "valor": valor,
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        if pj_id not in self.__historico_transacoes:
            self.__historico_transacoes[pj_id] = []
        
        self.__historico_transacoes[pj_id].append(transacao)

        return transacao

    def extrato(self, pj_id: int) -> List[Dict]:
        return self.__historico_transacoes.get(pj_id, [])
    
    def __withdraw_money_from_db(self, pj_id: int, valor: float) -> None:
        if not self.__pj_repository.sacar(pj_id, valor):
            raise ValueError("Saldo insuficiente.")
    