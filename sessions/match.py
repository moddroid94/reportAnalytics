from abc import ABC, abstractmethod
import datetime
import logging
import enum
from types import SimpleNamespace
import pandas as pd

_logger = logging.getLogger(__name__)


class Fields(enum.Enum):
    SETP1 = 'Setpoint 1'
    SETP2 = 'Setpoint 2'
    SETP3 = 'Setpoint 3'
    COMP1 = 'Modalità comp. 1'
    COMP2 = 'Modalità comp. 2'
    COMP3 = 'Modalità comp. 3'
    SENS1 = 'Sensore T1'
    SENS2 = 'Sensore T2'
    SENS3 = 'Sensore T3'
    
class Match(ABC):
    def __init__(self) -> None:
        self.name = str
        self.matches: dict
        self.compartments: int
        self.data: datetime.date
        self.start_time: datetime.time
        self.end_time: datetime.time
        self.duration: datetime.timedelta
        self.fields: list
        self.states: SimpleNamespace
        super().__init__()

    @abstractmethod
    def set_fields(self, headers:list):
        raise NotImplementedError

    @abstractmethod
    def rules(self, row:pd.Series, index):
        raise NotImplementedError

    @abstractmethod
    def add_row(self, row:pd.Series, index):
        raise NotImplementedError

    @abstractmethod
    def close_match(self):
        raise NotImplementedError


class Pulldown(Match):
    def __init__(self) -> None:
        super().__init__()
        self.states = SimpleNamespace(states=[False,False,False,False])
        self.start_time = SimpleNamespace(times=[0,0,0,0])
        self.name = 'pulldown'
        self.matches = {}
        self.compartments = 0
        self.delta_temp_0 = None
        self.delta_temp_1 = None

    def set_fields(self, headers: list):
        _fields = [
            "Data/Ora",
            "Setpoint 1",
            "Setpoint 2",
            "Setpoint 3",
            "Setpoint 4",
            "Sensore T1",
            "Sensore T2",
            "Sensore T3",
            "Sensore T4",
            "Modalità comp. 1",
            "Modalità comp. 2",
            "Modalità comp. 3",
            "Modalità comp. 4",
        ]
        fields = []
        for header in headers:
            if header in _fields:
                fields.append(header)
                if 'Setpoint' in header:
                    self.compartments =+ 1
                _logger.debug('Appended Field %s', header)
        for i in range(0, self.compartments):
            self.matches.update({i: {}})
        self.fields = fields

    def rules(self, row, index, compartment=None):
        _logger.debug(row)
        data = datetime.datetime.strptime(row['Data/Ora'], "%d/%m/%Y %H:%M")
        if compartment == 1:
            setp = row[Fields.SETP1.value].split(' ')[0]
            sens = row[Fields.SENS1.value].split(' ')[0]
            comp = row[Fields.COMP1.value]
            if 'Nessun' in sens or 'Nessun' in setp:
                self.close_match(row, 1)
            elif abs(int(setp)-float(sens)) > 5 and 'Raffreddamento' in comp:
                self.add_row(row, index, 1)
                
            else:
                self.close_match(row, 1)
                _logger.debug(self.matches)

        else:
            for i in range(0, compartment):
                
                setp = row[f'Setpoint {i}'].split(' ')[0]
                sens = row[f'Sensore T{i}'].split(' ')[0]
                comp = row[f'Modalità comp. {i}']
                if 'Nessun' in sens or 'Nessun' in setp:
                    self.close_match(row,i)

                elif abs(int(setp)-float(sens)) > 5 and 'Raffreddamento' in comp:
                    self.add_row(row, index, i)
                    _logger.debug(self.matches)
                else:
                    self.close_match(row,i)

        

    def add_row(self, row, index, comp=None):
        comp = comp -1
        if self.states.states[comp] is False:
            self.start_time.times[comp] = index
            self.matches[comp][self.start_time.times[comp]] = []
            self.matches[comp][self.start_time.times[comp]].append(row.to_dict())
            self.states.states[comp] = True
            
        elif self.states.states[comp] is True:
            self.matches[comp][self.start_time.times[comp]].append(row.to_dict())

    def close_match(self, row=None, comp=None):
        comp = comp -1
        if self.states.states[comp] is False:
            pass
            
        elif self.states.states[comp] is True:
            self.matches[comp][self.start_time.times[comp]].append(row.to_dict())
            self.states.states[comp] = False

