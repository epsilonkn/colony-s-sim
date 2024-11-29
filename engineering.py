from header import *



class engineer() :
    
    @classmethod
    def action(threat : int, population : int, it : int, gen : int, food : int, max_food : int, material : int, max_mat : int):
        popu = ( (MAX_POPU-population) / (MAX_POPU - MIN_POPU) ) * DRONE_BUILD_COEF
        food = ( food / max_food ) * STORAGE_COEF
        mat = ( material / max_mat ) * STORAGE_COEF


class defense():
    
    def __init__(self, pv : int, dmg : int, vit : int, iron : int, copper : int, silicium : int) -> None:
        self.pv = pv
        self.dmg = dmg
        self.vit = vit
        



class tourelle(defense):
    iron = 4
    copper = 2
    silicium = 5



class piege(defense):
    iron = 1
    copper = 2
    silicium = 3


class repair_station(defense):
    iron = 10
    copper = 5
    silicium = 5


class drone_station(defense):
    iron = 20
    copper = 15
    silicium = 10



#------------------------------------------------------------------


class storage():
    
    def __init__(self, capacity : int) -> None:
        self.capacity = capacity
        self.fill = 0


    def add(self, quant : int):
        self.fill += quant


    def take(self, quant : int):
        self.fill -= quant


class cellar(storage):
    
    def __init__(self, capacity: int) -> None:
        super().__init__(capacity)



class warehouse(storage):
        
    def __init__(self, capacity: int) -> None:
        super().__init__(capacity)


#------------------------------------------------------------------


class research():
    pass


class upgrade_drones(research):
    pass


class upgrade_defense(research):
    pass


class build_drone():
    iron = 2
    copper = 1
    silicium = 1
    sprite_path =  getcwd() + "image\\fourmi_soldat.png"
    scale = SPRITE_SCALING/8