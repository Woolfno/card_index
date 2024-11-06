from collections import OrderedDict

from faker.providers import BaseProvider
from pathlib import Path

BASE_DIR = Path(__file__).parent

class JobProvider(BaseProvider):
    '''Custom Job title Provider'''
    MANAGER_POSITIONS: OrderedDict[str, float]
    SPECIALISTS: OrderedDict[str, float]
    OTHERS: OrderedDict[str, float]

    def __init__(self, generator):
        super().__init__(generator)
        self.MANAGER_POSITIONS = self.load_data(BASE_DIR / "managers.txt")
        self.SPECIALISTS = self.load_data(BASE_DIR / "specialist.txt")
        self.OTHERS = self.load_data(BASE_DIR / 'others.txt')

    def load_data(self, filename:str)->OrderedDict[str, float]:
        dst = OrderedDict[str, float]()
        with open(filename, 'r', encoding="utf-8") as f:
            while True:
                line = f.readline()
                if line=="": 
                    break
                line = line.strip('()\n')
                line = line.split(',')
                dst[line[0].strip("'")]=float(line[-1])
        return dst
    
    def manager(self)->str:
        return self.random_elements(self.MANAGER_POSITIONS, length=1, use_weighting=True)[0]
    
    def specialist(self)->str:
        return self.random_elements(self.SPECIALISTS, length=1, use_weighting=True)[0]
    
    def other(self)->str:
        return self.random_elements(self.OTHERS, length=1, use_weighting=True)[0]
