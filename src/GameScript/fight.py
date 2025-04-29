from .bosses import BossTypes
import random

smallBosses = [BossTypes.Slime, BossTypes.RatKing, BossTypes.ChainChomper, BossTypes.LivingShadow, BossTypes.WanderingEye]
bigBosses = [BossTypes.HypnoticSpecter, BossTypes.GelatinousCube, BossTypes.MargittheFellOmen, BossTypes.RedWolfofRadagon, BossTypes.RennalaQueenoftheFullMoon]

def random_boss(type):
    if type == "b":
        return random.choice(smallBosses)
    elif type == "B":
        return random.choice(bigBosses)
    else:
        raise ValueError("Invalid boss type. Use 'b' for small or 'B' for big.")

