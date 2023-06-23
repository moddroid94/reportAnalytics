import logging

import pandas as pd

_logger = logging.getLogger(__name__)

class Loader():
    def __init__(self) -> None:
        self.wb = pd.DataFrame
        _logger.debug('Module Loaded')
    
    def load_wb(self, workbook: str):
        try:
            self.wb = pd.read_excel(workbook, header=6)
            return self.wb
        except FileNotFoundError as errore:
            _logger.error('File Not Found - %s', errore)
            raise FileNotFoundError from errore
        
            