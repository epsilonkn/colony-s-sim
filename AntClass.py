from header import *



class Ant():

    def __init__(self, 
                 type : str = "worker", 
                 id : str = None, 
                 sprite : object = None
                 ) -> None:
        """
        init de chaque fourmi

        Parameters
        ----------
        type : str
            type de la fourmi, "worker" ou "queen"
        """
        self.life : int = randint(40, 60) if type == "worker" else randint(80, 120)
        self.lifespan : int = randint(15000, 18000) if type == "worker" else randint(6000, 8000)
        self.vit : int = 2
        self.dmg : tuple[int] = (4,8) if type == "worker" else (6,10)
        self.id : str = id
        self.type : str = type
        self.fight_behave : str = "" if type == "worker" else "queen"
        self.hunger : int = randint(4500,5500)
        self.role : list[str] = []
        self.sprite : arcade.Sprite = sprite
        self.dest_list : list = []
        self.task : Task = None


    def __str__(self):
        return f"{self.id}"


    def fill_hunger(self):
        self.hunger = randint(4500,5500)


        

class Nest():

    def __init__(self) -> None:
        self.food : int = 0
        self.rooms : list = []
        self.eggs : int = 0
