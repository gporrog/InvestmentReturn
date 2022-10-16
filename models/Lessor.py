from datetime import date

class Lessor:
    def __init__(self, economic_closing_date: date, aircraft_purchase_value: int, name: str = None) -> None:
        self.economic_closing_date = economic_closing_date
        self.aircraft_purchase_value = aircraft_purchase_value
        self.name = name