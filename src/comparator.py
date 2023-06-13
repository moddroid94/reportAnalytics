#pylint: disable=C0103


import logging
import re
import pandas as pd

from rulesets import markers
from src import utils
from rulesets import markers



_logger = logging.getLogger(__name__)

class Comparator():
    def __init__(self):
        self.result = {}
        self.matches = {}
        self.match = {}
        self.session = []
    
    def check_conditions(self, wb:pd.DataFrame, ruleset:list):
        returns = []
        for rule in ruleset:
            rules = markers.MarkerRules(rule)
            returns.append(self.check_rows(wb, rules))
        return returns
    
    def check_rows(self, wb:pd.DataFrame, rules:markers.MarkerRules):
        self.result = {
            0: False,
            1: False,
            2: False,
            3: False,
        }
        self.session = []
        self.matches = {
            0:[],
            1:[],
            2:[],
            3:[]
        }
        self.match = {
            0:[],
            1:[],
            2:[],
            3:[]
        }
        headers = []
        for col in wb.columns:
            headers.append(col)
        sensnr, setsnr, compsnr = rules.get_fields(headers)

        for index, row in wb.iterrows():

            match setsnr:
                case 1:
                    set1 = row['Setpoint 1'].split(' ')[0]
                    sets = [set1]
                case 2:
                    set1 = row['Setpoint 1'].split(' ')[0]
                    set2 = row['Setpoint 2'].split(' ')[0]
                    sets = [set1, set2]
                case 3:
                    set1 = row['Setpoint 1'].split(' ')[0]
                    set2 = row['Setpoint 2'].split(' ')[0]
                    set3 = row['Setpoint 3'].split(' ')[0]
                    sets = [set1, set2, set3]
                case 4:
                    set1 = row['Setpoint 1'].split(' ')[0]
                    set2 = row['Setpoint 2'].split(' ')[0]
                    set3 = row['Setpoint 3'].split(' ')[0]
                    set4 = row['Setpoint 4'].split(' ')[0]
                    sets = [set1, set2, set3, set4]
                case _:
                    raise KeyError

            match sensnr:
                case 1:
                    t1 = row['Sensore T1'].split(' ')[0]
                    sens = [t1]
                case 2:
                    t1 = row['Sensore T1'].split(' ')[0]
                    t2 = row['Sensore T2'].split(' ')[0]
                    sens = [t1, t2]
                case 3:
                    t1 = row['Sensore T1'].split(' ')[0]
                    t2 = row['Sensore T2'].split(' ')[0]
                    t3 = row['Sensore T3'].split(' ')[0]
                    sens = [t1, t2, t3]
                case 4:
                    t1 = row['Sensore T1'].split(' ')[0]
                    t2 = row['Sensore T2'].split(' ')[0]
                    t3 = row['Sensore T3'].split(' ')[0]
                    t4 = row['Sensore T4'].split(' ')[0]
                    sens = [t1, t2, t3, t4]
                case _:
                    raise KeyError

            match compsnr:
                case 1:
                    comp1 = row['Modalità comp. 1']
                    comps = [comp1]
                case 2:
                    comp1 = row['Modalità comp. 1']
                    comp2 = row['Modalità comp. 2']
                    comps = [comp1, comp2]
                case 3:
                    comp1 = row['Modalità comp. 1']
                    comp2 = row['Modalità comp. 2']
                    comp3 = row['Modalità comp. 3']
                    comps = [comp1, comp2, comp3]
                case 4:
                    comp1 = row['Modalità comp. 1']
                    comp2 = row['Modalità comp. 2']
                    comp3 = row['Modalità comp. 3']
                    comp4 = row['Modalità comp. 4']
                    comps = [comp1, comp2, comp3, comp4]
                case _:
                    comps = [None]

            for i in sets:
                if self.result[sets.index(i)] is False:
                    if rules.begin(sets.index(i), i, sens, comps) is True:
                        self.result[sets.index(i)] = True #start pulldown
                        self.match[sets.index(i)] = []
                        _logger.debug('start pulldown')
                elif self.result[sets.index(i)] is True:
                    if rules.end(sets.index(i), i, sens, comps) is True:
                        self.result[sets.index(i)] = False #end pulldown
                        _logger.debug('end pulldown')

            for x in self.result.items():
                if x[1] is True:
                    dict_data = {index: row.to_dict()}
                    self.match[x[0]].append(dict_data)
                    _logger.debug('append')
                if x[1] is False and len(self.match[x[0]]) > 1:
                    self.matches[x[0]].append(self.match[x[0]])
                    self.match[x[0]] = []
                    _logger.debug('close match')

        
        #return matches only if present otherwise None
        if len(self.matches) > 1:
            return self.matches
        return False