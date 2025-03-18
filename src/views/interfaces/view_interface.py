from abc import ABC, abstractmethod
from src.views.http_types.http_response import HttpResponse
from src.views.http_types.http_request import HttpRequest 

class ViewInterface(ABC):

    @abstractmethod
    def create(self, http_request: HttpRequest) -> HttpResponse:
        pass
    
    @abstractmethod
    def get(self, http_request: HttpRequest) -> HttpResponse:
        pass
    
    @abstractmethod
    def sacar(self, http_request: HttpRequest) -> HttpResponse:
        pass
    
    @abstractmethod
    def extrato(self, http_request: HttpRequest) -> HttpResponse:
        pass
    
    