import pygame
import time
import random
import os

pygame.init()

# Definindo cores
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Definindo dimensões da tela
dis_width = 800
dis_height = 600

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()
snake_block = 10
snake_speed = 15

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Arquivo para salvar o recorde
record_file = "record.txt"

def save_record(record):
    with open(record_file, "w") as f:
        f.write(f"{record}\n")

def load_record():
    if os.path.exists(record_file):
        with open(record_file, "r") as f:
            record = int(f.readline().strip())
        return record
    else:
        return 0

def update_record(score, record):
    if score > record:
        record = score
        save_record(record)
    return record

def Pontuação(score):
    value = score_font.render("Pontuação: " + str(score), True, black)
    dis.blit(value, [0, 0])

def show_record(record):
    value = score_font.render(f"Recorde: {record}", True, black)
    dis.blit(value, [dis_width - 200, 50])

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def draw_button(text, x, y, w, h, color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(dis, color, [x, y, w, h])
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(dis, color, [x, y, w, h])

    small_text = pygame.font.SysFont("comicsansms", 20)
    text_surf = small_text.render(text, True, black)
    text_rect = text_surf.get_rect(center=((x + (w / 2)), (y + (h / 2))))
    dis.blit(text_surf, text_rect)

def quit_game():
    pygame.quit()
    quit()

def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    record = load_record()

    while not game_over:

        while game_close == True:
            dis.fill(blue)
            message("Game Over!", red)
            Pontuação(Length_of_snake - 1)
            record = update_record(Length_of_snake - 1, record)
            show_record(record)
            draw_button("Jogar Novamente", 150, 400, 200, 50, green, gameLoop)
            draw_button("Sair", 450, 400, 200, 50, red, quit_game)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        Pontuação(Length_of_snake - 1)
        show_record(record)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
