import pygame
import numpy
import random
import threading
from Aesthetics import *
pygame.font.init()
win = pygame.display.set_mode((1280, 720))


class PlayerStats():
    def __init__(self, industry_tokens, research_points, stability, construction, research_speed, attack, defend, speed, industry_output, resource_bonus, team, turn):
        self.tokens = industry_tokens
        self.research = research_points
        self.stability = stability
        self.construction = construction
        self.research_speed = research_speed
        self.attack = attack
        self.defend = defend
        self.speed = speed
        self.industry_output = industry_output
        self.resource_bonus = resource_bonus
        self.team = team
        self.turn = turn
        self.metals = 0
        self.organic = 0
        self.fuel = 0
        self.units = []
        self.units_built = pygame.sprite.Group()
        self.units_fighting = []
        self.units_moving = []
        self.units_working = []
        self.buildings = pygame.sprite.Group()
        self.buildings_built = pygame.sprite.Group()
        self.resource_deposits = pygame.sprite.Group()
        self.technologies_researched = []


class CameraGroup(pygame.sprite.Sprite):
    def __init__(self, offset, vel):
        super().__init__()
        self.surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2(offset)
        self.vel = vel

    def move_camera(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.offset[1] = self.offset[1] + self.vel
        if keys[pygame.K_a]:
            self.offset[0] = self.offset[0] + self.vel
        if keys[pygame.K_d]:
            self.offset[0] = self.offset[0] - self.vel
        if keys[pygame.K_s]:
            self.offset[1] = self.offset[1] - self.vel


    def custom_draw(self, buttons_for_ui, group_list, unit_group, tiles_group, tile_group_for_minimap, stats):
        win = self.surface
        x_stop = False
        y_stop = False
        #y_stop
        #basic_ui(buttons_for_ui)
        #print(group_list)
        if tiles_group.sprites()[0].x == 0 and self.offset[0] > 0:
            print("Hi1")
            x_stop = True
        if tiles_group.sprites()[::-1][0].x == 1280 and self.offset[0] < 0:
            print("Hi2")
            x_stop = True
        if tiles_group.sprites()[0].y == 0 and self.offset[1] > 0:
            print("Hi3")
            y_stop = True
        if tiles_group.sprites()[::-1][0].y == 704 and self.offset[1] < 0:
            print("Hi4")
            y_stop = True
        if x_stop == False and y_stop == False:
            for item in group_list:
                for item2 in item:
                    item2.x = item2.x + self.offset[0]
                    item2.y = item2.y + self.offset[1]
                    if item2.id == "tgr56":
                        print(item2.x)
        for item in group_list:
            item.draw(win)
            item.update(win, unit_group, tiles_group)
        unit_and_building_buttons, worker = unit_and_building_ui(stats)
        basic_ui(stats, win, buttons_for_ui, tiles_group, tile_group_for_minimap)
        self.offset = [0, 0]
        return unit_and_building_buttons, worker
            #item.update(unit_group, tiles_group)
        #pygame.time.delay(59468)
        #all_sprites =
        #for sprite in all_sprites:
            #win.blit(sprite,(self.offset))

def basic_ui(stats, win, buttons_for_ui, tile_group, tile_group_for_minimap):
    mouse_pos = pygame.mouse.get_pos()
    id = []
    pygame.draw.rect(win, (128, 128, 128), (100, 0, 300, 50))
    for item in buttons_for_ui:
        item.draw(win)
        if item.click(mouse_pos):
            item.tooltip(win)
    pygame.draw.rect(win, (0, 0, 0), (1090, 490, 180, 127))
    pygame.draw.rect(win, (0, 0, 255), (1095, 495, 170, 117))
    #print(tile_group_for_minimap.sprites()[0].x)
    #print(tile_group_for_minimap.sprites()[::-1][0].x)
    tile_group_for_minimap.draw(win)
    for item in tile_group:
        if item.x == 0 and item.y == 0:
            id.append(item)

    for item in stats.units_built:
        pygame.draw.rect(win, (0, 0, 0), ((1105 + item.x / 32) + (id[0].x - tile_group.sprites()[0].x) / 32, (505 + item.y / 32) + (id[0].y - tile_group.sprites()[0].y) / 32, 1, 1))
    #print("gre{}".format((id[0].y - tile_group.sprites()[0].y) / 32))
    #rect = pygame.Surface((40, 22))
    #rect.fill((0, 0, 0))
    #rect = rect.get_rect()
    #rect.topleft = (1105 + (id[0].x - tile_group.sprites()[0].x) / 32, 505 + (id[0].y - tile_group.sprites()[0].y) / 32)
    pygame.draw.rect(win, (255, 0, 0), (1105 + (id[0].x - tile_group.sprites()[0].x) / 24, 505 + (id[0].y - tile_group.sprites()[0].y) / 20, 40, 22.333333333333333), 1)

    pygame.display.update()

def unit_and_building_ui(stats):
    m_pos = pygame.mouse.get_pos()
    if stats.team == "Allies":
        team = "Allied"
        infantry_team = "ally"
    else:
        team = "Axis"
        infantry_team = "axis"
    buttons_for_workers = [Buttons(100, 600, 150, 50, "Build a factory", (255, 255, 255), "{}_factory.png".format(team)), Buttons(260, 600, 150, 50, "Build barracks", (255, 255, 255), "{}_barrack.png".format(team)), Buttons(420, 600, 160, 50, "Build a laboratory", (255, 255, 255), "{}_labratory.png".format(team)), Buttons(100, 660, 150, 50, "Build a refinery", (255, 255, 255), "{}_refinery.png".format(team)), Buttons(260, 660, 150, 50, "Build an AS", (255, 255, 255), "{}_flight_school.png".format(team)), Buttons(420, 660, 160, 50, "Build a TS", (255, 255, 255), "{}_tank_school.png".format(team)), Buttons(590, 600, 120, 40, "Autocollect f", (255, 255, 255), "Applied_fuel.png"), Buttons(590, 640, 120, 40, "Autocollect m", (255, 255, 255), "Applied_metals.png"), Buttons(590, 680, 120, 40, "Autocollect o", (255, 255, 255), "Applied_organic_matter.png")]
    buttons_for_infantry = []
    buttons_for_artillery = []
    buttons_for_tanks = []
    buttons_for_fighters = []
    buttons_for_bombers = []
    buttons_for_barracks = [Buttons(100, 600, 150, 100, "Build infantry", (255, 255, 255), "{}.png".format(infantry_team)), Buttons(260, 600, 170, 100, "Build mot infantry", (255, 255, 255), "{}_truck.png".format(team)), Buttons(440, 600, 180, 100, "Build mech infantry", (255, 255, 255), "{}_mech_infantry.png".format(team)), Buttons(620, 600, 150, 100, "Build artillery", (255, 255, 255), "{}_artillery.png".format(team))]
    buttons_for_tank_school = [Buttons(100, 600, 150, 100, "Build light tanks", (255, 255, 255), "{}_light_tank.png".format(team)), Buttons(260, 600, 170, 100, "Build medium tanks", (255, 255, 255), "{}_medium_tank.png".format(team)), Buttons(440, 600, 180, 100, "Build heavy tanks", (255, 255, 255), "{}_heavy_tank.png".format(team))]
    buttons_for_air_school = [Buttons(100, 600, 150, 100, "Build fighters", (255, 255, 255), "Allied_fighter.png")]
    buttons_for_refineries = []
    buttons_for_factories = [Buttons(100, 600, 150, 100, "Build workers", (255, 255, 255), "{}_construction_worker.png".format(team)), Buttons(260, 600, 150, 100, "Build adv workers", (255, 255, 255), "{}_advanced_construction_worker.png".format(team)), Buttons(420, 600, 150, 100, "Build con trucks", (255, 255, 255), "{}_construction_truck.png".format(team))]
    buttons_for_laboratories = []
    all_sprites = [stats.units_built, stats.buildings_built, stats.buildings]
    for group in all_sprites:
        for item in group:
            if item.selected == True:
                #name = ""
                #if len(list(item.name)) >= 8:
                    #name_list = list(item.name)
                    #for item2 in name_list[-8:]:
                        #name = name + item2
                #print(name)
                pygame.draw.rect(win, (0, 0, 0), (90, 590, 780, 710))
                pygame.draw.rect(win, (0, 0, 0), (90, 490, 200, 710))
                character = pygame.image.load("img/{}".format(item.name))
                font = pygame.font.SysFont("comicsans", 10)
                title = item.name.replace("_", " ")
                title = title.replace(".png", "")
                title = font.render("{}".format(title), 1, (255, 255, 255))
                win.blit(title, (90, 490))
                font = pygame.font.SysFont("comicsans", 20)
                text = font.render("Stats", 1, (255, 255, 255))
                win.blit(text, (90, 500))
                font = pygame.font.SysFont("comicsans", 10)
                text = font.render("Health: {}".format(item.health), 1, (255, 255, 255))
                win.blit(text, (90, 530))
                text = font.render("Speed: {}".format(item.speed), 1, (255, 255, 255))
                win.blit(text, (90, 550))
                text = font.render("Damage: {}".format(item.damage), 1, (255, 255, 255))
                win.blit(text, (90, 570))
                if item in stats.buildings:
                    text = font.render("being built", 1, (255, 255, 255))
                    win.blit(text, (93 + title.get_width(), 490))
                    text = font.render("Completed in: {} turns.".format(item.turn + item.time - stats.turn), 1, (255, 255, 255))
                    win.blit(text, (90, 590))
                #if item.team == "Allies":
                character = pygame.transform.flip(character, True, False)
                win.blit(character, (225, 510))
                if item.id == "Workers":
                    #print("Button")
                    for btn in buttons_for_workers:
                        btn.draw(win)
                        if btn.click(m_pos) == True:
                            btn.tooltip(win)
                    if item.autocollect == "Fuel":
                        pygame.draw.rect(win, (50, 168, 82), (590, 600, 5, 5))
                    elif item.autocollect == "Metals":
                        pygame.draw.rect(win, (50, 168, 82), (590, 640, 5, 5))
                    elif item.autocollect == "Organics":
                        pygame.draw.rect(win, (50, 168, 82), (590, 680, 5, 5))
                    else:
                        pass
                    return buttons_for_workers, item
                if item.id == "Infantry":
                    for btn in buttons_for_infantry:
                        btn.draw(win)
                        if btn.click(m_pos) == True:
                            btn.tooltip(win)
                    return buttons_for_infantry, item
                if item.id == "Artillery":
                    for btn in buttons_for_artillery:
                        btn.draw(win)
                        if btn.click(m_pos) == True:
                            btn.tooltip(win)
                    return buttons_for_artillery, item
                if item.id == "Tanks":
                    for btn in buttons_for_tanks:
                        btn.draw(win)
                        if btn.click(m_pos) == True:
                            btn.tooltip(win)
                    return buttons_for_tanks, item
                if item.id == "Fighters":
                    for btn in buttons_for_fighters:
                        btn.draw(win)
                        if btn.click(m_pos) == True:
                            btn.tooltip(win)
                    return buttons_for_fighters, item
                if item.id == "Bombers":
                    for btn in buttons_for_bombers:
                        btn.draw(win)
                        if btn.click(m_pos) == True:
                            btn.tooltip(win)
                    return buttons_for_bombers, item
                if item.id == "Barrack" and item in stats.buildings_built:
                    print("BARRACKS")
                    for btn in buttons_for_barracks:
                        btn.draw(win)
                        if btn.click(m_pos) == True:
                            btn.tooltip(win)
                    return buttons_for_barracks, item
                if item.id == "Factory" and item in stats.buildings_built:
                    for btn in buttons_for_factories:
                        btn.draw(win)
                        if btn.click(m_pos) == True:
                            btn.tooltip(win)
                    return buttons_for_factories, item

                if item.id == "Laboratory":
                     if item in stats.buildings_built:
                        for btn in buttons_for_laboratories:
                            btn.draw(win)
                            if btn.click(m_pos) == True:
                                btn.tooltip(win)
                        return buttons_for_laboratories, item
                if item.id == "Refinery":
                     if item in stats.buildings_built:
                        for btn in buttons_for_refineries:
                            btn.draw(win)
                            if btn.click(m_pos) == True:
                                btn.tooltip(win)
                        return buttons_for_refineries, item
                print("IMAGE: {}".format(item.image))
                if item.id == "Tank school":
                     print("KHAfoijgrtoiujr")
                     if item in stats.buildings_built:
                        for btn in buttons_for_tank_school:
                            btn.draw(win)
                            if btn.click(m_pos) == True:
                                btn.tooltip(win)
                        return buttons_for_tank_school, item

                if item.id == "Air school":
                     if item in stats.buildings_built:
                        for btn in buttons_for_air_school:
                            btn.draw(win)
                            if btn.click(m_pos) == True:
                                btn.tooltip(win)
                        return buttons_for_air_school, item
    else:
        return "No UI", None


def button_chain(win, amount_of_times, list_of_buttons, id):
    win.fill((0, 0, 0))
    try:
        buttons_for_this_area = list_of_buttons.pop(id)
    except IndexError:
        return "done"
    for btn in buttons_for_this_area:
        btn.draw(win)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in buttons_for_this_area:
                    if btn.click(pos) == True:
                        id = buttons_for_this_area.index(btn)
                        button_chain(win, amount_of_times, list_of_buttons,id)

def attack(stats, item, item2, units_fighting):
    different_units_fighting = 0
    units_fighting_counter = []
    population = [True, False]
    weight = [item.experience, 100 - item.experience]
    hit = random.choices(population, weight)
    #print("Hit3 {}".format(hit))
    units_fighting.append((item, item2))
    for x, y in units_fighting:
        if (x, y) not in units_fighting_counter and (y, x) not in units_fighting_counter:
            if x == item or y == item:
                different_units_fighting = different_units_fighting + 1
                units_fighting_counter.append((x, y))
        #if x == item:
            #if y != item2:
                #different_units_fighting = different_units_fighting + 1
        #if y == item:
            #if x != item2:
                #different_units_fighting = different_units_fighting + 1
    if hit == [True]:
        if item2.name != "Allied_fighter.png" or item2.name != "Axis_fighter.png":
            item2.health = item2.health - item.damage * stats.attack / different_units_fighting
        else:
            item2.health = item2.health - item.air_damage * stats.attack / different_units_fighting
        if item2.health <= 0:
            item2.kill()
            #units_fighting.pop(units_fighting.index(item))
            item.experience = item.experience + random.randint(1, 10)
            while True:
                for value in units_fighting:
                    if item in value and item2 in value:
                        units_fighting.pop(units_fighting.index(value))
                        break
                else:
                    break
            return "Fighting done"

def fighting(stats, units_built_group, defenders, run, units_fighting):
    print(units_built_group, defenders)
    for item in units_built_group:
        for item2 in defenders:
            if item.x == item2.x + 32 or item.x == item2.x - 32 or item.x == item2.x:
                if item.y == item2.y - 32 or item.y == item2.y + 32 or item.y == item2.y:
                    print("r: {}".format(run))
                    if item != item2 and item.team != item2.team and run == True:
                        print("hh")
                        rand_num = random.randint(1,2)
                        if rand_num == 1:
                            attack(stats, item, item2, units_fighting)
                            attack(stats, item2, item, units_fighting)
                        else:
                            attack(stats, item2, item, units_fighting)
                            attack(stats, item, item2, units_fighting)
                        print("H: {}, H2: {}".format(item.health, item2.health))

    return False

def moving_sprite(stats, m_pos, tiles_group, button_pressed):
    if button_pressed == False:
        for item in stats.units_built.sprites() + stats.buildings_built.sprites() + stats.buildings.sprites():
            item.click(win, m_pos)
            if item.selected == True:
                if item.team == stats.team:
                    sprs = [stats.units_built.sprites() + stats.buildings_built.sprites() + stats.buildings.sprites()][0]
                    sprs.pop(sprs.index(item))
                    for item in sprs:
                        item.selected = False
                else:
                    item.selected = False
        else:
            for item in tiles_group:
                for item2 in stats.units_built.sprites():
                    if item.click(m_pos) and item2.selected == True:
                        for item3 in stats.units_built.sprites():
                            if item3.x == item.x and item3.y == item.y and item3 != item2:
                                print(item3.id, item2.id, item.id)
                                print("You cannot do that!")
                                break
                        else:
                            if item2 not in stats.buildings_built and item2 not in stats.buildings:
                                if item2.speed * stats.speed >= abs(item2.x - item.x) / 32 + abs(item2.y - item.y) / 32 and item2 not in stats.units_moving:
                                    print("speed: {}".format(abs(item2.x - item.x) / 32 + abs(item2.y - item.y) / 32))
                                    item2.speed = item2.speed - abs(item2.x - item.x) / 32 - abs(item2.y - item.y) / 32
                                    thread = threading.Thread(target = unit_animation, args = (stats, item2, (item.x, item.y)))
                                    thread.start()
                                    #stats.units_moving.append(item2)
                                    #item2.x = item.x
                                    #item2.y = item.y
                                else:
                                    print("You cannot go there!")

def buttons_clicked(stats, run, buttons_for_ui, buttons_for_unit_ui, m_pos, turn, unit):
    for btns in buttons_for_ui:
        if btns.click(m_pos) == True:
            if btns.text == "End Turn":
                stats.turn = stats.turn + 1
                run = True
                return run, True
            if btns.text == "Stats":
                while True:
                    pygame.draw.rect(win, (255, 255, 255), (100, 100, 1080, 520))
                    exit_button = Buttons(1016, 100, 64, 64, "Exit", (0, 0, 0), "Axis_heavy_tank.png")
                    exit_button.draw(win)
                    font = pygame.font.SysFont("comicsans", 50)
                    text = font.render("Stats".format(stats.tokens), 1, (0, 0, 0))
                    win.blit(text, ((1080 - text.get_width()) / 2, 100))
                    font = pygame.font.SysFont("comicsans", 20)
                    text = font.render("Tokens: {}".format(stats.tokens), 1, (0, 0, 0))
                    win.blit(text, (150, 200))
                    text = font.render("Research points: {}".format(stats.research), 1, (0, 0, 0))
                    win.blit(text, (150, 250))
                    text = font.render("Metals: {}".format(stats.metals), 1, (0, 0, 0))
                    win.blit(text, (150, 300))
                    text = font.render("Organic Matter: {}".format(stats.organic), 1, (0, 0, 0))
                    win.blit(text, (150, 350))
                    text = font.render("Fuel: {}".format(stats.fuel), 1, (0, 0, 0))
                    win.blit(text, (150, 400))
                    text = font.render("Total amount of units: {}".format(len([x for x in stats.units_built if x.team == stats.team])), 1, (0, 0, 0))
                    win.blit(text, (150, 450))
                    text = font.render("Total amount of buildings: {}".format(len([x for x in stats.buildings_built if x.team == stats.team])), 1, (0, 0, 0))
                    win.blit(text, (150, 500))
                    text = font.render("Total amount of workers: {}".format(len([x for x in stats.units_built if x.id == "Workers"])), 1, (0, 0, 0))
                    win.blit(text, (150, 550))
                    text = font.render("Total amount of infantry: {}".format(len([x for x in stats.units_built if x.id == "Infantry"])), 1, (0, 0, 0))
                    win.blit(text, (500, 200))
                    text = font.render("Total amount of tanks: {}".format(len([x for x in stats.units_built if x.id == "Tanks"])),1, (0, 0, 0))
                    win.blit(text, (500, 250))
                    text = font.render("Total amount of fighters: {}".format(len([x for x in stats.units_built if x.id == "Fighters"])), 1, (0, 0, 0))
                    win.blit(text, (500, 300))
                    pygame.display.update()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print("Hi!")
                            m_pos = pygame.mouse.get_pos()
                            if exit_button.click(m_pos) == True:
                                return run, True
            if btns.text == "Research":
                research_buttons = [Buttons(110, 100, 128, 128, "+10% damage", (0, 0, 0), "Applied_attack_research1.png"), Buttons(302, 100, 128, 128, "+20% damage", (0, 0, 0), "Applied_attack_research2.png"), Buttons(494, 100, 128, 128, "+30% damage", (0, 0, 0), "Applied_attack_research3.png"), Buttons(686, 100, 128, 128, "+40% damage", (0, 0, 0), "Applied_attack_research4.png"), Buttons(878, 100, 128, 128, "+50% damage", (0, 0, 0), "Applied_attack_research5.png")]
                research_buttons2 = [Buttons(110, 240, 128, 128, "+10% speed", (0, 0, 0), "Applied_speed_research1.png"), Buttons(302, 240, 128, 128, "+20% speed", (0, 0, 0), "Applied_speed_research2.png"), Buttons(494, 240, 128, 128, "+30% speed", (0, 0, 0), "Applied_speed_research3.png"), Buttons(686, 240, 128, 128, "+40% speed", (0, 0, 0), "Applied_speed_research4.png"), Buttons(878, 240, 128, 128, "+50% speed", (0, 0, 0), "Applied_speed_research5.png")]
                research_buttons3 = [Buttons(110, 380, 128, 128, "+10% MG", (0, 0, 0), "Applied_material_research1.png"), Buttons(302, 380, 128, 128, "+20% MG", (0, 0, 0), "Applied_material_research2.png"), Buttons(494, 380, 128, 128, "+30% MG", (0, 0, 0), "Applied_material_research3.png"), Buttons(686, 380, 128, 128, "+40% MG", (0, 0, 0), "Applied_material_research4.png")]
                while True:
                    pygame.draw.rect(win, (255, 255, 255), (100, 100, 1080, 520))
                    exit_button = Buttons(1016, 100, 64, 64, "Exit", (0, 0, 0), "Axis_heavy_tank.png")
                    exit_button.draw(win)
                    m_pos = pygame.mouse.get_pos()
                    for btn in research_buttons:
                        btn.draw(win)
                        if btn.text in stats.technologies_researched:
                            pygame.draw.rect(win, (0, 0, 0), (btn.x, btn.y, 128, 128), 1)
                        if btn.click(m_pos) == True:
                            btn.tooltip(win)
                    for btn in research_buttons2:
                        btn.draw(win)
                        if btn.text in stats.technologies_researched:
                            pygame.draw.rect(win, (0, 0, 0), (btn.x, btn.y, 128, 128), 1)
                        if btn.click(m_pos) == True:
                            btn.tooltip(win)
                    for btn in research_buttons3:
                        btn.draw(win)
                        if btn.text in stats.technologies_researched:
                            pygame.draw.rect(win, (0, 0, 0), (btn.x, btn.y, 128, 128), 1)
                        if btn.click(m_pos) == True:
                            btn.tooltip(win)
                    pygame.display.update()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print("Hi!")
                            m_pos = pygame.mouse.get_pos()
                            if exit_button.click(m_pos) == True:
                                return run, True
                            for btn in research_buttons:
                                if btn.click(m_pos) == True:
                                    if btn.text == "+10% damage" and stats.research >= 10:
                                        stats.technologies_researched.append("+10% damage")
                                        stats.research = stats.research - 10
                                        stats.attack = stats.attack + 0.1
                                    elif btn.text == "+20% damage" and stats.research >= 20 and "+10% damage" in stats.technologies_researched:
                                        stats.technologies_researched.append("+20% damage")
                                        stats.research = stats.research - 20
                                        stats.attack = stats.attack + 0.2
                                    elif btn.text == "+30% damage" and stats.research >= 30 and "+20% damage" in stats.technologies_researched:
                                        stats.technologies_researched.append("+30% damage")
                                        stats.research = stats.research - 30
                                        stats.attack = stats.attack + 0.3
                                    elif btn.text == "+40% damage" and stats.research >= 40 and "+30% damage" in stats.technologies_researched:
                                        stats.technologies_researched.append("+40% damage")
                                        stats.research = stats.research - 40
                                        stats.attack = stats.attack + 0.4
                                    elif btn.text == "+50% damage" and stats.research >= 50 and "+40% damage" in stats.technologies_researched:
                                        stats.technologies_researched.append("+50% damage")
                                        stats.research = stats.research - 50
                                        stats.attack = stats.attack + 0.5
                                    else:
                                        pass

                            for btn in research_buttons2:
                                if btn.click(m_pos) == True:
                                    if btn.text == "+10% speed" and stats.research >= 10:
                                        stats.technologies_researched.append("+10% speed")
                                        stats.research = stats.research - 10
                                        stats.speed = stats.speed + 0.1
                                    elif btn.text == "+20% speed" and stats.research >= 20 and "+10% speed" in stats.technologies_researched:
                                        stats.technologies_researched.append("+20% speed")
                                        stats.research = stats.research - 20
                                        stats.speed = stats.speed + 0.2
                                    elif btn.text == "+30% speed" and stats.research >= 30 and "+20% speed" in stats.technologies_researched:
                                        stats.technologies_researched.append("+30% speed")
                                        stats.research = stats.research - 30
                                        stats.speed = stats.speed + 0.3
                                    elif btn.text == "+40% speed" and stats.research >= 40 and "+30% speed" in stats.technologies_researched:
                                        stats.technologies_researched.append("+40% speed")
                                        stats.research = stats.research - 40
                                        stats.speed = stats.speed + 0.4
                                    elif btn.text == "+50% speed" and stats.research >= 50 and "+40% speed" in stats.technologies_researched:
                                        stats.technologies_researched.append("+50% speed")
                                        stats.research = stats.research - 50
                                        stats.speed = stats.speed + 0.5
                                    else:
                                        pass

                            for btn in research_buttons3:
                                if btn.click(m_pos) == True:
                                    if btn.text == "+10% MG" and stats.research >= 10:
                                        stats.technologies_researched.append("+10% MG")
                                        stats.research = stats.research - 10
                                        stats.resource_bonus = stats.resource_bonus + 0.1
                                    elif btn.text == "+20% MG" and stats.research >= 20 and "+10% MG" in stats.technologies_researched:
                                        stats.technologies_researched.append("+20% MG")
                                        stats.research = stats.research - 20
                                        stats.resource_bonus = stats.resource_bonus + 0.2
                                    elif btn.text == "+30% MG" and stats.research >= 30 and "+20% MG" in stats.technologies_researched:
                                        stats.technologies_researched.append("+30% speed")
                                        stats.research = stats.research - 30
                                        stats.resource_bonus = stats.resource_bonus + 0.3
                                    elif btn.text == "+40% MG" and stats.research >= 40 and "+30% MG" in stats.technologies_researched:
                                        stats.technologies_researched.append("+40% MG")
                                        stats.research = stats.research - 40
                                        stats.resource_bonus = stats.resource_bonus + 0.4
                                    elif btn.text == "+50% MG" and stats.research >= 50 and "+40% MG" in stats.technologies_researched:
                                        stats.technologies_researched.append("+50% MG")
                                        stats.research = stats.research - 50
                                        stats.resource_bonus = stats.resource_bonus + 0.5
                                    else:
                                        pass


    else:
        if buttons_for_unit_ui != "No UI":
            for btns in buttons_for_unit_ui:
                if btns.click(m_pos) == True and btns.text == "Build a factory":
                    if stats.tokens - 300 >= 0 and stats.metals >= 15 and stats.fuel >= 4:
                        resources = {"Metals": 15, "Non organic": 4}
                        if unit.team == "Axis":
                            return build_something(stats, unit, run, "Axis_factory.png", "IT; +10", 100, 0, 0, 0, 0, 300, "Axis", 4, resources, "Factory")
                        else:
                            return build_something(stats, unit, run, "Allied_factory.png", "IT; +10", 100, 0, 0, 0, 0, 300, "Allies", 4, resources, "Factory")
                    else:
                        print("You do not have enough tokens or materials for that!")
                        return run, True

                if btns.click(m_pos) == True and btns.text == "Build barracks":
                    if stats.tokens - 200 >= 0 and stats.metals >= 2 and stats.organic >= 8:
                        resources = {"Metals": 2, "Organic": 8}
                        if unit.team == "Axis":
                            return build_something(stats, unit, run, "Axis_barrack.png", "Nothing", 50, 0, 0, 0, 0, 200, "Axis", 2, resources, "Barrack")
                        else:
                            return build_something(stats, unit, run, "Allied_barrack.png", "Nothing", 50, 0, 0, 0, 0, 200, "Allies", 2, resources, "Barrack")
                    else:
                        print("You do not have enough tokens or materials for that!")
                        return run, True

                if btns.click(m_pos) == True and btns.text == "Build an AS":
                    if stats.tokens - 200 >= 0 and stats.metals >= 10 and stats.organic >= 8 and stats.fuel >= 5:
                        resources = {"Metals": 10, "Organic": 8, "Non organic": 5}
                        if unit.team == "Axis":
                            return build_something(stats, unit, run, "Axis_flight_school.png", "Nothing", 50, 0, 0, 0, 0, 200, "Axis", 2, resources, "Air school")
                        else:
                            return build_something(stats, unit, run, "Allied_flight_school.png", "Nothing", 50, 0, 0, 0, 0, 200, "Allies", 2, resources, "Air school")
                    else:
                        print("You do not have enough tokens or materials for that!")
                        return run, True

                if btns.click(m_pos) == True and btns.text == "Build a TS":
                    if stats.tokens - 200 >= 0 and stats.metals >= 10 and stats.organic >= 8 and stats.fuel >= 5:
                        resources = {"Metals": 10, "Organic": 8, "Non organic": 5}
                        if unit.team == "Axis":
                            return build_something(stats, unit, run, "Axis_tank_school.png", "Nothing", 50, 0, 0, 0, 0, 200, "Axis", 2, resources, "Tank school")
                        else:
                            return build_something(stats, unit, run, "Allied_tank_school.png", "Nothing", 50, 0, 0, 0, 0, 200, "Allies", 2, resources, "Tank school")
                    else:
                        print("You do not have enough tokens or materials for that!")
                        return run, True

                if btns.click(m_pos) == True and btns.text == "Build a refinery":
                    if stats.tokens - 100 >= 0 and stats.metals >= 10 and stats.fuel >= 5:
                        resources = {"Metals": 10, "Non organic": 5}
                        if unit.team == "Axis":
                            return build_something(stats, unit, run, "Axis_refinery.png", "Nothing", 50, 0, 0, 0, 0, 100, "Axis", 1, resources, "Refinery")
                        else:
                            return build_something(stats, unit, run, "Allied_refinery.png", "Nothing", 50, 0, 0, 0, 0, 100, "Allies", 1, resources, "Refinery")
                    else:
                        print("You do not have enough tokens or materials for that!")
                        return run, True

                if btns.click(m_pos) == True and btns.text == "Build a laboratory":
                    if stats.tokens - 500 >= 0 and stats.metals >= 20 and stats.organic >= 5 and stats.fuel >= 10:
                        resources = {"Metals": 20, "Organic": 5, "Non organic": 10}
                        if unit.team == "Axis":
                            return build_something(stats, unit, run, "Axis_labratory.png", "Research; +10", 50, 0, 0, 0, 0, 500, "Axis", 2, resources, "Laboratory")
                        else:
                            return build_something(stats, unit, run, "Allied_labratory.png", "Research; + 10", 50, 0, 0, 0, 0, 500, "Allies", 2, resources, "Laboratory")
                    else:
                        print("You do not have enough tokens or materials for that!")
                        return run, True


                if btns.click(m_pos) == True and btns.text == "Autocollect f":
                    if unit.autocollect != "Fuel":
                        unit.autocollect = "Fuel"
                    else:
                        unit.autocollect = False
                    return run, True

                if btns.click(m_pos) == True and btns.text == "Autocollect m":
                    if unit.autocollect != "Metals":
                        unit.autocollect = "Metals"
                    else:
                        unit.autocollect = False
                    return run, True

                if btns.click(m_pos) == True and btns.text == "Autocollect o":
                    if unit.autocollect != "Organics":
                        unit.autocollect = "Organics"
                    else:
                        unit.autocollect = False
                    return run, True

                if btns.click(m_pos) == True and btns.text == "Build workers":
                    if stats.tokens - 50 >= 0 and stats.metals >= 1 and stats.organic >= 3:
                        resources = {"Metals": 1, "Organic": 3}
                        if unit.team == "Axis":
                            return build_something(stats, unit, run, "Axis_construction_worker.png", "Nothing", 10, 50, 1, 10, 0, 1, "Axis", 1, resources, "Workers")
                        else:
                            return build_something(stats, unit, run, "Allied_construction_worker.png", "Nothing", 10, 50, 1, 10, 0, 1, "Allies", 1, resources, "Workers")
                    else:
                        print("You do not have enough tokens or materials for that!")
                        return run, True

                if btns.click(m_pos) == True and btns.text == "Build adv workers":
                    if stats.tokens - 50 >= 0 and stats.metals >= 3 and stats.organic >= 3:
                        resources = {"Metals": 3, "Organic": 3}
                        if unit.team == "Axis":
                            return build_something(stats, unit, run, "Axis_advanced_construction_worker.png", "Nothing", 15, 50, 12, 2, 0, 3, "Axis", 1, resources, "Workers")
                        else:
                            return build_something(stats, unit, run, "Allied_advanced_construction_worker.png", "Nothing", 15, 50, 12, 2, 0, 3, "Allies", 1, resources, "Workers")
                    else:
                        print("You do not have enough tokens or materials for that!")
                        return run, True

                if btns.click(m_pos) == True and btns.text == "Build con trucks":
                    if stats.tokens - 50 >= 0 and stats.metals >= 3 and stats.organic >= 3:
                        resources = {"Metals": 8, "Organic": 3}
                        if unit.team == "Axis":
                            return build_something(stats, unit, run, "Axis_construction_truck.png", "Nothing", 30, 50, 40, 8, 0, 3, "Axis", 10, resources, "Workers")
                        else:
                            return build_something(stats, unit, run, "Allied_construction_truck.png", "Nothing", 30, 50, 40, 8, 0, 3, "Allies", 10, resources, "Workers")
                    else:
                        print("You do not have enough tokens or materials for that!")
                        return run, True

                if btns.click(m_pos) == True and btns.text == "Build infantry":
                    if stats.tokens - 50 >= 0 and stats.metals >= 1 and stats.organic >= 5:
                        resources = {"Metals": 1, "Organic": 5}
                        if unit.team == "Axis":
                            return build_something(stats, unit, run, "axis.png", "Nothing", 20, 50, 5, 7, 0, 3, "Axis", 2, resources, "Infantry")
                        else:
                            return build_something(stats, unit, run, "ally.png", "Nothing", 20, 50, 5, 7, 0, 3, "Allies", 2, resources, "Infantry")
                    else:
                        print("You do not have enough tokens or materials for that!")
                        return run, True

                if btns.click(m_pos) == True and btns.text == "Build mot infantry":
                    if stats.tokens - 300 >= 0 and stats.metals >= 5 and stats.organic >= 10 and stats.fuel >= 1:
                        resources = {"Metals": 5, "Organic": 10, "Non organic": 1}
                        if unit.team == "Axis":
                            return build_something(stats, unit, run, "Axis_truck.png", "Nothing", 50, 50, 30, 25, 0, 40, "Axis", 2, resources, "Infantry")
                        else:
                            return build_something(stats, unit, run, "Allied_truck.png", "Nothing", 50, 50, 30, 25, 0, 40, "Allies", 2, resources, "Infantry")
                    else:
                        print("You do not have enough tokens or materials for that!")
                        return run, True

                if btns.click(m_pos) == True and btns.text == "Build mech infantry":
                    if stats.tokens - 300 >= 0 and stats.metals >= 8 and stats.organic >= 12 and stats.fuel >= 3:
                        resources = {"Metals": 8, "Organic": 12, "Non organic": 3}
                        if unit.team == "Axis":
                            return build_something(stats, unit, run, "Axis_mech_infantry.png", "Nothing", 50, 50, 20, 40, 0, 60, "Axis", 2, resources, "Infantry")
                        else:
                            return build_something(stats, unit, run, "Allied_mech_infantry.png", "Nothing", 50, 50, 20, 40, 0, 60, "Allies", 2, resources, "Infantry")
                    else:
                        print("You do not have enough tokens or materials for that!")
                        return run, True

                if btns.click(m_pos) == True and btns.text == "Build artillery":
                    if stats.tokens - 300 >= 0 and stats.metals >= 8 and stats.organic >= 12:
                        resources = {"Metals": 5, "Organic": 10}
                        if unit.team == "Axis":
                            return build_something(stats, unit, run, "Axis_artillery.png", "Nothing", 15, 50, 10, 60, 0, 60, "Axis", 2, resources, "Artillery")
                        else:
                            return build_something(stats, unit, run, "Allied_artillery.png", "Nothing", 15, 50, 10, 60, 0, 60, "Allies", 2, resources, "Artillery")
                    else:
                        print("You do not have enough tokens or materials for that!")
                        return run, True

                if btns.click(m_pos) == True and btns.text == "Build light_tanks":
                    if stats.tokens - 50 >= 0 and stats.metals >= 6 and stats.organic >= 5 and stats.fuel >= 6:
                        resources = {"Metals": 6, "Organic": 5, "Non organic": 6}
                        if unit.team == "Axis":
                            return build_something(stats, unit, run, "Axis_light_tank.png", "Nothing", 40, 50, 60, 20, 0, 60, "Axis", 5, resources, "Tanks")
                        else:
                            return build_something(stats, unit, run, "Allied_light_tank.png", "Nothing", 40, 50, 60, 20, 0, 60, "Allies", 5, resources, "Tanks")
                    else:
                        print("You do not have enough tokens or materials for that!")
                        return run, True

                if btns.click(m_pos) == True and btns.text == "Build medium tanks":
                    if stats.tokens - 300 >= 0 and stats.metals >= 8 and stats.organic >= 10 and stats.fuel >= 8:
                        resources = {"Metals": 8, "Organic": 10, "Non organic": 8}
                        if unit.team == "Axis":
                            return build_something(stats, unit, run, "Axis_medium_tank.png", "Nothing", 70, 50, 30, 30, 0, 100, "Axis", 7, resources, "Tanks")
                        else:
                            return build_something(stats, unit, run, "Allied_medium_tank.png", "Nothing", 70, 50, 30, 30, 0, 100, "Allies", 7, resources, "Tanks")
                    else:
                        print("You do not have enough tokens or materials for that!")
                        return run, True

                if btns.click(m_pos) == True and btns.text == "Build heavy tanks":
                    if stats.tokens - 300 >= 0 and stats.metals >= 12 and stats.organic >= 12 and stats.fuel >= 12:
                        resources = {"Metals": 12, "Organic": 12, "Non organic": 12}
                        if unit.team == "Axis":
                            return build_something(stats, unit, run, "Axis_heavy_tanks.png", "Nothing", 100, 50, 10, 50, 0, 150, "Axis", 9, resources, "Tanks")
                        else:
                            return build_something(stats, unit, run, "Allied_heavy_tanks.png", "Nothing", 100, 50, 10, 50, 0, 150, "Allies", 9, resources, "Tanks")
                    else:
                        print("You do not have enough tokens or materials for that!")
                        return run, True

                if btns.click(m_pos) == True and btns.text == "Build fighters":
                    if stats.tokens - 300 >= 0 and stats.metals >= 8 and stats.fuel >= 5:
                        resources = {"Metals": 8, "Non organics":5}
                        if unit.team == "Axis":
                            return build_something(stats, unit, run, "Axis_fighter.png", "Nothing", 20, 50, 300, 20, 20, 75, "Axis", 10, resources, "Fighters")
                        else:
                            return build_something(stats, unit, run, "Allied_fighter.png", "Nothing", 20, 50, 300, 20, 20, 75, "Allies", 10, resources, "Fighters")
                    else:
                        print("You do not have enough tokens or materials for that!")
                        return run, True



            else:
                return run, False
        else:
            return run, False

def build_something(stats, unit, run, img_name, buff, health, experience, speed, damage, air_damage, cost, team, time, resources, id):
    total_list = stats.units_built.sprites() + stats.buildings_built.sprites() + stats.buildings.sprites() + stats.units_working
    if unit in stats.units_built:
        for item in total_list:
            if unit.x - 32 == item.x and unit.y == item.y:
                print("You cannot build there!")
                break
        else:
            factory = Buildings(unit.x - 32, unit.y, id, img_name, buff, health, experience, damage, cost, stats.turn, time, team)
            factory.image.set_alpha(128)
            stats.buildings.add(factory)
            stats.tokens = stats.tokens - factory.cost
            for value in list(resources):
                if value == "Metals":
                    stats.metals = stats.metals - resources[value]
                elif value == "Organic":
                    stats.organic = stats.organic - resources[value]
                else:
                    stats.fuel = stats.fuel - resources[value]
            stats.units_built.remove(unit)
            stats.units_working.append(unit)

        return run, True

    elif unit in stats.buildings_built:
        positions_list = [(32, 0), (32, 32), (0, 32), (-32, 32), (-32, 0), (-32, -32), (0, -32), (32, -32)]
        total_list = stats.units_built.sprites() + stats.buildings_built.sprites() + stats.buildings.sprites() + stats.units_working
        for x, y in positions_list:
            for item in total_list:
                if item.x == unit.x + x and item.y == unit.y + y:
                    break
            else:
                stats.units_built.add(Units(unit.x + x, unit.y + y, id, health, damage, air_damage, speed, img_name, False, "Allies", 50))
                stats.tokens = stats.tokens - cost
                for value in list(resources):
                    if value == "Metals":
                        stats.metals = stats.metals - resources[value]
                    elif value == "Organic":
                        stats.organic = stats.organic - resources[value]
                    else:
                        stats.fuel = stats.fuel - resources[value]
                break

        return run, True

    else:
        pass

def unit_animation(stats, unit, final_destination):
    stats.units_moving.append(unit)
    amount_of_tilesx = (int(final_destination[0]) - int(unit.x)) / 32
    amount_of_tilesy = (int(final_destination[1]) - int(unit.y)) / 32
    if amount_of_tilesx > 0:
        amount_of_tilesx = int(amount_of_tilesx)
        for num in range(amount_of_tilesx):
            unit.x = unit.x + 32
            pygame.time.delay(100)
    else:
        amount_of_tilesx = int(abs(amount_of_tilesx))
        for num in range(amount_of_tilesx):
            unit.x = unit.x - 32
            pygame.time.delay(100)

    if amount_of_tilesy > 0:
        amount_of_tilesy = int(amount_of_tilesy)
        for num in range(amount_of_tilesy):
            unit.y = unit.y + 32
            pygame.time.delay(100)
    else:
        amount_of_tilesy = int(abs(amount_of_tilesy))
        for num in range(amount_of_tilesy):
            unit.y = unit.y - 32
            pygame.time.delay(100)
    stats.units_moving.pop(stats.units_moving.index(unit))

def collect_materials(run, stats):
    if run == True:
        for item in stats.units_built:
            for item2 in stats.resource_deposits:
                if item.x == item2.x and item.y == item2.y and item.full == False:
                    item.full = item2.name
                    print("AAAAAAAAAAAAAA{}".format(item.full))
        for item in stats.units_built:
            for item2 in stats.buildings_built:
                if item.x + 32 == item2.x or item.x - 32 == item2.x or item.x == item.y:
                    if item.y + 32 == item2.y or item.y - 32 == item.y or item.y == item.y:
                        if item2.name == "Allied_refinery.png" and stats.team == "Allies":
                            if item.full == "Applied_metals.png":
                                stats.metals = stats.metals + item.space * (1 + stats.resource_bonus)
                            elif item.full == "Applied_organic_matter.png":
                                stats.organic = stats.organic + item.space * (1 + stats.resource_bonus)
                            elif item.full == "Applied_fuel.png":
                                stats.fuel = stats.fuel + item.space * (1 + stats.resource_bonus)
                            else:
                                pass
                            item.full = False
                        elif item2.name == "Axis_refinery.png" and stats.team == "Axis":
                            if item.full == "Applied_metals.png":
                                stats.metals = stats.metals + item.space * (1 + stats.resource_bonus)
                            elif item.full == "Applied_organic_matter.png":
                                stats.organic = stats.organic + item.space * (1 + stats.resource_bonus)
                            elif item.full == "Applied_fuel.png":
                                stats.fuel = stats.fuel + item.space * (1 + stats.resource_bonus)
                            else:
                                pass
                            item.full = False
                        else:
                            pass
def auto_collect(run, stats, resource):
    if resource == "Fuel":
        resource_img_name = "Applied_fuel.png"
    elif resource == "Metals":
        resource_img_name = "Applied_metals.png"
    else:
        resource_img_name = "Applied_organic_matter.png"
    if run == True:
        for item in stats.units_built:
            if item.autocollect == resource and item.full == False:
                x = 100000
                y = 100000
                for item2 in stats.resource_deposits:
                    if item2.name == resource_img_name:
                        if abs(item.x - item2.x) + abs(item.y - item2.y) < abs(item.x - x) + abs(item.y - y):
                            x = item2.x
                            y = item2.y
                print("rggrgttg {}{}".format(x, y))
                print("rggrgttg {}{}".format(item.x, item.y))
                #speed = [item.speed][0]
                x_locked_in = False
                y_locked_in = False
                while True:
                    if item.x < x:
                        item.x = item.x + 32
                        item.speed = item.speed - 1
                    elif item.x > x:
                        item.x = item.x - 32
                        item.speed = item.speed - 1
                    elif item.x == x:
                        x_locked_in = True
                    else:
                        pass

                    if item.y < y:
                        item.y = item.y + 32
                        item.speed = item.speed - 1
                    elif item.y > y:
                        item.y = item.y - 32
                        item.speed = item.speed - 1
                    elif item.y == y:
                        y_locked_in = True
                    else:
                        pass

                    if item.speed <= 0:
                        break
                    elif x_locked_in == True and y_locked_in == True:
                        print("Hello.")
                        break
                    else:
                        pass

def auto_deposit(run, stats):
    if run == True:
        for item in stats.units_built:
            if item.autocollect != False and item.full != False:
                x = 100000
                y = 100000
                for item2 in stats.buildings_built:
                    if item2.name == "Allied_refinery.png" and stats.team == "Allies":
                        if abs(item.x - item2.x) + abs(item.y - item2.y) < abs(item.x - x) + abs(item.y - y):
                            x = item2.x + 32
                            y = item2.y
                    elif item2.name == "Axis_refinery.png" and stats.team == "Axis":
                        if abs(item.x - item2.x) + abs(item.y - item2.y) < abs(item.x - x) + abs(item.y - y):
                            x = item2.x + 32
                            y = item2.y
                    else:
                        pass
                if x == 100000 and y == 100000:
                    x = item.x
                    y = item.y
                x_locked_in = False
                y_locked_in = False
                while True:
                    if item.x < x:
                        item.x = item.x + 32
                        item.speed = item.speed - 1
                    elif item.x > x:
                        item.x = item.x - 32
                        item.speed = item.speed - 1
                    elif item.x == x:
                        x_locked_in = True
                    else:
                        pass

                    if item.y < y:
                        item.y = item.y + 32
                        item.speed = item.speed - 1
                    elif item.y > y:
                        item.y = item.y - 32
                        item.speed = item.speed - 1
                    elif item.y == y:
                        y_locked_in = True
                    else:
                        pass

                    if item.speed <= 0:
                        break
                    elif x_locked_in == True and y_locked_in == True:
                        print("Hello.")
                        break
                    else:
                        pass


def reset_units(run, stats):
    total_list = stats.units_built.sprites() + stats.buildings_built.sprites() + stats.buildings.sprites()
    x_and_y_list = [[item.x, item.y] for item in total_list]

    if run == True:
        for item in stats.units_built:
            item.speed = item.original_speed
        for item in x_and_y_list:
            while True:
                if x_and_y_list.count(item) > 1:
                    item[0] = item[0] + 32
                else:
                    break
            total_list[x_and_y_list.index(item)].x = item[0]
            total_list[x_and_y_list.index(item)].y = item[1]


def apply_buffs(run, stats):
    if run == True:
        for value in stats.buildings_built:
            buff = value.buffs
            if buff == "IT; +10":
                stats.tokens = stats.tokens + 10
                print("irebfiunrijgnbgijnrtgorthnotrignurtjoignr")
            elif buff == "Research; +10":
                stats.research = stats.research + 10
            else:
                pass

def multilines(text, x, y, width):
    text_list = text.split(" ")
    line = []
    line_length = 0
    line_counter = 0
    font = pygame.font.SysFont("comicsans", 10)
    for item in text_list:
        text = font.render(item, 1, (0, 0, 0))
        line_length = line_length + text.get_width()
        print(item, line_length)
        if line_length < width:
            line.append(item)
        else:
            text2 = font.render(" ".join(line), 1, (0, 0, 0))
            win.blit(text2, (x, y + 20 * line_counter))
            line_counter = line_counter + 1
            line = [item]
            line_length = text.get_width()
    else:
        #line_counter = line_counter + 1
        text = font.render(" ".join(line), 1, (0, 0, 0))
        win.blit(text, (x, y + 20 * line_counter))

def change_offset(item_list, offset):
    for item2 in item_list:
        # print(item2.x)
        item2.x = item2.x + offset[0]
        item2.y = item2.y + offset[1]




def main(player_stats):
    stats = player_stats
    #stats.units_built.add(Units(96, 96, "tgr", 10, 1, 0, 0, "Axis_truck.png", False, "Axis", 100))
    #stats.units_built.add(Units(150, 80, "tgr5", 10, 0, 0, 0, "Allied_truck.png", False, "Allies", 100))
    #stats.units_built.add(Units(256, 256, "tgr56", 10, 0, 0, 0, "Allied_advanced_construction_worker.png", False, "Allies", 100))
    #stats.units_built.add(Units(512, 512, "tgr567", 10, 0, 0, 0, "Allied_advanced_construction_worker.png", False, "Allies", 100))
    #stats.units_built.add(Units(256, 256, "Workers", 10, 0, 0, 12, "Allied_advanced_construction_worker.png", False, "Allies", 100))
    #stats.units_built.add(Units(512, 512, "Workers", 10, 0, 0, 12, "Allied_advanced_construction_worker.png", False, "Allies", 100))
    #stats.buildings_built.add(Buildings(128, 128, "tgr5678", "Allied_factory.png", "IT; +10", 100, 0, 0, 100, 0, 0, "Allies"))
    #stats.buildings_built.add(Buildings(160, 160, "tgr5678", "Allied_refinery.png", "Nothing", 100, 0, 0, 100, 0, 0, "Allies"))
    tiles_group = pygame.sprite.Group()
    tiles_group_for_minimap = pygame.sprite.Group()
    cam = CameraGroup((0, 0), 32)
    if stats.team == "Allies":
        button_imgs = ["Allied_flag.png", "Applied_research.png", "Applied_stats.png", "Nothing"]
    else:
        button_imgs = ["Axis_flag.png", "Applied_research.png", "Applied_stats.png", "Nothing"]
    button_names = ["Flag", "Research", "Stats", "End Turn"]
    buttons_for_ui = []
    for x, y in enumerate(button_imgs):
        if button_names[x] == "End Turn":
            buttons_for_ui.append(Buttons(1080, 620, 200, 100, button_names[x], (255, 255, 255), y))
        else:
            buttons_for_ui.append(Buttons((x) * 100, 0, 100, 50, button_names[x], (255, 255, 255), y))
    for num in range(8040):
        #print((num - numpy.floor(num / 120) * 120) * 32)
        #print(numpy.floor(num / 120) * 32)
        tile = Tiles((num - numpy.floor(num / 120) * 120) * 32, numpy.floor(num / 120) * 32, "Plains", num)
        tiles_group.add(tile)
        if random.randint(1, 200) == 1:
            if random.randint(1, 3) == 1:
                stats.resource_deposits.add(Buildings((num - numpy.floor(num / 120) * 120) * 32, numpy.floor(num / 120) * 32, "Resource567", "Applied_metals.png", "Nothing", 100, 0, 0, 0, 0, 0, "No team"))
            elif random.randint(1, 3) == 2:
                stats.resource_deposits.add(Buildings((num - numpy.floor(num / 120) * 120) * 32, numpy.floor(num / 120) * 32, "Resource567", "Applied_organic_matter.png", "Nothing", 100, 0, 0, 0, 0, 0, "No team"))
            else:
                stats.resource_deposits.add(Buildings((num - numpy.floor(num / 120) * 120) * 32, numpy.floor(num / 120) * 32, "Resource567", "Applied_fuel.png", "Nothing", 100, 0, 0, 0, 0, 0, "No team"))
    for num in range(8040):
        tile = Tiles(num - numpy.floor(num / 120) * 120 + 1105, numpy.floor(num / 120) + 505, "Plains", num)
        tile.width = 1
        tile.height = 1
        tiles_group_for_minimap.add(tile)
    group_list = [tiles_group, stats.units_built, stats.buildings_built, stats.buildings, stats.resource_deposits]
    clock = pygame.time.Clock()
    run = True
    while True:
        clock.tick(60)
        win.fill((255,255,255))
        #tiles_group.draw(win)
        #tiles_group.update()
        #basic_ui(buttons_for_ui)
        cam.move_camera()
        buttons_for_unit_ui, worker = cam.custom_draw(buttons_for_ui, group_list, stats.units_built, tiles_group, tiles_group_for_minimap, stats)

        #buttons_for_unit_ui = unit_and_building_ui(stats)
        #apply_buffs(run, stats)
        pygame.display.update()
        #fighting(stats.units_built, stats.units_built, run, stats.units_fighting)
        #run = fighting(stats.units_built, stats.buildings_built, run, stats.units_fighting)
        #print(cam.offset)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_pos = pygame.mouse.get_pos()
                run, button_pressed = buttons_clicked(stats, run, buttons_for_ui, buttons_for_unit_ui, m_pos, stats.turn, worker)
                moving_sprite(stats, m_pos, tiles_group, button_pressed)

        # AI WILL GO HERE. PLEASE MAKE IT A FUNCTION.

        apply_buffs(run, stats)
        auto_collect(run, stats, "Fuel")
        auto_collect(run, stats, "Metals")
        auto_collect(run, stats, "Organics")
        #thread = threading.Thread(target = auto_collect, args = (run, stats))
        #thread.start
        auto_deposit(run, stats)
        collect_materials(run, stats)
        reset_units(run, stats)
        #auto_deposit(run, stats)
        print("Tokens: {}".format(stats.tokens))
        for item in stats.buildings:
            completed_building, stats.units_built, stats.units_working = item.build(stats.tokens, run, stats.turn, stats.units_built, stats.units_working)
            if completed_building != "No new building":
                stats.buildings.remove(item)
                stats.buildings_built.add(completed_building)
        fighting(stats, stats.units_built, stats.units_built, run, stats.units_fighting)
        #print("Sprites: {}".format(stats.units_built.sprites()))
        run = fighting(stats, stats.units_built, stats.buildings_built, run, stats.units_fighting)

def main_menu():
    button_list = [Buttons(490, 200, 300, 100, "Singleplayer", (0, 0, 0), "Nothing"), Buttons(490, 310, 300, 100, "Multiplayer", (0, 0, 0), "Nothing"), Buttons(490, 420, 300, 100, "Settings", (0,0,0), "Nothing")]
    img_list_for_nations = ["img/Allied_flag.png", "img/Axis_flag.png"]
    support_buttons_for_nations = [Buttons(1180, 0, 100, 64, "Go back", (0, 0, 0), "Nothing"), Buttons(490, 650, 300, 64, "Start Game", (0, 0, 0), "Nothing"), Buttons(1180, 400, 100, 64, "Next", (0, 0, 0), "Arrow.png"), Buttons(0, 400, 100, 64, "Before", (0, 0, 0), "Arrow.png")]
    support_buttons_for_nations[3].image = pygame.transform.flip(support_buttons_for_nations[3].image, True, False)
    bg = pygame.image.load("img/Background.png")
    bg = pygame.transform.scale(bg, (1280, 720))
    while True:
        win.blit(bg, (0, 0))
        font = pygame.font.SysFont("comicsans", 70)
        text = font.render("PyCiv", 1, (0, 0, 0))
        win.blit(text, (640 - text.get_width()/2, 50))
        for btn in button_list:
            btn.draw(win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                m_pos = pygame.mouse.get_pos()
                for btn in button_list:
                    if btn.click(m_pos):
                        if btn.text == "Singleplayer":
                            win.fill((255, 255, 255))
                            allied_leader = pygame.image.load("img/Allied_leader.png").convert_alpha()
                            axis_leader = pygame.image.load("img/Axis_leader.png").convert_alpha()
                            allied_leader = pygame.transform.scale(allied_leader, (128, 128))
                            axis_leader = pygame.transform.scale(axis_leader, (128, 128))
                            run = True
                            counter = 0
                            while run:
                                win.blit(bg, (0, 0))
                                pygame.draw.rect(win, (128, 128, 128), (300, 50, 680, 50))
                                pygame.draw.rect(win, (128, 128, 128), (100, 100, 1080, 520))
                                pygame.draw.rect(win, (0, 0, 0), (150, 120, 390, 300), 4)
                                pygame.draw.rect(win, (0, 0, 0), (740, 120, 390, 300), 4)
                                font = pygame.font.SysFont("comicsans", 20)
                                text = font.render("Do you want to play as...", 1, (0, 0, 0))
                                win.blit(text, (640 - text.get_width()/2, 50))
                                text = font.render("History", 1, (0, 0, 0))
                                win.blit(text, (150 + 390/2 - text.get_width() / 2, 140))
                                if counter == 0:
                                    multilines("Born during the fire of the American Revolution, the United States established independence from Great Britain in 1776 after economic maltreatment. By conquering the resource-rich lands of the west, fighting a minimal amount of European powers and embracing industrialization, the United States soon became the world's largest economy. In 1918, the United States joined the First World War, further cementing it's hedgemony over the North American continent. Unfortuantely, the American economy, and by extension the world was soon in a major depression. With economic power souring, the public turning against Republican rule, and a new president, Roosevelt, being elected, the United States finds itself at the turn of a new era.", 160, 170, 340)
                                else:
                                    multilines("After the disillusionment of the defeat in 1918, the German nation finds itself in ruins. With the Treaty of Versaille disarming it, obliterating it's economy, and eliminating all it's colonies, the new democratic Government finds itself in a difficult situation. Things only gets worse as the great depression hits while the Nazi party recruits new members and eliminates the socialists within it's ranks. After the rise of Kurt von Schleicher the office of Chancellory soon turns into chaos as the scheming general maneuvers his way to power. Unforunately for him though, the Nazis know his weaknesses, and soon force him to resign, with their own leader Adolf Hitler entering the office. With Hindenburg almost dead, and the Communists about to be blown up, the German people rise to their new Fuhrer.", 160, 170, 340)
                                text = font.render("Some information", 1, (0, 0, 0))
                                win.blit(text, (740 + 390 / 2 - text.get_width() / 2, 140))
                                if counter == 0:
                                    font = pygame.font.SysFont("comicsans", 10)
                                    text = font.render("Factories: 2", 1, (0, 0, 0))
                                    win.blit(text, (750, 170))
                                    text = font.render("Refineries: 3", 1, (0, 0, 0))
                                    win.blit(text, (750, 190))
                                    text = font.render("Barracks: 1", 1, (0, 0, 0))
                                    win.blit(text, (750, 210))
                                    text = font.render("Flight school: 1", 1, (0, 0, 0))
                                    win.blit(text, (750, 230))
                                    text = font.render("Construction workers: 5", 1, (0, 0, 0))
                                    win.blit(text, (750, 250))
                                    text = font.render("Infantry: 3", 1, (0, 0, 0))
                                    win.blit(text, (750, 270))
                                else:
                                    font = pygame.font.SysFont("comicsans", 10)
                                    text = font.render("Factories: 1", 1, (0, 0, 0))
                                    win.blit(text, (750, 170))
                                    text = font.render("Refineries: 3", 1, (0, 0, 0))
                                    win.blit(text, (750, 190))
                                    text = font.render("Barracks: 3", 1, (0, 0, 0))
                                    win.blit(text, (750, 210))
                                    text = font.render("Tank school: 2", 1, (0, 0, 0))
                                    win.blit(text, (750, 230))
                                    text = font.render("Flight school: 2", 1, (0, 0, 0))
                                    win.blit(text, (750, 250))
                                    text = font.render("Construction workers: 3", 1, (0, 0, 0))
                                    win.blit(text, (750, 270))
                                    text = font.render("Infantry: 5", 1, (0, 0, 0))
                                    win.blit(text, (750, 290))
                                    text = font.render("Tanks: 2", 1, (0, 0, 0))
                                    win.blit(text, (750, 310))
                                    text = font.render("Fighters: 1", 1, (0, 0, 0))
                                    win.blit(text, (750, 330))
                                for btn in support_buttons_for_nations:
                                    btn.draw(win)
                                if counter == 0:
                                    font = pygame.font.SysFont("comicsans", 50)
                                    text = font.render("America", 1, (0, 0, 0))
                                    win.blit(text, (640 - text.get_width() / 2, 75))
                                    win.blit(allied_leader, (564, 150))
                                elif counter == 1:
                                    font = pygame.font.SysFont("comicsans", 50)
                                    text = font.render("Germany", 1, (0, 0, 0))
                                    win.blit(text, (640 - text.get_width() / 2, 75))
                                    win.blit(axis_leader, (576, 150))
                                else:
                                    pass
                                img = pygame.image.load(img_list_for_nations[counter])
                                img = pygame.transform.scale(img, (128, 128))
                                win.blit(img, (576, 278))
                                pygame.display.update()
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                                    elif event.type == pygame.MOUSEBUTTONDOWN:
                                        m_pos = pygame.mouse.get_pos()
                                        for btn in support_buttons_for_nations:
                                            if btn.click(m_pos):
                                                if btn.text == "Next":
                                                    if counter == 1:
                                                        counter = 0
                                                    else:
                                                        counter = counter + 1
                                                elif btn.text == "Before":
                                                    if counter == 1:
                                                        counter = 0
                                                    else:
                                                        counter = counter + 1
                                                elif btn.text == "Start Game":
                                                    positions_x = [32 * x for x in range(2, 25)]
                                                    positions_y = [32 * x for x in range(2, 25)]
                                                    if counter == 0:
                                                        stats = PlayerStats(0, 0, 0, 0, 0, 1, 0, 1, 0, 0, "Allies", 0)
                                                        stats.buildings_built.add(Buildings(positions_x.pop(random.randint(0, len(positions_x) - 1)), positions_y.pop(random.randint(0, len(positions_y) - 1)), "Capital", "Allied_capitol.png", "Nothing", 500, 0, 0, 0, 0, 0, "Allies"))
                                                        stats.buildings_built.add(Buildings(positions_x.pop(random.randint(0, len(positions_x) - 1)), positions_y.pop(random.randint(0, len(positions_y) - 1)), "Factory", "Allied_factory.png", "IT; 10", 100, 0, 0, 0, 0, 0, "Allies"))
                                                        stats.buildings_built.add(Buildings(positions_x.pop(random.randint(0, len(positions_x) - 1)), positions_y.pop(random.randint(0, len(positions_y) - 1)), "Factory", "Allied_factory.png", "IT; 10", 100, 0, 0, 0, 0, 0, "Allies"))
                                                        stats.buildings_built.add(Buildings(positions_x.pop(random.randint(0, len(positions_x) - 1)), positions_y.pop(random.randint(0, len(positions_y) - 1)), "Refinery", "Allied_refinery.png", "Nothing", 50, 0, 0, 0, 0, 0, "Allies"))
                                                        stats.buildings_built.add(Buildings(positions_x.pop(random.randint(0, len(positions_x) - 1)), positions_y.pop(random.randint(0, len(positions_y) - 1)), "Refinery", "Allied_refinery.png", "Nothing", 50, 0, 0, 0, 0, 0, "Allies"))
                                                        stats.buildings_built.add(Buildings(positions_x.pop(random.randint(0, len(positions_x) - 1)), positions_y.pop(random.randint(0, len(positions_y) - 1)), "Refinery", "Allied_refinery.png", "Nothing", 50, 0, 0, 0, 0, 0, "Allies"))
                                                        stats.buildings_built.add(Buildings(positions_x.pop(random.randint(0, len(positions_x) - 1)), positions_y.pop(random.randint(0, len(positions_y) - 1)), "Barrack", "Allied_barrack.png", "Nothing", 50, 0, 0, 0, 0, 0, "Allies"))
                                                        stats.buildings_built.add(Buildings(positions_x.pop(random.randint(0, len(positions_x) - 1)), positions_y.pop(random.randint(0, len(positions_y) - 1)), "Air school", "Allied_flight_school.png", "Nothing", 50, 0, 0, 0, 0, 0, "Allies"))
                                                        stats.units_built.add(Units(positions_x.pop(random.randint(0, len(positions_x) - 1)), positions_y.pop(random.randint(0, len(positions_y) - 1)), "Workers", 10, 1, 0, 10, "Allied_construction_worker.png", False, "Allies", 50))
                                                        stats.units_built.add(Units(positions_x.pop(random.randint(0, len(positions_x) - 1)), positions_y.pop(random.randint(0, len(positions_y) - 1)), "Workers", 10, 1, 0, 10, "Allied_construction_worker.png", False, "Allies", 50))
                                                        stats.units_built.add(Units(positions_x.pop(random.randint(0, len(positions_x) - 1)), positions_y.pop(random.randint(0, len(positions_y) - 1)), "Workers", 10, 1, 0, 10, "Allied_construction_worker.png", False, "Allies", 50))
                                                        stats.units_built.add(Units(positions_x.pop(random.randint(0, len(positions_x) - 1)), positions_y.pop(random.randint(0, len(positions_y) - 1)), "Workers", 10, 1, 0, 10, "Allied_construction_worker.png", False, "Allies", 50))
                                                        stats.units_built.add(Units(positions_x.pop(random.randint(0, len(positions_x) - 1)), positions_y.pop(random.randint(0, len(positions_y) - 1)), "Workers", 10, 1, 0, 10, "Allied_construction_worker.png", False, "Allies", 50))
                                                        stats.units_built.add(Units(positions_x.pop(random.randint(0, len(positions_x) - 1)), positions_y.pop(random.randint(0, len(positions_y) - 1)), "Infantry", 20, 7, 0, 5, "ally.png", False, "Allies", 50))
                                                        stats.units_built.add(Units(positions_x.pop(random.randint(0, len(positions_x) - 1)), positions_y.pop(random.randint(0, len(positions_y) - 1)), "Infantry", 20, 7, 0, 5, "ally.png", False, "Allies", 50))
                                                        stats.units_built.add(Units(positions_x.pop(random.randint(0, len(positions_x) - 1)), positions_y.pop(random.randint(0, len(positions_y) - 1)), "Infantry", 20, 7, 0, 5, "ally.png", False, "Allies", 50))
                                                        main(stats)
                                                    elif counter == 1:
                                                        stats = PlayerStats(0, 0, 0, 0, 0, 1, 0, 1, 0, 0, "Axis", 0)
                                                        stats.buildings_built.add(Buildings(positions_x.pop(random.randint(0, len(positions_x) - 1)), positions_y.pop(random.randint(0, len(positions_y) - 1)), "Capital", "Axis_capital.png", "Nothing", 500, 0, 0, 0, 0, 0, "Axis"))
                                                        stats.buildings_built.add(Buildings(positions_x.pop(random.randint(0, len(positions_x) - 1)), positions_y.pop(random.randint(0, len(positions_y) - 1)), "Factory", "Axis_factory.png", "IT; 10", 100, 0, 0, 0, 0, 0, "Axis"))
                                                        stats.buildings_built.add(Buildings(positions_x.pop(random.randint(0, len(positions_x) - 1)), positions_y.pop(random.randint(0, len(positions_y) - 1)), "Refinery", "Axis_refinery.png", "Nothing", 50, 0, 0, 0, 0, 0, "Axis"))
                                                        stats.buildings_built.add(Buildings(positions_x.pop(random.randint(0, len(positions_x) - 1)), positions_y.pop(random.randint(0, len(positions_y) - 1)), "Refinery", "Axis_refinery.png", "Nothing", 50, 0, 0, 0, 0, 0, "Axis"))
                                                        stats.buildings_built.add(Buildings(positions_x.pop(random.randint(0, len(positions_x) - 1)), positions_y.pop(random.randint(0, len(positions_y) - 1)), "Refinery", "Axis_refinery.png", "Nothing", 50, 0, 0, 0, 0, 0, "Axis"))
                                                        stats.buildings_built.add(Buildings(positions_x.pop(random.randint(0, len(positions_x) - 1)), positions_y.pop(random.randint(0, len(positions_y) - 1)), "Barrack", "Axis_barrack.png", "Nothing", 50, 0, 0, 0, 0, 0, "Axis"))
                                                        stats.buildings_built.add(Buildings(positions_x.pop(random.randint(0, len(positions_x) - 1)), positions_y.pop(random.randint(0, len(positions_y) - 1)), "Barrack", "Axis_barrack.png", "Nothing", 50, 0, 0, 0, 0, 0, "Axis"))
                                                        stats.buildings_built.add(Buildings(positions_x.pop(random.randint(0, len(positions_x) - 1)), positions_y.pop(random.randint(0, len(positions_y) - 1)), "Barrack", "Axis_barrack.png", "Nothing", 50, 0, 0, 0, 0, 0, "Axis"))
                                                        stats.buildings_built.add(Buildings(positions_x.pop(random.randint(0, len(positions_x) - 1)), positions_y.pop(random.randint(0, len(positions_y) - 1)), "Tank school", "Axis_tank_school.png", "Nothing", 50, 0, 0, 0, 0, 0, "Axis"))
                                                        stats.buildings_built.add(Buildings(positions_x.pop(random.randint(0, len(positions_x) - 1)), positions_y.pop(random.randint(0, len(positions_y) - 1)), "Tank school", "Axis_tank_school.png", "Nothing", 50, 0, 0, 0, 0, 0, "Axis"))
                                                        stats.buildings_built.add(Buildings(positions_x.pop(random.randint(0, len(positions_x) - 1)), positions_y.pop(random.randint(0, len(positions_y) - 1)), "Air school", "Axis_flight_school.png", "Nothing", 50, 0, 0, 0, 0, 0, "Axis"))
                                                        stats.buildings_built.add(Buildings(positions_x.pop(random.randint(0, len(positions_x) - 1)), positions_y.pop(random.randint(0, len(positions_y) - 1)), "Air school", "Axis_flight_school.png", "Nothing", 50, 0, 0, 0, 0, 0, "Axis"))
                                                        stats.units_built.add(Units(positions_x.pop(random.randint(0, len(positions_x) - 1)), positions_y.pop(random.randint(0, len(positions_y) - 1)), "Workers", 10, 1, 0, 10, "Axis_construction_worker.png", False, "Axis", 50))
                                                        stats.units_built.add(Units(positions_x.pop(random.randint(0, len(positions_x) - 1)), positions_y.pop(random.randint(0, len(positions_y) - 1)), "Workers", 10, 1, 0, 10, "Axis_construction_worker.png", False, "Axis", 50))
                                                        stats.units_built.add(Units(positions_x.pop(random.randint(0, len(positions_x) - 1)), positions_y.pop(random.randint(0, len(positions_y) - 1)), "Workers", 10, 1, 0, 10, "Axis_construction_worker.png", False, "Axis", 50))
                                                        stats.units_built.add(Units(positions_x.pop(random.randint(0, len(positions_x) - 1)), positions_y.pop(random.randint(0, len(positions_y) - 1)), "Infantry", 20, 7, 0, 5, "axis.png", False, "Axis", 50))
                                                        stats.units_built.add(Units(positions_x.pop(random.randint(0, len(positions_x) - 1)), positions_y.pop(random.randint(0, len(positions_y) - 1)), "Infantry", 20, 7, 0, 5,"axis.png", False, "Axis", 50))
                                                        stats.units_built.add(Units(positions_x.pop(random.randint(0, len(positions_x) - 1)), positions_y.pop(random.randint(0, len(positions_y) - 1)), "Infantry", 20, 7, 0, 5, "axis.png", False, "Axis", 50))
                                                        stats.units_built.add(Units(positions_x.pop(random.randint(0, len(positions_x) - 1)), positions_y.pop(random.randint(0, len(positions_y) - 1)), "Infantry", 20, 7, 0, 5, "axis.png", False, "Axis", 50))
                                                        stats.units_built.add(Units(positions_x.pop(random.randint(0, len(positions_x) - 1)), positions_y.pop(random.randint(0, len(positions_y) - 1)), "Infantry", 20, 7, 0, 5, "axis.png", False, "Axis", 50))
                                                        stats.units_built.add(Units(positions_x.pop(random.randint(0, len(positions_x) - 1)), positions_y.pop(random.randint(0, len(positions_y) - 1)), "Tanks", 40, 20, 0, 60, "Axis_light_tank.png", False, "Axis", 50))
                                                        stats.units_built.add(Units(positions_x.pop(random.randint(0, len(positions_x) - 1)), positions_y.pop(random.randint(0, len(positions_y) - 1)), "Tanks", 40, 20, 0, 60, "Axis_light_tank.png", False, "Axis", 50))
                                                        stats.units_built.add(Units(positions_x.pop(random.randint(0, len(positions_x) - 1)), positions_y.pop(random.randint(0, len(positions_y) - 1)), "Fighters", 20, 20, 20, 300, "Axis_fighter.png", False, "Axis", 50))
                                                        main(stats)
                                                    else:
                                                        pass
                                                else:
                                                    run = False
                                    else:
                                        pass
            else:
                pass

main_menu()