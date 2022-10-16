import sys

from utils.IOManager import IOManager
from utils.DatesFormatter import DatesFormatter

from models.ResidualValue import ResidualValue
from models.Lease import Lease
from models.Lessor import Lessor
from models.Maintenance import Maintenance
from models.InvestmentReturn import InvestmentReturn
from constants import *

def perform_quant_dev():
    sys.tracebacklimit = 0 # To show only exceptions messages
    iom = IOManager()

    try:
        data = iom.input_data
        print("The data is validated and transformed. Initializing the expected IRR calculation.")
        
        lessor = Lessor(
            data[INPUT_PRICING_DICT_NAME][INPUT_PRICING_ECD_NAME],
            data[INPUT_PRICING_DICT_NAME][INPUT_PRICING_NET_PRICE]
        )

        maintenance = Maintenance(
            data[INPUT_MAINT_DICT_NAME][INPUT_MAINT_CHECK_INTERVAL],
            data[INPUT_MAINT_DICT_NAME][INPUT_MAINT_USED_LIFE],
            data[INPUT_MAINT_DICT_NAME][INPUT_MAINT_CHECK_MIN],
            data[INPUT_MAINT_DICT_NAME][INPUT_MAINT_CHECK_MAX]
        )

        lease = Lease(
            data[INPUT_LEASE_DICT_NAME][INPUT_LEASE_START_DATE],
            data[INPUT_LEASE_DICT_NAME][INPUT_LEASE_END_DATE],
            data[INPUT_LEASE_DICT_NAME][INPUT_LEASE_MONTHLY_RENT],
            data[INPUT_LEASE_DICT_NAME][INPUT_LEASE_MONTHLY_MR],
            lessor,
            maintenance)

        rv = ResidualValue(data[INPUT_LEASE_DICT_NAME][INPUT_LEASE_END_DATE], data[INPUT_RESIDUAL_DICT_NAME][INPUT_RESIDUAL_AS_OF],
                           data[INPUT_RESIDUAL_DICT_NAME][INPUT_RESIDUAL_AIRC_VALUE],
                           data[INPUT_RESIDUAL_DICT_NAME][INPUT_RESIDUAL_DEPR_RATE])
        
        ir = InvestmentReturn(lease, rv, data[INPUT_PRICING_DICT_NAME][INPUT_PRICING_NUM_SAMPLES])
        irr_result = ir.generate_investment_return()

        print("The result is the following: \n")
        print(irr_result)

        iom.generate_output_data(irr_result)
       
    except Exception as e:
        print(e)


if __name__ == "__main__":
    perform_quant_dev()
