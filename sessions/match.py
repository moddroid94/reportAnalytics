from abc import ABC, abstractmethod
import datetime
import logging

_logger = logging.getLogger(__name__)

class Match(ABC):
    def __init__(self) -> None:
        self.name = str
        self.matches: dict
        self.data: datetime.date
        self.start_time: datetime.time
        self.end_time: datetime.time
        self.duration: datetime.timedelta
        self.fields: list
        super().__init__()

    @abstractmethod
    def set_fields(self, headers:list):
        raise NotImplementedError

    @abstractmethod
    def rules(self):
        raise NotImplementedError

    @abstractmethod
    def add_row(self):
        raise NotImplementedError

    @abstractmethod
    def close_match(self):
        raise NotImplementedError


class Pulldown(Match):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'pulldown'
        self.delta_temp_0 = None
        self.delta_temp_1 = None

    def set_fields(self, headers: list):
        _fields = [
            "Setpoint 1",
            "Setpoint 2",
            "Setpoint 3",
            "Setpoint 4",
            "Sensore 1",
            "Sensore 2",
            "Sensore 3",
            "Sensore 4",
            "Modalità comp. 1",
            "Modalità comp. 2",
            "Modalità comp. 3",
            "Modalità comp. 4",
        ]
        fields = []
        for header in headers:
            if header in _fields:
                fields.append(header)
                _logger.debug('Appended Field %s', header)
        self.fields = fields

    def rules(self, row):
        print('call r')
    def add_row(self):
        print('call a')
    def close_match(self):
        print('call c')
