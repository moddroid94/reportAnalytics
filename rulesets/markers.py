#pylint: disable=c0103,w0613

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
            case _:
                mode = NotImplementedError
        return mode
    
    def end(self, *kwargs):
        match self.ruleset:
            case "pulldown":
                mode = self.p_end(*kwargs)
            case _:
                mode = NotImplementedError
        return mode
    
    def p_begin(self, setp:int, t1:int, costate1:str, opstate1:str='None', t2:int|None=None, t3:int|None=None, t4:int|None=None):
        '''
        Check if the parameters passed are the start of a pulldown
        Return True if row matche rules, false otherwise'''
        low = utils.get_low_temp(t1, t2, t3, t4)

        if abs(setp-float(low)) > 5 and 'Raffreddamento' in costate1:
            return True
        return False

    def p_end(self, setp:int, t1:int, costate1:str, opstate1:str='None', t2:int|None=None, t3:int|None=None, t4:int|None=None):
        '''
        Check if the parameters passed are the end of a pulldown
        Return True if row matches rules, False otherwise'''
        low = utils.get_low_temp(t1, t2, t3, t4)

        if 'Spento' in costate1:
            return True
        if abs(setp-float(low)) < 3:
            return True
        if 'Sbrinamento' in costate1:
            return True
        if 'Idle' in costate1 :
            return True

        return False
