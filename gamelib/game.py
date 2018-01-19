#! /usr/bin/env python
import re
import sys, os
import random

import pygame
from pygame.locals import *

from cutscenes import *
from  data import *
from sprites import *
from level import *
import random
from NEAT.generation import *
import numpy as np
import pickle
import re

choices = ["SHORT JUMP", "LONG JUMP", "RIGHT", "LEFT"]


def RelRect(actor, camera):
    return Rect(actor.rect.x - camera.rect.x, actor.rect.y - camera.rect.y, actor.rect.w, actor.rect.h)


class Camera(object):
    def __init__(self, player, width):
        self.player = player
        self.rect = pygame.display.get_surface().get_rect()
        self.world = Rect(0, 0, width, 480)
        self.rect.center = self.player.rect.center

    def update(self):
        if self.player.rect.centerx > self.rect.centerx + 1:
            self.rect.centerx = self.player.rect.centerx - 64

        self.rect.clamp_ip(self.world)

    def draw_sprites(self, surf, sprites):
        for s in sprites:
            if s.rect.colliderect(self.rect):
                surf.blit(s.image, RelRect(s, self))


        # return pygame.display.get_surface().


def save_level(lvl):
    open(filepath("saves/prog.sav"), "w").write(str(lvl))


def get_saved_level():
    try:
        return int(open(filepath("saves/prog.sav")).read())
    except:
        open(filepath("saves/prog.sav"), "w").write(str(1))
        return 1


def save_coin(coin):
    open(filepath("saves/coin.sav"), "w").write(str(coin))


def get_saved_coin():
    try:
        return int(open(filepath("saves/coin.sav")).read())
    except:
        open(filepath("saves/coin.sav"), "w").write(str(1))
        return 1


def save_score(score):
    open(filepath("saves/score.sav"), "w").write(str(score))


def get_saved_score():
    try:
        return int(open(filepath("saves/score.sav")).read())
    except:
        open(filepath("saves/score.sav"), "w").write(str(1))
        return 1


def save_lives(lives):
    open(filepath("saves/lives.sav"), "w").write(str(lives))


def get_saved_lives():
    try:
        return int(open(filepath("saves/lives.sav")).read())
    except:
        open(filepath("saves/lives.sav"), "w").write(str(1))
        return 1


