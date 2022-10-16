from datetime import date

from constants import *
from utils.DatesFormatter import DatesFormatter

class Statement:
    def get_amount(self, rate:float, is_end:bool=False) -> float:
        current_day = self._date.day

        if current_day == 1:
            return rate
        else:
            daily_payment = rate // DAYS_IN_MONTH
            
            lease_month_days = DatesFormatter.get_number_days_in_month(self._date)
            if is_end:
                count_days_to_pay = current_day
                self._date = DatesFormatter.get_first_of_the_month(self.date) # to show first of the month on the cashflow 
            else:
                count_days_to_pay = lease_month_days - current_day
            payment = count_days_to_pay * daily_payment
            
            return round(payment, DECIMALS)

    @property
    def date(self) -> date:
        return self._date

    @date.setter
    def date(self, new_date: date) -> None:
        self._date = new_date
    
    @property
    def amount(self) -> float:
        return self._amount

    @amount.setter
    def amount(self, new_amount: float) -> None:
        self._amount = new_amount

    def __init__(self, date: date, rate: float, is_end: bool = False, calculate_amount: bool = True):
        self._date = date
        if rate is not None and calculate_amount: 
            self._amount = self.get_amount(rate, is_end) 
        else: 
            self._amount = rate

    def __repr__(self) -> str:
        return f'["{self._date}", {self._amount}]'

    def get_serializable(self) -> list:
        return [str(self._date), self._amount]

    