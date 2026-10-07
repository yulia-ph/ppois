from Employee import Employee
from ClimateZone import ClimateZone
from museum_exhibits.Exhibit import Exhibit


#5/5
class Storage:
    """фондохранилище. изменить требуемый климат, изменить ответственного, сложить на склад"""
    def __init__(self, name, capacity, climate_zone: ClimateZone, keeper: Employee):
        self.name = name
        self.capacity = capacity
        self.climate_zone = climate_zone
        self.keeper = keeper
        self.exhibits =[]

    def add_exhibits(self, exhibit: Exhibit):
        self.exhibits.append(exhibit)

    def add_keeper(self, keeper: Employee):
        if keeper:
            self.keeper = keeper

    def change_climate_zone(self, climate_zone: ClimateZone):
        self.climate_zone = climate_zone