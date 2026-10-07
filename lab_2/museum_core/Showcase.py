from ClimateZone import ClimateZone

#6/3
class Showcase:
    """витрина. изменить климат, добавить экспонат"""
    def __init__(self, name, climate_zone: ClimateZone):
        self.name = name
        self.climate_zone = climate_zone
        self.exhibits = []