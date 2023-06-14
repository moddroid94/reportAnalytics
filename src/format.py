import datetime
import logging
from enum import Enum

_logger = logging.getLogger(__name__)


class Format():
    def __init__(self) -> None:
        self.end_pulldown: list
        self.begin_pulldown: list

    def format_matches(self, matches:list, index: int):
        for i in matches:
            
            self.end_pulldown = list(i[-1])
            self.begin_pulldown = list(i[0])
            dat2 = self.format_date(self.end_pulldown[0])
            dat1 = self.format_date(self.begin_pulldown[0])
            datf = dat2 - dat1

            setp = int(i[0][self.begin_pulldown[0]][f'Setpoint {index}'].split(' ')[0])
            first_temp = float(i[0][self.begin_pulldown[0]][f'Sensore T{index}'].split(' ')[0])
            last_temp = float(i[-1][self.end_pulldown[0]][f'Sensore T{index}'].split(' ')[0])

            print('date:', str(dat1).split(' ', maxsplit=1)[0],
                '\nfrom:', str(dat1).split(' ')[1],
                'to:', str(dat2).split(' ')[1],
                '\nduration:', datf,
                '\ndelta begin:', abs(first_temp - setp),
                '\ndelta end:', abs(last_temp - setp),
                '\nsetpoint', index
                )
            print('\n__\n')


    def format_date(self, date:str):
        return datetime.datetime.strptime(date, "%d/%m/%Y %H:%M")
