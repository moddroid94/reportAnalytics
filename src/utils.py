import logging

_logger=logging.getLogger(__name__)

def get_low_temp(t1:int, t2:int|None, t3:int|None, t4:int|None) -> int:
    temps = (t1, t2, t3, t4)
    try:
        low = temps.index(min)
    except Exception as errore: #pylint: disable=W0718
        _logger.error('error comparing temps %s', errore)
        low = t1
    return low

def get_setpoint_number(row):
    pass

def get_sensor_number():
    pass