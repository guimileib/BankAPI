from typing import Dict, List
from abc import ABC, abstractmethod

class PJControllerInterface(ABC):
    @abstractmethod
    def create(self, pj_info: Dict) -> Dict:
        pass
    
    @abstractmethod
    def get(self, pj_id:int) -> Dict:
        pass
    
    @abstractmethod
    def sacar(self, pj_id: int, valor: float) -> Dict:
        pass
    
    @abstractmethod
    def extrato(self, pj_id: int) -> List[Dict]:
        pass
