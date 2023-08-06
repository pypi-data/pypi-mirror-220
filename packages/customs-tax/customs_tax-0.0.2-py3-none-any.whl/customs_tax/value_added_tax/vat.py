class ValueAddedTax:
    def __init__(self, landed_cost: float, vat_rate=0.12) -> None:
        self.landed_cost = landed_cost
        self.vat_rate = vat_rate


class VatExciseTax(ValueAddedTax):
    def __init__(self, landed_cost: float, excise_tax: float) -> None:
        super().__init__(landed_cost, excise_tax)
        self.landed_cost = landed_cost
        self.excise_tax = excise_tax

    def calculate_vat(self) -> float:
        total_value_added_tax = round(
            (self.landed_cost + self.excise_tax) * self.vat_rate, 2
        )
        return total_value_added_tax


class VatNonExciseTax(ValueAddedTax):
    def __init__(self, landed_cost: float) -> None:
        super().__init__(landed_cost)

    def calculate_vat_non_excise_tax(self) -> float:
        total_value_added_tax = round(
            self.landed_cost * self.vat_rate, 2
        )
        return total_value_added_tax
