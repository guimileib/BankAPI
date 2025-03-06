from typing import Dict
from abc import ABC, abstractmethod

class PFControllerInterface(ABC):
    @abstractmethod
    def create(self, pf_info: Dict) -> Dict:
        pass
