import math


class DutiableValue:
    def __init__(self, fob_fca_value: float, dutiable_insurance: float, dutiable_freight: float,
                 rate_of_exchange: float) -> None:
        self.fob_fca_value = fob_fca_value
        self.dutiable_insurance = dutiable_insurance
        self.dutiable_freight = dutiable_freight
        self.rate_of_exchange = rate_of_exchange

    def calculate_dutiable_value(self) -> float:
        total_dutiable_value = (
            self.fob_fca_value, self.dutiable_insurance, self.dutiable_freight,
        )
        total_dutiable_value = round(math.fsum(total_dutiable_value) * self.rate_of_exchange, 2)
        return total_dutiable_value


class DutiableValueBySea(DutiableValue):
    def __init__(self, fob_fca_value: float, dutiable_insurance: float, dutiable_freight: float,
                 rate_of_exchange: float) -> None:
        super().__init__(fob_fca_value, dutiable_insurance, dutiable_freight, rate_of_exchange)

    def calculate_dutiable_value_by_sea(self):
        return self.calculate_dutiable_value()


class DutiableValueByAir(DutiableValue):
    def __init__(self, fob_fca_value: float, dutiable_insurance: float, dutiable_freight: float,
                 rate_of_exchange: float) -> None:
        super().__init__(fob_fca_value, dutiable_insurance, dutiable_freight, rate_of_exchange)

    def calculate_dutiable_value_by_air(self):
        return self.calculate_dutiable_value()
