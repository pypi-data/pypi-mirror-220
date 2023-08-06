class WharfageDueOutports:
    def __init__(self, total_metric_ton: float) -> None:
        self.total_metric_ton = total_metric_ton

    def calculate_wharfage_due_outports(self, wharfage_due_rate: float) -> float:
        total_wharfage_due = round(
            self.total_metric_ton * wharfage_due_rate, 2
        )
        return total_wharfage_due


class WharfageDueOutportsViaShipside(WharfageDueOutports):
    def __init__(self, total_metric_ton: float, wharfage_due_rate=17.00) -> None:
        super().__init__(total_metric_ton)
        self.wharfage_due_rate = wharfage_due_rate

    def calculate_wharfage_due_outport_via_shipside(self) -> float:
        return self.calculate_wharfage_due_outports(self.wharfage_due_rate)


class WharfageDueOutportsViaPierside(WharfageDueOutports):
    def __init__(self, total_metric_ton: float, wharfage_due_rate=34.00) -> None:
        super().__init__(total_metric_ton)
        self.wharfage_due_rate = wharfage_due_rate

    def calculate_wharfage_due_outport_via_pierside(self) -> float:
        return self.calculate_wharfage_due_outports(self.wharfage_due_rate)
