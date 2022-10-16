from argparse import ArgumentParser
import json

from constants import *
from utils.DatesFormatter import DatesFormatter

class IOManager:

    def __transform_data(self, input_data) -> None:
        input_data[INPUT_PRICING_DICT_NAME][INPUT_PRICING_ECD_NAME] = DatesFormatter.get_formatted_date(
            input_data[INPUT_PRICING_DICT_NAME][INPUT_PRICING_ECD_NAME])
        input_data[INPUT_LEASE_DICT_NAME][INPUT_LEASE_START_DATE] = DatesFormatter.get_formatted_date(
            input_data[INPUT_LEASE_DICT_NAME][INPUT_LEASE_START_DATE])
        input_data[INPUT_LEASE_DICT_NAME][INPUT_LEASE_END_DATE] = DatesFormatter.get_formatted_date(
            input_data[INPUT_LEASE_DICT_NAME][INPUT_LEASE_END_DATE])
        input_data[INPUT_RESIDUAL_DICT_NAME][INPUT_RESIDUAL_AS_OF] = DatesFormatter.get_formatted_date(
            input_data[INPUT_RESIDUAL_DICT_NAME][INPUT_RESIDUAL_AS_OF])

        if input_data[INPUT_PRICING_DICT_NAME][INPUT_PRICING_ECD_NAME] >= input_data[INPUT_LEASE_DICT_NAME][INPUT_LEASE_START_DATE]:
            raise Exception("ECD Date must be lower than lease start date.")

        if input_data[INPUT_LEASE_DICT_NAME][INPUT_LEASE_START_DATE] >= input_data[INPUT_LEASE_DICT_NAME][INPUT_LEASE_END_DATE]:
            raise Exception(
                "Lease start date must be lower than lease end date.")

        if input_data[INPUT_RESIDUAL_DICT_NAME][INPUT_RESIDUAL_AS_OF] >= input_data[INPUT_LEASE_DICT_NAME][INPUT_LEASE_END_DATE]:
            raise Exception(
                "Residual start date must be lower than lease end date.")

        # Input data correct
        return input_data

    def __validate_input_data(self, input_data: dict) -> dict:
        if INPUT_PRICING_DICT_NAME in input_data \
                and INPUT_LEASE_DICT_NAME in input_data \
                and INPUT_MAINT_DICT_NAME in input_data \
                and INPUT_RESIDUAL_DICT_NAME in input_data:

            if INPUT_PRICING_ECD_NAME not in input_data[INPUT_PRICING_DICT_NAME] \
               or INPUT_PRICING_NET_PRICE not in input_data[INPUT_PRICING_DICT_NAME] \
               or INPUT_PRICING_NUM_SAMPLES not in input_data[INPUT_PRICING_DICT_NAME]:
                raise Exception(
                    "There are missing values in the pricing dictionary.")

            if INPUT_LEASE_START_DATE not in input_data[INPUT_LEASE_DICT_NAME] \
               or INPUT_LEASE_END_DATE not in input_data[INPUT_LEASE_DICT_NAME] \
               or INPUT_LEASE_MONTHLY_RENT not in input_data[INPUT_LEASE_DICT_NAME] \
               or INPUT_LEASE_MONTHLY_MR not in input_data[INPUT_LEASE_DICT_NAME]:
                raise Exception(
                    "There are missing values in the lease dictionary.")

            if INPUT_MAINT_CHECK_INTERVAL not in input_data[INPUT_MAINT_DICT_NAME] \
               or INPUT_MAINT_USED_LIFE not in input_data[INPUT_MAINT_DICT_NAME] \
               or INPUT_MAINT_CHECK_MIN not in input_data[INPUT_MAINT_DICT_NAME] \
               or INPUT_MAINT_CHECK_MAX not in input_data[INPUT_MAINT_DICT_NAME]:
                raise Exception(
                    "There are missing values in the maintenance dictionary.")

            if INPUT_RESIDUAL_AIRC_VALUE not in input_data[INPUT_RESIDUAL_DICT_NAME] \
               or INPUT_RESIDUAL_AS_OF not in input_data[INPUT_RESIDUAL_DICT_NAME] \
               or INPUT_RESIDUAL_DEPR_RATE not in input_data[INPUT_RESIDUAL_DICT_NAME]:
                raise Exception(
                    "There are missing values in the residual value dictionary.")

            if type(input_data[INPUT_PRICING_DICT_NAME][INPUT_PRICING_NET_PRICE]) != int \
                    or type(input_data[INPUT_PRICING_DICT_NAME][INPUT_PRICING_NUM_SAMPLES]) != int \
                    or type(input_data[INPUT_LEASE_DICT_NAME][INPUT_LEASE_MONTHLY_RENT]) != int \
                    or type(input_data[INPUT_LEASE_DICT_NAME][INPUT_LEASE_MONTHLY_MR]) != int \
                    or type(input_data[INPUT_MAINT_DICT_NAME][INPUT_MAINT_CHECK_INTERVAL]) != int \
                    or type(input_data[INPUT_MAINT_DICT_NAME][INPUT_MAINT_USED_LIFE]) != int \
                    or type(input_data[INPUT_MAINT_DICT_NAME][INPUT_MAINT_CHECK_MIN]) != int \
                    or type(input_data[INPUT_MAINT_DICT_NAME][INPUT_MAINT_CHECK_MAX]) != int \
                    or type(input_data[INPUT_RESIDUAL_DICT_NAME][INPUT_RESIDUAL_AIRC_VALUE]) != int \
                    or type(input_data[INPUT_RESIDUAL_DICT_NAME][INPUT_RESIDUAL_DEPR_RATE]) != float:
                raise Exception(
                    "One or more attributes are expected to be numbers.")
            
            if input_data[INPUT_PRICING_DICT_NAME][INPUT_PRICING_NUM_SAMPLES] <= 0:
                raise Exception(
                    "Num samples must be greater than 0.")

            if input_data[INPUT_MAINT_DICT_NAME][INPUT_MAINT_CHECK_MIN] >= input_data[INPUT_MAINT_DICT_NAME][INPUT_MAINT_CHECK_MAX]:
                raise Exception(
                    "The maintenance min check cost must be lower than the max check cost.")

            return self.__transform_data(input_data)
        else:
            raise Exception(
                "One or more mandatory dictionaries missing in the input data.")

    def __get_input_data(self) -> None:
        input_path: str = self.__arguments[PATH_JSON_PARAM_NAME]
        name, ext = input_path.split(".")
        if name != "" and ext == INPUT_FILE_EXT:
            try:
                with(open(input_path, "r")) as input_file:
                    input_data = json.load(input_file)
                    input_data = self.__validate_input_data(input_data)
                    input_file.close()
                    return input_data
            except IOError:
                raise Exception("Error: can\'t find file or read data.")
        else:
            raise Exception("Incorrect extension or missing filename.")

    @property
    def input_data(self):
        return self._input_data

    def __init__(self: object) -> None:
        self.__parser = ArgumentParser(
            description="Process input JSON data. Calculates cashflow and expected IRR.",
            usage="%(prog)s [PATH_JSON]")
        self.__parser.add_argument(
            PATH_JSON_PARAM_NAME,
            type=str
        )
        # vars -> return a dict
        self.__arguments = vars(self.__parser.parse_args())
        self.output = dict()
        self._input_data = self.__get_input_data()

    def generate_output_data(self, output_dict: dict) -> None:
        try:
            with open(PATH_OUTPUT_FILE, "w") as outfile:
                json.dump(output_dict, outfile)
                print(f"\nResult saved in {PATH_OUTPUT_FILE}")
        except:
            raise Exception("Can't serialise the output file.")
