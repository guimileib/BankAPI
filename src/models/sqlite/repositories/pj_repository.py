from typing import Dict, List
from sqlalchemy.orm.exc import NoResultFound
from src.models.sqlite.entities.pessoa_juridica import PessoaJuridicaTable
from src.models.sqlite.interfaces.pj_repository_interface import PJRepositoryInterface  

class PJRepository(PJRepositoryInterface):
    
    def __init__(self, db_connection) -> None:
        self.__db_connection = db_connection # Injeção de dependencia do banco de dados
        
    def create(self, nome_fantasia: str, faturamento: float, idade: int, celular: str, 
                  email_corporativo: str, categoria: str, saldo: float) -> None: # é um insert não retorna nada
        with self.__db_connection as database:
            try:
                pj_data = PessoaJuridicaTable(
                    nome_fantasia=nome_fantasia,
                    faturamento=faturamento,
                    idade=idade,
                    celular=celular,
                    email_corporativo=email_corporativo,
                    categoria=categoria,
                    saldo=saldo
                )
                database.session.add(pj_data) # Operação ocorre so dentro da sessao ativa (.sessao)
                database.session.commit()
            except Exception as exception:
                database.session.rollback() # desfaz operação
                raise exception
            
    def get(self, pj_id:int) -> PessoaJuridicaTable:
        with self.__db_connection as database:
            try:
                pj = (
                    database.session
                    .query(PessoaJuridicaTable)
                    .filter(PessoaJuridicaTable.id == pj_id)
                    .one()
                    )
                return pj
            except NoResultFound:
                return None
            
    def sacar(self, pj_id: int, valor: float) -> bool:
        with self.__db_connection as database:
            try:
                saldo_atual = database.fetch_one("SELECT saldo FROM pessoas_juridicas WHERE id = ?", (pj_id,))
                if saldo_atual and saldo_atual[0] >= valor:
                    novo_saldo = saldo_atual[0] - valor
                    database.execute("UPDATE pessoas_juridicas SET saldo = ? WHERE id = ?", (novo_saldo, pj_id))
                    return True
                return False
            except Exception as exception:
                return False
    
    def extrato(self, pj_id: int) -> List[Dict]:
        with self.__db_connection as database:
            try:
                query = "SELECT tipo, valor, data FROM transacoes WHERE id = ? ORDER BY data DESC"
                return database.fetch_all(query, (pj_id,))
            except Exception:
                return []