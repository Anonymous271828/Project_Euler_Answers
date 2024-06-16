import pygame
import random
import time
import sys
import threading
from queue import Queue

# All images are courtesy of artists on Open Game Art, with Carlos Alface; Spaceships-13.zip file, jlunesc; sprite_ship3.png file, clear_code; extra, green, yellow, and red png files, ZomBCool for the boss.png files and lastly Tiao Ferrira for bubble_explo1 to 10 png files.

pygame.font.init()
pygame.mixer.init()
win = pygame.display.set_mode((900, 700))


# Basic player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, vel, shots, health, kills, image, damage, proj_area, armour):
        super().__init__()
        self.x = x
        self.y = y
        self.vel = vel
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y
        self.shots = shots
        self.health = health
        self.armour = armour
        self.kills = kills
        self.damage = damage
        self.proj = proj_area

    def update(self, projectile_group, enemy_group, player):
        #global projectile_group
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            if self.y > self.vel:
                self.y = self.y - self.vel
        if keys[pygame.K_a]:
            if self.x > self.vel:
                self.x = self.x - self.vel
        if keys[pygame.K_s]:
            if self.y + self.vel < 700:
                self.y = self.y + self.vel
        if keys[pygame.K_d]:
            if self.x + self.vel < 800:
                self.x = self.x + self.vel
        if keys[pygame.K_SPACE] and self.shots > 0:
            #pygame.time.delay(50)
            proj = Projectile(self.x, self.y - 20, 20, (255, 255, 0), self.damage, self.proj, False)
            projectile_group.add(proj)
            self.shots = self.shots - 1

        self.rect.center = self.x, self.y
        if pygame.sprite.spritecollide(player,enemy_group, False):
            pop = [True, False]
            weights = [player.armour, 1 - player.armour]
            if random.choices(pop, weights):
                self.health = 0
        pygame.draw.rect(win, (128, 128, 128), (self.x - 24, self.y + 50, 50, 30))
        pygame.draw.rect(win, (0, 128, 0), (self.x - 24, self.y + 50, min(50, self.health / 500 * 50), 30))



class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, vel, colour, damage, area, tracker):
        super().__init__()
        self.x = x
        self.y = y
        self.vel = vel
        self.colour = colour
        self.damage = damage
        self.area = area
        self.tracker = tracker
        self.image = pygame.Surface([5 + 2.5 * self.area, 10])
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        #print(self.rect)

    def update(self, projectile_group, enemy_group, boss_group, player):
        if self.tracker == False:
            self.y = self.y - self.vel
        else:
            if self.x < player.x:
                self.x = self.x - self.vel / 4
            if self.x > player.x:
                self.x = self.x + self.vel / 4
            self.y = self.y - self.vel
            #if self.y > player.y:
                #self.y = self.y + self.vel
        self.rect.center = self.x, self.y
        collision = pygame.sprite.groupcollide(projectile_group, enemy_group, True, False)
        collisions = list(collision.values())
        for item in collisions:
            for item2 in item:
                item2.health = item2.health - self.damage
        collision = pygame.sprite.groupcollide(projectile_group, boss_group, True, False)
        collisions = list(collision.values())
        #print(collisions)
        for item in collisions:
            for item2 in item:
                item2.health = item2.health - self.damage
                #print(item2.health)
        #print(pygame.sprite.spritecollide(player, projectile_group, True))
        if pygame.sprite.spritecollide(player, projectile_group, True):
            pop = [True, False]
            weights = [player.armour, 1 - player.armour]
            if random.choices(pop, weights):
                player.health = player.health - self.damage

