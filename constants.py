"""This module defines project-level constants."""

DATE_FORMAT = "%Y-%m-%d"
DAYS_IN_MONTH = 30
DAYS_IN_YEAR = 360
DECIMALS = 3
PATH_JSON_PARAM_NAME = "path_input_json"
INPUT_FILE_EXT = "json"
PATH_OUTPUT_FILE = "output.json"

### INPUT DATA NAMING EXPECTATIONS ###
INPUT_PRICING_DICT_NAME = "pricing"
INPUT_LEASE_DICT_NAME = "lease"
INPUT_MAINT_DICT_NAME = "maintenance"
INPUT_RESIDUAL_DICT_NAME = "residual_value"

## TODO ADD THE REST OF NAMES
INPUT_PRICING_ECD_NAME = "economic_closing_date"
INPUT_PRICING_NET_PRICE = "net_price"
INPUT_PRICING_NUM_SAMPLES = "num_samples"

INPUT_LEASE_START_DATE = "start_date"
INPUT_LEASE_END_DATE = "end_date"
INPUT_LEASE_MONTHLY_RENT = "monthly_rent_dollars"
INPUT_LEASE_MONTHLY_MR = "monthly_mr_rate_dollars"

INPUT_MAINT_CHECK_INTERVAL = "check_interval_months"
INPUT_MAINT_USED_LIFE = "initial_used_life_months"
INPUT_MAINT_CHECK_MIN = "check_cost_min_dollars"
INPUT_MAINT_CHECK_MAX = "check_cost_max_dollars"

INPUT_RESIDUAL_AIRC_VALUE = "appraised_aircraft_value"
INPUT_RESIDUAL_AS_OF = "as_of"
INPUT_RESIDUAL_DEPR_RATE = "depreciation_rate"