from typing import List, Dict
from sqlalchemy.orm.exc import NoResultFound
from src.models.sqlite.entities.pessoa_fisica import PessoaFisicaTable
from src.models.sqlite.interfaces.pf_repository_interface import PFRepositoryInterface

class PFRepository(PFRepositoryInterface):
    
    def __init__(self, db_connection) -> None:
        self.__db_connection = db_connection
    
    def create(self, nome_completo: str, idade: int, celular: str, email: str, 
                  categoria: str, saldo: float, renda_mensal: float) -> None: # não vou retornar nada porque é uma operação de escrita
        with self.__db_connection as database:
            try: 
                pf_data = PessoaFisicaTable(
                    nome_completo=nome_completo,
                    idade=idade,
                    celular=celular,
                    email=email,
                    categoria=categoria,
                    saldo=saldo,
                    renda_mensal=renda_mensal
                )
                database.session.add(pf_data)
                database.session.commit()
            except Exception as exception:
                database.session.rollback()
                raise exception
            
    def get(self, pf_id: int) -> PessoaFisicaTable:
        with self.__db_connection as database:
            try:
                pf = (
                    database.session
                    .query(PessoaFisicaTable)
                    .filter(PessoaFisicaTable.id == pf_id)
                    .one()
                )
                return pf
            except NoResultFound:
                return None
    
    def sacar(self, pf_id: int, valor: float) -> bool:
        # Verifica saldo
        with self.__db_connection as database:
            try:
                saldo_atual = database.fetch_one("SELECT saldo FROM pessoas_fisicas WHERE id = ?", (pf_id,))
                if saldo_atual and saldo_atual[0] >= valor:
                    novo_saldo = saldo_atual[0] - valor
                    database.execute("UPDATE pessoas_fisicas SET saldo = ? WHERE id = ?", (novo_saldo, pf_id))
                    return True
                return False
            except Exception as exception:
                return False
    
    def extrato(self, pf_id: int) -> List[Dict]:
        with self.__db_connection as database:
            try:
                query = "SELECT tipo, valor, data FROM transacoes WHERE id = ? ORDER BY data DESC"
                return database.fetch_all(query, (pf_id,))
            except Exception:
                return []