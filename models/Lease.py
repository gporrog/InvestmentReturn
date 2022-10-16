from datetime import date

from models.Lessor import Lessor
from models.Maintenance import Maintenance

class Lease:
    def __init__(self, start_date: date, end_date: date, monthly_rent: int, monthly_mr: int, lessor: Lessor, maintenance: Maintenance) -> None:
        self.start_date = start_date
        self.end_date = end_date
        self.monthly_rent = monthly_rent
        self.monthly_mr = monthly_mr
        self.lessor = lessor
        self.maintenance = maintenance