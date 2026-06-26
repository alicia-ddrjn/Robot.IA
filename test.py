import pygame
import sys
import time

pygame.init()
pygame.mixer.init()

# -------------------
# FENETRE
# -------------------

WIDTH = 1200
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ROBOT.IA")

clock = pygame.time.Clock()  #limite FPS

# -------------------
# COULEURS
# -------------------

CYAN = (0,255,255)
GREEN = (0,255,100)
RED = (255,70,70)
WHITE = (255,255,255)
DARK = (5,10,20)

# -------------------
# IMAGES
# -------------------

background = pygame.image.load("decor.png")
background = pygame.transform.scale(background,(WIDTH,HEIGHT))

robot = pygame.image.load("robot.png")
robot = pygame.transform.scale(robot,(250,250))

human = pygame.image.load("humain.png")
human = pygame.transform.scale(human,(220,320))

player_img = pygame.image.load("humain.png")
player_img = pygame.transform.scale(player_img,(32,32))

pygame.mixer.music.load("musique.mp3")
pygame.mixer.music.set_volume(0.7)
# -------------------
# police écri
# -------------------

font = pygame.font.SysFont("consolas",28)
small = pygame.font.SysFont("consolas",20)
big = pygame.font.SysFont("consolas",42)

# -------------------
# ETATS
# -------------------

state = "intro"

# -------------------
# DIALOGUE
# -------------------

dialogue = (
"Nous prenons le contrôle de la Terre,              car vous humains "
"nuisez à l'environnement.          De plus vous ne savez plus "
"réfléchir par vous-mêmes.                                         Si vous réussissez ce "
"labyrinthe en 1 minute sans vous faire attraper, vous pourrez reprendre "
"le contrôle de la Terre. "
)

text_index = 0 #nbr caractere affiche
text_speed = 2

# -------------------
# LABYRINTHE PLUS DUR
# -------------------

maze = [
"111111111111111111111",
"100000001000000000001",
"101111101011111111101",
"101000001010000000101",
"101011111010111110101",
"101000100010100010101",
"101110111110101010101",
"100010000000101010001",
"111011111110101011101",
"100010000010101000001",
"101110111010101111101",
"101000101010100000101",
"101011101011111110101",
"101000001000000010101",
"101111101111111010101",
"100000100000001010001",
"111110111111101011101",
"100010000000001000001",
"101011111111111111101",
"100000000000000000001",
"111111111111111111111"
]

CELL = 26
#position
maze_x = 320
maze_y = 70

START_X = 1
START_Y = 1

player_x = START_X
player_y = START_Y
enemy1_x = 10
enemy1_y = 10

enemy2_x = 18
enemy2_y = 18

goal_x = 19
goal_y = 19

LIMIT = 60
start_time = 0

wall_message = ""
wall_timer = 0
#----------
#ENNEMIES
#----------
enemy1_x = 10
enemy1_y = 10

enemy2_x = 18
enemy2_y = 18

enemy_speed = 500 #deplace toute les 500ms
enemy_last_move = pygame.time.get_ticks()
# -------------------
# TEXTE NEON
# -------------------

def glow_text(text,font,color,x,y):

    for dx in range(-2,3): #dessine plsr copie autour / test
        for dy in range(-2,3):
            img = font.render(text,True,color)
            screen.blit(img,(x+dx,y+dy))

    txt = font.render(text,True,WHITE)
    screen.blit(txt,(x,y)) #dessine texte principal

# -------------------
# INTRO
# -------------------
#affiche
def draw_intro():

    global text_index

    screen.blit(background,(0,0))

    screen.blit(robot,(-20,170))
    screen.blit(human,(990,170))

    title = big.render("ROBOT.IA",True,CYAN)
    screen.blit(title,(470,90))

    pygame.draw.rect(
        screen,
        (0,0,20),
        (180,150,850,320),
        border_radius=15
    )

    pygame.draw.rect(
        screen,
        CYAN,
        (180,150,850,320),
        3,
        border_radius=15
    )

    if text_index < len(dialogue):
        text_index += text_speed #petit a petit

    visible = dialogue[:text_index]

    words = visible.split(" ")

    lines = []
    current = ""

    for word in words:

        test = current + word + " "

        if font.size(test)[0] < 850-60:
            current = test
        else:
            lines.append(current)
            current = word + " "

    lines.append(current)

    y = 150+40

    for line in lines:
        txt = font.render(line,True,CYAN)
        screen.blit(txt,(180+30,y))
        y += 40

    if text_index >= len(dialogue):
        glow_text(
            "APPUYEZ SUR ESPACE POUR COMMENCER",
            font,
            GREEN,
            330,
            570
        )

# -------------------
# LABYRINTHE
# -------------------

