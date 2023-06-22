#pylint: disable=C0103

import logging
import pandas as pd
from rulesets import markers
from src import loader as ld
from src import comparator as cp
from src import format as fm
from sessions import match
import enum

logging.basicConfig(encoding="utf-8", level=logging.DEBUG)
_logger = logging.getLogger(__name__)

class Rule(enum.Enum):
    pulldown = match.Pulldown()
    
class ReportScraper():
    wb: pd.DataFrame|None

    def __init__(self) -> None:
        self.loader = ld.Loader()
        self.comparator = cp.Comparator()
        self.formatter = fm.Format()
        self.ruleset = ['pulldown', 'defrost']
        self.rules = []
        self.headers = []
        _logger.debug('loaded')

        #testload
        if self.load_report('reports/26677.xlsx') is True and self.load_rules(self.ruleset) is True:
            self.iter_loop()

    def load_report(self, workbook: str):
        try:
            self.wb = self.loader.load_wb(workbook)
            return True
        except (FileNotFoundError, NotImplementedError) as errore:
            self.wb = None
            _logger.error('Error while loading %s', errore)
            raise errore

    def load_rules(self, ruleset):
        for rule in Rule:
            if rule.name in ruleset:
                self.rules.append(rule.value)
        return True


    def iter_loop(self):
        if len(self.rules) < 1 or self.wb is None:
            _logger.error('No data or Rule found')
            raise ValueError

        for col in self.wb.columns:
            self.headers.append(col)

        for rule in self.rules:
            rule.set_fields(self.headers)
            new = self.wb.filter(list(rule.fields))
            for row in new.itertuples(name=None):
                for x in range(1,rule.compartments+1):
                    _logger.debug((row, x))
                    
            ###THIS DEPENDS UPON WHAT DATA STRUCTURE WE WANNA USE IN PRODUCTION####


    def format_result(self, matches:list):
        for x in matches:
            print(x)
            for i in x:
                loop = i+1
                if len(x[i]) > 0:
                    self.formatter.format_matches(matches[0][i], loop)

if __name__ == "__main__":
    ReportScraper()