class Game(object):
    def __init__(self, continuing=False):
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        # pygame.mixer.pre_init(44100, -16, 2, 4096)

        pygame.init()
        pygame.mouse.set_visible(0)
        pygame.display.set_icon(pygame.image.load(filepath("bowser1.gif")))
        pygame.display.set_caption("Super Mario Python")
        screen = pygame.display.set_mode((640, 480), HWSURFACE | DOUBLEBUF | RESIZABLE)
        self.generation = None
        self.current_fitness = 0
        self.last_fitness = 0
        self.countdown_time = 2
        self.start_new_game = False

        self.screen = screen
        self.sprites = pygame.sprite.OrderedUpdates()
        self.players = pygame.sprite.OrderedUpdates()
        self.platforms = pygame.sprite.OrderedUpdates()
        self.platformblues = pygame.sprite.OrderedUpdates()
        self.grasss = pygame.sprite.OrderedUpdates()
        self.grays = pygame.sprite.OrderedUpdates()
        self.bricks = pygame.sprite.OrderedUpdates()
        self.brickblues = pygame.sprite.OrderedUpdates()
        self.movingplatforms = pygame.sprite.OrderedUpdates()
        self.movingplatformtwos = pygame.sprite.OrderedUpdates()
        self.undergrounds = pygame.sprite.OrderedUpdates()
        self.baddies = pygame.sprite.OrderedUpdates()
        self.cannons = pygame.sprite.OrderedUpdates()
        self.flowers = pygame.sprite.OrderedUpdates()
        self.flowertwos = pygame.sprite.OrderedUpdates()
        self.flowerthrees = pygame.sprite.OrderedUpdates()
        self.firebowsers = pygame.sprite.OrderedUpdates()
        self.spikeshots = pygame.sprite.OrderedUpdates()
        self.roses = pygame.sprite.OrderedUpdates()
        self.nomoveplatforms = pygame.sprite.OrderedUpdates()
        self.coins = pygame.sprite.OrderedUpdates()
        self.playerdying = pygame.sprite.OrderedUpdates()
        self.bombs = pygame.sprite.OrderedUpdates()
        self.shots = pygame.sprite.OrderedUpdates()
        self.springs = pygame.sprite.OrderedUpdates()
        self.bosses = pygame.sprite.OrderedUpdates()
        self.platformqs = pygame.sprite.OrderedUpdates()
        self.mushroomgreens = pygame.sprite.OrderedUpdates()
        self.axes = pygame.sprite.OrderedUpdates()
        self.bridges = pygame.sprite.OrderedUpdates()
        self.toads = pygame.sprite.OrderedUpdates()
        self.spikers = pygame.sprite.OrderedUpdates()
        self.skys = pygame.sprite.OrderedUpdates()
        self.pipegreenends = pygame.sprite.OrderedUpdates()
        self.flag2s = pygame.sprite.OrderedUpdates()
        self.pipeends = pygame.sprite.OrderedUpdates()
        self.flowerblues = pygame.sprite.OrderedUpdates()
        self.mountains = pygame.sprite.OrderedUpdates()
        self.hill2 = pygame.sprite.OrderedUpdates()
        self.bush2 = pygame.sprite.OrderedUpdates()
        self.bush3 = pygame.sprite.OrderedUpdates()
        Player.right_images = [load_image("mario1.png"), load_image("mario2.png"), load_image("mario3.png"),
                               load_image("mario4.png"), load_image("mario5.png")]
        Platform.images = {"platform-top.png": load_image("platform-top.png"),
                           "platform-middle.png": load_image("platform-top.png")}
        Platformblue.images = {"platform-blue1.png": load_image("platform-blue1.png"),
                               "platform-blue2.png": load_image("platform-blue1.png")}
        Grass.images = {"grass-1.png": load_image("grass-1.png"), "grass-middle.png": load_image("grass-middle.png")}
        Mountain.images = {"mountains1.png": load_image("mountains1.png"),
                           "mountains2.png": load_image("mountains2.png")}
        Gray.images = {"gray1.png": load_image("gray1.png"), "gray2.png": load_image("gray2.png")}
        Brick.images = {"brick1.png": load_image("brick1.png"), "brick2.png": load_image("brick2.png")}
        Brickblue.images = {"brickblue1.png": load_image("brickblue1.png"),
                            "brickblue2.png": load_image("brickblue2.png")}
        Bridge.images = {"bridge.png": load_image("bridge.png"), "bridge2.png": load_image("bridge2.png")}
        MovingPlatform.image = load_image("moving-platform.png")
        Firebowser.images = [load_image("bowser-fireball%s.png" % i) for i in range(1, 3)]
        MovingPlatformtwo.image = load_image("moving-platformlong.png")
        Underground.image = load_image("moving-platformlong.png")
        Baddie.left_images1 = [load_image("monster%d.png" % i) for i in range(1, 3)]
        Baddie.left_images2 = [load_image("slub%d.png" % i) for i in range(1, 3)]
        Baddie.left_images3 = [load_image("squidge%d.png" % i) for i in range(1, 3)]
        Baddie.left_images4 = [load_image("monster-red%d.png" % i) for i in range(1, 3)]
        Baddie.left_images5 = [load_image("slubblue%d.png" % i) for i in range(1, 3)]
        Baddie.left_images6 = [load_image("bluemonster%d.png" % i) for i in range(1, 3)]
        Baddie.left_images7 = [load_image("black%d.png" % i) for i in range(1, 3)]
        Cannon.left_images1 = [load_image("cannon%d.png" % i) for i in range(1, 3)]
        Cannon.left_images2 = [load_image("cannonbig%d.png" % i) for i in range(1, 3)]
        Cannon.left_images4 = [load_image("smallcannon%d.png" % i) for i in range(1, 3)]
        Spiker.left_images1 = [load_image("spiker%d.png" % i) for i in range(1, 3)]
        Sky.left_images1 = [load_image("sky%d.png" % i) for i in range(1, 2)]
        BaddieBoom.left_images1 = [load_image("monster2.png"), load_image("monster3.png"), load_image("exp1.png"),
                                   load_image("exp2.png"), load_image("exp3.png")]
        BaddieBoom.left_images2 = [load_image("slub2.png"), load_image("slub3.png"), load_image("exp1.png"),
                                   load_image("exp2.png"), load_image("exp3.png")]
        BaddieBoom.left_images3 = [load_image("squidge2.png"), load_image("squidge3.png"), load_image("exp1.png"),
                                   load_image("exp2.png"), load_image("exp3.png")]
        BaddieBoom.left_images4 = [load_image("monster-red2.png"), load_image("monster-red3.png"),
                                   load_image("exp1.png"), load_image("exp2.png"), load_image("exp3.png")]
        BaddieBoom.left_images5 = [load_image("slubblue2.png"), load_image("slubblue3.png"), load_image("exp1.png"),
                                   load_image("exp2.png"), load_image("exp3.png")]
        BaddieBoom.left_images6 = [load_image("bluemonster2.png"), load_image("bluemonster3.png"),
                                   load_image("exp1.png"), load_image("exp2.png"), load_image("exp3.png")]
        BaddieBoom.left_images7 = [load_image("black2.png"), load_image("black3.png"), load_image("exp1.png"),
                                   load_image("exp2.png"), load_image("exp3.png")]
        Coin.images = [load_image("coin%s.png" % i) for i in range(1, 5)]
        CoinDie.images = [load_image("exp2-%d.png" % i) for i in range(1, 4)]
        PlayerDie.right_images = [load_image("mariodie.png"), load_image("exp2-1.png"), load_image("exp2-2.png"),
                                  load_image("exp2-3.png")]
        Bomb.image = load_image("flagpole.png")
        Flag2.image = load_image("flagpole.png")
        Toad.image = load_image("toad.png")
        BaddieShot.image = load_image("shot.png")
        SpikeShot.images = [load_image("spikeshot%s.png" % i) for i in range(1, 3)]
        Fireball.images = [load_image("bowser-fireball%s.png" % i) for i in range(1, 3)]
        CannonShot.image = load_image("cannonbullet1.png")
        CannonShotbig.image = load_image("cannonbullet1.png")
        CannonShotsmall.image = load_image("cannonbullet1.png")
        Spring.images = [load_image("spring1.png"), load_image("spring2.png")]
        AirPlatform.image = load_image("platform-air.png")
        AirPlatformblue.image = load_image("platform-blue3.png")
        PlatformQ.images = [load_image("platform-q%s.png" % i) for i in range(1, 4)]
        Pipe.image = load_image("pipe.png")
        Flag.image = load_image("flagpole.png")
        Castle.image = load_image("castle.png")
        Castlebig.image = load_image("castle-big.png")
        Hill.image = load_image("hill.png")
        Bush.image = load_image("bush-1.png")
        Bush2.image = load_image("bush-2.png")
        Bush3.image = load_image("bush-3.png")
        Cloud.image = load_image("cloud.png")
        Cloud2.image = load_image("dobbelclouds.png")
        Platform_Brick.image = load_image("platform-brick.png")
        Boss.left_images = [load_image("bowser1.png"), load_image("bowser2.png"), load_image("bowser3.png"),
                            load_image("bowser4.png")]
        Flower.left_images1 = [load_image("flower%d.png" % i) for i in range(1, 2)]
        Flowertwo.left_images1 = [load_image("flower%d.png" % i) for i in range(1, 2)]
        Flowerthree.left_images1 = [load_image("flower%d.png" % i) for i in range(1, 2)]
        Flowerblue.left_images1 = [load_image("blueflower%d.png" % i) for i in range(1, 2)]
        MushroomGreen.image = load_image("mushroom-green.png")
        MushroomGreendie.images = [load_image("exp2-%d.png" % i) for i in range(1, 4)]
        Axe.image = load_image("trigger.png")
        AxeDie.images = [load_image("exp2-%d.png" % i) for i in range(1, 4)]
        PipeBig.image = load_image("pipe-big.png")
        Fence.image = load_image("fence.png")
        Tree1.image = load_image("tree-1.png")
        Tree2.image = load_image("tree-2.png")
        Rose.image = load_image("rose2.png")
        Grasstexture.image = load_image("grass-texture.png")
        Grass1.image = load_image("grass-1.png")
        Grass2.image = load_image("grass-2.png")
        GrassSprite.image = load_image("grass-texturesprite.png")
        Wall.image = load_image("wall-1.png")
        Lava.image = load_image("lava.png")
        Chain.image = load_image("chain.png")
        Invisiblewall.image = load_image("invisible_wall.png")
        PipeEnd.image = load_image("pipe-end.png")
        PipeDown.image = load_image("pipe_down.png")
        PipeGreen.image = load_image("pipe_green.png")
        PipeGreenBig.image = load_image("pipe_greenbig.png")
        PipeGreenEnd.image = load_image("pipe_greenend.png")
        Railing.image = load_image("railing.png")
        Hill2.image = load_image("hill2.png")

        Player.groups = self.sprites, self.players
        Platform.groups = self.sprites, self.platforms, self.nomoveplatforms
        Platformblue.groups = self.sprites, self.platformblues, self.nomoveplatforms
        Grass.groups = self.sprites, self.grasss, self.nomoveplatforms
        Brick.groups = self.sprites, self.bricks, self.nomoveplatforms
        Brickblue.groups = self.sprites, self.brickblues, self.nomoveplatforms
        Gray.groups = self.sprites, self.grays, self.nomoveplatforms
        MovingPlatform.groups = self.sprites, self.platforms, self.movingplatforms
        MovingPlatformtwo.groups = self.sprites, self.platforms, self.movingplatformtwos
        Underground.groups = self.sprites, self.platforms, self.undergrounds
        Baddie.groups = self.sprites, self.baddies
        Cannon.groups = self.sprites, self.cannons, self.platforms
        BaddieBoom.groups = self.sprites
        Coin.groups = self.sprites, self.coins
        CoinDie.groups = self.sprites
        MushroomGreen.groups = self.sprites, self.mushroomgreens
        MushroomGreendie.groups = self.sprites
        Axe.groups = self.sprites, self.axes
        AxeDie.groups = self.sprites
        PlayerDie.groups = self.sprites, self.playerdying
        Bomb.groups = self.sprites, self.bombs
        Toad.groups = self.sprites, self.toads
        BaddieShot.groups = self.sprites, self.shots
        SpikeShot.groups = self.sprites, self.shots, self.spikeshots
        Fireball.groups = self.sprites, self.shots
        CannonShot.groups = self.sprites, self.shots
        CannonShotbig.groups = self.sprites, self.shots
        CannonShotsmall.groups = self.sprites, self.shots
        Spring.groups = self.sprites, self.springs
        AirPlatform.groups = self.sprites, self.platforms, self.nomoveplatforms
        AirPlatformblue.groups = self.sprites, self.platforms, self.nomoveplatforms
        Pipe.groups = self.sprites, self.platforms, self.nomoveplatforms
        PlatformQ.groups = self.sprites, self.platformqs, self.platforms
        Platform_Brick.groups = self.sprites, self.platforms, self.nomoveplatforms
        Flag.groups = self.sprites
        Flag2.groups = self.sprites, self.flag2s
        Castle.groups = self.sprites
        Castlebig.groups = self.sprites
        Cloud.groups = self.sprites
        Cloud2.groups = self.sprites
        Bush.groups = self.sprites
        Hill.groups = self.sprites
        Boss.groups = self.sprites, self.bosses
        Flower.groups = self.sprites, self.flowers
        Flowertwo.groups = self.sprites, self.flowertwos
        Flowerthree.groups = self.sprites, self.flowerthrees
        Flowerblue.groups = self.sprites, self.flowerblues
        PipeBig.groups = self.sprites, self.platforms, self.nomoveplatforms
        Firebowser.groups = self.sprites, self.firebowsers
        Fence.groups = self.sprites
        Tree1.groups = self.sprites
        Tree2.groups = self.sprites
        Rose.groups = self.sprites, self.roses
        Grasstexture.groups = self.sprites, self.platforms, self.nomoveplatforms
        Grass1.groups = self.sprites, self.platforms, self.nomoveplatforms
        Grass2.groups = self.sprites, self.platforms, self.nomoveplatforms
        GrassSprite.groups = self.sprites
        Wall.groups = self.sprites
        Lava.groups = self.sprites
        Bridge.groups = self.sprites, self.bridges, self.platforms, self.nomoveplatforms
        Chain.groups = self.sprites
        Invisiblewall.groups = self.sprites, self.platforms, self.nomoveplatforms
        Spiker.groups = self.sprites, self.spikers
        PipeEnd.groups = self.sprites, self.pipeends
        Sky.groups = self.sprites, self.skys
        PipeDown.groups = self.sprites
        PipeGreen.groups = self.sprites, self.platforms, self.nomoveplatforms
        PipeGreenBig.groups = self.sprites, self.platforms, self.nomoveplatforms
        PipeGreenEnd.groups = self.sprites, self.pipegreenends
        Mountain.groups = self.sprites, self.nomoveplatforms, self.mountains, self.platforms
        Railing.groups = self.sprites
        Hill2.groups = self.sprites
        Bush2.groups = self.sprites
        Bush3.groups = self.sprites

        self.score = 0
        self.coin = 0
        self.lives = 99
        self.lvl = 1  # Edit what level to start at
        if continuing:
            self.lvl = get_saved_level()
            self.coin = 0
            self.score = 0
            self.lives = 99
        self.player = Player((0, 0))
        self.clock = pygame.time.Clock()
        self.bg = load_image("background-2.png")
        self.level = Level(self.lvl)
        self.camera = Camera(self.player, self.level.get_size()[0])
        self.font = pygame.font.Font(filepath("fonts/font.ttf"), 16)
        self.heart1 = load_image("mario1.png")
        self.heart2 = load_image("mario-life2.png")
        self.heroimg = load_image("mario5.png")
        self.heroimg2 = load_image("coin1.png")
        # self.baddie_sound = load_sound("jump2.ogg")
        # self.coin_sound = load_sound("coin.ogg")
        # self.hurry_sound = load_sound("hurry-main.ogg", 0.05)
        # self.win_sound = load_sound("miniboss.ogg", 0.05)
        # self.up_sound = load_sound("1up.ogg")
        # self.pipe_sound = load_sound("pipe.ogg")
        # self.bonus_sound = load_sound("bonus.ogg")
        # self.bowser_sound = load_sound("bowser.ogg", 0.08)
        self.time = 400
        self.running = 1
        self.booming = True
        self.boom_timer = 0
        # self.music = "maintheme.ogg"
        # if self.lvl == 1:
        #     self.intro_level()
        # if self.lvl == 2:
        #     self.intro_level()
        # if self.lvl == 3:
        #     self.world1_2()
        # if self.lvl == 4:
        #     self.world1_2()
        # if self.lvl == 5:
        #     self.world1_3()
        # if self.lvl == 6:
        #     self.world1_4()
        #     if continuing:
        #         # self.music = "castle.ogg"
        #         self.bg = load_image("background-1.png")
        # if self.lvl == 7:
        #     self.world2_1()
        # if self.lvl == 8:
        #     self.world2_2()
        # if self.lvl == 9:
        #     self.time = 250
        #     self.world2_3()
        # if self.lvl == 10:
        #     self.time = 250
        #     self.world2_4()
        #     if continuing:
        #         self.bg = load_image("background-1.png")
        # if self.lvl == 11:
        #     self.time = 250
        #     self.world2_5()
        #     if continuing:
        #         self.bg = load_image("background-2.png")

        # if not continuing:
            # stop_music()
        # self.neural_network.initialize_generation()

        filelist = []
        save_path = os.getcwd() + "/records/generation/"
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        for file in os.listdir(save_path):
            if file.endswith(".json") and re.match(r'generation_', file):
                filelist.append(file)
        if len(filelist) >= 1:
            filelist.sort(cmp=lambda x, y : 1 if self.find_number(x) - self.find_number(y) > 0 else
                                            0 if self.find_number(x) == self.find_number(y) else -1)
            with open(save_path + filelist[len(filelist) -1], 'rb') as f:
                self.generation = pickle.load(f)

        self.main_loop()

    def end(self):
        self.running = 0

    def intro_level(self):
        # stop_music()
        self.screen.fill((0, 0, 0))
        self.draw_stats()
        ren = self.font.render("World 1-%d" % self.lvl, 1, (255, 255, 255))
        self.screen.blit(ren, (320 - ren.get_width() / 2, 230))
        ren = self.font.render("Lives x%d" % self.lives, 1, (255, 255, 255))
        self.screen.blit(ren, (320 - ren.get_width() / 2, 255))
        # pygame.display.flip()
        pygame.time.wait(1000)
        # play_music(self.music)

    def world1_2(self):
        # stop_music()
        self.screen.fill((0, 0, 0))
        self.draw_stats()
        if self.lvl == 3:  # (World 1-2)
            ren = self.font.render("World 1-2", 1, (255, 255, 255))
            self.screen.blit(ren, (320 - ren.get_width() / 2, 230))
        if self.lvl == 4:
            ren = self.font.render("World 1-2", 1, (255, 255, 255))
            self.screen.blit(ren, (320 - ren.get_width() / 2, 230))
        ren = self.font.render("Lives x%d" % self.lives, 1, (255, 255, 255))
        self.screen.blit(ren, (320 - ren.get_width() / 2, 255))
        pygame.display.flip()
        pygame.time.wait(2500)
        # play_music(self.music)

    def world1_3(self):
        # stop_music()
        self.screen.fill((0, 0, 0))
        self.draw_stats()
        if self.lvl == 5:  # (World 1-3)
            ren = self.font.render("World 1-3", 1, (255, 255, 255))
            self.screen.blit(ren, (320 - ren.get_width() / 2, 230))
        ren = self.font.render("Lives x%d" % self.lives, 1, (255, 255, 255))
        self.screen.blit(ren, (320 - ren.get_width() / 2, 255))
        pygame.display.flip()
        pygame.time.wait(2500)
        # play_music(self.music)

    def world1_4(self):
        # stop_music()
        self.screen.fill((0, 0, 0))
        self.draw_stats()
        if self.lvl == 6:  # (World 1-4)
            ren = self.font.render("World 1-4", 1, (255, 255, 255))
            self.screen.blit(ren, (320 - ren.get_width() / 2, 230))
        ren = self.font.render("Lives x%d" % self.lives, 1, (255, 255, 255))
        self.screen.blit(ren, (320 - ren.get_width() / 2, 255))
        pygame.display.flip()
        pygame.time.wait(2500)
        # play_music(self.music)

    def world2_1(self):
        # stop_music()
        self.screen.fill((0, 0, 0))
        self.draw_stats()
        if self.lvl == 7:  # (World 2-1)
            ren = self.font.render("World 2-1", 1, (255, 255, 255))
            self.screen.blit(ren, (320 - ren.get_width() / 2, 230))
        ren = self.font.render("Lives x%d" % self.lives, 1, (255, 255, 255))
        self.screen.blit(ren, (320 - ren.get_width() / 2, 255))
        pygame.display.flip()
        pygame.time.wait(2500)
        # play_music(self.music)

    def world2_2(self):
        # stop_music()
        self.screen.fill((0, 0, 0))
        self.draw_stats()
        if self.lvl == 8:  # (World 2-2)
            ren = self.font.render("World 2-2", 1, (255, 255, 255))
            self.screen.blit(ren, (320 - ren.get_width() / 2, 230))
        ren = self.font.render("Lives x%d" % self.lives, 1, (255, 255, 255))
        self.screen.blit(ren, (320 - ren.get_width() / 2, 255))
        pygame.display.flip()
        pygame.time.wait(2500)
        # play_music(self.music)

    def world2_3(self):
        # stop_music()
        self.screen.fill((0, 0, 0))
        self.draw_stats()
        if self.lvl == 9:  # (World 2-3)
            ren = self.font.render("World 2-3", 1, (255, 255, 255))
            self.screen.blit(ren, (320 - ren.get_width() / 2, 230))
        ren = self.font.render("Lives x%d" % self.lives, 1, (255, 255, 255))
        self.screen.blit(ren, (320 - ren.get_width() / 2, 255))
        pygame.display.flip()
        pygame.time.wait(2500)
        # play_music(self.music)

    def world2_4(self):
        # stop_music()
        self.screen.fill((0, 0, 0))
        self.draw_stats()
        if self.lvl == 10:  # (World 2-4)
            ren = self.font.render("World 2-4", 1, (255, 255, 255))
            self.screen.blit(ren, (320 - ren.get_width() / 2, 230))
        ren = self.font.render("Lives x%d" % self.lives, 1, (255, 255, 255))
        self.screen.blit(ren, (320 - ren.get_width() / 2, 255))
        pygame.display.flip()
        pygame.time.wait(2500)
        # play_music(self.music)

    def world2_5(self):
        # stop_music()
        self.screen.fill((0, 0, 0))
        self.draw_stats()
        if self.lvl == 11:  # (World FINAL)
            ren = self.font.render("FINAL CHAPTER", 1, (255, 255, 255))
            self.screen.blit(ren, (320 - ren.get_width() / 2, 230))
        ren = self.font.render("Lives x%d" % self.lives, 1, (255, 255, 255))
        self.screen.blit(ren, (320 - ren.get_width() / 2, 255))
        pygame.display.flip()
        pygame.time.wait(2500)
        # play_music(self.music)

    def next_level(self):

        # self.hurry_sound.stop()
        # self.bowser_sound.stop()
        self.time = 400
        self.booming = True
        self.boom_timer = 0
        try:
            self.lvl = 1
            self.coin == 0
            self.score == 0
            self.lives == 99

            if self.lvl == 1:
                self.intro_level()
            if self.lvl == 2:
                self.intro_level()
            # if self.lvl == 4:
                #self.music = "maintheme.ogg"
            if self.lvl == 5:
                self.world1_3()
                self.booming = False
            if self.lvl == 6:
                # self.music = "castle.ogg"
                self.world1_4()
                self.booming = False
            if self.lvl == 7:
                # self.music = "maintheme.ogg"
                self.world2_1()
                self.booming = False
            if self.lvl == 8:
                self.world2_2()
                self.booming = False
            if self.lvl == 9:
                self.time = 250
                self.world2_3()
                self.booming = False
            if self.lvl == 10:
                self.time = 250
                self.world2_4()
                self.booming = False
            if self.lvl == 11:
                self.time = 250
                self.world2_5()
                self.booming = False

            self.clear_sprites()
            self.level = Level(self.lvl)
            self.player = Player((0, 430))
            self.camera = Camera(self.player, self.level.get_size()[0])
            save_level(1)
            save_coin(0)
            save_score(0)
            save_lives(99)
        except:
            if self.lives == 0:  # Fix
                self.lives = 99
            cutscene(self.screen,
                     ["Thank you for playing!",
                      "",
                      "",
                      "Check out the tutorial on how",
                      "to create your own levels!",
                      "Follow the guideline",
                      "in the picture",
                      "in the main folder.",
                      "",
                      "",
                      "The end"])
            self.screen.fill((0, 0, 0))
            # play_music("bonus.ogg")

            ren = self.font.render("Your Run:", 1, (255, 255, 255))
            self.screen.blit(ren, (320 - ren.get_width() / 2, 180))
            ren = self.font.render("Score%06d" % self.score, 1, (255, 255, 255))
            self.screen.blit(ren, (320 - ren.get_width() / 2, 210))
            ren = self.font.render("Lives%d" % self.lives, 1, (255, 255, 255))
            self.screen.blit(ren, (320 - ren.get_width() / 2, 240))
            ren = self.font.render("Coins%02d" % self.coin, 1, (255, 255, 255))
            self.screen.blit(ren, (320 - ren.get_width() / 2, 270))
            self.screen.blit(self.heroimg2, (240, 260))
            pygame.display.flip()
            pygame.time.wait(6000)
            self.end()

    def redo_level(self):
        self.booming = False
        self.boom_timer = 0
        self.time = 400
        self.score = 0

        if self.running:
            self.clear_sprites()
            self.level = Level(self.lvl)
            self.camera = Camera(self.player, self.level.get_size()[0])
            # self.hurry_sound.stop()
            # self.bowser_sound.stop()
            self.draw_stats()
            Chain.image = load_image("chain.png")
            # play_music("maintheme.ogg")
            # play_music("maintheme.ogg")
            if self.lvl == 1:
                self.player = Player((0, 430))  # Makes Player spawn at ground not mid-air.
                self.camera = Camera(self.player, self.level.get_size()[0])
            if self.lvl == 2:
                self.player = Player((0, 430))
                self.camera = Camera(self.player, self.level.get_size()[0])
            if self.lvl == 3:
                # play_music("underworld.ogg")
                self.player = Player((0, 0))  # Fall through pipe
                self.camera = Camera(self.player, self.level.get_size()[0])
                # self.pipe_sound.play()
            if self.lvl == 4:
                self.player = Player((0, 430))
                self.camera = Camera(self.player, self.level.get_size()[0])
                # self.pipe_sound.play()
            if self.lvl == 5:
                self.player = Player((0, 430))
                self.camera = Camera(self.player, self.level.get_size()[0])
            if self.lvl == 6:
                # play_music("castle.ogg")
                self.player = Player((0, 230))
                self.camera = Camera(self.player, self.level.get_size()[0])
            if self.lvl == 7:
                self.player = Player((0, 430))
                self.camera = Camera(self.player, self.level.get_size()[0])
            if self.lvl == 8:
                self.time = 250
                self.player = Player((0, 430))
                self.camera = Camera(self.player, self.level.get_size()[0])
            if self.lvl == 9:
                self.time = 250
                self.player = Player((0, 430))
                self.camera = Camera(self.player, self.level.get_size()[0])
            if self.lvl == 10:
                self.time = 250
                self.player = Player((0, 430))
                self.camera = Camera(self.player, self.level.get_size()[0])
            if self.lvl == 11:
                self.time = 250
                self.player = Player((0, 430))
                self.camera = Camera(self.player, self.level.get_size()[0])

    def show_death(self):
        # self.hurry_sound.stop()
        # self.bowser_sound.stop()
        ren = self.font.render("YOU DIED", 1, (255, 255, 255))
        self.screen.blit(ren, (320 - ren.get_width() / 2, 235))
        pygame.display.flip()
        pygame.time.wait(2500)

    def toad(self):
        ren = self.font.render("THE PRINCESS IS", 1, (255, 255, 255,))
        self.screen.blit(ren, (320 - ren.get_width() / 2, 235))
        ren = self.font.render("IN ANOTHER CASTLE!", 1, (255, 255, 255,))
        self.screen.blit(ren, (320 - ren.get_width() / 2, 255))
        pygame.display.flip()
        pygame.time.wait(5000)
        cutscene(self.screen,
                 ["",
                  "Normal story over",
                  "time for custom made maps",
                  ""])

    def show_end(self):
        # self.hurry_sound.stop()
        # self.bowser_sound.stop()
        # play_music("goal.ogg")
        pygame.time.wait(1000)
        pygame.display.flip()

    def gameover_screen(self):
        # self.hurry_sound.stop()
        # self.bowser_sound.stop()
        # stop_music()
        # play_music("gameover.ogg")
        cutscene(self.screen, ["Game Over"])
        self.end()

    def clear_sprites(self):
        for s in self.sprites:
            pygame.sprite.Sprite.kill(s)

    # MAIN PART:

    def main_loop(self):

        if self.generation is None:
            self.initialize_neural_network()
        while self.running:
            species = self.generation.species[self.generation.current_species]
            genome = species.genomes[self.generation.current_genome]

            BaddieShot.player = self.player
            Fireball.player = self.player
            CannonShot.player = self.player
            CannonShotbig.player = self.player
            CannonShotsmall.player = self.player
            SpikeShot.player = self.player
            if not self.running:
                return

            self.boom_timer -= 1

            self.clock.tick(60)
            self.camera.update()
            for s in self.sprites:
                s.update()

            if self.lvl == 3:
                self.bg = load_image("background-1.png")
                # self.music = "underworld.ogg"
            else:
                if self.lvl == 4:
                    self.bg = load_image("background-2.png")
                    # self.music = "maintheme.ogg"

            if self.lvl == 5:
                self.bg = load_image("background-2.png")
                # self.music = "maintheme.ogg"
            else:
                if self.lvl == 6:
                    self.bg = load_image("background-1.png")
                    # self.music = "castle.ogg"

            if self.lvl == 7:
                self.bg = load_image("background-2.png")
                # self.music = "maintheme.ogg"

            if self.lvl == 10:
                self.bg = load_image("background-1.png")
            if self.lvl == 11:
                self.bg = load_image("background-2.png")

            if self.player.rect.right > self.camera.world.w:
                if self.generation.max_fitness < genome.fitness:
                    self.generation.solved = True
                    if not self.generation.solution_genome.__contains__(genome):
                        self.generation.solution_genome = genome
                    self.player.kill()
                # if not self.toads and self.lvl < 30:
                    # self.next_level()
                    # self.player.kill()
                # else:
                #     self.player.rect.right = self.camera.world.w

            # if self.player.rect.right > self.camera.world.w:
                # self.next_level()
                # if self.generation.max_fitness < genome.fitness:
                #     self.generation.solved = True
                #     if not self.generation.solution_genome.__contains__(genome):
                #         self.generation.solution_genome = genome
                #     self.player.kill()

            self.player.collide(self.platforms)
            self.player.collide(self.springs)

            # PROJECTILES:

            for f in self.firebowsers:
                if self.player.rect.colliderect(f.rect):
                    self.player.kill()

            for s in self.shots:
                if not s.rect.colliderect(self.camera.rect):
                    s.kill()
                if s.rect.colliderect(self.player.rect):
                    self.player.kill()
                    s.kill()
            if self.booming and self.boom_timer <= 0:
                self.player.kill()

            for s in self.skys:
                if s.rect.colliderect(self.camera.rect):
                    if s.type == "sky":
                        if not random.randrange(130):
                            SpikeShot(s.rect.center)

            for c in self.cannons:
                c.update()
                if c.rect.colliderect(self.camera.rect):
                    if c.type == "cannon":
                        if not random.randrange(135):
                            CannonShot(c.rect.center)
                    if c.type != "cannon":
                        c.collide(self.nomoveplatforms)
                        c.collide(self.springs)
                    if c.type == "cannonbig":
                        if not random.randrange(120):
                            CannonShotbig(c.rect.center)
                    if c.type != "cannonbig":
                        c.collide(self.nomoveplatforms)
                        c.collide(self.springs)
                        c.collide(self.cannons)
                    if c.type == "smallcannon":
                        if not random.randrange(145):
                            CannonShotsmall(c.rect.center)
                    if c.type != "smallcannon":
                        c.collide(self.nomoveplatforms)
                        c.collide(self.springs)
                        c.collide(self.cannons)

            # ENDING:

            for b in self.bombs:
                if self.player.rect.colliderect(b.rect):
                    self.player.kill()
                    # self.show_end()
                    # self.next_level()

            for f in self.flag2s:
                if self.player.rect.colliderect(f.rect):
                    # self.show_end()
                    # self.next_level()
                    self.player.kill()

            for t in self.toads:
                if self.player.rect.colliderect(t.rect):
                    self.player.kill()
                    # self.toad()
                    # self.next_level()
                if self.booming and self.boom_timer <= 0:
                    self.player.kill()

            for p in self.pipegreenends:
                if self.player.rect.colliderect(p.rect):
                    self.player.kill()
                    # self.next_level()
                    # self.pipe_sound.play()
                if self.booming and self.boom_timer <= 0:
                    # self.redo_level()
                    self.player.kill()

            for p in self.pipeends:
                if self.player.rect.colliderect(p.rect):
                    self.player.kill()

                    # self.next_level()
                if self.booming and self.boom_timer <= 0:
                    self.player.kill()
                    # self.redo_level()

                    # PLATFORMS:

            for p in self.platforms:
                self.player.collide(self.springs)
                self.player.collide(self.platforms)

            for m in self.mountains:
                self.player.collide(self.mountains)

            for p in self.platformblues:
                self.player.collide(self.platformblues)

            for b in self.brickblues:
                self.player.collide(self.brickblues)

            for g in self.grasss:
                self.player.collide(self.grasss)

            for b in self.bricks:
                self.player.collide(self.bricks)

            for l in self.grays:
                self.player.collide(self.grays)

            for p in self.movingplatformtwos:
                p.collide(self.players)
                for p2 in self.platforms:
                    if p != p2:
                        p.collide_with_platforms(p2)

            for p in self.movingplatforms:
                p.collide(self.players)
                for p2 in self.platforms:
                    if p != p2:
                        p.collide_with_platforms(p2)

            for u in self.undergrounds:
                u.collide(self.players)
                for u2 in self.platforms:
                    if u != u2:
                        u.collide_with_platforms(u2)

            for m in self.mushroomgreens:
                if self.player.rect.colliderect(m.rect):
                    m.kill()
                    MushroomGreendie(m.rect.center)
                    self.score += 50
                    # self.lives += 1
                    # self.up_sound.play()

            # WALK THROUGH:

            for a in self.axes:
                if self.player.rect.colliderect(a.rect):
                    # self.bowser_sound.stop()
                    a.kill()
                    AxeDie(a.rect.center)
                for b in self.bosses:
                    b.collide(self.nomoveplatforms)
                    b.collide(self.platforms)
                    if self.player.rect.colliderect(a.rect):
                        Chain.image = load_image("trap.png")
                for b in self.bridges:
                    if self.player.rect.colliderect(a.rect):
                        b.kill()
                        # stop_music()
                        # self.win_sound.play()

            for c in self.coins:
                if self.player.rect.colliderect(c.rect):
                    c.kill()
                    # self.coin_sound.play()
                    CoinDie(c.rect.center)
                    # self.coin += 1
                    self.score += 50
                if self.coin == 100:
                    self.coin -= self.coin
                    # self.up_sound.play()
                    # self.lives += 1

            # BADDIES:

            for b in self.baddies:
                b.collide(self.nomoveplatforms)
                b.collide(self.springs)
                b.collide(self.cannons)

            for s in self.spikers:
                s.collide(self.platforms)
                s.collide(self.nomoveplatforms)
                if self.player.rect.colliderect(s.rect):
                    self.player.kill()

            for b in self.flowers:
                if self.player.rect.colliderect(b.rect):
                    self.player.kill()

            for b in self.flowertwos:
                if self.player.rect.colliderect(b.rect):
                    self.player.kill()

            for b in self.flowerthrees:
                if self.player.rect.colliderect(b.rect):
                    self.player.kill()

            for b in self.flowerblues:
                if self.player.rect.colliderect(b.rect):
                    self.player.kill()

            for b in self.flowers:
                if self.player.rect.colliderect(b.rect):
                    self.player.kill()

            for r in self.roses:
                if self.player.rect.colliderect(r.rect):
                    self.player.kill()

            for b in self.bosses:
                b.collide(self.nomoveplatforms)
                b.rect.colliderect(self.camera.rect)
                    # self.bowser_sound.play()
                    # stop_music()
                if self.player.rect.colliderect(b.rect) and not b.dead:
                    self.player.kill()
                if b.die_time > 0:
                    for s in self.shots:
                        s.kill()
                    for b2 in self.baddies:
                        b2.kill()
                        BaddieBoom(b2.rect.center, b2.speed, b2.type)
                if not random.randrange(75) and not b.dead:
                    Fireball(b.rect.center)

            for b in self.baddies:
                if self.player.rect.colliderect(b.rect):
                    if self.player.jump_speed > 0 and \
                                    self.player.rect.bottom < b.rect.top + 10 and \
                            b.alive():
                        b.kill()
                        self.player.jump_speed = -3
                        self.player.jump_speed = -5
                        self.player.rect.bottom = b.rect.top - 1
                        self.score += 100
                        # self.baddie_sound.play()
                        BaddieBoom(b.rect.center, b.speed, b.type)
                    else:
                        if b.alive():
                            self.player.kill()

            # TIMER:

            if self.player.alive():
                self.time -= 0.060
            else:
                self.start_new_game = True

            if self.time <= 0:
                self.player.kill()

            # if self.time <= 100:
                # self.hurry_sound.play()
                # stop_music()

            # EVENTS (KEYBINDINGS)

            for e in pygame.event.get():
                if e.type == QUIT:
                    # self.hurry_sound.stop()
                    # self.bowser_sound.stop()
                    self.save_records()
                    sys.exit()
                if e.type == KEYDOWN:
                    # if e.key == K_s:
                        # stop_music()
                    # if e.key == K_p:
                        # play_music(self.music)
                    if e.key == K_ESCAPE:
                        # self.hurry_sound.stop()
                        # self.bowser_sound.stop()
                        self.end()
                    # if e.key == K_y:
                        # self.player.jump()
            if self.player.alive() and not self.playerdying and not self.start_new_game:
                self.current_fitness = self.player.rect.center[0] - 15 + self.score
                if self.countdown_time <= 0:
                    if self.current_fitness <= self.last_fitness:
                        self.player.kill()
                        self.start_new_game = True
                    else:
                        self.countdown_time = 2
                    self.last_fitness = self.current_fitness

                if not self.start_new_game:
                    self.countdown_time -= 0.060
                    outputs = self.run_neural_network()

                    if outputs[0] > 0 and outputs[1] > 0:
                        outputs[0] = 0.0
                        outputs[1] = 0.0
                    if outputs[2] > 0 and outputs[3] > 0:
                        outputs[2] = 0.0
                    # print outputs
                    decisions = self.make_decision(outputs)
                    # print "decisions = [%s]" % decisions
                    for decision in decisions:
                        if decisions[0] == "LEFT":
                            self.current_fitness -= 10
                        self.player.move_decision(decision)
                    # print "%s" % genome


            if not self.running:
                self.save_records()
                return
            self.screen.blit(self.bg, ((-self.camera.rect.x / 1) % 640, 0))
            self.screen.blit(self.bg, ((-self.camera.rect.x / 1) % 640 + 640, 0))
            self.screen.blit(self.bg, ((-self.camera.rect.x / 1) % 640 - 640, 0))
            self.camera.draw_sprites(self.screen, self.sprites)
            self.draw_stats()

            if (not self.player.alive() and not self.playerdying) or self.start_new_game:
                genome.fitness = self.current_fitness
                self.generation.list_fitness.append(genome.fitness)

                if genome.fitness > self.generation.current_max_fitness:
                    self.generation.current_max_fitness = genome.fitness
                if genome.fitness > self.generation.max_fitness:
                    self.generation.max_fitness = genome.fitness
                    self.save_records()
                # print "generation[%d]---species[%d]-------genome [%d]------len genome = %d " % (
                #     self.generation.generation_number, self.generation.current_species + 1,
                #     self.generation.current_genome + 1, len(species.genomes))
                print "fitness = %d -------- top fitness of species = %d --------max fitness in generation= %d" % \
                      (genome.fitness, species.top_fitness, self.generation.max_fitness)
                genomes = (g.genes for g in species.genomes)
                print "-- max len gene = %s" % (max(len(g) for g in genomes))
                print "   length of gene : %d" % len(genome.genes)
                if len(self.generation.species) == self.generation.current_species + 1:
                    if len(species.genomes) == self.generation.current_genome + 1:
                        self.save_records()
                self.generation.increase_genome()
                self.generation.initialize_game()

                self.countdown_time = 2
                self.current_fitness = 0
                self.last_fitness = 0
                pygame.time.wait(1000)

                self.redo_level()
                self.start_new_game = False

                # self.neural_network.create_new_generation()
                # if self.lives <= 0:
                #     self.gameover_screen()
                # else:
                    # self.show_death()
                    # self.lives -= 1

            pygame.display.flip()
            if not self.running:
                self.save_records()
                return

    def find_number(self, text):
        return (int)(re.split('(\d+)', text)[1])

    def save_records(self):
        save_path = os.getcwd() + "/records/generation/"
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        filename = "generation_%d.json" % self.generation.generation_number
        complete_name = os.path.join(save_path, filename)
        with open(complete_name, 'wb') as f:
            pickle.dump(self.generation, f)

    def initialize_neural_network(self):
        self.generation = Generation()
        self.generation.initialize_generation()
        self.generation.initialize_game()

    def run_neural_network(self):
        inputs = self.get_inputs()
        species = self.generation.species[self.generation.current_species]
        genome = species.genomes[self.generation.current_genome]
        return genome.evaluate_network(inputs)

    def get_inputs(self):
        min_x = self.camera.rect[0]
        max_x = min_x + 640
        sprite_list = self.get_all_sprites_in_screen(min_x, max_x)
        if min_x >= 48:
            min_x = min_x + 32
        inputs = [[0 for x in xrange(20)] for y in xrange(16)]
        # inputs[self.player.rect.center[1] / 32][(self.player.rect.center[0] - min_x) / 32] = 2
        for s in sprite_list:
            y = [s.rect.center[1] / 32]
            x = [(s.rect.center[0] - min_x) / 32]
            x_left = s.rect.left
            x_right = s.rect.right
            x_diff = abs(x_right - x_left)
            y_top = s.rect.top
            y_bottom = s.rect.bottom
            y_diff = abs(y_top - y_bottom)

            if x_diff > 32:
                x = []
                diff = x_diff / 32
                while diff != 1:
                    x.append((s.rect.center[0] + (diff - 1) * 16 - min_x) / 32)
                    x.append((s.rect.center[0] - (diff - 1) * 16 - min_x) / 32)
                    diff -= 1
            if y_diff > 32:
                y = []
                diff = y_diff / 32
                while diff != 0:
                    # y.append((s.rect.center[1] + (diff) * 32) / 32 + 1)
                    y.append((s.rect.center[1] - (diff) * 32) / 32 + 1)
                    diff -= 1
            #
            # print "Type : %s  " % s.type
            # print "           center_x=%d, center_y = %d --------minx = %d" % (
            #         s.rect.center[0], s.rect.center[1], min_x)
            # print "           x_left=%d, x_right=%d -------- x_diff = %d   " % (x_left, x_right, x_diff)
            # print "           y_top=%d, y_bottom=%d -------- y_diff = %d   " % (y_top, y_bottom, y_diff)
            # print "      Mario        dx = %s,   dy=%s," % (self.player.rect.center[0], self.player.rect.center[1])
            # print "                   x = "
            # for i in x:
            #     print "                      %d" % i
            # print "                   y = "
            # for i in y:
            #     print "                      %d" % i

            if self.is_brick(s):
                for i in xrange(len(y)):
                    for j in xrange(len(x)):
                        inputs[y[i]][x[j]] = 1
            elif self.is_coin(s) or self.is_mushroom(s):
                for i in xrange(len(y)):
                    for j in xrange(len(x)):
                        inputs[y[i]][x[j]] = 2
                # inputs.__setitem__(x * 16 + y, 1)
            elif self.is_flag(s):
                for i in xrange(len(y)):
                    for j in xrange(len(x)):
                        inputs[y[i]][x[j]] = 3
            elif abs(s.rect.center[0] - self.player.rect.center[0]) < 100 and \
                    abs(s.rect.center[1] - self.player.rect.center[1]) < 100:
                for i in xrange(len(y)):
                    for j in xrange(len(x)):
                        inputs[y[i]][x[j]] = -1

                # inputs.__setitem__(x * 16 + y, -1)
        # print " ------------------------------------------"
        # for y in xrange(16):
        #     print inputs[y]
        # self.end()
        return np.array(inputs).flatten('F')

    def get_all_sprites_in_screen(self, min_x, max_x):
        sprites = []
        for s in self.sprites:
            if min_x <= s.rect.center[0] <= max_x and self.check_qualified_sprite(s):
                sprites.append(s)

        return sprites

    def check_qualified_sprite(self, s):
        return not (isinstance(s, Player) or isinstance(s, PlayerDie) or self.is_instance_grass(s) or \
                    self.is_instance_bush(s) or self.is_instance_castle(s) or \
                    self.is_instance_hill(s) or self.is_instance_chain(s) or \
                    self.is_instance_cloud(s) or self.is_instance_fence(s) or \
                    self.is_instance_tree(s) or self.is_instance_wall(s))

    def is_flag(selfs, s):
        return isinstance(s, Flag) or isinstance(s, Flag2) or \
                isinstance(s, Bomb)

    def is_brick(self, s):
        return  isinstance(s, Brick) or isinstance(s, Brickblue) or \
                isinstance(s, Platform_Brick) or isinstance(s, PlatformQ) or \
                isinstance(s, Platformblue) or isinstance(s, Platform) or \
                isinstance(s, Pipe) or isinstance(s, PipeEnd) or \
                isinstance(s, PipeDown) or isinstance(s, PipeBig) or \
                isinstance(s, PipeGreen) or isinstance(s, PipeGreenBig) or \
                isinstance(s, PipeGreenEnd)

    def is_coin(self, s):
        return isinstance(s, Coin) or isinstance(s, CoinDie)

    def is_mushroom(self, s):
        return isinstance(s, MushroomGreen) or isinstance(s, MushroomGreendie)

    def is_instance_grass(self, s):
        return isinstance(s, Grass) or isinstance(s, Grass1) or isinstance(s, Grass2) or \
               isinstance(s, GrassSprite) or isinstance(s, Grasstexture)
    
    def is_instance_bush(self, s):
        return isinstance(s, Bush) or isinstance(s, Bush2) or isinstance(s, Bush3)
    
    def is_instance_castle(self, s):
        return isinstance(s, Castle) or isinstance(s, Castlebig)
    
    def is_instance_hill(self, s):
        return isinstance(s, Hill) or isinstance(s, Hill2)
    
    def is_instance_chain(self, s):
        return isinstance(s, Chain)
    
    def is_instance_cloud(self, s):
        return isinstance(s, Cloud) or isinstance(s, Cloud2)
    
    def is_instance_fence(self, s):
        return isinstance(s, Fence)
    
    def is_instance_tree(self, s):
        return isinstance(s, Tree1) or isinstance(s, Tree2)
    
    def is_instance_wall(self, s):
        return isinstance(s, Wall)
    
    def make_decision(self, output):
        decisions = []
        if output[0] > 0:
            decisions.append("LEFT")
        if output[1] > 0:
            decisions.append("RIGHT")
        if output[2] > 0:
            decisions.append("SHORT JUMP")
        if output[3] > 0:
            decisions.append("LONG JUMP")
        return decisions

    def draw_stats(self):
        # for i in range(1):
        #     self.screen.blit(self.heart2, (16 + i*34, 16))
        # for i in range(self.player.hp):
        #     self.screen.blit(self.heart1, (16 + i*34, 16))
        # self.screen.blit(self.heroimg, (313, 16))
        # self.screen.blit(self.heroimg2, (235, 10))
        lives = self.lives
        if lives < 0:
            lives = 0
        # ren = self.font.render("Mario", 1, (255, 255, 255))
        # self.screen.blit(ren, (132-ren.get_width(), 16))
        ren = self.font.render("Score:%06d" % self.score, 1, (255, 255, 255))
        self.screen.blit(ren, (200 - ren.get_width(), 1))
        # ren = self.font.render("Lives:x%d" % lives, 1, (255, 255, 255))
        # self.screen.blit(ren, (ren.get_width(), 33))
        ren = self.font.render("Coins:x%02d" % self.coin, 1, (255, 255, 255))
        self.screen.blit(ren, (150 - ren.get_width(), 18))
        ren = self.font.render("FPS %d" % self.clock.get_fps(), 1, (255, 255, 255))
        self.screen.blit(ren, (540, 1))
        ren = self.font.render("Fitness %s" % self.current_fitness, 1, (255, 255, 255))
        self.screen.blit(ren, (400, 18))
        ren1 = self.font.render("Time: %d" % self.time, 1, (255, 255, 255))
        # ren2 = self.font.render("Time: %d" % self.time, 1, Color("#ffffff"))
        self.screen.blit(ren1, (150 + ren.get_width(), 1))
        # self.screen.blit(ren2, (130 + ren.get_width(), 18))
        # if self.time <= 100:
        #     ren = self.font.render("GOTTA GO FAST", 1, (255, 255, 255))
        #     self.screen.blit(ren, (630-ren.get_width(), 60))

# end
#     def make_decision(self):
#
#
#         # Obtain Prediction
#         if self.neural_network.decision() == 1:
#             return 1