class Enemies(pygame.sprite.Sprite):
    def __init__(self, x, y, vel, health, image, damage, tracker):
        super().__init__()
        self.x = x
        self.y = y
        self.vel = vel
        self.health = health
        if image == "Red":
            self.image = pygame.image.load("red.png")
        elif image == "Green":
            self.image = pygame.image.load("green.png")
        elif image == "Yellow":
            self.image = pygame.image.load("yellow.png")
        elif image == "Extra":
            self.image = pygame.image.load("extra.png")
        else:
            pass
        self.damage = damage
        self.tracker = tracker
        self.rect = self.image.get_rect()
    def update(self, events, bullet_event, projectile_group):
        self.y = self.y + 1
        self.rect.center = self.x, self.y
        #events = pygame.event.get()
        for event in events:
            if event.type == bullet_event:
                proj = Projectile(self.x, self.y + 20, -20, (255, 0, 0), self.damage, 0, self.tracker)
                projectile_group.add(proj)
        pygame.draw.rect(win, (128, 128, 128), (self.x - 14, self.y - 50, 30, 10))
        pygame.draw.rect(win, (0, 128, 0), (self.x - 14, self.y - 50, min(30, self.health / 50 * 30), 10))

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, vel, damage, health):
        super().__init__()
        self.x = x
        self.y = y
        self.vel = vel
        self.image = pygame.image.load("Boss.png")
        self.damage = damage
        self.health = health
        self.rect = self.image.get_rect()
        self.width = self.rect[2]
        self.height = self.rect[3]
    def update(self, events, attack_event, asteroid_group, player, projectile_group):
        global direction
        if self.x > 800:
            direction = "Backwards"
        elif self.x < 0:
            direction = "Forwards"
        else:
            direction = direction
        #print(direction)
        if direction == "Forwards":
            self.x = self.x + self.vel
        elif direction == "Backwards":
            self.x = self.x - self.vel
        else:
            pass

        self.rect.center = self.x, self.y
        attack = "No attack"
        #for event in events:
            #if event.type == boss_event:
                #attacks = ["Laser", "Trackers", "Ramming", "Asteroid"]
                #attack = random.choice(attacks)
                #t = threading.Thread(target=warning_signs, args=(self.x + 24, self.y))
                #t.start()
        for event in events:
            if event.type == attack_event:
                attacks = ["Laser", "Trackers", "Ramming", "Asteroid"]
                attack = random.choice(attacks)
                if attack == "Laser":
                    pygame.draw.rect(win, (0, 0, 150), (self.x, self.y, 50, 800))
                    if self.x <= player.x <= self.x + self.width:
                        player.health = player.health - 120
                elif attack == "Trackers":
                    #print("Trackers")
                    for num in range(30):
                        proj = Projectile(self.x, self.y + 50, -20, (255, 0, 0), self.damage, 30, True)
                        projectile_group.add(proj)
                elif attack == "Asteroid":
                    # asteroid_y = random.randint(200, 600)
                    aster = Asteroid(900, player.y, 10)
                    asteroid_group.add(aster)
                else:
                    pass
        pygame.draw.rect(win, (128, 128, 128), (self.x - 24, self.y + 50, 50, 30))
        pygame.draw.rect(win, (0, 128, 0), (self.x - 24, self.y + 50, min(50, self.health / 10000 * 50), 30))

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x ,y, vel):
        super().__init__()
        self.x = x
        self.y = y
        self.vel = vel
        self.image = pygame.image.load("Asteroid.png")
        self.rect = self.image.get_rect()
    def update(self, player, asteroid_group):
        self.x = self.x - self.vel
        self.rect.center = self.x, self.y
        if pygame.sprite.spritecollide(player, asteroid_group, False):
            player.health = 0

class Button():
    def __init__(self, x, y, width, height, text, font):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font
        self.rect = (self.x, self.y, self.width, self.height)
    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 255), self.rect)
        font = pygame.font.SysFont("comicsans", self.font)
        text = font.render(self.text, 1, (0, 0, 0))
        win.blit(text, (round((self.x * 2 + self.width - text.get_width())/2), self.y))
    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False