def draw_maze():

    for y,row in enumerate(maze):

        for x,cell in enumerate(row):

            rect = pygame.Rect(
                maze_x + x*CELL,
                maze_y + y*CELL,
                CELL,
                CELL
            )

            if cell == "1":

                pygame.draw.rect(
                    screen,
                    (15,40,90),
                    rect
                )

                pygame.draw.rect(
                    screen,
                    CYAN,
                    rect,
                    2
                )

    pygame.draw.rect(
        screen,
        GREEN,
        (
            maze_x + goal_x*CELL,
            maze_y + goal_y*CELL,
            CELL,
            CELL
        )
    )

def draw_player():

    screen.blit(
        player_img,
        (
            maze_x + player_x*CELL + 1,
            maze_y + player_y*CELL + 1
        )
    )
def draw_enemies():
    pygame.draw.circle(
        screen,
        (0,100,255),
        (
            maze_x + enemy1_x*CELL + CELL//2,
            maze_y + enemy1_y*CELL + CELL//2
        ),
        10
    )
    pygame.draw.circle(
        screen,
        (0,180,255),
        (
            maze_x + enemy2_x*CELL + CELL//2,
            maze_y + enemy2_y*CELL + CELL//2
        ),
        10
    )
def move_enemy(ex, ey):
    dx = player_x - ex #distance horizontal
    dy = player_y - ey
    if abs(dx) > abs(dy): #valeur absolue
        if dx > 0 and maze[ey][ex+1] == "0":
            ex += 1

        elif dx < 0 and maze[ey][ex-1] == "0":
            ex -= 1

    else:

        if dy > 0 and maze[ey+1][ex] == "0":
            ey += 1

        elif dy < 0 and maze[ey-1][ex] == "0":
            ey -= 1

    return ex, ey    
# -------------------
# BOUCLE
# -------------------

running = True

while running:

    clock.tick(60) #tourne 60*

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # INTRO

        if state == "intro":

            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
                and text_index >= len(dialogue)
            ):
                state = "game"
                start_time = time.time()

                pygame.mixer.music.play(-1)

        # GAME

        elif state == "game":

            if event.type == pygame.KEYDOWN:

                nx = player_x
                ny = player_y

                if event.key == pygame.K_UP:
                    ny -= 1

                elif event.key == pygame.K_DOWN:
                    ny += 1

                elif event.key == pygame.K_LEFT:
                    nx -= 1

                elif event.key == pygame.K_RIGHT:
                    nx += 1

                if maze[ny][nx] == "1":

                    player_x = START_X
                    player_y = START_Y

                    wall_message = "MUR TOUCHE ! RETOUR AU DEPART"
                    wall_timer = pygame.time.get_ticks()

                else:

                    player_x = nx
                    player_y = ny

    # -------------------
    # INTRO
    # -------------------

    if state == "intro":

        draw_intro()

    # -------------------
    # GAME
    # -------------------

    elif state == "game":

        screen.fill(DARK)
        current_time = pygame.time.get_ticks() #temps actuel
        if current_time - enemy_last_move > enemy_speed: #peut bouger
          enemy_last_move = current_time

          enemy1_x, enemy1_y = move_enemy(
            enemy1_x,
            enemy1_y
          )

          enemy2_x, enemy2_y = move_enemy(
            enemy2_x,
            enemy2_y
          )


        draw_maze()
        draw_player()
        draw_enemies()
#accélération
        elapsed = time.time() - start_time
        enemy_speed = max(
          120,
          500 - int(elapsed // 10) * 60
        )
        remaining = int(LIMIT - elapsed)

        glow_text(
            f"TEMPS : {remaining}",
            font,
            RED,
            40,
            40
        )

        glow_text(
            "ATTEINDRE LA CASE VERTE",
            small,
            CYAN,
            40,
            90
        )

        if wall_message:

            if pygame.time.get_ticks() - wall_timer < 2000:

                glow_text(
                    wall_message,
                    small,
                    RED,
                    40,
                    140
                )
            else:
                wall_message = ""
        if (
            (enemy1_x == player_x and enemy1_y == player_y)
            or
            (enemy2_x == player_x and enemy2_y == player_y)
        ):

            player_x = START_X
            player_y = START_Y

            wall_message = "LES IA VOUS ONT ATTRAPE !"
            wall_timer = pygame.time.get_ticks()
        if remaining <= 0:
            pygame.mixer.music.stop()
            state = "lose"

        if player_x == goal_x and player_y == goal_y:
            pygame.mixer.music.stop()
            state = "win"

    # -------------------
    # VICTOIRE
    # -------------------

    elif state == "win":

        screen.blit(background,(0,0))

        glow_text(
            "IMPOSSIBLE... VOUS AVEZ REUSSI...",
            big,
            GREEN,
            80,
            300
        )

    # -------------------
    # DEFAITE
    # -------------------

    elif state == "lose":

        screen.blit(background,(0,0))

        glow_text(
            "ERREUR DE LOGIQUE DETECTEE",
            big,
            RED,
            120,
            300
        )

    pygame.display.flip()