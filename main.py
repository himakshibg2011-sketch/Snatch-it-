import pygame
import random
import math
import cv2
import os

print("Current folder:", os.getcwd())
print("Intro exists:", os.path.exists("SNACTH IT! (1).mp4"))
print("Home exists:", os.path.exists("Add a heading.mp4"))


pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Apple Grab Multiplayer")
clock = pygame.time.Clock()

# ===== BACKGROUND MUSIC =====
BG_MUSIC = "bg_music.ogg"

# ===== SOUNDS =====
CLICK_SOUND = pygame.mixer.Sound("click.ogg")
CLICK_SOUND.set_volume(0.8)

APPLE_SOUND = pygame.mixer.Sound("apple.ogg")
APPLE_SOUND.set_volume(0.8)

SWEET_SOUND = pygame.mixer.Sound("sweet.ogg")
SWEET_SOUND.set_volume(0.8)

WIN_SOUND = None

def play_sound(sound):
    sound.play()


FONT = pygame.font.SysFont("arial", 28)
BIG_FONT = pygame.font.SysFont("arial", 48)
COMIC_SMALL = pygame.font.SysFont("comicsansms", 14)
TITLE_FONT = pygame.font.SysFont("comicsansms", 60)

WHITE = (255,255,255)
BLACK = (20,20,20)
RED = (220,70,70)
GREEN = (60,200,80)
YELLOW = (255,215,0)
BLUE = (70,140,255)
PURPLE = (180,80,255)
GRAY = (220,220,220)

INTRO_VIDEO = r"SNACTH IT! (1).mp4"
HOME_VIDEO = r"Add a heading.mp4"



# ===== BACKGROUND MUSIC =====
BG_MUSIC = "bg_music.ogg"

# ===== SOUNDS =====
CLICK_SOUND = pygame.mixer.Sound("click.ogg")
CLICK_SOUND.set_volume(0.8)

APPLE_SOUND = pygame.mixer.Sound("apple.ogg")
APPLE_SOUND.set_volume(0.8)

SWEET_SOUND = pygame.mixer.Sound("sweet.ogg")
SWEET_SOUND.set_volume(0.8)


if os.path.exists("winner.ogg"):
    WIN_SOUND = pygame.mixer.Sound("winner.ogg")
    WIN_SOUND.set_volume(0.9)
else:
    WIN_SOUND = None



def play_sound(sound):
    sound.play()




players = [
    {"name":"Player 1","color":RED,"corner":(120,120)},
    {"name":"Player 2","color":BLUE,"corner":(WIDTH-120,120)},
    {"name":"Player 3","color":GREEN,"corner":(120,HEIGHT-120)},
    {"name":"Player 4","color":PURPLE,"corner":(WIDTH-120,HEIGHT-120)},
]

selected_time = None
control_mode = None
show_warning = False

CONTROL_MAP = {
    "WASD": {
        pygame.K_w:0,
        pygame.K_a:1,
        pygame.K_s:2,
        pygame.K_d:3
    },
    "ARROWS": {
        pygame.K_UP:0,
        pygame.K_LEFT:1,
        pygame.K_DOWN:2,
        pygame.K_RIGHT:3
    }
}


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x,y,w,h)
        self.text = text

    def draw(self, active=False):
        mouse = pygame.mouse.get_pos()
        hover = self.rect.collidepoint(mouse)

        scale = 5 if hover else 0

        rect = pygame.Rect(
            self.rect.x-scale//2,
            self.rect.y-scale//2,
            self.rect.w+scale,
            self.rect.h+scale
        )

        color = (255,220,120) if active else (255,255,255)

        pygame.draw.rect(screen, color, rect, border_radius=15)
        pygame.draw.rect(screen, BLACK, rect, 3, border_radius=15)

        txt = FONT.render(self.text, True, BLACK)
        screen.blit(txt, txt.get_rect(center=rect.center))

    def clicked(self, pos):
        return self.rect.collidepoint(pos)


