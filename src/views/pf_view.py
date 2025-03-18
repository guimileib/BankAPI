from typing import Dict
from src.controllers.interfaces.pf_controller_interface import PFControllerInterface
from .http_types.http_request import HttpRequest
from .http_types.http_response import HttpResponse
from .interfaces.view_interface import ViewInterface

class PFView(ViewInterface):
    def __init__(self, controller: PFControllerInterface):
        self.controller = controller

    def create(self, http_request: HttpRequest) -> HttpResponse:
        try:
            body = http_request.body

            response = self.controller.create(body)
            
            return HttpResponse(status_code=201, body=response)
        except ValueError as error:
            return HttpResponse(
                status_code=400,
                body={"error": {"message": str(error)}}
            )
        except Exception as error:
            return HttpResponse(
                status_code=500,
                body={"error": {"message": "Erro interno do servidor"}}
            )

    def get(self, http_request: HttpRequest) -> HttpResponse:
        try:
            pf_id = int(http_request.param.get("id"))
            
            response = self.controller.get(pf_id)
            
            return HttpResponse(status_code=200, body=response)
        except ValueError as error:
            return HttpResponse(
                status_code=404,
                body={"error": {"message": str(error)}}
            )
        except Exception as error:
            return HttpResponse(
                status_code=500,
                body={"error": {"message": "Erro interno do servidor"}}
            )

    def sacar(self, http_request: HttpRequest) -> HttpResponse:
        try:
            pf_id = int(http_request.param.get("id"))
            valor = float(http_request.body.get("valor"))

            if valor <= 0:
                return HttpResponse(
                    status_code=400,
                    body={"error": {"message": "Valor de saque deve ser positivo"}}
                )

            response = self.controller.sacar(pf_id, valor)
            
            return HttpResponse(status_code=200, body={"data": response})
        except ValueError as error:
            return HttpResponse(
                status_code=400,
                body={"error": {"message": str(error)}}
            )
        except Exception as error:
            return HttpResponse(
                status_code=500,
                body={"error": {"message": "Erro interno do servidor"}}
            )

    def extrato(self, http_request: HttpRequest) -> HttpResponse:
        try:
            pf_id = int(http_request.param.get("id"))
            
            transacoes = self.controller.extrato(pf_id) 
            
            return HttpResponse(
                status_code=200, 
                body={"data": {"transacoes": transacoes}}
            )
        except ValueError as error:
            return HttpResponse(
                status_code=404,
                body={"error": {"message": str(error)}}
            )
        except Exception as error:
            return HttpResponse(
                status_code=500,
                body={"error": {"message": "Erro interno do servidor"}}
            )
            