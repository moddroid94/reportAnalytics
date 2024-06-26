#pylint: disable=C0103

import logging
import pandas as pd
from rulesets import markers
from src import loader as ld
from src import comparator as cp
from src import format as fm


logging.basicConfig(encoding="utf-8", level=logging.DEBUG)
_logger = logging.getLogger(__name__)


class ReportScraper():
    wb: pd.DataFrame

    def __init__(self) -> None:
        self.loader = ld.Loader()
        self.comparator = cp.Comparator()
        self.formatter = fm.Format()
        self.ruleset = ['pulldown', 'defrost']
        _logger.debug('loaded')

        #testload
        if self.load('reports/26677.xlsx') is True:
            self.compare(self.wb, self.ruleset)

    def load(self, workbook: str):
        try:
            self.wb = self.loader.load_wb(workbook)
            return True
        except (FileNotFoundError, NotImplementedError) as errore:
            _logger.error('Error while loading %s', errore)
            raise errore

    def compare(self, wb:pd.DataFrame , ruleset:list):
        matches = self.comparator.check_conditions(wb, ruleset)
        if matches is not None:
            for match in matches:
                self.format_result([match])

    def format_result(self, matches:list):
        for x in matches:
            print(x)
            for i in x:
                loop = i+1
                if len(x[i]) > 0:
                    self.formatter.format_matches(matches[0][i], loop)

if __name__ == "__main__":
    ReportScraper()
