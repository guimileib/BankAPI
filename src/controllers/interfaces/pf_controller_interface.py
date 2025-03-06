from typing import Dict, List
from abc import ABC, abstractmethod

class PFControllerInterface(ABC):
    @abstractmethod
    def create(self, pf_info: Dict) -> Dict:
        pass
    
    @abstractmethod
    def get(self, pf_id:int) -> Dict:
        pass
    
    @abstractmethod
    def sacar(self, pf_id: int, valor: float) -> Dict:
        pass
    
    @abstractmethod
    def extrato(self, pf_id: int) -> List[Dict]:
        pass