timer_buttons = {
    15: Button(150,520,100,55,"15s"),
    30: Button(280,520,100,55,"30s"),
    45: Button(410,520,100,55,"45s"),
    60: Button(540,520,100,55,"60s"),
}

wasd_btn = Button(700,510,120,55,"WASD")
arrow_btn = Button(840,510,120,55,"ARROWS")
play_btn = Button(420,610,160,60,"PLAY!")
start_btn = Button(400,580,200,70,"START")


def play_sound(sound):
    if sound:
        sound.play()



def play_video_frame(cap, video_type="home"):

    # video info
    total_frames = int(
        cap.get(cv2.CAP_PROP_FRAME_COUNT)
    )

    fps = cap.get(
        cv2.CAP_PROP_FPS
    )

    if fps == 0:
        fps = 30

    # ===== DIFFERENT SETTINGS =====

    if video_type == "intro":
        # Snatch It video
        cut_end_seconds = 1.5
        restart_seconds = 2.1

    else:
        # Add a heading video
        cut_end_seconds = 3.5
        restart_seconds = 1.3

    cut_frames = int(
        cut_end_seconds * fps
    )

    restart_frame = int(
        restart_seconds * fps
    )

    current_frame = int(
        cap.get(cv2.CAP_PROP_POS_FRAMES)
    )

    # stop early before ending
    if current_frame >= total_frames - cut_frames:

        cap.set(
            cv2.CAP_PROP_POS_FRAMES,
            restart_frame
        )

    success, frame = cap.read()

    if not success:

        cap.set(
            cv2.CAP_PROP_POS_FRAMES,
            restart_frame
        )

        success, frame = cap.read()

    frame = cv2.resize(
        frame,
        (WIDTH, HEIGHT)
    )

    frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    frame_surface = pygame.surfarray.make_surface(
        frame.swapaxes(0, 1)
    )

    screen.blit(
        frame_surface,
        (0, 0)
    )


def intro_screen():

    cap = cv2.VideoCapture(INTRO_VIDEO)

    # start looping music
    pygame.mixer.music.load(BG_MUSIC)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)   # -1 = infinite loop

    start_button = pygame.Rect(
        430,
        430,
        130,
        55
    )

    while True:

        play_video_frame(cap, "intro")

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if start_button.collidepoint(event.pos):

                    CLICK_SOUND.play()

                    cap.release()
                    return

        clock.tick(30)


def homepage():
    global selected_time, control_mode, show_warning

    cap = cv2.VideoCapture(HOME_VIDEO)

    # ===== INVISIBLE BUTTONS =====

    # TIMER BUTTONS
    btn15 = pygame.Rect(125, 180, 130, 50)
    btn30 = pygame.Rect(330, 180, 130, 50)
    btn45 = pygame.Rect(540, 185, 130, 50)
    btn60 = pygame.Rect(750, 185, 130, 50)

    # CONTROL BUTTONS
    wasd_btn = pygame.Rect(150, 440, 160, 60)
    arrow_btn = pygame.Rect(650, 440, 180, 60)

    # PLAY BUTTON
    play_btn = pygame.Rect(720, 45, 180, 70)

    while True:

        play_video_frame(cap, "home")

        # ===== TIMER UNDERLINES =====
        if selected_time == 15:
            pygame.draw.line(
                screen,
                BLACK,
                (125, 230),
                (215, 230),
                5
            )

        elif selected_time == 30:
            pygame.draw.line(
                screen,
                BLACK,
                (350, 230),
                (440, 230),
                5
            )

        elif selected_time == 45:
            pygame.draw.line(
                screen,
                BLACK,
                (560, 235),
                (650, 235),
                5
            )

        elif selected_time == 60:
            pygame.draw.line(
                screen,
                BLACK,
                (770, 235),
                (860, 235),
                5
            )

        # ===== CONTROL UNDERLINES =====
        if control_mode == "WASD":
            pygame.draw.line(
                screen,
                BLACK,
                (180, 505),
                (285, 505),
                5
            )

        elif control_mode == "ARROWS":
            pygame.draw.line(
                screen,
                BLACK,
                (690, 505),
                (810, 505),
                5
            )

        # ===== WARNING TEXT =====
        if show_warning:

            warning = COMIC_SMALL.render(
                "pls chose the modes first",
                True,
                (255, 0, 0)
            )

            warning_rect = warning.get_rect(
                center=(865, 135)  # moved more right
            )

            screen.blit(warning, warning_rect)

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                pos = event.pos

                # TIMER BUTTONS
                if btn15.collidepoint(pos):
                    selected_time = 15
                    show_warning = False
                    CLICK_SOUND.play()

                elif btn30.collidepoint(pos):
                    selected_time = 30
                    show_warning = False
                    play_sound(CLICK_SOUND)

                elif btn45.collidepoint(pos):
                    selected_time = 45
                    show_warning = False
                    play_sound(CLICK_SOUND)

                elif btn60.collidepoint(pos):
                    selected_time = 60
                    show_warning = False
                    play_sound(CLICK_SOUND)

                # CONTROL BUTTONS
                elif wasd_btn.collidepoint(pos):
                    control_mode = "WASD"
                    show_warning = False
                    play_sound(CLICK_SOUND)

                elif arrow_btn.collidepoint(pos):
                    control_mode = "ARROWS"
                    show_warning = False
                    play_sound(CLICK_SOUND)

                # PLAY BUTTON
                elif play_btn.collidepoint(pos):

                    if (
                        selected_time is None
                        or control_mode is None
                    ):
                        show_warning = True

                    else:
                        play_sound(CLICK_SOUND)
                        cap.release()
                        return

        clock.tick(30)



