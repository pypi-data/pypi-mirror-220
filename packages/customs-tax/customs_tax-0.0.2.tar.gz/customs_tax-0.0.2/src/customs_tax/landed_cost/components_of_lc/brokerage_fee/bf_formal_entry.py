class BrokerageFeeFormalEntry:
    def __init__(self, dutiable_value=0.0, bank_charge=0.00125, brokerage_fee_1300=1300.00, brokerage_fee_2000=2000.00,
                 brokerage_fee_2700=2700.00, brokerage_fee_3300=3300.00, brokerage_fee_3600=3600.00,
                 brokerage_fee_4000=4000.00, brokerage_fee_4700=4700.00, brokerage_fee_5300=5300.00,
                 brokerage_fee_5050=5050.00) -> None:
        self.brokerage_fee_1300 = brokerage_fee_1300
        self.brokerage_fee_2000 = brokerage_fee_2000
        self.brokerage_fee_2700 = brokerage_fee_2700
        self.brokerage_fee_3300 = brokerage_fee_3300
        self.brokerage_fee_3600 = brokerage_fee_3600
        self.brokerage_fee_4000 = brokerage_fee_4000
        self.brokerage_fee_4700 = brokerage_fee_4700
        self.brokerage_fee_5300 = brokerage_fee_5300
        self.brokerage_fee_5050 = brokerage_fee_5050
        self.dutiable_value = dutiable_value
        self.bank_charge = bank_charge

    def calculate_dutiable_value_to_brokerage_fee_formal(self) -> float:
        brokerage_fee = 0.0

        if self.dutiable_value <= 10000:
            brokerage_fee = self.brokerage_fee_1300

        elif 10000 < self.dutiable_value <= 20000:
            brokerage_fee = self.brokerage_fee_2000

        elif 20000 < self.dutiable_value <= 30000:
            brokerage_fee = self.brokerage_fee_2700

        elif 30000 < self.dutiable_value <= 40000:
            brokerage_fee = self.brokerage_fee_3300

        elif 40000 < self.dutiable_value <= 50000:
            brokerage_fee = self.brokerage_fee_3600

        elif 50000 < self.dutiable_value <= 60000:
            brokerage_fee = self.brokerage_fee_4000

        elif 60000 < self.dutiable_value <= 100000:
            brokerage_fee = self.brokerage_fee_4700

        elif 100000 < self.dutiable_value <= 200000:
            brokerage_fee = self.brokerage_fee_5300

        elif self.dutiable_value > 200000:
            brokerage_fee = self.brokerage_fee_5050

        total_brokerage_fee = round(
            self.dutiable_value * self.bank_charge + brokerage_fee, 2
        )
        return total_brokerage_fee
