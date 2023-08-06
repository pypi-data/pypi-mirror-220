class CustomsDocumentaryStamp:
    def __init__(self, type_of_entry: float) -> None:
        self.type_of_entry = type_of_entry
        self.formal_entry = 1
        self.informal_entry = 2

    def calculate_customs_documentary_stamp(self):
        if self.type_of_entry == self.formal_entry:
            customs_documentary_stamp = 280.00
            return customs_documentary_stamp

        elif self.type_of_entry == self.informal_entry:
            customs_documentary_stamp = 30.00
            return customs_documentary_stamp
