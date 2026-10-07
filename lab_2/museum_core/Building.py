from Hall import Hall
from Room import Room

#2/6
class Building:
    """здание музея (главный корпус, фондохранилище, админкорпус). добавить залы/комнаты"""
    def __init__(self, name, address, type_, floors):
        self.name = name
        self.address = address
        self.type_ = type_
        self.floors = floors
        self.halls=[]
        self.rooms=[]

    def add_hall(self, hall: Hall):
        self.halls.append(hall)

    def add_room(self, room: Room):
        self.rooms.append(room)