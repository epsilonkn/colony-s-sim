import arcade
import random
from multiprocessing.dummy import Pool as ThreadPool


# Constantes pour la taille de l'écran et la vitesse du sprite
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SPRITE_SPEED = 2
DETECTION_RADIUS = 100

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Déplacement Autonome de Sprite avec Détection")
        arcade.set_background_color(arcade.color.ASH_GREY)
        self.sprite1 = None
        self.sprite2 = None
        self.previous_change_x = 0
        self.previous_change_y = 0

    def setup(self):
        # Charger les sprites
        self.liste = arcade.SpriteList()
        self.sprite1 = arcade.Sprite("C:\\Users\ywan\\Documents\\programmation\\Ant Sim\\fourmi_soldat.png", scale=0.5)
        self.sprite1.center_x = SCREEN_WIDTH // 2
        self.sprite1.center_y = SCREEN_HEIGHT // 2
        self.sprite1.change_x = random.uniform(-SPRITE_SPEED, SPRITE_SPEED)
        self.sprite1.change_y = random.uniform(-SPRITE_SPEED, SPRITE_SPEED)

        self.sprite2 = arcade.Sprite("C:\\Users\ywan\\Documents\\programmation\\Ant Sim\\fourmi_soldat.png", scale=0.5)
        self.sprite2.center_x = random.uniform(0, SCREEN_WIDTH)
        self.sprite2.center_y = random.uniform(0, SCREEN_HEIGHT)
        self.liste.append(self.sprite2)

    def update(self, delta_time):
        # Garder une copie des changements précédents
        self.previous_change_x = self.sprite1.change_x
        self.previous_change_y = self.sprite1.change_y

        # Mettre à jour la position du sprite
        self.sprite1.center_x += self.sprite1.change_x
        self.sprite1.center_y += self.sprite1.change_y

        # Ajouter un peu de bruit pour un mouvement plus naturel
        change_x = self.previous_change_x + random.uniform(-0.5, 0.5)
        change_y = self.previous_change_y + random.uniform(-0.5, 0.5)

        # Limiter la vitesse du sprite pour éviter des mouvements trop rapides
        change_x = max(-SPRITE_SPEED, min(change_x, SPRITE_SPEED))
        change_y = max(-SPRITE_SPEED, min(change_y, SPRITE_SPEED))

        # Empêcher le sprite de retourner sur ses pas
        if abs(change_x + self.previous_change_x) < 0.1:
            change_x = -self.previous_change_x
        if abs(change_y + self.previous_change_y) < 0.1:
            change_y = -self.previous_change_y

        self.sprite1.change_x = change_x
        self.sprite1.change_y = change_y

        # Garder le sprite à l'intérieur de l'écran
        if self.sprite1.left < 0 or self.sprite1.right > SCREEN_WIDTH:
            self.sprite1.change_x *= -1
        if self.sprite1.bottom < 0 or self.sprite1.top > SCREEN_HEIGHT:
            self.sprite1.change_y *= -1

        # Détection de proximité avec l'autre sprite
        if arcade.check_for_collision_with_list(self.sprite1, self.liste):
            distance = arcade.get_distance_between_sprites(self.sprite1, self.sprite2)
            if distance < DETECTION_RADIUS:
                print("Sprite détecté à proximité")

    def on_draw(self):
        # Dessiner les sprites
        arcade.start_render()
        self.sprite1.draw()
        self.sprite2.draw()

def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()