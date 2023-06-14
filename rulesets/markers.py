#pylint: disable=c0103,w0613, R0911

import logging
from src import utils

_logger = logging.getLogger(__name__)

class MarkerRules():
    def __init__(self, ruleset:str) -> None:
        self.ruleset = ruleset
       
    def begin(self, *kwargs):
        match self.ruleset:
            case "pulldown":
                mode = self.p_begin(*kwargs)
            case "defrost":
                mode = self.d_begin(*kwargs)
            case _:
                raise KeyError
        return mode
    
    def end(self, *kwargs):
        match self.ruleset:
            case "pulldown":
                mode = self.p_end(*kwargs)
            case "defrost":
                mode = self.d_end(*kwargs)
            case _:
                raise KeyError
        return mode
    
    def get_fields(self, *kwargs):
        match self.ruleset:
            case "pulldown":
                mode = self.p_get_fields(*kwargs)
            case "defrost":
                mode = self.d_get_fields(*kwargs)
            case _:
                raise KeyError
        return mode
        
    def p_get_fields(self, headers:list):
        sets = 0
        sens = 0
        comp = 0
        for key in headers:
            if 'Setpoint' in key:
                sets += 1
            if 'Sensore T' in key:
                sens += 1
            if 'Modalità comp.' in key:
                comp += 1
        return {'sens':sens,'sets': sets,'comps': comp}

    def p_begin(self, index:int, setp, temps:list, comps:list):
        '''
        Check if the parameters passed are the start of a pulldown
        Return True if row matche rules, false otherwise'''
        low = utils.get_low_temp(temps, index)

        if index is None:
            comps_valid = comps
        else:
            comps_valid = comps[index]

        if low is None:
            return False
        if setp == 'Nessun':
            return False
        if abs(int(setp)-float(low)) > 5 and 'Raffreddamento' in comps_valid:
            return True
        return False

    def p_end(self, index:int, setp, temps:list, comps:list):
        '''
        Check if the parameters passed are the end of a pulldown
        Return True if row matches rules, False otherwise'''
        low = utils.get_low_temp(temps, index)

        if index is None:
            comps_valid = comps
        else:
            comps_valid = comps[index]
        
        if low is None:
            return True
        if setp == 'Nessun':
            return True
        if 'Spento' in comps_valid:
            return True
        if abs(int(setp)-float(low)) < 3:
            return True
        if 'Sbrinamento' in comps_valid:
            return True
        if 'Idle' in comps_valid:
            return True

        return False

    def d_get_fields(self, headers:list):
        temp = 0
        comp = 0
        for key in headers:
            if 'Sensore T' in key:
                temp += 1
            if 'Modalità comp.' in key:
                comp += 1
        return {'sens':temp,'comps': comp}

    def d_begin(self, index:int, setp, temps:list, comps:list):
        '''
        Check if the parameters passed are the start of a defrost
        Return True if row matche rules, false otherwise'''
        if index is None:
            comps_valid = comps
        else:
            comps_valid = comps[index]

        if 'Sbrinamento' in comps_valid:
            return True

        return False

    def d_end(self, index:int, setp, temps:list, comps:list):
        '''
        Check if the parameters passed are the end of a pulldown
        Return True if row matches rules, False otherwise'''
        if index is None:
            comps_valid = comps
        else:
            comps_valid = comps[index]

        if 'Sbrinamento' not in comps_valid:
            return True

        return False
