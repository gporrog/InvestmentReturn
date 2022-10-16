from datetime import date
import math

from models.Statement import Statement
import constants

class ResidualValue(Statement):
    def get_amount(self) -> int:
        y_valuation = round((self._date - self.residual_start).days / constants.DAYS_IN_YEAR, constants.DECIMALS)
        residual_value = self.appraised_aircraft_value * math.exp((-self.depreciation_rate * y_valuation))
        return round(residual_value)

    def __init__(self, date: date, residual_start: date, appraised_aircraft_value: int, depreciation_rate: float, is_end: bool = False) -> None:
        super(ResidualValue, self).__init__(date, None, is_end)
        self.residual_start = residual_start
        self.appraised_aircraft_value = appraised_aircraft_value
        self.depreciation_rate = depreciation_rate
        self._amount = self.get_amount()