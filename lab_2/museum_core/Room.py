from Employee import Employee

#4/4
class Room:
    """служебное помещение (касса, охрана). закрыть комнату, изменить ответственного"""
    def __init__(self, name, purpose, responsible: Employee):
        self.name = name
        self.purpose = purpose
        self.responsible = responsible
        self.locked = False

    def locked(self, locked: bool):
        self.locked = locked

    def add_responsible(self, responsible: Employee):
        if responsible:
            self.responsible = responsible