def threading_for_enemies(levels, enemy_group, boss_group, in_q):
    levels = [levels]
    levels = levels[0]
    while True:
        data = in_q.get()
        if data != "Paused":
            pop = ["Red", "Green", "Yellow", "Extra"]
            weights = [(((1 - 0.1 * levels[0]) - (1 - 0.1 * levels[0]) * 0.2) - (1 - 0.1 * levels[0] - (1 - 0.1 * levels[0]) * 0.2) * 0.3), (1 - 0.1 * levels[0] - (1 - 0.1 * levels[0]) * 0.2) * 0.3, (1 - 0.1 * levels[0]) * 0.2, 0.1 * levels[0]]
            c = random.choices(pop, weights)
            c = c[0]
            if levels[0] <= 5:
                if c == "Red":
                    enemy = Enemies(random.randint(0, 800), 0, 10, 60, "Red", 3, False)
                elif c == "Green":
                    enemy = Enemies(random.randint(0, 800), 0, 20, 150, "Green", 5, False)
                elif c == "Yellow":
                    enemy = Enemies(random.randint(0, 800), 0, 30, 210, "Yellow", 10, False)
                else:
                    enemy = Enemies(random.randint(0, 800), 0, 50, 300, "Extra", 15, False)
                enemy_group.add(enemy)
                #print("gr")
            elif levels[0] % 10 == 0:
                if len(boss_group.sprites()) < 1:
                    boss = Boss(0, 0, 10, 120, 10000)
                    boss_group.add(boss)
                else:
                    pass
            else:
                if c == "Red":
                    enemy = Enemies(random.randint(0, 800), 0, 10, 60, "Red", 3, True)
                elif c == "Green":
                    enemy = Enemies(random.randint(0, 800), 0, 20, 150, "Green", 5, True)
                elif c == "Yellow":
                    enemy = Enemies(random.randint(0, 800), 0, 30, 210, "Yellow", 10, True)
                else:
                    enemy = Enemies(random.randint(0, 800), 0, 50, 300, "Extra", 15, True)
                time.sleep(10 / (levels[0] - 5))
                enemy_group.add(enemy)
            time.sleep(1/levels[0])
        else:
            pass

#class Stopwatch(threading.Thread):
    #def __init__(self, event, boss_group, player, projectile_group, asteroid_group):
        #threading.Thread.__init__(self)
        #self.stop = event
        #self.boss = boss_group
        #self.player = player
        #self.projectile = projectile_group
        #self.asteroid = asteroid_group
    #def run(self):
        #if self.boss == 0 and self.player == 0 and self.projectile == 0 and self.asteroid == 0:
            #pass
        #else:
            #while not self.stop.wait(5):
                #boss_attacks(self.boss, self.player, self.projectile, self.asteroid)


def warning_signs(x, y):
    warning_counter = 0
    while True:
        if warning_counter == 6:
            break
        if warning_counter % 2 != 0:
            warn = pygame.image.load("Warning.png")
            win.blit(warn, (x, y))
            pygame.display.update()
            time.sleep(5)
        warning_counter = warning_counter + 1
        #print(warning_counter)

def skip():
    pass


#def boss_attacks(boss_group, player, projectile_group, asteroid_group):
    #threading.Timer(5, boss_attacks, args=(boss_group, player, projectile_group, asteroid_group)).start()
    #original_time = time.perf_counter()
    #for boss in boss_group:
        #boss.attack(original_time - 5, asteroid_group, player, projectile_group)

