#7/6
class ClimateZone:
    """микроклимат помещения. обновить данные"""
    def __init__(self, norm_temperature, norm_humidity):
        self.temperature = 0
        self.humidity = 0
        self.norm_temperature = norm_temperature
        self.norm_humidity = norm_humidity
        self.sensors = []
        self.alarm = False