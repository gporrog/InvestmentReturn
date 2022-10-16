from datetime import date, datetime
from calendar import monthrange
from dateutil.relativedelta import relativedelta

import constants

class DatesFormatter:
    
    @staticmethod
    def get_formatted_date(str_date: str) -> date:
        # If there is an error with the format, python will raise an exception automatically
        return datetime.strptime(str_date, constants.DATE_FORMAT).date()
        
    @staticmethod
    def get_next_month(current: date) -> date:
        return current + relativedelta(months=1)

    @staticmethod
    def get_first_of_the_month(current: date) -> date:
        return current.replace(day=1)

    @staticmethod
    def get_number_days_in_month(current: date) -> int:
        # monthrange returns (1) week day and (2) number of days in a month in a given YYYY/MM
        return monthrange(current.year, current.month)[1]

    
