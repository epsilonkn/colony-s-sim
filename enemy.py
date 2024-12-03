from fimport import *


class Enemy():

    def __init__(self, life, dmg, vit, type,sprite):
        self.life = life
        self.dmg = dmg
        self.vit = vit
        self.enemy_type = type
        self.detection = 150
        self.image = "image/enemy.png"
        self.sprite = sprite



class Combat():

    @classmethod
    def fight(Combat, atker : object, target : object):
        target.life -= atker.dmg
        if target.life <= 0:
            return True
        return False

    
    @classmethod
    def defineProrityTarget(Combat, enemy : Enemy, ants : list[object]):
        liste = []
        for ant in ants :
            if abs(ant.sprite.center_x - enemy.sprite.center_x) < enemy.detection and abs(ant.sprite.center_y - enemy.sprite.center_y) < enemy.detection :
                liste.append((ant, math.sqrt((ant.sprite.center_x - enemy.sprite.center_x)**2 + (ant.sprite.center_y - enemy.sprite.center_y)**2)))
        Combat.sort(liste)
        return liste


    def sort(l : list) :
        for i in range(len(l)):
            j = i
            while (l[j][1] < l[j-1][1] and j > 0) :
                l[j], l[j-1] = l[j-1], l[j]
                j -= 1