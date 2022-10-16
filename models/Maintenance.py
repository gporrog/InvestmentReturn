from random import randrange

class Maintenance:
    def __init__(self, check_interval_months: int, initial_used_life_months: int, check_cost_min_dollars: int, check_cost_max_dollars: int) -> None:
        self._check_interval_months = check_interval_months
        self._initial_used_life_months = initial_used_life_months
        self._check_cost_min_dollars = check_cost_min_dollars
        self._check_cost_max_dollars = check_cost_max_dollars

    def get_random_check_cost(self) -> int:
        return randrange(self._check_cost_min_dollars, self._check_cost_max_dollars)

    def is_time_for_maintenance_check(self) -> bool:
        return self._initial_used_life_months % self._check_interval_months == 0

    def increment_used_life(self):
        self._initial_used_life_months += 1
