class Player:
    def __init__(self, name: str, health: int, player_id):
        self.name = name
        self.health = health
        self.player_id = player_id
        self.inventory = [[],[]]
    
    def get_inventory(self):
        return [list(self.inventory[0]), list(self.inventory[1])]

    def get_weapons(self):
        return self.inventory[0]
    
    def get_heals(self):
        return self.inventory[1]

    def get_player_health(self):
        return self.health
    
    def add_weapon(self, name):
        self.inventory[0].append(name)

    def add_heal(self, name):
        self.inventory[1].append(name)

    def remove_heal(self, name):
        self.inventory[1].remove(name)
    
    def heal_player(self, heal):
        self.health += heal

