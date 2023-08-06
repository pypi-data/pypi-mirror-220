class ArrastreChargeOutports:
    def __init__(self, total_metric_ton: float) -> None:
        self.total_metric_ton = total_metric_ton

    def calculate_arrastre_charge_outports(self, arrastre_charge_rate: float) -> float:
        total_arrastre_charge = round(
            self.total_metric_ton * arrastre_charge_rate, 2
        )
        return total_arrastre_charge


class ArrastreChargeOutportsViaShipside(ArrastreChargeOutports):
    def __init__(self, total_metric_ton: float, arrastre_charge_rate=8.00) -> None:
        super().__init__(total_metric_ton)
        self.arrastre_charge_rate = arrastre_charge_rate

    def calculate_arrastre_charge_outport_via_shipside(self) -> float:
        return self.calculate_arrastre_charge_outports(self.arrastre_charge_rate)


class ArrastreChargeOutportsViaPierside(ArrastreChargeOutports):
    def __init__(self, total_metric_ton: float, arrastre_charge_rate=110.00) -> None:
        super().__init__(total_metric_ton)
        self.arrastre_charge_rate = arrastre_charge_rate

    def calculate_arrastre_charge_outport_via_pierside(self) -> float:
        return self.calculate_arrastre_charge_outports(self.arrastre_charge_rate)
