from Showcase import Showcase
from ClimateZone import ClimateZone
from Exhibition import Exhibition

#3/6
class Hall:
    """выставочный зал. Разместить/убрать выставку, добавить ветрину. проверить климат"""
    def __init__(self, name, max_capacity, climate_zone: ClimateZone):
        self.name = name
        self.max_capacity = max_capacity
        self.climate_zone = climate_zone
        self.show_cases = []
        self.current_exhibition = None

    def add_show_case(self, show_case: Showcase):
        self.show_cases.append(show_case)

    def manage_current_exhibition(self, exhibition: Exhibition, flag):
        if flag:
            self.current_exhibition = exhibition
            return
        self.current_exhibition = None