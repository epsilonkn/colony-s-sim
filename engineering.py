from header import *

DEFENSE_COEF = 1
STORAGE_COEF = 0.7
RESEARCH_COEF = 0.7
DRONE_BUILD_COEF = 0.7
MIN_POPU = 15
MAX_POPU = 25

SEUIL_ACTIVATION = 0.5


class engineer() :

    @classmethod
    def _population(engineer):
        return "build_ant"

    
    @classmethod
    def _food_stock(engineer):
        return "upgrade_cellar"

    
    @classmethod
    def _mat_stock(engineer):
        return "upgrade_warehouse"


    @classmethod
    def threat_behave(engineer):
        pass


    behave = {"popu" : "build_ant", "food" : "upgrade_cellar", "mat" : "upgrade_warehouse", "threat" : threat_behave}

    
    @classmethod
    def action(engineer, threat_nb : int, population : int, it : int, gen : int, food : int, max_food : int, material : int, max_mat : int):
        """
        fonction de calcul des coefficients pour la prise de décision dans la construction

        Args:
            threat_nb (int): _description_
            population (int): nombre d'individus en vie
            it (int): itération
            gen (int): génération
            food (int): quantité de nourriture en stock
            max_food (int): stock max de nourriture
            material (int): quantité de matériel divers en stock
            max_mat (int): stock max de matériel

        Returns:
            _type_: _description_
        """
        threat = 0
        popu = ( (MAX_POPU-population) / (MAX_POPU - MIN_POPU) ) * DRONE_BUILD_COEF
        food = ( food / max_food ) * STORAGE_COEF
        mat = ( material / max_mat ) * STORAGE_COEF
        coef_list = [("popu", popu), ("food", food), ("mat", mat), ("threat", threat)]
        engineer.sort(coef_list)
        return engineer.behave[coef_list[0][0]] if coef_list[0][1] > SEUIL_ACTIVATION else "no_new"



    def sort(l : list) :
        for i in range(len(l)):
            j = i
            while (l[j][1] > l[j-1][1] and j > 0) :
                l[j], l[j-1] = l[j-1], l[j]
                j -= 1



class defense():
    
    def __init__(self, pv : int, dmg : int, vit : int, iron : int, copper : int, silicium : int) -> None:
        self.pv = pv
        self.dmg = dmg
        self.vit = vit
        



class tourelle(defense):
    iron = 4
    copper = 2
    silicium = 5
    sprite = getcwd() + "\\image\\tourelle.png"



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
        self.level = 1


    def add(self, quant : int):
        self.fill += quant


    def take(self, quant : int):
        self.fill -= quant

    
    def get_stock(self):
        return self.fill
    

    def full(self):
        return (self.capacity == self.fill)



class Cellar(storage):

    iron = 3
    copper = 2
    silicium = 1
    
    def __init__(self, capacity: int) -> None:
        super().__init__(capacity)



class Warehouse(storage):

    iron = 3
    copper = 2
    silicium = 1
        
    def __init__(self, capacity: int, iron : int = 0, copper : int = 0, silicium : int = 0) -> None:
        super().__init__(capacity)
        self.iron = iron
        self.copper = copper
        self.silicium = silicium


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
    sprite_path =  getcwd() + "\\image\\fourmi_soldat.png"
    #scale = SPRITE_SCALING/8



if __name__ == "__main__":
    print(engineer.action(0,15,0,0,100,200,100,200))