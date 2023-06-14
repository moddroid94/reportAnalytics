import datetime
import logging
from enum import Enum

_logger = logging.getLogger(__name__)


class Format():
    def __init__(self) -> None:
        self.end_row: list
        self.begin_row: list

    def format_matches(self, matches:list, index: int):
        for x in matches:
            mode = x['mode']
            i = x['data']
            self.end_row = list(i[-1])
            self.begin_row = list(i[0])
            data1 = self.format_date(self.begin_row[0])
            data2 = self.format_date(self.end_row[0])
            delta_data = data2 - data1

            setp = int(i[0][self.begin_row[0]][f'Setpoint {index}'].split(' ')[0])
            first_temp = float(i[0][self.begin_row[0]][f'Sensore T{index}'].split(' ')[0])
            last_temp = float(i[-1][self.end_row[0]][f'Sensore T{index}'].split(' ')[0])

            print('date:', str(data1).split(' ', maxsplit=1)[0],
                '\nfrom:', str(data1).split(' ')[1],
                'to:', str(data2).split(' ')[1],
                '\nduration:', delta_data,
                '\ndelta begin:', abs(first_temp - setp),
                '\ndelta end:', abs(last_temp - setp),
                '\nmode:', mode,
                '\nsetpoint:', index
                )
            print('\n__\n')


    def format_date(self, date:str):
        return datetime.datetime.strptime(date, "%d/%m/%Y %H:%M")
