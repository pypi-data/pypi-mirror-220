class ACContainerizedCargo:
    def __init__(self, size_of_container: float, total_number_of_containers: float):
        self.size_of_container = size_of_container
        self.total_number_of_containers = total_number_of_containers
        self.arrastre_charge_rate = float
        self.twenty_footer = 20
        self.forty_footer = 40
        self.forty_five_footer = 45


class ACContainerizedCargoImport(ACContainerizedCargo):
    def __init__(self, size_of_container: float, total_number_of_containers: float) -> None:
        super().__init__(size_of_container, total_number_of_containers)

    def calculate_containerized_cargo_import(self):
        twenty_footer_rate = 3727.00
        forty_footer_rate = 8551.00
        forty_five_footer_rate = 8551.00

        if self.size_of_container == self.twenty_footer:
            self.arrastre_charge_rate = twenty_footer_rate

        elif self.size_of_container == self.forty_footer:
            self.arrastre_charge_rate = forty_footer_rate

        elif self.size_of_container == self.forty_five_footer:
            self.arrastre_charge_rate = forty_five_footer_rate

        total_arrastre_charge = round(
            self.total_number_of_containers * self.arrastre_charge_rate, 2
        )
        return total_arrastre_charge


class ACContainerizedCargoExport(ACContainerizedCargo):
    def __init__(self, size_of_container: float, total_number_of_containers: float, ) -> None:
        super().__init__(size_of_container, total_number_of_containers)

    def calculate_containerized_cargo_export(self):
        twenty_footer_rate = 3043.00
        forty_footer_rate = 6989.00
        forty_five_footer_rate = 6989.00

        if self.size_of_container == self.twenty_footer:
            self.arrastre_charge_rate = twenty_footer_rate

        elif self.size_of_container == self.forty_footer:
            self.arrastre_charge_rate = forty_footer_rate

        elif self.size_of_container == self.forty_five_footer:
            self.arrastre_charge_rate = forty_five_footer_rate

        total_arrastre_charge = round(
            self.total_number_of_containers * self.arrastre_charge_rate, 2
        )
        return total_arrastre_charge


class ACContainerizedCargoShutOutExport:
    def __init__(self, total_number_of_containers: float, type_of_shutout_export_container: float) -> None:
        self.total_number_of_containers = total_number_of_containers
        self.type_of_shutout_export_container = type_of_shutout_export_container
        self.arrastre_charge_rate = float
        self.full_or_loaded_container = 1
        self.empty_container = 2

    def calculate_containerized_cargo_shutout_export(self) -> float:
        full_or_loaded_container = 3039.00
        empty_container = 1519.00

        if self.type_of_shutout_export_container == self.full_or_loaded_container:
            self.arrastre_charge_rate = full_or_loaded_container

        elif self.type_of_shutout_export_container == self.empty_container:
            self.arrastre_charge_rate = empty_container

        total_arrastre_charge = round(
            self.total_number_of_containers * self.arrastre_charge_rate, 2
        )
        return total_arrastre_charge