def redraw_window(win, player, bg, kills, levels, music):
    win.fill((255, 255, 255))
    bg = pygame.transform.scale(bg, (800, 700))
    win.blit(bg, (0, 0))
    pygame.draw.rect(win, (128, 128, 128), (800, 400, 100, 80))
    pygame.draw.rect(win, (128, 128, 128), (800, 50, 100, 80))
    pygame.draw.rect(win, (128, 128, 128), (800, 200, 100, 150))
    font = pygame.font.SysFont("comicsans", 20)
    text = font.render("Bullets;", 1, (0,0,0))
    win.blit(text, (800, 400))
    text = font.render(str(player.shots), 1, (0,0,0))
    win.blit(text, (800, 450))
    text = font.render("Level;", 1, (0,0,0))
    win.blit(text, (800, 50))
    text = font.render(str(levels), 1, (0, 0, 0))
    win.blit(text, (800, 100))
    text = font.render("Amount of", 1, (0, 0, 0))
    win.blit(text, (800, 200))
    text = font.render("kills", 1, (0, 0, 0))
    win.blit(text, (800, 225))
    text = font.render("needed to", 1, (0, 0, 0))
    win.blit(text, (800, 250))
    text = font.render("level up", 1, (0, 0, 0))
    win.blit(text, (800, 275))
    text = font.render(str(round((levels[0] * 10) ** 1.5 / 3.1) - kills), 1, (0, 0, 0))
    win.blit(text, (800, 325))
    pause = pygame.image.load("Settings.png")
    win.blit(pause, (800, 500))
    if music == True:
        music_button = pygame.image.load("Music.png")
        win.blit(music_button, (800, 600))
    else:
        music_button = pygame.image.load("No_Music.png")
        win.blit(music_button, (800, 600))

def paused(pause_text, levels, btns_when_exiting, out_q):
    pygame.draw.rect(win, (128, 128, 128), (150, 10, 500, 650))
    font = pygame.font.SysFont("comicsans", 50)
    text = font.render(pause_text[0], 1, (255, 0, 0))
    win.blit(text, ((800 - text.get_width()) / 2, 10))
    text = font.render(pause_text[1], 1, (255, 0, 0))
    win.blit(text, ((800 - text.get_width()) / 2, 110))
    text = font.render(pause_text[2], 1, (255, 0, 0))
    win.blit(text, ((800 - text.get_width()) / 2, 210))
    with out_q.mutex:
        out_q.queue.clear()
    for btn in btns_when_exiting:
        btn.draw(win)
    pygame.display.update()
    con = True
    while con:
        out_q.put("Paused")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns_when_exiting:
                    if btn.click(pos) and btn.text == "Quit to main menu.":
                        coins = (levels[0] - 1) * random.randint(30, 50)
                        return True, coins
                    elif btn.click(pos) and btn.text == "Quit":
                        pygame.quit()
                        sys.exit()
                    elif btn.click(pos) and btn.text == pause_text[3]:
                        coins = (levels[0] - 1) * random.randint(30, 50)
                        out_q.put("No longer paused.")
                        return False, coins
                    else:
                        pass


def explosion(player, file_name):
    #print(file_name)
    bubble_explosion = pygame.image.load(file_name)
    win.blit(bubble_explosion, (player.x, player.y))
    pygame.time.delay(500)

def purchase_procedure(btn, pos, coins, font, ship, ship_status, ships_list, x, y, what_ship):
    if btn.click(pos) and btn.x == x and btn.y == y:
        if btn.text == "Buy.":
            if coins < 300:
                text = font.render("You cannot afford to purchase that", 1, (255, 0, 0))
                win.blit(text, (200, 200))
                pygame.display.update()
                pygame.time.delay(1000)
            else:
                coins = coins - 300
                ship_status[what_ship] = True
        else:
            ship = ships_list[what_ship - 1]
    else:
        pass
    return ship, ship_status, coins



#thread.start()


