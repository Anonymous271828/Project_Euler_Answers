import pygame
pygame.font.init()


class Buttons():
    def __init__(self, x, y, width, height, text, colour, img_name):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.colour = colour
        self.rect = (self.x, self.y, self.width, self.height)
        if img_name == "Nothing":
            self.image = (self.x, self.y, self.width, self.height)
        else:
            self.image = pygame.image.load("img/{}".format(img_name)).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def draw(self, win):
        if type(self.image) == tuple:
            pygame.draw.rect(win, (self.colour), self.rect)
            font = pygame.font.SysFont("comicsans", 20)
            r = 255 - self.colour[0]
            g = 255 - self.colour[1]
            b = 255 - self.colour[2]
            text = font.render(self.text, 1, (r, g, b))
            win.blit(text, (self.x + self.width / 2 - text.get_width() / 2, self.y + 10))
        else:
            win.blit(self.image, (self.x, self.y))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True

    def tooltip(self, win):
        pygame.draw.rect(win, self.colour, self.rect)
        font = pygame.font.SysFont("comicsans", 20)
        r = 255 - self.colour[0]
        g = 255 - self.colour[1]
        b = 255 - self.colour[2]
        text = font.render(self.text, 1, (r, g, b))
        win.blit(text, (self.x + self.width/2 - text.get_width()/2, self.y + 10))



class Tiles(pygame.sprite.Sprite):
    def __init__(self, x, y, terrain, id):
        super().__init__()
        self.x = x
        self.y = y
        self.terrain = terrain
        self.id = id
        self.width = 32
        self.height = 32
        self.image = pygame.Surface([self.width, self.height])
        if terrain == "River":
            self.colour = (43, 191, 166)
        elif terrain == "Mountain":
            self.colour = (65, 191, 66)
        elif terrain == "Lake":
            self.colour = (43, 191, 200)
        else:
            self.colour = (0, 255, 0)
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.x, self.y

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + 32 and self.y <= y1 <= self.y + 32:
            return True

    def update(self, win, unit_group, tile_group):
        self.rect.center = self.x, self.y

class Units(pygame.sprite.Sprite):
    def __init__(self, x, y, id, health, damage, air_damage, speed, img_name, selected, team, experience):
        super().__init__()
        self.x = x
        self.y = y
        self.id = id
        self.health = health
        self.damage = damage
        self.air_damage = air_damage
        self.speed = speed
        self.original_speed = speed
        self.team = team
        self.experience = experience
        self.name = img_name
        self.image = pygame.image.load("img/{}".format(img_name)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))
        if team == "Axis" or self.name == "Allied_medium_tank.png" or self.name == "Allied_heavy_tank.png" or self.name == "Allied_fighter.png":
            self.image = pygame.transform.flip(self.image, True, False)
        if self.name  == "Allied_construction_worker.png" or self.name == "Axis_construction_worker.png":
            self.space = 2
        elif self.name == "Allied_advanced_construction_worker.png" or self.name == "Axis_advanced_construction_worker.png":
            self.space = 4
        elif self.name == "Allied_construction_truck.png" or self.name == "Axis_construction_truck.png":
            self.space = 20
        else:
            self.space = 0
        self.full = False
        self.autocollect = False
        self.width = 32
        self.height = 32
        #self.original_colours = []
        #pixel_array = pygame.PixelArray(self.image)
        #for x in range(self.width):
            #for y in range(self.height):
                #colour_for_hue = self.image.unmap_rgb(pixel_array[x][y])
                #colour_for_hue = pygame.Color(*colour_for_hue)
                #h, s, l, a = colour_for_hue.hsla
                #self.original_colours.append((h, s, l, a))
        self.selected = selected

        #print(self.original_colours)
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y
    def click(self, win, m_pos):
        x1 = m_pos[0]
        y1 = m_pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            if self.selected == True:
                self.selected = False
            else:
                self.selected = True
            #pixel_array = pygame.PixelArray(self.image)
            #for x in range(self.width):
                #for y in range(self.height):
                    #colour_for_hue = self.image.unmap_rgb(pixel_array[x][y])
                    #colour_for_hue = pygame.Color(*colour_for_hue)
                    #h, s, l, a = colour_for_hue.hsla
                    #print(round(h), round(s), round(l), a)
                    #if round(h) == 63 and round(s) == 100 and round(l) == 69:
                        #for h, s, l, a in self.original_colours:
                            #print(2, h, s, l, a)
                            #colour_for_hue.hsla = (int(h), int(s), int(s), int(a))
                    #else:
                        #colour_for_hue.hsla = (63, 100, 69, int(a))
                    #pixel_array[x][y] = colour_for_hue
            #del pixel_array
    def update(self, win, unit_group, tile_group):
        self.rect.topleft = self.x, self.y
        collisions = pygame.sprite.groupcollide(unit_group, tile_group, False, False)
        if self.selected == True:
            pygame.draw.rect(win, (0, 0, 0), (self.x, self.y, self.width, self.height), 1)
        #for coll in list(collisions):
            #coll.x = collisions[coll][0].x
            #coll.y = collisions[coll][0].y

class Buildings(pygame.sprite.Sprite):
    def __init__(self, x, y, id, image, buffs, health, experience, damage, cost, turn, time, team):
        super().__init__()
        self.x = x
        self.y = y
        self.id = id
        self.name = image
        self.image = pygame.image.load("img/{}".format(self.name)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.buffs = buffs
        self.health = health
        self.speed = "Cannot move."
        self.experience = experience
        self.damage = damage
        self.selected = False
        self.cost = cost
        self.turn = turn
        self.time = time
        self.team = team

    def build(self, industry_tokens, run, turn, unit_group, working_units):
        #for item in other_objects:
            #obj_x = item[0]
            #obj_y = item[1]
            #if self.x == obj_x or self.x == obj_y:
                #print("You cannot do that.")
                #break
        #else:
        if run == True:
            if turn - self.turn >= self.time:
                for item in working_units:
                    if item.x == self.x + 32 or item.x == self.x - 32:
                        if item.y == self.y:
                            unit_group.add(item)
                            working_units.pop(working_units.index(item))
                completed_buildings = Buildings(self.x, self.y, self.id, self.name, self.buffs, self.health, self.experience, self.damage, self.cost, self.turn, self.time, self.team)
                return completed_buildings, unit_group, working_units
            #elif turn - self.turn == 0:
                #unit_group.remove(worker)
                #working_units.append(worker)
                #industry_tokens = industry_tokens - self.cost
                #not_completed_buildings = Buildings(self.x, self.y, self.image, self.buffs, self.health, self.cost, self.turn, self.time)
                #return industry_tokens, not_completed_buildings, unit_group, working_units
        return "No new building", unit_group, working_units

    def click(self, win, m_pos):
        x1 = m_pos[0]
        y1 = m_pos[1]
        if self.x <= x1 <= self.x + 32 and self.y <= y1 <= self.y + 32:
            if self.selected == True:
                self.selected = False
            else:
                self.selected = True

    def update(self, win, unit_group, tile_group):
        self.rect.topleft = (self.x, self.y)