def spawn_item():
    return {
        "type": random.choice(["apple","sweet"])
    }


def draw_player(player, score):

    pygame.draw.circle(
        screen,
        player["color"],
        player["corner"],
        50
    )

    txt = FONT.render(str(score), True, WHITE)
    screen.blit(txt, txt.get_rect(center=player["corner"]))


def draw_item(item):

    cx, cy = WIDTH//2, HEIGHT//2

    if item["type"] == "apple":
        pygame.draw.circle(screen, RED, (cx,cy), 35)
        pygame.draw.rect(screen, (90,50,20), (cx-3, cy-45, 6, 20))
        pygame.draw.ellipse(screen, GREEN, (cx+5, cy-45, 22, 12))

    else:
        pygame.draw.rect(
            screen,
            YELLOW,
            (cx-40, cy-18, 80, 36),
            border_radius=12
        )
        pygame.draw.circle(screen, YELLOW, (cx-40,cy), 18)
        pygame.draw.circle(screen, YELLOW, (cx+40,cy), 18)


def draw_center_item(item):

    cx = WIDTH // 2
    cy = HEIGHT // 2

    # ===== APPLE =====
    if item["type"] == "apple":

        pygame.draw.circle(
            screen,
            RED,
            (cx, cy),
            35
        )

        pygame.draw.rect(
            screen,
            (90, 50, 20),
            (cx - 3, cy - 45, 6, 20)
        )

        pygame.draw.ellipse(
            screen,
            GREEN,
            (cx + 5, cy - 45, 22, 12)
        )

    # ===== SWEET =====
    else:

        pygame.draw.rect(
            screen,
            YELLOW,
            (cx - 40, cy - 18, 80, 36),
            border_radius=12
        )

        pygame.draw.circle(
            screen,
            YELLOW,
            (cx - 40, cy),
            18
        )

        pygame.draw.circle(
            screen,
            YELLOW,
            (cx + 40, cy),
            18
        )


