#pylint: disable=C0103


import logging
from rulesets import markers
import pandas as pd


_logger = logging.getLogger(__name__)

class Comparator():
    def __init__(self):
        self.is_loop = False
        self.match = {}
        self.matches = []
    
    def check_rows(self, wb:pd.DataFrame, ruleset:markers.MarkerRules):
        self.match = {}
        for index, row in wb.iterrows():
            t1 = row['Sensore T1'].split(' ')[0]
            try:
                t2 = row['Sensore T2'].split(' ')[0]
                t3 = row['Sensore T3'].split(' ')[0]
                t4 = row['Sensore T4'].split(' ')[0]
            except KeyError as errore:
                _logger.error('Key error %s', errore)
                
            
            costate1 = row['Modalità comp. 1']
            
            if 'C' in row['Setpoint 1']:
                setp = int(row['Setpoint 1'].split(' ')[0])
                if self.is_loop is False:
                    if ruleset.begin(setp, t1, costate1) is True:
                        self.is_loop = True
                elif self.is_loop is True:
                    if ruleset.end(setp, t1, costate1) is True:
                        self.is_loop = False
            else:
                self.is_loop = False
                
                
            
            if self.is_loop is True:
                self.match[index] = row.to_dict()
            if self.is_loop is False and len(self.match) > 1:
                self.matches.append(self.match)
                self.match = {}
        
        if len(self.matches) > 1:
            return self.matches
        
        return None