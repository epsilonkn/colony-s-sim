from header import *
from fimport import *



class Ant():

    def __init__(self, 
                 id : str = None, 
                 sprite : object = None,
                 coef : float = 1
                 ) -> None:
        """
        init de chaque fourmi

        Parameters
        ----------
        type : str
            type de la fourme, "worker"
        """
        self.life : int = randint(30, 45)
        self.lifespan : int = randint(15000, 20000)
        self.vit : int = 2*coef
        self.dmg : tuple[int] = randint(4,8)
        self.id : str = id
        self.type : str = type
        self.fight_behave : str = ""
        self.hunger : int = randint(4500,5500)
        self.sprite : arcade.Sprite = sprite
        self.dest_list : list = []
        self.dest_memory : list = []
        self.task : Task = None
        self.def_fatigue : int = randint(20,80)
        self.current_fatigue : float = self.def_fatigue
        self.status : str = "none"
        self.transport_will : float = randint(5,15)/10


    def __str__(self):
        return f"{self.id}"


    def fill_hunger(self):
        self.hunger = randint(4500,5500)

    def change_fatigue(self, new_val):
        self.current_fatigue = new_val
