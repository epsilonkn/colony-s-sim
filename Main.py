from header import *



class Task():

    def __init__(self, 
                 sprite : object = None, 
                 coords : tuple[int] = (0.0), 
                 final : tuple[int] = (0,0), 
                 iteration : int = 1, 
                 task_type : str = "food", 
                 parent = None) -> None:
        self.sprite : arcade.Sprite = sprite
        self.coords : tuple[int] = coords
        self.final : tuple[int] = final
        self.it : int = iteration
        self.print_it = iteration
        self.type : str = task_type
        self.status : str = "in_wait"
        self.parent = parent

    def __str__(self) -> str:
        return f"{self.type} | {self.it}"



class MyGame(arcade.Window):
    """ Main application class. """
    def __init__(self, width, height, title):
        """
        Initializer
        """
        super().__init__(width, height, title, resizable=True)

        #lists
        self.consumable_sprite_list = None
        self.consumable_list = []
        self.all_task_list : list[int, Task] = []
        self.current_task_list : list[Task] = []
        self.ant_obj_list : list[Ant] = []
        self.death_soon_ant : list[Ant] = []
        self.hungry_ant : list[Ant] = []
        self.corpse_list : arcade.SpriteList = None
        self.object_type : dict = {}

        # Set up the num of ant
        self.ant_number = 0
        self.ant_id = 0
        self.gen = 1

        self.gather_ant = 0

        # Set up the number of iteration :
        self.iteration = 0

        #set up camera's sets :
        self.camera_scale = 1
        self.camera_moving = False
        self.camera_start_x = 0
        self.camera_start_y = 0
        self.camera_pos_x = 0
        self.camera_pos_y = 0

        self.out_food = 0
        self.nest_food = 20
        self.enemy = False
        self.iron = 0
        self.copper = 0
        self.silicium = 0

        # Create the cameras. One for the GUI, one for the sprites.
        # We scroll the 'sprite world' but not the GUI.
        self.camera_sprites = arcade.Camera(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT)
        self.camera_gui = arcade.Camera(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT)



    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.consumable_sprite_list = arcade.SpriteList()
        self.ant_list = arcade.SpriteList()
        self.corpse_list = arcade.SpriteList()


        # Set up the player


        self.fourmiliere = arcade.Sprite( getcwd() + "image\\fourmiliere.png", SPRITE_SCALING)
        self.fourmiliere.center_x = -10
        self.fourmiliere.center_y = -20

        for i in range(randint(2,4)):
            self.create_event("food")

        for i in range(START_ANT_NB): 
            self.create_ant()

        for _ in range(randint(4,6)):
            self.create_event("ore")
        #self.physics_engine = arcade.PhysicsEngineSimple(, [])

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

        self.set_update_rate(1/100)



    def create_ant(self):
        ant = arcade.Sprite( getcwd() + "image\\fourmi_soldat.png", (SPRITE_SCALING/8))
        ant.center_x = 0
        ant.center_y = 0
        self.ant_number += 1
        self.ant_list.append(ant)
        ant_obj = Ant(id = "<Ant{}>".format(self.ant_id), sprite= ant)
        self.ant_obj_list.append(ant_obj)
        self.ant_id += 1


    def create_task(self, **kwargs):
        """create_task 
        args :
        sprite
        coords
        final
        iteration
        task_type
        """
        new_task = Task(kwargs["sprite"] if "sprite" in kwargs.keys() else 0, 
                        kwargs["coords"] if "coords" in kwargs.keys() else (0,0), 
                        kwargs["final"] if "final" in kwargs.keys() else (0,0),
                        kwargs["iteration"] if "iteration" in kwargs.keys() else 1,
                        kwargs["task_type"] if "task_type" in kwargs.keys() else "food")
        self.out_food += new_task.it if new_task.type == "food" else 0
        self.current_task_list.append(new_task)
        self.all_task_list.append((self.iteration,new_task))


    
    def create_task2(self, **kwargs):
        """create_task 
        args :
        sprite
        coords
        final
        iteration
        task_type
        """
        new_task = Task(kwargs["sprite"] if "sprite" in kwargs.keys() else None, 
                        kwargs["coords"] if "coords" in kwargs.keys() else (0,0),
                        kwargs["final"] if "final" in kwargs.keys() else (0,0),
                        kwargs["iteration"] if "iteration" in kwargs.keys() else 1,
                        kwargs["task_type"] if "task_type" in kwargs.keys() else "food",
                        kwargs["parent"] if "parent" in kwargs.keys() else None)
        return new_task



    def close_task(self, ant : Ant, **kwargs):
        match ant.task.type :

            case "food" :
                self.nest_food += 1
                self.gather_ant -= 1
            case "found_food" :
                for _ , task in self.all_task_list :
                    if task.sprite == kwargs["sprite"] or task.sprite == None :
                        ant.task = None
                        return
                self.create_task(sprite = kwargs["sprite"], coords = (kwargs["sprite"].center_x, kwargs["sprite"].center_y), iteration = randint(10,15))
            case "eat" :
                if self.nest_food > 0 :
                    self.nest_food -= 1
                    ant.fill_hunger()
                else : 
                    ant.dest_list = []
                    self.hungry_ant.append(ant)
                    return
            case "found_corpse" :
                for it, task in self.all_task_list :
                    if task.sprite == kwargs["sprite"] or task.sprite == None  :
                        ant.task = None
                        return
                self.create_task(sprite = kwargs["sprite"], coords = (kwargs["sprite"].center_x, kwargs["sprite"].center_y), iteration = 1, task_type = "corpse")
            case "found_iron" :
                for _ , task in self.all_task_list :
                    if task.sprite == kwargs["sprite"] or task.sprite == None  :
                        ant.task = None
                        return
                self.create_task(sprite = kwargs["sprite"], coords = (kwargs["sprite"].center_x, kwargs["sprite"].center_y), iteration = randint(10,15), task_type = "iron")
            case "iron" :
                self.iron += 1
            case "found_copper" :
                for _ , task in self.all_task_list :
                    if task.sprite == kwargs["sprite"] or task.sprite == None  :
                        ant.task = None
                        return
                self.create_task(sprite = kwargs["sprite"], coords = (kwargs["sprite"].center_x, kwargs["sprite"].center_y), iteration = randint(5,10), task_type = "copper") 
            case "copper" :
                self.copper += 1
            case "found_silicium" :
                for _ , task in self.all_task_list :
                    if task.sprite == kwargs["sprite"] or task.sprite == None  :
                        ant.task = None
                        return
                self.create_task(sprite = kwargs["sprite"], coords = (kwargs["sprite"].center_x, kwargs["sprite"].center_y), iteration = randint(5,10), task_type = "silicium") 
            case "silicium" :
                self.silicium += 1
              
        ant.task = None


    def create_event(self, type : str):
        match type :
            case "food": 
                food = arcade.Sprite( getcwd() + "image\\food.png", (SPRITE_SCALING/2))
                food.center_x, food.center_y = self.spawn_pos()
                self.consumable_sprite_list.append(food)
                self.object_type[food] = "food"
            case "un":
                task = arcade.Sprite( getcwd() + "image\\box.png", (SPRITE_SCALING/4))
                task.center_x = randint(-1300,1300)
                task.center_y =  randint(-1300,1300)
                self.consumable_sprite_list.append(task)
                self.create_task(sprite = task, coords = (task.center_x, task.center_y), iteration = randint(10,15), task_type = "un")
            case "ore" :
                ore_type = randint(1,3)
                match ore_type :

                    case 1 :
                        ore = arcade.Sprite( getcwd() + "image\\iron.png", (SPRITE_SCALING))
                        self.object_type[ore] = "iron"
                    case 2 :
                        ore = arcade.Sprite( getcwd() + "image\\copper.png", (SPRITE_SCALING))
                        self.object_type[ore] = "copper"
                    case 3 :
                        ore = arcade.Sprite( getcwd() + "image\\silicium.png", (SPRITE_SCALING))
                        self.object_type[ore] = "silicium"
                ore.center_x, ore.center_y = self.spawn_pos()
                self.consumable_sprite_list.append(ore)


    def spawn_pos(self, mini = 400, maxi = 1100):
        distance = uniform(mini, maxi)

        # Générer un angle aléatoire entre 0 et 2 * pi
        angle = uniform(0, 2 * math.pi)

        # Calculer les coordonnées en utilisant la distance et l'angle
        x = distance * math.cos(angle)
        y = distance * math.sin(angle)

        return x, y



    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        # Modifier le facteur de zoom de la caméra
        if scroll_y > 0 and self.camera_scale > MIN_ZOOM:
            self.camera_scale -= ZOOM_INCREMENT
        elif scroll_y < 0 and self.camera_scale < MAX_ZOOM:
            self.camera_scale += ZOOM_INCREMENT
        
        # Appliquer le facteur de zoom à la caméra
        self.camera_sprites.scale = self.camera_scale



    def on_draw(self):
        """ Render the screen. """
        t1 = time.time_ns()

        # This command has to happen before we start drawing
        self.clear()

        # Select the camera we'll use to draw all our sprites
        self.camera_sprites.use()

        self.fourmiliere.draw()

        # Draw all the sprites.
        self.consumable_sprite_list.draw()
        self.ant_list.draw()
        self.corpse_list.draw()


        for it, task in self.all_task_list :
            arcade.draw_text(task.print_it, task.sprite.center_x - 5, task.sprite.center_y - 5, arcade.color.BLACK, 15)

        # Select the (unscrolled) camera for our GUI
        self.camera_gui.use()

        # Draw the GUI
        arcade.draw_rectangle_filled(self.width // 2,
                                     20,
                                     self.width,
                                     40,
                                     arcade.color.ALMOND)
        text = f"it : {self.iteration}, ant nb : {self.ant_number}, out_food : {self.out_food}, nest_food : {self.nest_food}\ngen : {self.gen}, " \
            + f"iron : {self.iron}, copper : {self.copper}, silicium : {self.silicium}"
        arcade.draw_text(text, 10, 10, arcade.color.BLACK, 15)

        arcade.draw_rectangle_filled(self.width-60,
                                     self.height//2,
                                     120,
                                     self.height,
                                     arcade.color.ALMOND)
        arcade.draw_text("fatigue :", self.width-110, self.height-20, arcade.color.BLACK, 15)
        y = 40
        for ant in self.ant_obj_list :
            arcade.draw_text(f"{ant.id}", self.width-110, self.height-y, arcade.color.BLACK, 10)
            y += 15
            arcade.draw_text(f"{round(ant.current_fatigue, 2)}", self.width-110, self.height-y, arcade.color.BLACK, 10)
            y += 20

        t2 = time.time_ns()

        print((t2-t1)/1000000000)



    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        ...



    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        ...



    def on_update(self, delta_time):
        """ Movement and game logic """

        def check_death():
            dead_ant = None
            if self.death_soon_ant != [] :
                    new_list = []
                    for ant in self.death_soon_ant :
                        if ant.lifespan <= 0 and ant.type != "dead":
                            #dead = self.kill_ant(ant)
                            #on la déclare morte
                            ant.type = "dead"

                            #on fait les modifications de tâche
                            if ant.task != None and ant.task.type not in ("eat", "found_food", "found_corpse") :
                                if ant.task.parent in self.current_task_list and ant.task.status == "in_wait" : ant.task.parent.it += 1
                                elif ant.task.parent not in self.current_task_list and ant.task.status == "in_wait" : 
                                    self.current_task_list.append(ant.task.parent)
                                    ant.task.parent.it += 1

                            #on change son sprite
                            if math.sqrt((ant.sprite.center_x) ** 2+ (ant.sprite.center_y) ** 2) > 100 :
                                dead_ant = arcade.Sprite( getcwd() + "image\\fourmi_morte.png", (SPRITE_SCALING/8))
                                dead_ant.center_x = ant.sprite.center_x
                                dead_ant.center_y = ant.sprite.center_y
                                dead_ant.angle = ant.sprite.angle
                            ant.sprite.kill()
                            del self.ant_obj_list[self.ant_obj_list.index(ant)]
                            del ant

                            self.ant_number -= 1
                        else :
                            new_list.append(ant) if ant.type != "dead" else None

                    self.death_soon_ant = new_list[::]
            return dead_ant

        def check_hunger():
            if self.hungry_ant != [] :
                new_list = []
                for ant in self.hungry_ant :
                    if self.nest_food > 0 :
                        if ant.task != None and ant.task.type not in ("eat", "found_food", "found_corpse") :
                            if ant.task.parent in self.current_task_list and ant.task.status == "in_wait" : ant.task.parent.it += 1
                            elif ant.task.parent not in self.current_task_list and ant.task.status == "in_wait" : 
                                self.current_task_list.append(ant.task.parent)
                                ant.task.parent.it += 1
                        
                        new_task = self.create_task2(sprite = None, task_type = "eat")
                        new_task.status = "completed"
                        ant.task = new_task
                        ant.dest_list = [new_task.final]

                    else : 
                        new_list.append(ant)
                self.hungry_ant = new_list

        def check_task_spanlife():
            sub_list = []
            for task in self.all_task_list:
                if task[1].it <= 0 :
                    task.sprite.kill()
                elif task[0] +6000 > self.iteration  and task[1].it > 0 :
                    sub_list.append(task)
            self.all_task_list = sub_list[::]

        self.iteration +=1

        life_check = False
        if self.iteration%100 == 0 :
            life_check = True
            if self.iteration%4000 == 0:
                for i in range(randint(5,7)):
                    self.create_ant()
                self.gen += 1

            if self.iteration%1000 == 0 and len(self.consumable_sprite_list) < 10:
                self.create_event("food")



        self.update_ant()

        with ThreadPoolExecutor(max_workers=2) as executor:
            future_death = executor.submit(check_death)
        
        with ThreadPoolExecutor(max_workers=2) as executor:
            future_hunger = executor.submit(check_hunger)

        with ThreadPoolExecutor(max_workers=1) as executor:
            future_task_spanlife = executor.submit(check_task_spanlife)



        dead_ant = future_death.result()
        if dead_ant : 
            self.corpse_list.append(dead_ant)
        future_hunger.result()
        future_task_spanlife.result()



    def on_resize(self, width, height):
        """
        Resize window
        Handle the user grabbing the edge and resizing the window.
        """
        self.camera_sprites.resize(int(width), int(height))
        self.camera_gui.resize(int(width), int(height))


    
    def update_ant(self):
        task_ind = 0
        for ant in self.ant_obj_list :
            if ant.type == "dead" :
                continue
            ant.lifespan -= 1
            ant.hunger -= 1
            behave = self._ant_behave(ant)
            if behave == "transport" : 
                try : 
                    task = self.current_task_list[0]
                    ant.task = self.create_task2(sprite = task.sprite, coords = task.coords, final = task.final, iteration = task.it, task_type = task.type, parent = task)
                    ant.dest_list = [ant.task.coords, ant.task.final]
                except AttributeError :
                    print(self.current_task_list)
                if ant.task != None : 
                    if task.it > 1 : task.it -=1
                    else : self.current_task_list.pop(self.current_task_list.index(task))
                
                task_ind = task_ind +1 if task_ind < len(self.current_task_list) -1 else 0
            
            elif behave == "explo" and ant.dest_list == [] :
                path = self.create_path(ant, 10)
                ant.dest_list = path
            
            
            if ant.dest_list != [] :
                coords = self._move(ant, coord = (ant.sprite.center_x, ant.sprite.center_y), dest = (ant.dest_list[0]))
                ant.sprite.change_x, ant.sprite.change_y = coords[0], coords[1]
                if self.iteration%2 == 0 :
                    ant.sprite.update()
            
            
            if self.iteration%100 == 0 : 
                if ant.lifespan <= 100 and ant not in self.death_soon_ant :
                    self.death_soon_ant.append(ant)
                if ant.hunger < 1500 and ant not in self.hungry_ant :
                    if not ant.task or ant.task.type != "eat":
                        self.hungry_ant.append(ant)
                if ant.hunger <= 0 :
                    self.kill_ant(ant)


    def _ant_behave(self, ant : Ant):
        if ant.hunger < 1500 :
            return
        if self.enemy :
            pass # si l'ennemi est à portée d'elle, soit elle se bat, soit elle fuit (?), sinon elle continue sa vie
        else : 
            if ant.current_fatigue >= 100 or ant.status == "rest" :


                if ant.dest_list != [] :
                    ant.dest_memory = ant.dest_list[:]
                    ant.dest_list = []


                ant.status = "rest" #passer le status de la fourmi en repos + décrémenter sa fatigue
                ant.change_fatigue(ant.current_fatigue -0.2) 


                if ant.current_fatigue <= ant.def_fatigue : 

                    if ant.task != None and ant.task.type == "food" :
                        ant.status = "transport"

                    else : ant.status = "none"

                    ant.dest_list = ant.dest_memory[:]
                    ant.current_fatigue = ant.def_fatigue
            else : 
                ant.change_fatigue(ant.current_fatigue+0.02)

                if len(self.current_task_list)*ant.transport_will > 1 and ant.task == None :

                    ant.status = "transport"
                    return "transport" #là elle part faire du transport
                
                elif ant.task == None and (len(self.current_task_list)*ant.transport_will <= 1):
                    return "explo" #là elle fait de l'exploration
                
        return "no_new"



    def kill_ant(self, ant : Ant):
        ant.type = "dead"

        #on fait les modifications de tâche
        if ant.task != None and ant.task.type not in ("eat", "found_food", "found_corpse") :
            if ant.task.parent in self.current_task_list and ant.task.status == "in_wait" : ant.task.parent.it += 1
            elif ant.task.parent not in self.current_task_list and ant.task.status == "in_wait" : 
                self.current_task_list.append(ant.task.parent)
                ant.task.parent.it += 1

        #on change son sprite
        if math.sqrt((ant.sprite.center_x) ** 2+ (ant.sprite.center_y) ** 2) > 100 :
            dead_ant = arcade.Sprite( getcwd() + "image\\fourmi_morte.png", (SPRITE_SCALING/8))
            dead_ant.center_x = ant.sprite.center_x
            dead_ant.center_y = ant.sprite.center_y
            dead_ant.angle = ant.sprite.angle
            self.corpse_list.append(dead_ant)
        ant.sprite.kill()
        del self.ant_obj_list[self.ant_obj_list.index(ant)]
        del ant

        self.ant_number -= 1


    def create_path(self,ant : Ant, num_points : int) -> list[tuple]:
        path = []
        current_x = ant.sprite.center_x
        current_y = ant.sprite.center_y
        for _ in range(num_points):
            angle = uniform(0, 2 * math.pi)
            distance = uniform(50, 150)  # Distance entre les points
            new_x = current_x + distance * math.cos(angle)
            new_y = current_y + distance * math.sin(angle)

            path.append((new_x, new_y))
            current_x, current_y = new_x, new_y
        return path



    def _move(self, ant : Ant, coord : tuple[int], dest : tuple[int]) -> tuple[int]:

        # Where are we
        start_x = coord[0]
        start_y = coord[1]

        # Where are we going
        dest_x = dest[0]
        dest_y = dest[1]

        # X and Y diff between the two
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y

        # Calculate angle to get there
        angle = math.atan2(y_diff, x_diff)
        ant.sprite.angle = -(90- angle*180/math.pi)

        # How far are we?
        distance = math.sqrt((start_x - dest_x) ** 2 + (start_y - dest_y) ** 2)

        # How fast should we go? If we are close to our destination,
        # lower our speed so we don't overshoot.
        speed = min(ant.vit, distance)

        # Calculate vector to travel
        change_x = math.cos(angle) * speed
        change_y = math.sin(angle) * speed


        # bloc 2 

        def check_pos() :
            if ant.task != None :

                final = (int(start_x + change_x) == int(ant.task.final[0])) and \
                        (int(start_y + change_y) == int(ant.task.final[1]))
                
                if ant.task.sprite != None :

                    if (int(start_x + change_x)== int(ant.task.sprite.center_x)) and (int(start_y + change_y) == int(ant.task.sprite.center_y)) and ant.task.type not in ("eat", "found_corpse", "found_food"):
                            print(ant, ant.task, ant.task.parent)
                            if ant.task.type == "food" :
                                    self.out_food -= 1
                            if ant.task.parent.print_it > 1 : ant.task.parent.print_it -= 1
                            else : 
                                ant.task.sprite.kill()
                                ant.task.sprite = None
                                for task in self.all_task_list :
                                    if task[1] == ant.task.parent :
                                        del self.all_task_list[self.all_task_list.index(task)]
                                        ant.task.parent.status = "completed"
                                        break
                            ant.task.status = "completed"
                    
                if final and ant.task.status == "completed" :
                    self.close_task(ant, sprite = ant.task.sprite if ant.task.type in ("found_food", "found_corpse", "found_iron", "found_copper", "found_silicium") else None)


            if (int(start_x + change_x)== int(dest_x)) and (int(start_y + change_y) == int(dest_y)) and ant.dest_list != []:
                ant.dest_list.pop(0)

        with ThreadPoolExecutor(max_workers=1) as executor:
            future_pos = executor.submit(check_pos)


        #bloc 3 

        def check_object():
            if ant.task == None : 
                for sprite in self.consumable_sprite_list :
                    if abs(ant.sprite.center_x - sprite.center_x) < OBJECT_DETECTION and abs(ant.sprite.center_y - sprite.center_y) < OBJECT_DETECTION :
                        distance = arcade.get_distance_between_sprites(ant.sprite, sprite)
                        if distance < OBJECT_DETECTION:
                            ant.task = self.create_task2(sprite = sprite, task_type = "found_" + self.object_type[sprite])
                            ant.task.status = "completed"
                            ant.dest_list = [ant.task.final]


        def check_corpse():
            if ant.task == None : 
                for corpse in self.corpse_list :
                    if abs(ant.sprite.center_x - corpse.center_x) < CORPS_DETECTION and abs(ant.sprite.center_y - corpse.center_y) < CORPS_DETECTION :
                        distance = arcade.get_distance_between_sprites(ant.sprite, corpse)
                        if distance < CORPS_DETECTION:
                            ant.task = self.create_task2(sprite = corpse, task_type = "found_corpse")
                            ant.task.status = "completed"
                            ant.dest_list = [ant.task.final]
        
        if ant.task == None :

            if self.iteration%2 == 0 :
                with ThreadPoolExecutor(max_workers=2) as executor:
                    future_food = executor.submit(check_object)

                    future_food.result()

            if self.iteration%2 != 0 :
                with ThreadPoolExecutor(max_workers=2) as executor:
                    future_corpse = executor.submit(check_corpse)

                    future_corpse.result()

            if ant.dest_list == [] :
                ant.dest_list = self.create_path(ant, 10)
        
        future_pos.result()


        return (change_x, change_y)
    


    def on_mouse_press(self, x, y, button, modifiers):
        # Démarrer le déplacement de la caméra au clic gauche
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.camera_moving = True
            self.camera_start_x = x
            self.camera_start_y = y



    def on_mouse_release(self, x, y, button, modifiers):
        # Arrêter le déplacement de la caméra au relâchement du clic gauche
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.camera_moving = False



    def on_mouse_motion(self, x, y, dx, dy):
        # Déplacer la caméra si le clic gauche est maintenu
        if self.camera_moving:
            move_x = (self.camera_start_x - x) * self.camera_scale
            move_y = (self.camera_start_y - y) * self.camera_scale

            # Mettre à jour la position de la caméra
            self.camera_pos_x += move_x
            self.camera_pos_y += move_y

            # Appliquer le déplacement à la caméra
            self.camera_sprites.move_to((self.camera_pos_x, self.camera_pos_y))

            # Mettre à jour les positions de départ de la souris
            self.camera_start_x = x
            self.camera_start_y = y



def main():
    """ Main function """
    window = MyGame(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":    
    main()