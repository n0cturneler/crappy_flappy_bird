import time
import random
import pygame

default_bird_data = {
    "life_count" : 1,
    "color" : (255, 255, 0),
    "outline_color" : (0,0,0),
    "weight" : 1,
    "size" : 25,
    "pos_x" : 200,
    "pos_y" : 450,
    "jump_force" : -75
}

def_pos = {
    "x" : 250,
    "y" : 250
}

cur_walls = []
score_walls = []

wall_data = {
    "gap_thickness" : 300,
    "gap_pos_y" : 200,
    "wall_thickness" : 75,
    "wall_speed" : 3,
    "color" : (0, 200, 0),
    "outline_color" : (144, 252, 3),
    "pos_x" : 900,
}

game_data = {
    "run_state" : True,
    "tick" : 0,
    "res_x" : 900,
    "res_y" : 900,
    "mouse_tick" : 0,
    "score" : 0
}

class bird():
    def __init__(self, life_count, color, outline_color, weight, size, pos_x, pos_y, jump_force):
        self.life_count = life_count
        self.color = color
        self.outline_color = outline_color

        self.weight = weight
        self.size = size
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.jump_force = jump_force

    def draw_bird(self, screen):
        pygame.draw.circle(screen, self.outline_color, (self.pos_x, self.pos_y), self.size + 2)
        pygame.draw.circle(screen, self.color, (self.pos_x, self.pos_y), self.size)

    def __str__(self):
        return f"lives {self.life_count}"

class exit():
    pygame.quit()

class wall():
    def __init__(self, gap_thickness, gap_pos_y, color, outline_color, wall_thickness, wall_speed, pos_x):
        self.gap_thickness = gap_thickness
        self.gap_pos_y = gap_pos_y
        self.color = color
        self.outline_color = outline_color

        self.wall_thickness = wall_thickness
        self.wall_speed = wall_speed
        self.pos_x = pos_x

    def draw_walls(self, screen):
        down_wall = (self.gap_pos_y + self.gap_thickness/2)
        up_wall = (self.gap_pos_y - self.gap_thickness/2)
        down_thickness = 900 - down_wall

        pygame.draw.rect(screen, self.color, (self.pos_x, 0, self.wall_thickness, up_wall))
        pygame.draw.rect(screen, self.outline_color, (self.pos_x+10, 10, self.wall_thickness-20, up_wall-20))

        pygame.draw.rect(screen, self.color, (self.pos_x, down_wall, self.wall_thickness, down_thickness))
        pygame.draw.rect(screen, self.outline_color, (self.pos_x+10, down_wall+10, self.wall_thickness-20, down_thickness-20))

class main_loop():
    def __init__(self, clock, screen, cur_bird, my_font, run_state, tick, mouse_tick, res_x, res_y, score):
        self.run_state = run_state
        self.screen = screen
        self.clock = clock

        self.my_font = my_font

        self.cur_bird = cur_bird
        self.score = score

        self.tick = tick
        self.res_x = res_x
        self.res_y = res_y
        self.mouse_tick = mouse_tick

    def run(self):
        while self.run_state:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run_state = False

            keys = pygame.key.get_pressed()
            buttons =  pygame.mouse.get_pressed()

            if keys[pygame.K_ESCAPE] :
                self.run_state = False

            if buttons[0]:
                self.mouse_tick = self.cur_bird.jump_force
            else:
                self.mouse_tick += 3

            if self.tick > 119:
                self.tick = 0

            if self.tick == 0:
                new_wall = wall(**wall_data)
                new_wall.gap_pos_y = random.randint(200,700)
                cur_walls.insert(0, new_wall)

            self.tick += 1

            self.screen.fill('light blue')

            for walls in cur_walls:
                if walls:
                    if walls.pos_x < self.cur_bird.pos_x - wall_data['wall_thickness'] and walls not in score_walls:
                        self.score += 1
                        score_walls.insert(0, walls)

                    if walls.pos_x < -wall_data['wall_thickness']:
                        score_walls.remove(walls)
                        cur_walls.remove(walls)

                    else:
                        walls.pos_x -= walls.wall_speed
                        walls.draw_walls(self.screen)

            if self.run_state:
                self.cur_bird.pos_y += 0.1 * (self.mouse_tick^2)

                self.cur_bird.pos_y = max(min(self.cur_bird.pos_y, 900-self.cur_bird.size), self.cur_bird.size)
                print(self.cur_bird.pos_y)
                
                if self.cur_bird.pos_y == 875 or self.cur_bird.pos_y == 25:
                    self.run_state = False

                check_up = self.screen.get_at((self.cur_bird.pos_x, int(self.cur_bird.pos_y - self.cur_bird.size)))
                check_down = self.screen.get_at((self.cur_bird.pos_x, int(self.cur_bird.pos_y + self.cur_bird.size-1)))
                check_front = self.screen.get_at((int(self.cur_bird.pos_x+self.cur_bird.size+2), int(self.cur_bird.pos_y)))

                if check_up == (0, 200, 0, 255) or check_down == (0, 200, 0, 255) or check_front == (0, 200, 0, 255):
                    self.run_state = False

            self.cur_bird.draw_bird(self.screen)

            text_surface = self.my_font.render(f'Score:{self.score}', True, (176, 41, 255))
            self.screen.blit(text_surface, (0, 0))

            self.clock.tick(60)
            pygame.display.flip()

class init():
    def __init__(self):
        pygame.init()
        pygame.font.init()

        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((game_data['res_x'], game_data['res_y']))
        my_font = pygame.font.SysFont('Calluna', 60)

        self.cur_bird = bird(**default_bird_data)
        self.cur_loop = main_loop(clock, screen, self.cur_bird, my_font, **game_data)
        self.cur_loop.run()


game = init()
time.sleep(1)
print(':), <3')

