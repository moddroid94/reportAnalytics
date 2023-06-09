#pylint: disable=C0103

import logging
import pandas as pd
from rulesets import markers
from src import loader as ld
from src import comparator as cp


logging.basicConfig(encoding="utf-8", level=logging.DEBUG)
_logger = logging.getLogger(__name__)


class ReportScraper():
    ruleset: markers.MarkerRules
    wb: pd.DataFrame
    
    def __init__(self) -> None:
        self.loader = ld.Loader()
        self.comparator = cp.Comparator()
        _logger.debug('loaded')
        
        #testload
        if self.load('reports/27060.xlsx', 'pulldown') is True:
            self.compare(self.wb, self.ruleset)

    def load(self, workbook: str, ruleset: str):
        try:
            self.wb = self.loader.load_wb(workbook)
            self.ruleset = markers.MarkerRules(ruleset)
            return True
        except (FileNotFoundError, NotImplementedError) as errore:
            _logger.error('Error while loading %s', errore)
            raise errore
        

    def compare(self, wb:pd.DataFrame , ruleset:markers.MarkerRules):
        matches = self.comparator.check_rows(wb, ruleset)
        if matches is not None:
            print(matches)
            


if __name__ == "__main__":
    ReportScraper()
