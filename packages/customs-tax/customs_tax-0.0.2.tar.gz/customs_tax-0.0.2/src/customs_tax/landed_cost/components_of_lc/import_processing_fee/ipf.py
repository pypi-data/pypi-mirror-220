class ImportProcessingFee:
    def __init__(self, dutiable_value=0.0, import_processing_fee_250=250.00, import_processing_fee_500=500.00,
                 import_processing_fee_750=750.00, import_processing_fee_1000=1000.00) -> None:
        self.import_processing_fee_250 = import_processing_fee_250
        self.import_processing_fee_500 = import_processing_fee_500
        self.import_processing_fee_750 = import_processing_fee_750
        self.import_processing_fee_1000 = import_processing_fee_1000
        self.dutiable_value = dutiable_value

    def calculate_dutiable_value_to_import_processing_fee(self) -> float:
        if self.dutiable_value <= 250000:
            import_processing_fee = self.import_processing_fee_250
            return import_processing_fee

        elif 250000 < self.dutiable_value <= 500000:
            import_processing_fee = self.import_processing_fee_500
            return import_processing_fee

        elif 500000 < self.dutiable_value <= 750000:
            import_processing_fee = self.import_processing_fee_750
            return import_processing_fee

        elif self.dutiable_value > 750000:
            import_processing_fee = self.import_processing_fee_1000
            return import_processing_fee
