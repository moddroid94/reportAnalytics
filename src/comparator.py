#pylint: disable=C0103

import types
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
        self.multi = None
    
    def check_conditions(self, wb:pd.DataFrame, ruleset:list):
        returns = []
        for rule in ruleset:
            rules = markers.MarkerRules(rule)
            returns.append(self.iter_wb_check(wb, rules, rule))
        #return returns
    
    def iter_wb_check(self, wb:pd.DataFrame, ruleset:markers.MarkerRules, rule:str):
        

    def check_rows(self, wb:pd.DataFrame, rules:markers.MarkerRules, rule:str):
        self.result = {
            0: False,
            1: False,
            2: False,
            3: False,
        }
        self.session = []
        self.matches = {}
        self.match = {
            0:[],
            1:[],
            2:[],
            3:[]
        }
        headers = []
        for col in wb.columns:
            headers.append(col)
        fields = rules.get_fields(headers)

        '''for index, row in wb.iterrows():
            pop_fields = self.populate_fields(fields, row)
            pf = types.SimpleNamespace(**pop_fields)
            
            for idx, i in enumerate(pf.sets):
                if len(pf.sets) > 1:
                    self.multi = idx
                else:
                    self.multi = None
                if self.result[idx] is False:
                    if rules.begin(self.multi, i, pf.sens, pf.comps) is True:
                        self.result[idx] = True #start pulldown
                        self.match[idx] = []
                        _logger.debug('start %s match set: %s',rule, idx)
                elif self.result[idx] is True:
                    if rules.end(self.multi, i, pf.sens, pf.comps) is True:
                        self.result[idx] = False #end pulldown
                        _logger.debug('end %s match set: %s ',rule,idx)

            for x in self.result.items():
                if x[1] is True:
                    dict_data = {index: row.to_dict()}
                    self.match[x[0]].append(dict_data)
                    _logger.debug('append %s match to set %s',rule, x[0])
                elif x[1] is False and len(self.match[x[0]]) > 1:
                    #TODO Could add this line too and sort later with reason of the ending
                    try:
                        self.matches[x[0]].append({'mode':rule,'data':self.match[x[0]]})
                    except KeyError:
                        _logger.debug('create %s dict %s', rule, x[0])
                        self.matches[x[0]] = []
                        self.matches[x[0]].append({'mode':rule,'data':self.match[x[0]]})
                    self.match[x[0]] = []
                    _logger.debug('close %s set for %s', rule, x[0])

        return self.matches'''


    def populate_fields(self, fields:dict, row:pd.Series):
        field_populated = {}
        for field in fields:
            if field == 'sets':
                match fields[field]:
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
                field_populated[field] = sets
            if field == 'sens':
                match fields[field]:
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
                field_populated[field] = sens
            if field == 'comps':
                match fields[field]:
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
                        raise KeyError
                field_populated[field] = comps
        return field_populated