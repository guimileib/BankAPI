from src.models.sqlite.settings.connection import db_connection_handler
from src.models.sqlite.repositories.pj_repository import PJRepository
from src.controllers.pj_controller import PJController
from src.views.pj_view import PJView

def pj_composer():
    model = PJRepository(db_connection_handler)
    controller = PJController(model)
    view = PJView(controller)
    
    return view
