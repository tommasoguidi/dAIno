import pygame
import os
import random
import sys
import neat
from PIL import Image

pygame.init()

# Global Constants
points_max= 0
best_generation = 0
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))
FONT = pygame.font.Font('freesansbold.ttf', 20)


class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5
    index_jump = 0   #indice della quantità di salto
    MAX_JUMP_FRAME=11

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False
        self.state_dinoJump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0



    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    #jump modificato

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:

            if (self.dino_jump and self.index_jump<self.MAX_JUMP_FRAME):
                self.index_jump +=1
                self.dino_rect.y -= self.jump_vel * 4
                self.jump_vel -= 0.8
                self.state_dinoJump = True
            else:
                if self.index_jump != self.MAX_JUMP_FRAME:
                    self.jump_vel=0.5

                self.index_jump = self.MAX_JUMP_FRAME
                self.dino_rect.y += abs(self.jump_vel) * 4
                self.jump_vel += 0.8
                self.state_dinoJump = False



        if self.dino_rect.y >= self.Y_POS - 15:
            self.dino_jump = False
            self.index_jump = 0
            self.jump_vel = self.JUMP_VEL

    #def jump(self):
    #    self.image = self.jump_img
    #   if self.dino_jump:
    #        self.dino_rect.y -= self.jump_vel * 4
    #        self.jump_vel -= 0.8
    #   if self.jump_vel < - self.JUMP_VEL:
    #        self.dino_jump = False
    #        self.jump_vel = self.JUMP_VEL


    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop(0)

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300

class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 340 - 100 - 20#10*random.randint(1,4)
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1

def remove(index):
    dinosaurs.pop(index)
    ge.pop(index)
    nets.pop(index)

def eval_genomes(genomes, config):
    global game_speed, x_pos_bg, y_pos_bg, obstacles, dinosaurs, ge, nets, points, points_max, best_generation
    clock = pygame.time.Clock()
    points = 0
    cloud = Cloud()

    obstacles = []
    dinosaurs = []
    ge = []
    nets = []

    x_pos_bg = 0
    y_pos_bg = 380
    game_speed = 20

    for genome_id, genome in genomes:
        dinosaurs.append(Dinosaur())
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

    def score():
        global points, game_speed, points_max, best_generation
        points += 1
        if points % 100 == 0:
            game_speed += 1
        if (points_max < points):
            points_max = points
            best_generation = pop.generation + 1
        text_1 = FONT.render(f'Points:  {str(points)}', True, (0, 0, 0))
        text_2 = FONT.render(f'Points Max:  {str(points_max)} at generation {str(best_generation)}', True, (0, 0, 0))

        SCREEN.blit(text_1, (950, 50))
        SCREEN.blit(text_2, (50, 540))

    def statistics():
        global dinosaurs, game_speed, ge
        text_1 = FONT.render(f'Dinosaurs Alive:  {str(len(dinosaurs))}', True, (0, 0, 0))
        text_2 = FONT.render(f'Generation:  {pop.generation + 1}', True, (0, 0, 0))
        text_3 = FONT.render(f'Game Speed:  {str(game_speed)}', True, (0, 0, 0))

        SCREEN.blit(text_1, (50, 450))
        SCREEN.blit(text_2, (50, 480))
        SCREEN.blit(text_3, (50, 510))

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        SCREEN.fill((255, 255, 255))

        for dinosaur in dinosaurs:
            dinosaur.update()
            dinosaur.draw(SCREEN)

        if len(dinosaurs) == 0:
            break

        rand_obst = random.randint(0, 3)
        if (len(obstacles) == 0 or (len(obstacles) == 1 and obstacles[0].rect.x < random.randint(0, SCREEN_WIDTH * .3))):
            if rand_obst == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif rand_obst == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif rand_obst > 1:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            for i, dinosaur in enumerate(dinosaurs):
                ge[i].fitness += 1
                if dinosaur.dino_rect.colliderect(obstacle.rect):
                    ge[i].fitness -= 1
                    remove(i)

        for i, dinosaur in enumerate(dinosaurs):
            output = nets[i].activate((dinosaur.dino_rect.y,
                                       obstacles[0].rect.x if len(obstacles) > 0 else SCREEN_WIDTH,
                                       obstacles[0].rect.y if len(obstacles) > 0 else SCREEN_HEIGHT,
                                       obstacles[1].rect.x if len(obstacles) > 1 else SCREEN_WIDTH,
                                       obstacles[1].rect.y if len(obstacles) > 1 else SCREEN_HEIGHT))

            if output[0] > 0.5 and not dinosaur.dino_duck:
                dinosaur.dino_duck = False
                dinosaur.dino_run = False
                dinosaur.dino_jump = True
            elif output[1] > 0.5 and not dinosaur.dino_jump:
                dinosaur.dino_duck = True
                dinosaur.dino_run = False
                dinosaur.dino_jump = False
            elif not (dinosaur.dino_jump or output[1]>0.5):
                dinosaur.dino_duck = False
                dinosaur.dino_run = True
                dinosaur.dino_jump = False


        statistics()
        score()
        background()
        clock.tick(240)
        cloud.draw(SCREEN)
        cloud.update()
        pygame.display.update()


# Setup the NEAT Neural Network
def run(config_path):
    global pop
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    pop.add_reporter(neat.StatisticsReporter())
    pop.run(eval_genomes, 500)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)