#8/2
class Sensor:
    """датчик (температура/влажность)"""
    def __init__(self, type_):
        self.type_ = type_
        self.value = 0