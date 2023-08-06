class WDBulkBreakBulkCargo:
    def __init__(self, type_of_ton: float, total_metric_or_revenue_tons: float) -> None:
        self.type_of_ton = type_of_ton
        self.total_metric_or_revenue_tons = total_metric_or_revenue_tons
        self.wharfage_due_rate = float
        self.revenue_ton_type = 1
        self.metric_ton_type = 2

    def calculate_lcl(self, wharfage_due_rate) -> float:
        total_wharfage_due = round(
            self.total_metric_or_revenue_tons * wharfage_due_rate, 2
        )
        return total_wharfage_due


class WDBulkBreakBulkCargoImport(WDBulkBreakBulkCargo):
    def __init__(self, type_of_ton, total_metric_or_revenue_tons) -> None:
        super().__init__(type_of_ton, total_metric_or_revenue_tons)
        self.revenue_ton = 30.55
        self.metric_ton = 36.65

    def calculate_lcl_import(self) -> float:
        if self.type_of_ton == self.revenue_ton_type:
            self.wharfage_due_rate = self.revenue_ton

        elif self.type_of_ton == self.metric_ton_type:
            self.wharfage_due_rate = self.metric_ton

        return self.calculate_lcl(self.wharfage_due_rate)


class WDBulkBreakBulkCargoExport(WDBulkBreakBulkCargo):
    def __init__(self, type_of_ton, total_metric_or_revenue_tons) -> None:
        super().__init__(type_of_ton, total_metric_or_revenue_tons)
        self.revenue_ton = 15.25
        self.metric_ton = 18.35

    def calculate_lcl_export(self) -> float:
        if self.type_of_ton == self.revenue_ton_type:
            self.wharfage_due_rate = self.revenue_ton

        elif self.type_of_ton == self.metric_ton_type:
            self.wharfage_due_rate = self.metric_ton

        return self.calculate_lcl(self.wharfage_due_rate)
