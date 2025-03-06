from typing import Dict, List
from sqlalchemy.orm.exc import NoResultFound
from src.models.sqlite.entities.pessoa_juridica import PessoaJuridica
from src.models.sqlite.interfaces.pj_repository_interface import PJRepositoryInterface  

class PJRepository(PJRepositoryInterface):
    
    def __init__(self, db_connection) -> None:
        self.__db_connection = db_connection # Injeção de dependencia do banco de dados
        
    def create(self, nome_fantasia: str, faturamento: float, idade: int, celular: str, 
                  email_corporativo: str, categoria: str, saldo: float) -> None: # é um insert não retorna nada
        with self.__db_conncetion as database:
            try:
                pj_data = PessoaJuridica(
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
            
    def get(self, pj_id:int) -> PessoaJuridica:
        with self.__db_connection as database:
            try:
                pj = (
                    database.session
                    .query(PessoaJuridica)
                    .filter(PessoaJuridica.id == pj_id)
                    .one()
                    )
                return pj
            except NoResultFound:
                return None
            
    def sacar(self, pf_id: int, valor: float) -> bool:
        saldo_atual = self.__db_connection.fetch_one("SELECT saldo FROM pessoas_juridicas WHERE id = ?", (pf_id,))
        if saldo_atual and saldo_atual[0] >= valor:
            novo_saldo = saldo_atual[0] - valor
            self.__db.execute("UPDATE pessoas_juridicas SET saldo = ? WHERE id = ?", (novo_saldo, pf_id))
            return True
        return False
    
    def extrato(self, pf_id: int) -> List[Dict]:
        query = "SELECT tipo, valor, data FROM transacoes WHERE id = ? ORDER BY data DESC"
        return self.__db.fetch_all(query, (pf_id,))