def game():

    # ===== LOAD TEMPLATE =====
    GAME_BG = pygame.image.load(
        "game_template.png"
    ).convert()

    GAME_BG = pygame.transform.scale(
        GAME_BG,
        (WIDTH, HEIGHT)
    )

    scores = [0, 0, 0, 0]

    item = None
    item_spawn_time = 0

    next_spawn = (
        pygame.time.get_ticks()
        + random.randint(500, 2500)
    )

    start = pygame.time.get_ticks()
    total_time = selected_time * 1000

    while True:

        now = pygame.time.get_ticks()

        remaining = max(
            0,
            (total_time - (now - start)) // 1000
        )

        # ===== END GAME =====
        if now - start >= total_time:
            return scores

        # ===== DRAW TEMPLATE =====
        screen.blit(
            GAME_BG,
            (0, 0)
        )



        # ===== PLAYER SCORES =====
        score_font = pygame.font.SysFont(
            "comic sans ms",
            42,
            bold=True
        )

        p1 = score_font.render(
            str(scores[0]),
            True,
            BLACK
        )

        p2 = score_font.render(
            str(scores[1]),
            True,
            BLACK
        )

        p3 = score_font.render(
            str(scores[2]),
            True,
            BLACK
        )

        p4 = score_font.render(
            str(scores[3]),
            True,
            BLACK
        )

        # ===== SCORE POSITIONS =====
        screen.blit(p1, p1.get_rect(center=(66, 149)))
        screen.blit(p2, p2.get_rect(center=(69, 642)))
        screen.blit(p3, p3.get_rect(center=(939, 129)))
        screen.blit(p4, p4.get_rect(center=(935, 633)))

        # ===== TIMER =====
        timer_font = pygame.font.SysFont(
            "comic sans ms",
            36,
            bold=True
        )

        timer_text = timer_font.render(
            f"{remaining}",
            True,
            BLACK
        )

        screen.blit(
            timer_text,
            (485, 30)
        )

        # ===== SPAWN ITEM =====
        if item is None and now >= next_spawn:
            item = spawn_item()
            item_spawn_time = now

        # ===== REMOVE ITEM AFTER 1.5 SEC =====
        if item and now - item_spawn_time >= 1500:

            item = None

            next_spawn = (
                now
                + random.randint(
                    500,
                    2500
                )
            )

        # ===== DRAW CENTER ITEM =====
        if item:

            center_x = WIDTH // 2
            center_y = HEIGHT // 2

            if item["type"] == "apple":

                pygame.draw.circle(
                    screen,
                    RED,
                    (center_x, center_y),
                    35
                )

                pygame.draw.rect(
                    screen,
                    (90, 50, 20),
                    (
                        center_x - 3,
                        center_y - 45,
                        6,
                        20
                    )
                )

                pygame.draw.ellipse(
                    screen,
                    GREEN,
                    (
                        center_x + 5,
                        center_y - 45,
                        22,
                        12
                    )
                )

            else:

                pygame.draw.rect(
                    screen,
                    YELLOW,
                    (
                        center_x - 40,
                        center_y - 18,
                        80,
                        36
                    ),
                    border_radius=12
                )

                pygame.draw.circle(
                    screen,
                    YELLOW,
                    (
                        center_x - 40,
                        center_y
                    ),
                    18
                )

                pygame.draw.circle(
                    screen,
                    YELLOW,
                    (
                        center_x + 40,
                        center_y
                    ),
                    18
                )

        # ===== EVENTS =====
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if (
                event.type == pygame.KEYDOWN
                and item
            ):

                mapping = CONTROL_MAP[
                    control_mode
                ]

                if event.key in mapping:

                    player_index = mapping[
                        event.key
                    ]

                    # ===== APPLE =====
                    if item["type"] == "apple":

                        scores[
                            player_index
                        ] += 1

                        APPLE_SOUND.play()

                    # ===== SWEET =====
                    else:

                        scores[
                            player_index
                        ] -= 2

                        SWEET_SOUND.play()

                    item = None

                    next_spawn = (
                        now
                        + random.randint(
                            500,
                            2500
                        )
                    )

        pygame.display.flip()
        clock.tick(60)



def generate_confetti(winner_index):

    particles = []

    colors = [
        RED,
        BLUE,
        GREEN,
        PURPLE,
        YELLOW
    ]

    # player positions
    positions = [
        (100, 120),
        (100, 580),
        (900, 120),
        (900, 580)
    ]

    px, py = positions[winner_index]

    for _ in range(150):

        angle = random.uniform(
            0,
            math.pi * 2
        )

        speed = random.uniform(
            2,
            8
        )

        particles.append({

            "x": px,
            "y": py,

            "vx": math.cos(angle)
            * speed,

            "vy": math.sin(angle)
            * speed,

            "color": random.choice(
                colors
            )
        })

    return particles


