import logging
import ast

import pandas as pd


_logger=logging.getLogger(__name__)

def get_low_temp(temps:list) -> int:
    try:
        low = min(temps)
    except Exception as errore: #pylint: disable=W0718
        _logger.error('error comparing temps %s', errore)
        low = temps[0]
    return low
