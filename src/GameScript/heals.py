from enum import Enum

class Heals(Enum):
    Bandages = 15
    MediKit = 40

    @staticmethod
    def access_heal(name):
        try:
            return Heals[name].value
        except:
            ValueError(f"{name} is not a valid heal")
