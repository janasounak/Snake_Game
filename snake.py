import pygame as pg 
import random
import sys
from time import sleep

pg.init() 
pg.font.init()
SCREENWIDTH = 300
SCREENHEIGHT = 500

SCREEN = pg.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pg.display.set_caption('SNAKE GAME')
pg.display.set_icon(pg.image.load('snakeicon.png').convert_alpha())

black = (0, 0, 0)
green = (0, 255, 0)

background = pg.image.load('bg.png').convert()
front_pic = pg.image.load('front_page.png').convert_alpha()

eat = pg.mixer.Sound('snake eat.mp3')
game_over = pg.mixer.Sound('game over.mp3')

FPS = 10

clock = pg.time.Clock()

joysticks = []
for i in range(pg.joystick.get_count()):
    joysticks.append(pg.joystick.Joystick(i))
    joysticks[-1].init()

def welcome():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT or  (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            if event.type == pg.JOYBUTTONDOWN and event.button == 5:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and (event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER):
                return
            if event.type == pg.JOYBUTTONDOWN and event.button ==0 :
                return

        SCREEN.blit(background, [0,0])
        SCREEN.blit(front_pic, [0,50])
        text(35, 'Press enter to play', black, 5, 240)

        pg.display.update()
        clock.tick(FPS)

def main_game():
    snake_head = pg.image.load('snake_head.png').convert_alpha()
    starting_head = pg.image.load('snake_head1.png').convert_alpha()

    food = pg.image.load('food.png').convert_alpha()

    snake_size = 20
    food_size =20

    snake_x = 100
    snake_y = 100

    food_x = (random.randint(5, (SCREENWIDTH/20)-5))*20 
    food_y = (random.randint(5, (SCREENWIDTH/20)-5))*20

    snake_list = []
    snake_length = 1

    move_direction = 'any'
    snake_vel = 20

    score = 0 

    snake_head1 = pg.transform.rotate(snake_head, 90)
    snake_head2 = pg.transform.rotate(snake_head, -90)
    snake_head3 = pg.transform.rotate(snake_head, 0)
    snake_head4 = pg.transform.rotate(snake_head, 180)

    starting_head1 = pg.transform.rotate(starting_head, 90)
    starting_head2 = pg.transform.rotate(starting_head, -90)
    starting_head3 = pg.transform.rotate(starting_head, 0)
    starting_head4 = pg.transform.rotate(starting_head, 180)

    try:
        with open('highscore.txt', 'r') as f:
            highscore = int(f.read())
    except:
        highscore = 0

    while True:
        for event in pg.event.get():
            if (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE) or event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.JOYBUTTONDOWN and event.button == 5:
                pg.quit()
                sys.exit()
            if (event.type == pg.KEYDOWN and event.key == pg.K_UP) and (move_direction != 'down') and (0 <= snake_x <= (SCREENWIDTH - snake_size)):
                move_direction = 'up' 
            if (event.type == pg.KEYDOWN and event.key == pg.K_DOWN) and (move_direction != 'up') and (0 <= snake_x <= (SCREENWIDTH - snake_size)):
                move_direction = 'down'
            if (event.type == pg.KEYDOWN and event.key == pg.K_RIGHT) and (move_direction != 'left') and (0 <= snake_y <= (SCREENHEIGHT - snake_size)):
                move_direction = 'right'
            if (event.type == pg.KEYDOWN and event.key == pg.K_LEFT) and (move_direction != 'right') and (0 <= snake_y <= (SCREENHEIGHT - snake_size)):
                move_direction = 'left'
            if event.type == pg.JOYBUTTONDOWN and event.button == 1 and (move_direction != 'down') and (0 <= snake_x <= (SCREENWIDTH - snake_size)):
                move_direction ='up'
            if event.type == pg.JOYBUTTONDOWN and event.button == 2 and (move_direction != 'up') and (0 <= snake_x <= (SCREENWIDTH - snake_size)):
                move_direction ='down'
            if event.type == pg.JOYBUTTONDOWN and event.button == 3 and (move_direction != 'right') and (0 <= snake_y <= (SCREENHEIGHT - snake_size)):
                move_direction ='left'
             event.type == pg.JOYBUTTONDOWN and event.button == 4 and (move_direction != 'left') and (0 <= snake_y <= (SCREENHEIGHT - snake_size)):
                move_direction ='right'

        if move_direction == 'up':
            snake_head = snake_head1
            starting_head = starting_head1
            snake_x += 0
            snake_y -= snake_vel
        if move_direction == 'down':
            snake_head = snake_head2
            starting_head = starting_head2
            snake_x += 0
            snake_y += snake_vel
        if move_direction == 'right':
            snake_head = snake_head3
            starting_head = starting_head3
            snake_x += snake_vel
            snake_y += 0
        if move_direction == 'left':
            snake_head = snake_head4
            starting_head = starting_head4
            snake_x -= snake_vel
            snake_y += 0

        snake_block = []
        snake_block.append(snake_x)
        snake_block.append(snake_y)
        snake_list.append(snake_block)

        if (snake_x + snake_size > food_x and snake_x < food_x + food_size) and (snake_y + snake_size > food_y and snake_y < food_y + food_size):
            score += 5
            eat.play()
            food_x = (random.randint(5, (SCREENWIDTH/20)-5))*20 
            food_y = (random.randint(5, (SCREENWIDTH/20)-5))*20
            snake_length += 1

        if len(snake_list) > snake_length:
            del snake_list[0]

        if snake_block in snake_list[:-1]:
            game_over.play()
            sleep(0.5)
            return score

        if snake_x + snake_size < 0 :
            snake_x = SCREENWIDTH
        if snake_x > SCREENWIDTH :
            snake_x = -snake_size
        if snake_y + snake_size < 0 :
            snake_y = SCREENHEIGHT
        if snake_y > SCREENHEIGHT:
            snake_y = -snake_size

        if score > highscore :
            highscore = score

        SCREEN.blit(background, [0,0])
        SCREEN.blit(food, [food_x, food_y])
        for x,y in snake_list[:-1]:
            pg.draw.rect(SCREEN, black, [x, y, snake_size, snake_size])
        if snake_length > 1 :
            SCREEN.blit(snake_head, [snake_list[-1][0],snake_list[-1][1]])
        else:
            if move_direction == 'right':
                SCREEN.blit(starting_head, [snake_list[-1][0] - 10,snake_list[-1][1]])
            elif move_direction == 'down':
                SCREEN.blit(starting_head, [snake_list[-1][0],snake_list[-1][1] - 10])
            else:
                SCREEN.blit(starting_head, [snake_list[-1][0],snake_list[-1][1]])

        text(23, ('Score: ' + str(score)), green, 10, 10)
        text(23, ('HighScore: ' + str(highscore)), green, 130, 10)

        with open('highscore.txt', 'w') as f:
            f.write(str(highscore))

        pg.display.update()
        clock.tick(FPS)

def game():
    score = main_game()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT or  (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            if event.type == pg.JOYBUTTONDOWN and event.button == 5:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and (event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER):
                return
            if event.type == pg.JOYBUTTONDOWN and event.button == 0 :
                return

        SCREEN.blit(background, [0,0])
        text(50, 'GAME OVER', black, 4, 200)
        text(30, ('Score : ' + str(score)), black, 90, 270)
        text(25, 'Press enter to play again', black, 15, 340)

        pg.display.update()
        clock.tick(FPS)

def text(font_size, font_text, font_color, font_x, font_y):
    font = pg.font.SysFont('Harrington', font_size)
    text_img = font.render(font_text, True, font_color)
    SCREEN.blit(text_img, [font_x, font_y])

welcome()
while True:
    game()
