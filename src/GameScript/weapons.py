from enum import Enum

class Weapons(Enum):
    AK47 = 60
    RPG = 85
    KNIFE = 25
    GLOCK = 40
    FIST = 15
    SWORD = 25

    @staticmethod
    def access_dammage(name):
        try:
            return Weapons[name].value
        except:
            ValueError(f"{name} is not a valid weapon")

