import pygame
import sys
import time
import random
import math

pygame.init()

scrn_width = 1280
scrn_height = 1020
scrn = pygame.display.set_mode((scrn_width, scrn_height))
pygame.display.set_caption('Alshabaab War of Tanks')

try:
    title_font = pygame.font.SysFont('Stencil', 80, bold=True)
    subtitle_font = pygame.font.SysFont('Garamond', 50, bold=True)
    button_font = pygame.font.SysFont('Arial', 30, bold=True)
    smallfont = pygame.font.SysFont('Arial', 24, bold=True)
    info_font = pygame.font.SysFont('Arial', 30, bold=True)
except:
    title_font = pygame.font.SysFont('Arial', 80, bold=True)
    subtitle_font = pygame.font.SysFont('Arial', 50, bold=True)
    button_font = pygame.font.SysFont('Arial', 30, bold=True)
    smallfont = pygame.font.SysFont('Arial', 24, bold=True)
    info_font = pygame.font.SysFont('Arial', 30, bold=True)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
DARK_GRAY = (30, 30, 30)
GREEN = (0, 200, 0)
BRIGHT_GREEN = (0, 255, 0)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
BUTTON_BORDER = (100, 255, 100)
BLUE = (100, 100, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

try:
    bg_raw = pygame.image.load('alshaabab_terrain.jpg')
    BgImage = pygame.transform.scale(bg_raw, (scrn_width, scrn_height))
except:
    BgImage = pygame.Surface((scrn_width, scrn_height))
    BgImage.fill(DARK_GRAY)


def draw_tank(surface, x, y, w, h, t_type, color, is_p2, shield_active=False):
    cx = x + w // 2
    cy = y + h // 2

    if shield_active:
        pygame.draw.circle(surface, GOLD, (cx, cy), w // 2 + 15, 4)

    if t_type == 0:
        if is_p2:
            pts = [(x + w, y), (x + w, y + h), (x, y + h // 2)]
        else:
            pts = [(x, y), (x, y + h), (x + w, y + h // 2)]
        pygame.draw.polygon(surface, color, pts)

    elif t_type == 1:
        pygame.draw.rect(surface, color, (x, y, w, h))
        pygame.draw.rect(surface, BLACK, (x + 10, y + 10, w - 20, h - 20))

    elif t_type == 2:
        pygame.draw.circle(surface, color, (cx, cy), w // 2)
        if is_p2:
            pygame.draw.line(surface, BLACK, (cx, cy), (x, cy), 5)
        else:
            pygame.draw.line(surface, BLACK, (cx, cy), (x + w, cy), 5)

    elif t_type == 3:
        pts = [(cx, y), (x + w, cy), (cx, y + h), (x, cy)]
        pygame.draw.polygon(surface, color, pts)
        if is_p2:
            pygame.draw.line(surface, BLACK, (cx, cy), (x - 10, cy), 3)
        else:
            pygame.draw.line(surface, BLACK, (cx, cy), (x + w + 10, cy), 3)


tank_stats = [
    {"name": "SCOUT", "hp": 3, "speed": 8, "b_speed": 10, "ult": "NITRO BOOST"},
    {"name": "HEAVY", "hp": 8, "speed": 3, "b_speed": 7, "ult": "IRON FORTRESS"},
    {"name": "ASSAULT", "hp": 5, "speed": 5, "b_speed": 8, "ult": "SHOTGUN"},
    {"name": "SNIPER", "hp": 3, "speed": 4, "b_speed": 18, "ult": "RAILGUN"}
]

ShapeX1 = 80
ShapeY1 = 80
ShapeX2 = 80
ShapeY2 = 80

score1 = 0
score2 = 0
bullets = []
last_round_winner = 0

MENU = 0
P1_SELECT = 1
P2_SELECT = 2
GAME = 3
INSTRUCTIONS = 4
HOW_TO_PLAY = 5
GAME_OVER = 6

game_state = MENU

p1_choice = 0
p2_choice = 0
p1_current_hp = 0
p2_current_hp = 0
p1_max_hp = 0
p2_max_hp = 0
p1_spd = 0
p2_spd = 0
p1_b_spd = 0
p2_b_spd = 0

p1_ult_used = False
p2_ult_used = False
p1_ult_active = False
p2_ult_active = False
p1_ult_timer = 0
p2_ult_timer = 0

time_stop_active = False
time_stop_owner = 0
time_stop_start_time = 0
p1_time_cheat_used = False
p2_time_cheat_used = False

p1_barrage_used = False
p2_barrage_used = False
hovering_ammo = []

playerPositionX = 100
playerPositionY = 400
playerPositionX2 = 1000
playerPositionY2 = 400

winner_msg = ""
winner_color = WHITE


def draw_text(text, font, color, x, y, center=False):
    obj = font.render(text, True, color)
    rect = obj.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    scrn.blit(obj, rect)


def draw_text_with_shadow(text, font, color, shadow_color, x, y, center=False, offset=3):
    draw_text(text, font, shadow_color, x + offset, y + offset, center)
    draw_text(text, font, color, x, y, center)


def reset_positions():
    global playerPositionX, playerPositionY, playerPositionX2, playerPositionY2, bullets, time_stop_active, hovering_ammo
    playerPositionX = 100
    playerPositionY = 400
    playerPositionX2 = 1000
    playerPositionY2 = 400
    bullets = []
    hovering_ammo = []
    time_stop_active = False


def reset_hp():
    global p1_current_hp, p2_current_hp
    p1_current_hp = p1_max_hp
    p2_current_hp = p2_max_hp


def reset_ults():
    global p1_ult_used, p2_ult_used, p1_ult_active, p2_ult_active
    p1_ult_used = False
    p2_ult_used = False
    p1_ult_active = False
    p2_ult_active = False


def reset_cheats():
    global p1_time_cheat_used, p2_time_cheat_used, p1_barrage_used, p2_barrage_used
    p1_time_cheat_used = False
    p2_time_cheat_used = False
    p1_barrage_used = False
    p2_barrage_used = False


def draw_game_screen():
    scrn.blit(BgImage, (0, 0))

    if time_stop_active:
        overlay = pygame.Surface((scrn_width, scrn_height))
        overlay.set_alpha(50)
        overlay.fill(PURPLE)
        scrn.blit(overlay, (0, 0))
        draw_text_with_shadow("!! TIME STOP !!", title_font, PURPLE, WHITE, scrn_width // 2, 200, center=True)

    pygame.draw.rect(scrn, BLACK, (scrn_width // 2 - 5, 0, 10, scrn_height))

    draw_text(f"P1: {score1}", subtitle_font, WHITE, 50, 50)
    draw_text(f"P2: {score2}", subtitle_font, WHITE, scrn_width - 150, 50)

    pygame.draw.rect(scrn, RED, (playerPositionX, playerPositionY - 20, ShapeX1, 10))
    if p1_max_hp > 0:
        current_bar_width = ShapeX1 * (p1_current_hp / p1_max_hp)
        pygame.draw.rect(scrn, BRIGHT_GREEN, (playerPositionX, playerPositionY - 20, current_bar_width, 10))

    pygame.draw.rect(scrn, RED, (playerPositionX2, playerPositionY2 - 20, ShapeX2, 10))
    if p2_max_hp > 0:
        current_bar_width = ShapeX2 * (p2_current_hp / p2_max_hp)
        pygame.draw.rect(scrn, BRIGHT_GREEN, (playerPositionX2, playerPositionY2 - 20, current_bar_width, 10))

    if not p1_ult_used:
        draw_text("ULT READY (SPACE)", smallfont, GOLD, playerPositionX, playerPositionY - 45)
    if not p2_ult_used:
        draw_text("ULT READY (ENTER)", smallfont, GOLD, playerPositionX2 - 40, playerPositionY2 - 45)

    p1_shield = (p1_choice == 1 and p1_ult_active)
    p2_shield = (p2_choice == 1 and p2_ult_active)

    p1_color = GRAY if (time_stop_active and time_stop_owner == 2) else RED
    p2_color = GRAY if (time_stop_active and time_stop_owner == 1) else BLUE

    draw_tank(scrn, playerPositionX, playerPositionY, ShapeX1, ShapeY1, p1_choice, p1_color, False, p1_shield)
    draw_tank(scrn, playerPositionX2, playerPositionY2, ShapeX2, ShapeY2, p2_choice, p2_color, True, p2_shield)

    for ammo in hovering_ammo:
        h_color = ORANGE if ammo[0] == 1 else CYAN
        h_x = (playerPositionX + ShapeX1 // 2) if ammo[0] == 1 else (playerPositionX2 + ShapeX2 // 2)
        h_y = (playerPositionY + ShapeY1 // 2) if ammo[0] == 1 else (playerPositionY2 + ShapeY2 // 2)
        pygame.draw.circle(scrn, h_color, (h_x + ammo[2], h_y + ammo[3]), 6)

    for b in bullets:
        is_powerful = b[3] > 1
        is_tracking = b[4]
        b_color = GOLD if is_powerful else (RED if b[2] == 1 else (100, 100, 255))

        if is_tracking:
            b_color = ORANGE if b[2] == 1 else CYAN

        if time_stop_active:
            if b[2] != time_stop_owner:
                b_color = GRAY

        w, h = (30, 10) if is_powerful else (20, 10)
        if is_tracking: w, h = 15, 15

        visual_rect = pygame.Rect(b[0].x, b[0].y, w, h)
        pygame.draw.rect(scrn, b_color, visual_rect)


load = True
while load:
    scrn.blit(BgImage, (0, 0))
    mx, my = pygame.mouse.get_pos()
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            load = False

        if game_state == GAME:
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LALT and not time_stop_active and not p1_time_cheat_used:
                    time_stop_active = True
                    time_stop_owner = 1
                    time_stop_start_time = current_time
                    p1_time_cheat_used = True

                if event.key == pygame.K_RALT and not time_stop_active and not p2_time_cheat_used:
                    time_stop_active = True
                    time_stop_owner = 2
                    time_stop_start_time = current_time
                    p2_time_cheat_used = True

                if event.key == pygame.K_z and not p1_barrage_used:
                    p1_barrage_used = True
                    for _ in range(100):
                        off_x = random.randint(-200, -50)
                        off_y = random.randint(-250, 250)
                        hovering_ammo.append([1, current_time, off_x, off_y])

                if event.key == pygame.K_SLASH and not p2_barrage_used:
                    p2_barrage_used = True
                    for _ in range(100):
                        off_x = random.randint(50, 200)
                        off_y = random.randint(-250, 250)
                        hovering_ammo.append([2, current_time, off_x, off_y])

                if not (time_stop_active and time_stop_owner == 2):
                    if event.key == pygame.K_LCTRL:
                        b_rect = pygame.Rect(playerPositionX + ShapeX1, playerPositionY + ShapeY1 // 2 - 5, 20, 10)
                        bullets.append([b_rect, p1_b_spd, 1, 1, False])

                    if event.key == pygame.K_SPACE and not p1_ult_used:
                        p1_ult_used = True
                        p1_ult_active = True
                        p1_ult_timer = current_time

                        if p1_choice == 2:
                            for i in [-1, 0, 1]:
                                b_rect = pygame.Rect(playerPositionX + ShapeX1,
                                                     playerPositionY + ShapeY1 // 2 - 5 + (i * 20), 20, 10)
                                bullets.append([b_rect, p1_b_spd, 1, 1, False])
                            p1_ult_active = False

                        elif p1_choice == 3:
                            b_rect = pygame.Rect(playerPositionX + ShapeX1, playerPositionY + ShapeY1 // 2 - 5, 40, 15)
                            bullets.append([b_rect, p1_b_spd * 2.5, 1, 3, False])
                            p1_ult_active = False

                if not (time_stop_active and time_stop_owner == 1):
                    if event.key == pygame.K_RSHIFT:
                        b_rect = pygame.Rect(playerPositionX2 - 20, playerPositionY2 + ShapeY2 // 2 - 5, 20, 10)
                        bullets.append([b_rect, -p2_b_spd, 2, 1, False])

                    if event.key == pygame.K_RETURN and not p2_ult_used:
                        p2_ult_used = True
                        p2_ult_active = True
                        p2_ult_timer = current_time

                        if p2_choice == 2:
                            for i in [-1, 0, 1]:
                                b_rect = pygame.Rect(playerPositionX2 - 20,
                                                     playerPositionY2 + ShapeY2 // 2 - 5 + (i * 20), 20, 10)
                                bullets.append([b_rect, -p2_b_spd, 2, 1, False])
                            p2_ult_active = False

                        elif p2_choice == 3:
                            b_rect = pygame.Rect(playerPositionX2 - 40, playerPositionY2 + ShapeY2 // 2 - 5, 40, 15)
                            bullets.append([b_rect, -p2_b_spd * 2.5, 2, 3, False])
                            p2_ult_active = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == MENU:
                button_rect = pygame.Rect(scrn_width // 2 - 125, 450, 250, 100)
                if button_rect.collidepoint((mx, my)):
                    game_state = INSTRUCTIONS

            elif game_state == INSTRUCTIONS:
                play_btn = pygame.Rect(scrn_width // 2 - 260, 750, 250, 80)
                how_btn = pygame.Rect(scrn_width // 2 + 10, 750, 250, 80)
                back_btn = pygame.Rect(scrn_width // 2 - 125, 850, 250, 80)

                if play_btn.collidepoint((mx, my)):
                    game_state = P1_SELECT
                elif how_btn.collidepoint((mx, my)):
                    game_state = HOW_TO_PLAY
                elif back_btn.collidepoint((mx, my)):
                    game_state = MENU

            elif game_state == HOW_TO_PLAY:
                back_btn = pygame.Rect(scrn_width // 2 - 125, 800, 250, 80)
                if back_btn.collidepoint((mx, my)):
                    game_state = INSTRUCTIONS

            elif game_state == GAME_OVER:
                play_again_btn = pygame.Rect(scrn_width // 2 - 260, 600, 250, 80)
                menu_btn = pygame.Rect(scrn_width // 2 + 10, 600, 250, 80)

                if play_again_btn.collidepoint((mx, my)):
                    score1 = 0
                    score2 = 0
                    last_round_winner = 0
                    reset_positions()
                    reset_hp()
                    reset_ults()
                    reset_cheats()
                    game_state = P1_SELECT
                elif menu_btn.collidepoint((mx, my)):
                    score1 = 0
                    score2 = 0
                    last_round_winner = 0
                    reset_positions()
                    reset_ults()
                    reset_cheats()
                    game_state = MENU

            elif game_state == P1_SELECT:
                for i in range(4):
                    x_pos = 100 + (i * 300)
                    if x_pos < mx < x_pos + 200 and 300 < my < 600:
                        p1_choice = i

                        p1_stats = tank_stats[p1_choice]
                        p1_max_hp = p1_stats['hp']
                        p1_spd = p1_stats['speed']
                        p1_b_spd = p1_stats['b_speed']

                        pygame.time.delay(150)

                        if last_round_winner == 1:
                            reset_hp()
                            reset_positions()
                            reset_ults()
                            game_state = GAME
                        else:
                            game_state = P2_SELECT

                back_btn = pygame.Rect(scrn_width // 2 - 125, 800, 250, 80)
                if back_btn.collidepoint((mx, my)):
                    game_state = INSTRUCTIONS

            elif game_state == P2_SELECT:
                for i in range(4):
                    x_pos = 100 + (i * 300)
                    if x_pos < mx < x_pos + 200 and 300 < my < 600:
                        p2_choice = i

                        p2_stats = tank_stats[p2_choice]
                        p2_max_hp = p2_stats['hp']
                        p2_spd = p2_stats['speed']
                        p2_b_spd = p2_stats['b_speed']

                        if last_round_winner == 0:
                            p1_stats = tank_stats[p1_choice]
                            p1_max_hp = p1_stats['hp']
                            p1_spd = p1_stats['speed']
                            p1_b_spd = p1_stats['b_speed']

                        reset_hp()
                        reset_positions()
                        reset_ults()

                        game_state = GAME

                back_btn = pygame.Rect(scrn_width // 2 - 125, 800, 250, 80)
                if back_btn.collidepoint((mx, my)):
                    game_state = P1_SELECT

    if game_state == MENU:
        draw_text_with_shadow("ALSHABAAB WAR OF TANKS", title_font, WHITE, BLACK, scrn_width // 2, 250, center=True)
        draw_text("PRESS START TO BATTLE", subtitle_font, GOLD, scrn_width // 2, 350, center=True)
        button_x, button_y, button_w, button_h = scrn_width // 2 - 125, 450, 250, 100
        button_rect = pygame.Rect(button_x, button_y, button_w, button_h)

        if button_rect.collidepoint((mx, my)):
            pygame.draw.rect(scrn, BRIGHT_GREEN, button_rect, border_radius=15)
            pygame.draw.rect(scrn, WHITE, button_rect, 3, border_radius=15)
            draw_text("START", button_font, BLACK, button_x + button_w // 2, button_y + button_h // 2, center=True)
        else:
            pygame.draw.rect(scrn, GREEN, button_rect, border_radius=15)
            pygame.draw.rect(scrn, BUTTON_BORDER, button_rect, 3, border_radius=15)
            draw_text("START", button_font, WHITE, button_x + button_w // 2, button_y + button_h // 2, center=True)

    elif game_state == INSTRUCTIONS:
        draw_text_with_shadow("GAME CONTROLS", title_font, GOLD, BLACK, scrn_width // 2, 80, center=True)

        pygame.draw.rect(scrn, (50, 0, 0), (100, 150, 500, 550))
        pygame.draw.rect(scrn, RED, (100, 150, 500, 550), 4)
        draw_text("PLAYER 1", subtitle_font, RED, 350, 200, center=True)
        draw_text("MOVE: W A S D", button_font, WHITE, 350, 300, center=True)
        draw_text("SHOOT: L-CTRL", button_font, WHITE, 350, 400, center=True)
        draw_text("ULTIMATE: SPACE", button_font, GOLD, 350, 500, center=True)
        draw_text("(Once per round)", smallfont, WHITE, 350, 540, center=True)

        pygame.draw.rect(scrn, (0, 0, 50), (680, 150, 500, 550))
        pygame.draw.rect(scrn, BLUE, (680, 150, 500, 550), 4)
        draw_text("PLAYER 2", subtitle_font, BLUE, 930, 200, center=True)
        draw_text("MOVE: ARROWS", button_font, WHITE, 930, 300, center=True)
        draw_text("SHOOT: R-SHIFT", button_font, WHITE, 930, 400, center=True)
        draw_text("ULTIMATE: ENTER", button_font, GOLD, 930, 500, center=True)
        draw_text("(Once per round)", smallfont, WHITE, 930, 540, center=True)

        play_btn = pygame.Rect(scrn_width // 2 - 260, 750, 250, 80)
        how_btn = pygame.Rect(scrn_width // 2 + 10, 750, 250, 80)
        back_btn = pygame.Rect(scrn_width // 2 - 125, 850, 250, 80)

        if play_btn.collidepoint((mx, my)):
            pygame.draw.rect(scrn, BRIGHT_GREEN, play_btn, border_radius=10)
            draw_text("CONTINUE", button_font, BLACK, play_btn.centerx, play_btn.centery, center=True)
        else:
            pygame.draw.rect(scrn, GREEN, play_btn, border_radius=10)
            draw_text("CONTINUE", button_font, WHITE, play_btn.centerx, play_btn.centery, center=True)

        if how_btn.collidepoint((mx, my)):
            pygame.draw.rect(scrn, (200, 200, 0), how_btn, border_radius=10)
            draw_text("HOW TO PLAY", button_font, BLACK, how_btn.centerx, how_btn.centery, center=True)
        else:
            pygame.draw.rect(scrn, (150, 150, 0), how_btn, border_radius=10)
            draw_text("HOW TO PLAY", button_font, WHITE, how_btn.centerx, how_btn.centery, center=True)

        if back_btn.collidepoint((mx, my)):
            pygame.draw.rect(scrn, (200, 50, 50), back_btn, border_radius=10)
            draw_text("BACK", button_font, BLACK, back_btn.centerx, back_btn.centery, center=True)
        else:
            pygame.draw.rect(scrn, RED, back_btn, border_radius=10)
            draw_text("BACK", button_font, WHITE, back_btn.centerx, back_btn.centery, center=True)

    elif game_state == HOW_TO_PLAY:
        draw_text_with_shadow("HOW TO PLAY", title_font, GOLD, BLACK, scrn_width // 2, 100, center=True)

        pygame.draw.rect(scrn, DARK_GRAY, (200, 200, 880, 500))
        pygame.draw.rect(scrn, WHITE, (200, 200, 880, 500), 3)

        lines = [
            "Welcome to Alshabaab War of Tanks!",
            "",
            "1. Select your favorite Tank class.",
            "2. Each tank has a UNIQUE ULTIMATE SKILL:",
            "   - Scout: Nitro Boost (2x Speed)",
            "   - Heavy: Iron Fortress (Invincible)",
            "   - Assault: Shotgun (3 Bullets)",
            "   - Sniper: Railgun (3x Damage)",
            "3. Winner chooses tank, Loser keeps same tank.",
            "4. The first player to reach 5 points wins!",
        ]

        for i, line in enumerate(lines):
            draw_text(line, info_font, WHITE, scrn_width // 2, 250 + (i * 40), center=True)

        back_btn = pygame.Rect(scrn_width // 2 - 125, 800, 250, 80)
        if back_btn.collidepoint((mx, my)):
            pygame.draw.rect(scrn, (200, 50, 50), back_btn, border_radius=10)
            draw_text("BACK", button_font, BLACK, back_btn.centerx, back_btn.centery, center=True)
        else:
            pygame.draw.rect(scrn, RED, back_btn, border_radius=10)
            draw_text("BACK", button_font, WHITE, back_btn.centerx, back_btn.centery, center=True)

    elif game_state == P1_SELECT or game_state == P2_SELECT:

        current_round_num = score1 + score2 + 1

        if game_state == P1_SELECT:
            header = "PLAYER 1: CHOOSE YOUR TANK"
            header_color = (255, 100, 100)
            p_color = RED
            is_p2 = False
        else:
            header = "PLAYER 2: CHOOSE YOUR TANK"
            header_color = (100, 100, 255)
            p_color = BLUE
            is_p2 = True

        draw_text_with_shadow(f"ROUND {current_round_num}", title_font, GOLD, BLACK, scrn_width // 2, 80, center=True)
        draw_text_with_shadow(header, subtitle_font, header_color, BLACK, scrn_width // 2, 160, center=True)

        for i in range(4):
            x_base = 100 + (i * 300)
            stats = tank_stats[i]
            card_rect = pygame.Rect(x_base, 300, 220, 300)
            pygame.draw.rect(scrn, (40, 40, 40, 200), card_rect)

            if card_rect.collidepoint((mx, my)):
                pygame.draw.rect(scrn, header_color, card_rect, 3)
            else:
                pygame.draw.rect(scrn, (100, 100, 100), card_rect, 2)

            draw_text(stats['name'], smallfont, GOLD, x_base + 10, 310)
            draw_text(f"HP: {stats['hp']}", smallfont, WHITE, x_base + 10, 350)
            draw_text(f"Speed: {stats['speed']}", smallfont, WHITE, x_base + 10, 380)
            draw_text(f"Ult: {stats['ult']}", smallfont, ORANGE, x_base + 10, 410)

            prev_w = 80
            prev_h = 80
            px = x_base + (220 - prev_w) // 2
            py = 460
            draw_tank(scrn, px, py, prev_w, prev_h, i, p_color, is_p2)

        back_btn = pygame.Rect(scrn_width // 2 - 125, 800, 250, 80)
        if back_btn.collidepoint((mx, my)):
            pygame.draw.rect(scrn, (200, 50, 50), back_btn, border_radius=10)
            draw_text("BACK", button_font, BLACK, back_btn.centerx, back_btn.centery, center=True)
        else:
            pygame.draw.rect(scrn, RED, back_btn, border_radius=10)
            draw_text("BACK", button_font, WHITE, back_btn.centerx, back_btn.centery, center=True)

    elif game_state == GAME:
        keys = pygame.key.get_pressed()

        if time_stop_active:
            if current_time - time_stop_start_time > 1000:
                time_stop_active = False

        if p1_ult_active and p1_choice in [0, 1]:
            if current_time - p1_ult_timer > 3000:
                p1_ult_active = False

        if p2_ult_active and p2_choice in [0, 1]:
            if current_time - p2_ult_timer > 3000:
                p2_ult_active = False

        for ammo in hovering_ammo[:]:
            if current_time - ammo[1] > 2000:
                start_x = (playerPositionX + ShapeX1 // 2) if ammo[0] == 1 else (playerPositionX2 + ShapeX2 // 2)
                start_y = (playerPositionY + ShapeY1 // 2) if ammo[0] == 1 else (playerPositionY2 + ShapeY2 // 2)

                b_rect = pygame.Rect(start_x + ammo[2], start_y + ammo[3], 15, 15)
                bullets.append([b_rect, 12, ammo[0], 1, True])
                hovering_ammo.remove(ammo)

        current_p1_spd = p1_spd * 2 if (p1_choice == 0 and p1_ult_active) else p1_spd
        current_p2_spd = p2_spd * 2 if (p2_choice == 0 and p2_ult_active) else p2_spd

        if not (time_stop_active and time_stop_owner == 2):
            if keys[pygame.K_a]: playerPositionX -= current_p1_spd
            if keys[pygame.K_d]: playerPositionX += current_p1_spd
            if keys[pygame.K_w]: playerPositionY -= current_p1_spd
            if keys[pygame.K_s]: playerPositionY += current_p1_spd

        if not (time_stop_active and time_stop_owner == 1):
            if keys[pygame.K_LEFT]: playerPositionX2 -= current_p2_spd
            if keys[pygame.K_RIGHT]: playerPositionX2 += current_p2_spd
            if keys[pygame.K_UP]: playerPositionY2 -= current_p2_spd
            if keys[pygame.K_DOWN]: playerPositionY2 += current_p2_spd

        if playerPositionX < 0: playerPositionX = 0
        if playerPositionX > (scrn_width // 2) - ShapeX1 - 5: playerPositionX = (scrn_width // 2) - ShapeX1 - 5
        if playerPositionY < 0: playerPositionY = 0
        if playerPositionY > scrn_height - ShapeY1: playerPositionY = scrn_height - ShapeY1

        if playerPositionX2 < (scrn_width // 2) + 5: playerPositionX2 = (scrn_width // 2) + 5
        if playerPositionX2 > scrn_width - ShapeX2: playerPositionX2 = scrn_width - ShapeX2
        if playerPositionY2 < 0: playerPositionY2 = 0
        if playerPositionY2 > scrn_height - ShapeY2: playerPositionY2 = scrn_height - ShapeY2

        for b in bullets:
            move_allowed = True
            if time_stop_active:
                if b[2] != time_stop_owner:
                    move_allowed = False

            if move_allowed:
                is_tracking = b[4]
                if is_tracking:
                    target_x = (playerPositionX2 + ShapeX2 // 2) if b[2] == 1 else (playerPositionX + ShapeX1 // 2)
                    target_y = (playerPositionY2 + ShapeY2 // 2) if b[2] == 1 else (playerPositionY + ShapeY1 // 2)

                    dx = target_x - b[0].centerx
                    dy = target_y - b[0].centery
                    dist = math.sqrt(dx ** 2 + dy ** 2)

                    if dist != 0:
                        speed = b[1]  # speed is magnitude here
                        vel_x = (dx / dist) * speed
                        vel_y = (dy / dist) * speed
                        b[0].x += vel_x
                        b[0].y += vel_y
                else:
                    b[0].x += b[1]

        round_over = False
        winner = 0

        for b in bullets[:]:
            if b[0].x < -500 or b[0].x > scrn_width + 500 or b[0].y < -500 or b[0].y > scrn_height + 500:
                bullets.remove(b)
                continue

            p1_rect = pygame.Rect(playerPositionX, playerPositionY, ShapeX1, ShapeY1)
            p2_rect = pygame.Rect(playerPositionX2, playerPositionY2, ShapeX2, ShapeY2)

            hit = False
            bullet_dmg = b[3]

            if b[2] == 1 and b[0].colliderect(p2_rect):
                if not (p2_choice == 1 and p2_ult_active):
                    p2_current_hp -= bullet_dmg
                bullets.remove(b)
                hit = True
                if p2_current_hp <= 0:
                    score1 += 1
                    round_over = True
                    winner = 1

            elif b[2] == 2 and b[0].colliderect(p1_rect):
                if not (p1_choice == 1 and p1_ult_active):
                    p1_current_hp -= bullet_dmg
                bullets.remove(b)
                hit = True
                if p1_current_hp <= 0:
                    score2 += 1
                    round_over = True
                    winner = 2

            if hit: break

        draw_game_screen()

        if round_over:
            pygame.display.flip()
            pygame.time.delay(1000)

            last_round_winner = winner

            if score1 >= 5 or score2 >= 5:
                if score1 >= 5:
                    winner_msg = "PLAYER 1 WINS THE GAME!"
                    winner_color = RED
                else:
                    winner_msg = "PLAYER 2 WINS THE GAME!"
                    winner_color = BLUE

                game_state = GAME_OVER
            else:
                reset_positions()
                reset_hp()
                reset_ults()

                if last_round_winner == 2:
                    game_state = P2_SELECT
                else:
                    game_state = P1_SELECT

    elif game_state == GAME_OVER:
        draw_text_with_shadow(winner_msg, title_font, winner_color, BLACK, scrn_width // 2, 300, center=True)
        draw_text("GAME OVER", subtitle_font, WHITE, scrn_width // 2, 450, center=True)

        play_again_btn = pygame.Rect(scrn_width // 2 - 260, 600, 250, 80)
        menu_btn = pygame.Rect(scrn_width // 2 + 10, 600, 250, 80)

        if play_again_btn.collidepoint((mx, my)):
            pygame.draw.rect(scrn, BRIGHT_GREEN, play_again_btn, border_radius=10)
            draw_text("PLAY AGAIN", button_font, BLACK, play_again_btn.centerx, play_again_btn.centery, center=True)
        else:
            pygame.draw.rect(scrn, GREEN, play_again_btn, border_radius=10)
            draw_text("PLAY AGAIN", button_font, WHITE, play_again_btn.centerx, play_again_btn.centery, center=True)

        if menu_btn.collidepoint((mx, my)):
            pygame.draw.rect(scrn, (200, 200, 200), menu_btn, border_radius=10)
            draw_text("MAIN MENU", button_font, BLACK, menu_btn.centerx, menu_btn.centery, center=True)
        else:
            pygame.draw.rect(scrn, GRAY, menu_btn, border_radius=10)
            draw_text("MAIN MENU", button_font, WHITE, menu_btn.centerx, menu_btn.centery, center=True)

    pygame.display.flip()

pygame.quit()
sys.exit()