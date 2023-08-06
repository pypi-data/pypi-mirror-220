class ContainerizedDangerousCargoClass:
    def __init__(self, classification_of_dangerous_cargo: float, total_number_of_containers: float) -> None:
        self.classification_of_dangerous_cargo = classification_of_dangerous_cargo
        self.total_number_of_containers = total_number_of_containers
        self.arrastre_charge_rate = float
        self.class_1_6_8 = 1
        self.class_2_3_4_7 = 2
        self.class_5_9 = 3

    def calculate_fcl_footer(self, arrastre_charge_rate) -> float:
        total_arrastre_charge = round(
            self.total_number_of_containers * arrastre_charge_rate, 2
        )
        return total_arrastre_charge


class ACContainerizedDangerousCargo20Footer(ContainerizedDangerousCargoClass):
    def __init__(self, classification_of_dangerous_cargo: float, total_number_of_containers: float) -> None:
        super().__init__(classification_of_dangerous_cargo, total_number_of_containers)
        self.class_1_6_8_rate = 5590.50
        self.class_2_3_4_7_rate = 4658.75
        self.class_5_9_rate = 4099.70

    def calculate_fcl_20_footer(self) -> float:
        if self.classification_of_dangerous_cargo == self.class_1_6_8:
            self.arrastre_charge_rate = self.class_1_6_8

        elif self.classification_of_dangerous_cargo == self.class_2_3_4_7:
            self.arrastre_charge_rate = self.class_2_3_4_7

        elif self.classification_of_dangerous_cargo == self.class_5_9:
            self.arrastre_charge_rate = self.class_5_9

        return self.calculate_fcl_footer(self.arrastre_charge_rate)


class ACContainerizedDangerousCargo40Footer(ContainerizedDangerousCargoClass):
    def __init__(self, classification_of_dangerous_cargo: float, total_number_of_containers: float) -> None:
        super().__init__(classification_of_dangerous_cargo, total_number_of_containers)
        self.class_1_6_8 = 12826.00
        self.class_2_3_4_7 = 10688.75
        self.class_5_9 = 9406.10

    def calculate_fcl_40_footer(self) -> float:
        if self.classification_of_dangerous_cargo == self.class_1_6_8:
            self.arrastre_charge_rate = self.class_1_6_8

        elif self.classification_of_dangerous_cargo == self.class_2_3_4_7:
            self.arrastre_charge_rate = self.class_2_3_4_7

        elif self.classification_of_dangerous_cargo == self.class_5_9:
            self.arrastre_charge_rate = self.class_5_9

        return self.calculate_fcl_footer(self.arrastre_charge_rate)
