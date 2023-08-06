class BankCharge:
    def __init__(self, total_dutiable_value: float, bank_charge_rate=0.00125) -> None:
        self.total_dutiable_value = total_dutiable_value
        self.bank_charge_rate = bank_charge_rate

    def calculate_bank_charge(self) -> float:
        total_bank_charge = round(
            self.total_dutiable_value * self.bank_charge_rate, 2
        )
        return total_bank_charge