def winner_screen(scores):

    # ===== FIND WINNER / TIE =====
    max_score = max(scores)

    winners = [
        i for i, score in enumerate(scores)
        if score == max_score
    ]

    is_tie = len(winners) > 1
    winner = winners[0]

    # ===== PLAY WIN SOUND ONLY IF NOT TIE =====
    if WIN_SOUND and not is_tie:
        play_sound(WIN_SOUND)

    # ===== LOAD TEMPLATE =====
    WIN_TEMPLATE = pygame.image.load(
        "winner_template.png"
    ).convert()

    WIN_TEMPLATE = pygame.transform.scale(
        WIN_TEMPLATE,
        (WIDTH, HEIGHT)
    )

    replay_font = pygame.font.Font(
        "Chewy-Regular.ttf",
        30
    )

    # ===== WINNER TITLE FONT =====
    winner_font = pygame.font.Font(
        "Chewy-Regular.ttf",
        42
    )

    # ===== CONFETTI =====
    particles = []

    # ONLY CREATE CONFETTI IF THERE IS A WINNER
    if not is_tie:

        colors = [
            (255, 80, 80),
            (80, 140, 255),
            (80, 220, 120),
            (255, 220, 80),
            (180, 80, 255)
        ]

        for _ in range(200):

            particles.append({

                "x": random.randint(
                    0,
                    WIDTH
                ),

                "y": random.randint(
                    -HEIGHT,
                    0
                ),

                "speed": random.uniform(
                    2,
                    6
                ),

                "color": random.choice(
                    colors
                ),

                "size": random.randint(
                    3,
                    6
                )
            })

    while True:

        # ===== DRAW TEMPLATE =====
        screen.blit(WIN_TEMPLATE, (0, 0))

        # ===== CONFETTI (ONLY IF WINNER) =====
        if not is_tie:

            for p in particles:

                p["y"] += p["speed"]

                if p["y"] > HEIGHT:

                    p["y"] = random.randint(
                        -20,
                        0
                    )

                    p["x"] = random.randint(
                        0,
                        WIDTH
                    )

                pygame.draw.circle(
                    screen,
                    p["color"],
                    (
                        int(p["x"]),
                        int(p["y"])
                    ),
                    p["size"]
                )

        # ===== WINNER / TIE TEXT =====
        if is_tie:

            title = "A Tie!"

        else:

            title = (
                f"Player {winner + 1} "
                f"has won the game!"
            )

        winner_text = winner_font.render(
            title,
            True,
            (230, 200, 255)  # #e6c8ff
        )

        screen.blit(
            winner_text,
            winner_text.get_rect(
                center=(WIDTH // 2, 275)
            )
        )

        # ===== SCORES =====
        score_font = pygame.font.SysFont(
            "arial",
            28,
            bold=True
        )

        for i, player in enumerate(players):

            score_text = score_font.render(
                f"{player['name']} : {scores[i]}",
                True,
                player["color"]
            )

            screen.blit(
                score_text,
                score_text.get_rect(
                    center=(
                        WIDTH // 2,
                        340 + (i * 55)
                    )
                )
            )

        # ===== REPLAY TEXT =====
        space_text = replay_font.render(
            "Press SPACE to Play Again",
            True,
            (191, 235, 244)
        )

        esc_text = replay_font.render(
            "Press ESC to Quit",
            True,
            (191, 235, 244)
        )

        # ===== YOUR POSITIONS =====
        screen.blit(
            space_text,
            (334, 568)
        )

        screen.blit(
            esc_text,
            (400, 141)
        )

        pygame.display.flip()

        # ===== EVENTS =====
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    return

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        clock.tick(60)


while True:

    intro_screen()
    homepage()
    scores = game()
    winner_screen(scores)

