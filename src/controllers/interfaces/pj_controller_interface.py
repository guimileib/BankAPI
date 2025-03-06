from typing import Dict
from abc import ABC, abstractmethod

class PJControllerInterface(ABC):
    @abstractmethod
    def create(self, pj_info: Dict) -> Dict:
        pass
