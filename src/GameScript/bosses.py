from enum import Enum

class BossTypes(Enum):
    Slime = (60, 8)
    RatKing = (80, 12)
    ChainChomper = (50, 10)
    LivingShadow = (80, 15)
    WanderingEye = (40, 5)
    
    HypnoticSpecter = (150, 20)
    GelatinousCube = (400, 22)
    MargittheFellOmen = (300, 25)
    RedWolfofRadagon = (800, 41)
    RennalaQueenoftheFullMoon = (500, 33)
    
    @staticmethod
    def access_health(name: str):
        try:
            return BossTypes[name].value[0]
        except KeyError:
            raise ValueError(f"{name} is not a valid BossType")

    @staticmethod
    def access_dammage(name: str):
        try:
            return BossTypes[name].value[1]
        except KeyError:
            raise ValueError(f"{name} is not a valid BossType")