def main(image):
    # This is only necessary to bypass error messages that may occur if we cancel a thread that doesn't exist on the first iteration of the while loop.
    #thread = threading.Thread(target=skip)
    #thread.start()
    #stopwatch = Stopwatch(threading.Thread, 0, 0, 0, 0)
    #stopwatch.start()
    coins = 0
    coins_generated = 0
    q = Queue()
    while True:
        global direction
        stat_points = [0, 0, 0, 0, 0]
        stat_upgrades = 0
        player = Player(352, 500, 10, 800, 1000, 0, image, 10, 0, 0)
        player_group = pygame.sprite.Group()
        player_group.add(player)

        # Will be used as a global variable for the Player and Enemy classes
        projectile_group = pygame.sprite.Group()

        asteroid_group = pygame.sprite.Group()
        enemy_group = pygame.sprite.Group()
        boss_group = pygame.sprite.Group()
        clock = pygame.time.Clock()
        bg = pygame.image.load("background.png")
        bg_music = pygame.mixer.music.load("Space.wav")
        pygame.mixer.music.play(-1)
        bullet_delay = 500
        bullet_event = pygame.USEREVENT + 1
        pygame.time.set_timer(bullet_event, bullet_delay)
        #bullet_delay = 5000
        #boss_event = pygame.USEREVENT + 2
        #pygame.time.set_timer(boss_event, bullet_delay)
        bullet_delay = 1000
        attack_event = pygame.USEREVENT + 2
        pygame.time.set_timer(attack_event, bullet_delay)
        # Only globally located in the redraw_window() function.
        levels = [1]
        thread_counter = 0
        coins = coins + coins_generated
        direction = "Forwards"
        music = True
        btns_when_exiting = [Button(200, 320, 400, 100, "Play again.", 50), Button(200, 430, 400, 100, "Quit", 50),
                Button(180, 540, 440, 100, "Quit to main menu.", 50)]
        while True:
            clock.tick(60)
            if thread_counter == 0:
                #q = Queue()
                thread = threading.Thread(target=threading_for_enemies, args=(levels, enemy_group, boss_group, q))
                thread.start()
                thread_counter = thread_counter + 1
            redraw_window(win, player, bg, player.kills, levels, music)
            q.put("ujgreugjrtiuog")
            if music == True:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.pause()
            for spr in enemy_group:
                if spr.health <= 0:
                    enemy_group.remove(spr)
                    player.kills = player.kills + 1
                elif spr.y >= 800:
                    enemy_group.remove(spr)
                    player.kills = player.kills - 1
                else:
                    pass
            for spr in projectile_group:
                if spr.y >= 800 or spr.y <= 0:
                    projectile_group.remove(spr)
            player_group.draw(win)
            player_group.update(projectile_group, enemy_group, player)
            enemy_group.draw(win)
            events = pygame.event.get()
            enemy_group.update(events,bullet_event, projectile_group)
            boss_group.draw(win)
            boss_group.update(events, attack_event, asteroid_group, player, projectile_group)
            asteroid_group.draw(win)
            asteroid_group.update(player, asteroid_group)
            projectile_group.draw(win)
            projectile_group.update(projectile_group, enemy_group, boss_group, player)
            for spr in boss_group:
                if spr.health <= 0:
                    for num in range(1,11):
                        bubble_explosion = pygame.image.load("bubble_explo{}.png".format(str(num)))
                        bubble_explosion = pygame.transform.scale(bubble_explosion, (320, 320))
                        win.blit(bubble_explosion, (spr.x - 100, spr.y - 100))
                        pygame.display.update()
                        pygame.time.delay(50)
                    boss_group.remove(spr)
                    player.kills = round((levels[0] * 10) ** 1.5 / 3.1)

            if player.health <= 0:
                for num in range(1,11):
                    #print(num)
                    bubble_explosion = pygame.image.load("bubble_explo{}.png".format(str(num)))
                    bubble_explosion = pygame.transform.scale(bubble_explosion, (320, 320))
                    win.blit(bubble_explosion, (player.x - 100, player.y - 100))
                    pygame.display.update()
                    pygame.time.delay(50)
                q.put("Paused")
                pause_text = ["GAME OVER.", "YOU GOT TO LEVEL", str(levels), "Play again."]
                prog, coins_generated = paused(pause_text, levels, btns_when_exiting, q)
                if prog == True:
                    return coins + coins_generated
                else:
                    break
            if player.kills >= round((levels[0] * 10) ** 1.5 / 3.1):
                stat_upgrades = stat_upgrades + 1
                #player.health = 100 + stat_points[0] * 10
                #player.armour = stat_points[1] * 5
                #player.damage = player.damage + stat_points[2] * 10
                #player.shots = 800 + stat_points[3] * 50
                #levels[0] = levels[0] + 1
                #thread_counter = 0
                #kills = 0
                run_for_stats = True
                while run_for_stats:
                    btns_for_stats = [Button(700, 0, 190, 90, "Health", 20), Button(700, 140, 190, 90, "Armour", 20), Button(700, 280, 190, 90, "Damage", 20), Button(700, 420, 190, 90, "Projectile Area", 20), Button(700, 560, 190, 90, "Ammunition", 20), Button(450 - 95, 660, 190, 40, "Skip", 10)]
                    bg = pygame.transform.scale(bg, (900, 700))
                    win.blit(bg, (0,0))
                    for btn in btns_for_stats:
                        btn.draw(win)
                    for num in range(0, 25):
                        if num <= 4:
                            if num < stat_points[0]:
                                pygame.draw.rect(win, (0, 255, 0), (num * 140, 0, 132, 90))
                            else:
                                pygame.draw.rect(win, (128, 128, 128), (num * 140, 0, 132, 90))
                        elif 4 < num <= 9:
                            if (num - 5) < stat_points[1]:
                                pygame.draw.rect(win, (0, 255, 0), ((num - 5) * 140, 140, 132, 90))
                            else:
                                pygame.draw.rect(win, (128, 128, 128), ((num - 5) * 140, 140, 130, 90))
                        elif 9 < num <= 14:
                            if (num - 10) < stat_points[2]:
                                pygame.draw.rect(win, (0, 255, 0), ((num - 10) * 140, 280, 132, 90))
                            else:
                                pygame.draw.rect(win, (128, 128, 128), ((num - 10) * 140, 280, 130, 90))
                        elif 14 < num <= 19:
                            if (num - 15) < stat_points[3]:
                                pygame.draw.rect(win, (0, 255, 0), ((num - 15) * 140, 420, 132, 90))
                            else:
                                pygame.draw.rect(win, (128, 128, 128), ((num - 15) * 140, 420, 130, 90))
                        elif 19 < num <= 24:
                            if (num - 20) < stat_points[4]:
                                pygame.draw.rect(win, (0, 255, 0), ((num - 20) * 140, 560, 132, 90))
                            else:
                                pygame.draw.rect(win, (128, 128, 128), ((num - 20) * 140, 560, 130, 90))
                        else:
                            pass

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            #print('tg')
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            pos = pygame.mouse.get_pos()
                            for btn in btns_for_stats:
                                if btn.click(pos) and btn.text == "Health" and stat_points[0] <= 5 and stat_upgrades <= 1:
                                    #print("irugh")
                                    stat_points[0] = stat_points[0] + 1
                                    stat_upgrades = stat_upgrades - 1
                                elif btn.click(pos) and btn.text == "Armour" and stat_points[1] <= 5:
                                    stat_points[1] = stat_points[1] + 1
                                    stat_upgrades = stat_upgrades - 1
                                elif btn.click(pos) and btn.text == "Damage" and stat_points[2] <= 5:
                                    stat_points[2] = stat_points[2] + 1
                                    stat_upgrades = stat_upgrades - 1
                                elif btn.click(pos) and btn.text == "Projectile Area" and stat_points[3] <= 5:
                                    stat_points[3] = stat_points[3] + 1
                                    stat_upgrades = stat_upgrades - 1
                                elif btn.click(pos) and btn.text == "Ammunition" and stat_points[4] <= 5:
                                    stat_points[4] = stat_points[4] + 1
                                    stat_upgrades = stat_upgrades - 1
                                elif btn.click(pos) and btn.text == "Ammunition" and stat_points[4] <= 5:
                                    stat_points[4] = stat_points[4] + 1
                                    stat_upgrades = stat_upgrades - 1
                                elif btn.click(pos) and btn.text == "Skip":
                                    #print("bnrihtg")
                                    run_for_stats = False
                                else:
                                    pass


                    pygame.display.update()
                    if stat_upgrades == 0:
                        run_for_stats = False
                player.stats = stat_points
                player.health = 500 + stat_points[0] * 100
                player.armour = stat_points[1] * 8
                player.damage = player.damage + stat_points[2] * 10
                player.shots = 800 + stat_points[4] * 50
                player.proj = stat_points[3]
                levels[0] = levels[0] + 1
                thread_counter = 0
                kills = 0
                if levels[0] % 10 == 0:
                    pygame.mixer.music.load("Boss_music.wav")
                    pygame.mixer.music.play(-1)
                elif (levels[0] - 1) % 10 == 0:
                    pygame.mixer.music.load("Space.wav")
                    pygame.mixer.music.play(-1)
                else:
                    pass

                for spr in enemy_group:
                    enemy_group.remove(spr)
            pygame.display.update()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #print("bgt3")
                    pos = pygame.mouse.get_pos()
                    #print(pos)
                    if 800 <= pos[0] <= 848 and 500 <= pos[1] <= 548:
                        btns_when_exiting = [Button(200, 320, 400, 100, "Continue", 50),
                                             Button(200, 430, 400, 100, "Quit", 50),
                                             Button(180, 540, 440, 100, "Quit to main menu.", 50)]
                        q.put("Paused")
                        pause_text = ["PAUSED", " ", " ", "Continue"]
                        prog, coins_generated = paused(pause_text, levels, btns_when_exiting, q)
                        if prog == True:
                            return coins + coins_generated
                        else:
                            btns_when_exiting = [Button(200, 320, 400, 100, "Play again.", 50),
                                                 Button(200, 430, 400, 100, "Quit", 50),
                                                 Button(180, 540, 440, 100, "Quit to main menu.", 50)]
                            break
                    elif 800 <= pos[0] <= 848 and 600 <= pos[1] <= 648:
                        if music == True:
                            music = False
                        else:
                            music = True
                else:
                    pass


