import logging
import ast

import pandas as pd


_logger=logging.getLogger(__name__)

def get_low_temp(temps:list, multi:int|None=None) -> float|None:
    if multi is not None:
        try:
            return float(temps[multi])
        except ValueError:
            _logger.debug('multi temps not found')
            return None
    else:
        try:
            low = min(temps)
        except Exception as errore: #pylint: disable=W0718
            _logger.error('error comparing temps %s', errore)
            return None
        return low

def zip_fields(wb:pd.DataFrame, fields:list):
    fields_number = len(fields)
    zip_head = zip(wb.index, list(fields))
    return zip_head