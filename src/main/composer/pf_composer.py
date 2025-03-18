from src.models.sqlite.settings.connection import db_connection_handler
from src.models.sqlite.repositories.pf_repository import PFRepository
from src.controllers.pf_controller import PFController
from src.views.pf_view import PFView

def pf_composer():
    model = PFRepository(db_connection_handler)
    controller = PFController(model)
    view = PFView(controller)
    
    return view