def main_menu():
    run = True
    coins = 500
    ship = "ship1.png"
    # True represents that the ship is owned.
    ship_status = {1:False, 2:False, 3:False, 4:False, 5:False, 6:False, 7:False, 8:True}
    ships_list = ["a-01.png", "b-03.png", "c-01.png", "e-02.png", "h-02.png", "j-03.png", "sprite_ship_3.png", "ship1.png"]
    btns = [Button(250, 320, 400, 100, "Play", 50), Button(250, 430, 400, 100, "Shop", 50),
                Button(250, 540, 400, 100, "Quit", 50)]
    btns_in_shop = [Button(0, 600, 240, 100, "Go back", 50)]
    bg = pygame.image.load("background.png")
    logo = pygame.image.load("Logo1.png")
    pygame.transform.scale(bg, (900, 700))
    while run:
        win.blit(bg, (0,0))
        win.blit(logo, (120, 30))
        for btn in btns:
            btn.draw(win)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and btn.text == "Play":
                        pygame.time.delay(500)
                        new_coins = main(ship)
                        coins = coins + new_coins
                        break
                    elif btn.click(pos) and btn.text == "Shop":
                        run_for_shop = True
                        while run_for_shop:
                            win.blit(bg, (0,0))
                            font = pygame.font.SysFont("comicsans", 50)
                            text = font.render("Coins; {}".format(coins), 1, (255, 0, 0))
                            win.blit(text, (10, 10))
                            #for btn in btns_in_shop:
                                #btn.draw(win)
                            btns_in_shop[0].draw(win)
                            for num in range(1,9):
                                if ship != ships_list[num - 1]:
                                    #print(ship, ships_list[num - 1])
                                    if num <= 4:
                                        if ship_status[num] == False:
                                            btn = Button(num * 210 - 170, 200, 200, 70, "Buy.", 50)
                                            btn.draw(win)
                                            ship_on_display = pygame.image.load(ships_list[num - 1])
                                            ship_on_display = pygame.transform.scale(ship_on_display, (48, 48))
                                            win.blit(ship_on_display, (btn.x + btn.width/2 - 24, btn.y - 50))
                                            btns_in_shop.append(btn)
                                        else:
                                            btn = Button(num * 210 - 170, 200, 200, 70, "Equip.", 50)
                                            btn.draw(win)
                                            ship_on_display = pygame.image.load(ships_list[num - 1])
                                            ship_on_display = pygame.transform.scale(ship_on_display, (48, 48))
                                            win.blit(ship_on_display, (btn.x + btn.width / 2 - 24, btn.y - 50))
                                            btns_in_shop.append(btn)
                                    else:
                                        if ship_status[num] == False:
                                            btn = Button((num - 4) * 210 - 170, 450, 200, 70, "Buy.", 50)
                                            btn.draw(win)
                                            ship_on_display = pygame.image.load(ships_list[num - 1])
                                            ship_on_display = pygame.transform.scale(ship_on_display, (48, 48))
                                            win.blit(ship_on_display, (btn.x + btn.width / 2 - 24, btn.y - 50))
                                            btns_in_shop.append(btn)
                                        else:
                                            btn = Button((num - 4) * 210 - 170, 450, 200, 70, "Equip.", 50)
                                            btn.draw(win)
                                            ship_on_display = pygame.image.load(ships_list[num - 1])
                                            ship_on_display = pygame.transform.scale(ship_on_display, (48, 48))
                                            win.blit(ship_on_display, (btn.x + btn.width / 2 - 24, btn.y - 50))
                                            btns_in_shop.append(btn)
                                else:
                                    if num <= 4:
                                        ship_on_display = pygame.image.load(ships_list[num - 1])
                                        ship_on_display = pygame.transform.scale(ship_on_display, (48, 48))
                                        win.blit(ship_on_display, (num * 210 - 170 + 200 / 2 - 24, 150))
                                        text = font.render("Equipped", 1, (255, 255, 255))
                                        win.blit(text, (num * 210 - 170 + 200 / 2 - text.get_width() / 2, 200))
                                    else:
                                        ship_on_display = pygame.image.load(ships_list[num - 1])
                                        ship_on_display = pygame.transform.scale(ship_on_display, (48, 48))
                                        win.blit(ship_on_display, ((num - 4) * 210 - 170 + 200 / 2 - 24, 400))
                                        text = font.render("Equipped", 1, (255, 255, 255))
                                        win.blit(text, ((num - 4) * 210 - 170 + 200 / 2 - text.get_width() / 2, 450))
                            pygame.display.update()
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                elif event.type == pygame.MOUSEBUTTONDOWN:
                                    real_btn = False
                                    pos = pygame.mouse.get_pos()
                                    x1 = pos[0]
                                    y1 = pos[0]
                                    for btn in btns_in_shop:
                                        if btn.click(pos):
                                            real_btn = btn
                                    if real_btn != False:
                                        if real_btn.click(pos) and real_btn.text == "Go back":
                                            run_for_shop = False
                                        ship, ship_status, coins = purchase_procedure(real_btn, pos, coins, font, ship, ship_status, ships_list, 40, 200, 1)
                                        ship, ship_status, coins = purchase_procedure(real_btn, pos, coins, font, ship, ship_status, ships_list, 250, 200, 2)
                                        ship, ship_status, coins = purchase_procedure(real_btn, pos, coins, font, ship, ship_status, ships_list, 460, 200, 3)
                                        ship, ship_status, coins = purchase_procedure(real_btn, pos, coins, font, ship, ship_status, ships_list, 670, 200, 4)

                                        ship, ship_status, coins = purchase_procedure(real_btn, pos, coins, font, ship, ship_status, ships_list, 40, 450, 5)
                                        ship, ship_status, coins = purchase_procedure(real_btn, pos , coins, font, ship, ship_status, ships_list, 250, 450, 6)
                                        ship, ship_status, coins = purchase_procedure(real_btn, pos, coins, font, ship, ship_status, ships_list, 460, 450, 7)
                                        ship, ship_status, coins = purchase_procedure(real_btn, pos, coins, font, ship, ship_status, ships_list, 670, 450, 8)
                            pygame.display.update()
                    elif btn.click(pos) and btn.text == "Quit":
                        run = False
                        pygame.quit()
                        sys.exit()
                    else:
                        pass
            else:
                pass
        pygame.display.update()
main_menu()