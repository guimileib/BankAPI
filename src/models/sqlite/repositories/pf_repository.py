from sqlalchemy.orm.exc import NoResultFound
from src.models.sqlite.entities.pessoa_fisica import PessoaFisicaTable
from src.models.sqlite.interfaces.pf_repository_interface import PFRepositoryInterface


class PFRepository(PFRepositoryInterface):
    
    def __init_(self, db_connection) -> None:
        self.__db_connection = db_connection
    
    def create_pf(self, nome: str, idade: int, celular: str, email: str, 
                  categoria: str, saldo: float) -> None: # não vou retornar nada porque é uma operação de escrita
        with self.__db_connection as database:
            try: 
                pf_data = PessoaFisicaTable(
                    nome=nome,
                    idade=idade,
                    celular=celular,
                    email=email,
                    categoria=categoria,
                    saldo=saldo
                )
                database.session.add(pf_data)
                database.session.commit()
            except Exception as exception:
                database.session.rollback()
                raise exception
            
        def get_pf(self, pf_id: int) -> PessoaFisicaTable:
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
        