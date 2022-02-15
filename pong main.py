import pygame
import random
import sys

pygame.init()

dis_width = 1000
dis_height = 600
score_font = pygame.font.Font("freesansbold.ttf", 300)
instructions_font = pygame.font.Font("freesansbold.ttf", 64)

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption("Pong")
pygame.display.set_icon(pygame.image.load("ball.png"))

l_score = 0
r_score = 0

ball_x = 500
ball_y = 300
ball_x_speed = random.choice((-0.5, 0.5))
ball_y_speed = random.uniform(-0.5, 0.5)
ball_width = 8
ball_height = 8


def draw_ball():
    pygame.draw.rect(dis, (255, 255, 255), (ball_x, ball_y, ball_width, ball_height))
    # rectangular ball because ive never seen a pong game with a circular ball HAHA


l_paddle_width = 10
l_paddle_height = 80
l_paddle_x = 0
l_paddle_y = dis_height / 2 - l_paddle_height / 2
l_paddle_y_speed = 0


def draw_left_paddle():
    pygame.draw.rect(dis, (255, 255, 255), (l_paddle_x, l_paddle_y, l_paddle_width, l_paddle_height))


r_paddle_width = 10
r_paddle_height = 80
r_paddle_x = dis_width - r_paddle_width
r_paddle_y = dis_height / 2 - r_paddle_height / 2
r_paddle_y_speed = 0


def draw_right_paddle():
    pygame.draw.rect(dis, (255, 255, 255), (r_paddle_x, r_paddle_y, r_paddle_width, r_paddle_height))


def draw_center_line():
    pygame.draw.rect(dis, (50, 50, 50, 0), (495, 0, 10, dis_height))


def show_score():
    left_score = score_font.render(f"{l_score}", True, (50, 50, 50))
    dis.blit(left_score, (200, 200))
    right_score = score_font.render(f"{r_score}", True, (50, 50, 50))
    dis.blit(right_score, (700, 200))


def show_instructions():
    instructions = instructions_font.render("Press SPACE to play", True, (150, 150, 150))
    dis.blit(instructions, (200, 300))


running = False


# starting screen // restarting screen
def start_screen():
    global running
    global ball_x
    global ball_y
    global ball_x_speed
    global ball_y_speed
    global l_paddle_y
    global l_paddle_x
    global r_paddle_y
    global r_paddle_x
    global l_paddle_y_speed
    global r_paddle_y_speed

    ball_x_speed = random.choice((-0.5, 0.5))
    ball_y_speed = random.uniform(-0.5, 0.5)
    l_paddle_x = 0
    l_paddle_y = dis_height / 2 - l_paddle_height / 2
    r_paddle_x = dis_width - r_paddle_width
    r_paddle_y = dis_height / 2 - r_paddle_height / 2
    l_paddle_y_speed = 0
    r_paddle_y_speed = 0

    while not running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = True
            if event.type == pygame.QUIT:
                sys.exit()

        ball_x = 500
        ball_y = 300

        draw_left_paddle()
        draw_right_paddle()
        draw_center_line()
        show_score()
        show_instructions()

        pygame.display.update()


start_screen()

while running:

    # print(ball_x,ball_y)
    dis.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # setting the reactions for key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                l_paddle_y_speed = -1
            if event.key == pygame.K_s:
                l_paddle_y_speed = 1
            if event.key == pygame.K_UP:
                r_paddle_y_speed = -1
            if event.key == pygame.K_DOWN:
                r_paddle_y_speed = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                l_paddle_y_speed = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                r_paddle_y_speed = 0

    # for ball to rebound off top and bottom borders
    if ball_y < 0 + ball_height or ball_y > 600 - ball_height:
        ball_y_speed = -ball_y_speed

    # game restart / score
    if ball_x < 0:
        r_score += 1
        running = False
        start_screen()
    elif ball_x > 1000:
        l_score += 1
        running = False
        start_screen()

    # setting borders for paddles
    if l_paddle_y > dis_height - l_paddle_height:
        l_paddle_y = dis_height - l_paddle_height
    if l_paddle_y < 0:
        l_paddle_y = 0
    if r_paddle_y > dis_height - r_paddle_height:
        r_paddle_y = dis_height - r_paddle_height
    if r_paddle_y < 0:
        r_paddle_y = 0

    # collisions. the lines below are because range is unable to take floats -_-
    left_pad = int(l_paddle_y // 1)
    right_pad = int(r_paddle_y // 1)
    ball_y_int = int(ball_y // 1)
    if ball_y_int in range(left_pad + 26, left_pad + 64) and ball_x == 10:
        ball_x_speed = -ball_x_speed
    elif ball_y_int in range(right_pad + 26, right_pad + 64) and ball_x == 990:
        ball_x_speed = -ball_x_speed
    # more collisions. I want the ball to change directions on the y-axis when you hit it on the edge of the paddle
    # left paddle
    elif ball_y_int in range(left_pad, left_pad + 10) and ball_x == 10:
        ball_y_speed = -0.5
        ball_x_speed = -ball_x_speed
    elif ball_y_int in range(left_pad + 10, left_pad + 26) and ball_x == 10 or \
            ball_y_int in range(left_pad + 64, left_pad + 70) and ball_x == 10:
        ball_y_speed = -ball_y_speed
        ball_x_speed = -ball_x_speed
    elif ball_y_int in range(left_pad + 70, left_pad + 80) and ball_x == 10:
        ball_y_speed = 0.5
        ball_x_speed = -ball_x_speed
    # right paddle
    elif ball_y_int in range(right_pad, right_pad + 10) and ball_x == 990:
        ball_y_speed = -0.5
        ball_x_speed = -ball_x_speed
    elif ball_y_int in range(right_pad + 10, right_pad + 26) and ball_x == 990 or \
            ball_y_int in range(left_pad + 64, left_pad + 70) and ball_x == 990:
        ball_y_speed = -ball_y_speed
        ball_x_speed = -ball_x_speed
    elif ball_y_int in range(right_pad + 70, right_pad + 80) and ball_x == 990:
        ball_y_speed = 0.5
        ball_x_speed = -ball_x_speed

    # ball movements
    ball_x += ball_x_speed
    ball_y += ball_y_speed

    # paddle movements
    l_paddle_y += l_paddle_y_speed
    r_paddle_y += r_paddle_y_speed

    # drawing everything
    draw_left_paddle()
    draw_right_paddle()
    draw_center_line()
    show_score()
    draw_ball()

    pygame.display.update()