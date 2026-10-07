from Building import Building
from Employee import Employee
from Fund import Fund
from Exhibition import Exhibition

#1/7
class Museum:
    """усилить функции"""
    def __init__(self, name, address, website):
        self.name = name
        self.address = address
        self.website = website
        self.buildings=[]
        self.employees=[]
        self.exhibitions=[]
        self.funds=[]
        self.budget = 0

    def add_building(self, building: Building):
        self.buildings.append(building)

    def add_employee(self, employee: Employee):
        self.employees.append(employee)

    def add_exhibition(self, exhibition: Exhibition):
        self.exhibitions.append(exhibition)

    def add_fund(self, fund: Fund):
        self.funds.append(fund)

    def set_budget(self, budget):
        self.budget = budget