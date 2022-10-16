from pyxirr import xirr
import pandas as pd
import numpy as np
from constants import DECIMALS

from models.Statement import Statement
from models.ResidualValue import ResidualValue
from models.Lease import Lease

from utils.DatesFormatter import DatesFormatter

class InvestmentReturn:

    def __init__(self, lease: Lease, residual_value: ResidualValue, num_samples: int) -> None:
        self.lease = lease
        self.num_samples = num_samples
        self.residual_value = residual_value
        
    def __calculate_cashflows(self) -> None:
        # First Statement on ECD
        cashflows = [Statement(
            self.lease.lessor.economic_closing_date, -self.lease.lessor.aircraft_purchase_value, calculate_amount=False)]
        mr_balance = [Statement(self.lease.lessor.economic_closing_date, None)]

        current_date = self.lease.start_date
        check_cost = self.lease.maintenance.get_random_check_cost()

        while current_date < self.lease.end_date:
            if current_date.month == self.lease.end_date.month \
                    and current_date.year == self.lease.end_date.year:
                rent = Statement(self.lease.end_date,
                                 self.lease.monthly_rent, True)
                mr = Statement(self.lease.end_date,
                               self.lease.monthly_mr, True)
            else:
                rent = Statement(current_date, self.lease.monthly_rent)
                mr = Statement(current_date, self.lease.monthly_mr)

            cashflows.append(rent)
            previous_mr = mr_balance[-1].amount
            if previous_mr is None:
                previous_mr = 0

            mr.amount = mr.amount + previous_mr
            mr_balance.append(mr)

            # Used Life expresses used life on the last 1st of month before lease start
            # I need to increment here in case, there is a check to do immediately after start, otherwise it would go
            # wrongly to the next month
            if current_date.day != 1:
                self.lease.maintenance.increment_used_life()

            if self.lease.maintenance.is_time_for_maintenance_check():
                # discount the cost from the last inserted mr payment
                mr_balance[-1].amount = mr_balance[-1].amount - check_cost
                # the rest is payed by the lessee
                if mr_balance[-1].amount < 0:
                    mr_balance[-1].amount = 0

            # Go to next month (t i+1)
            current_date = DatesFormatter.get_next_month(current_date)
            current_date = DatesFormatter.get_first_of_the_month(current_date)

            if current_date.day == 1:
                self.lease.maintenance.increment_used_life()
        
        # Append last statement on the end date lease.
        # Cashflow: Aircraft sale + MR Balance
        # MR Balance: 0 -> Since it goes to cashflow    
        last_statement = Statement(self.lease.end_date, self.residual_value.amount + mr_balance[-1].amount, calculate_amount=False)
        cashflows.append(last_statement)
        mr_balance.append(Statement(self.lease.end_date, 0, calculate_amount=False))

        return cashflows, mr_balance 

    def __calculate_xirr(self) -> float:
        cashflows, mr_balance = self.__calculate_cashflows()
        dates = []
        amounts = []
        serialisable_cashflow = []
        serialisable_mr_balance = []
        for i in range(0, len(cashflows)):
            dates.append(cashflows[i].date)
            amounts.append(cashflows[i].amount)
            serialisable_cashflow.append(cashflows[i].get_serializable())
            serialisable_mr_balance.append(mr_balance[i].get_serializable())
    
        return serialisable_cashflow, serialisable_mr_balance, round(xirr(dates, amounts), DECIMALS)


    def generate_investment_return(self):
        xirrs = np.array([])
        
        for i in range(1, self.num_samples + 1):
            cashflows, mr_balance, xirr = self.__calculate_xirr()
            xirrs = np.append(xirrs, xirr)

        expected_xirr = xirrs.mean()
        # This will return the expected xirr plus the last cashflow and last mr_balance
        return {
            "cashflow": cashflows, 
            "mr_balance": mr_balance,
            "pricing": {
                "expected_irr": expected_xirr
            }
        }
