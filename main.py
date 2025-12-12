import pygame
import sys

pygame.init()

scrn_width = 1280
scrn_height = 1020
scrn = pygame.display.set_mode((scrn_width, scrn_height))
pygame.display.set_caption('Alshabaab War of Tanks')

try:
    title_font = pygame.font.SysFont('Stencil', 80, bold=True)
    subtitle_font = pygame.font.SysFont('Garamond', 50, bold=True)
    button_font = pygame.font.SysFont('Arial', 40, bold=True)
    smallfont = pygame.font.SysFont('Arial', 24, bold=True)
except:
    title_font = pygame.font.SysFont('Arial', 80, bold=True)
    subtitle_font = pygame.font.SysFont('Arial', 50, bold=True)
    button_font = pygame.font.SysFont('Arial', 40, bold=True)
    smallfont = pygame.font.SysFont('Arial', 24, bold=True)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
DARK_GRAY = (30, 30, 30)
GREEN = (0, 200, 0)
BRIGHT_GREEN = (0, 255, 0)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
BUTTON_BORDER = (100, 255, 100)

try:
    bg_raw = pygame.image.load('alshaabab_terrain.jpg')
    BgImage = pygame.transform.scale(bg_raw, (scrn_width, scrn_height))
except:
    BgImage = pygame.Surface((scrn_width, scrn_height))
    BgImage.fill(DARK_GRAY)


def load_tank_img(path):
    try:
        img = pygame.image.load(path).convert_alpha()
        img.set_colorkey(WHITE)
        return img
    except:
        s = pygame.Surface((64, 64))
        s.fill(RED)
        return s


p1_img_1 = load_tank_img('FastRED.png')
p1_img_2 = load_tank_img('tankRED.png')
p1_img_3 = load_tank_img('balanceRED.png')
p1_img_4 = load_tank_img('sniperRED.png')

p2_img_1 = load_tank_img('fastBLUE.png')
p2_img_2 = load_tank_img('tankBLUE.png')
p2_img_3 = load_tank_img('balanceBLUE.png')
p2_img_4 = load_tank_img('sniperBLUE.png')

tank_stats = [
    {"name": "SCOUT", "hp": 3, "speed": 8, "b_speed": 10},
    {"name": "HEAVY", "hp": 8, "speed": 3, "b_speed": 7},
    {"name": "ASSAULT", "hp": 5, "speed": 5, "b_speed": 8},
    {"name": "SNIPER", "hp": 3, "speed": 4, "b_speed": 18}
]

ShapeX1 = 80
ShapeY1 = 80
ShapeX2 = 80
ShapeY2 = 80

score1 = 0
score2 = 0
bullets = []

MENU = 0
P1_SELECT = 1
P2_SELECT = 2
GAME = 3
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

Player1Image = None
Player2Image = None
playerPositionX = 100
playerPositionY = 400
playerPositionX2 = 1000
playerPositionY2 = 400


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
    global playerPositionX, playerPositionY, playerPositionX2, playerPositionY2, bullets
    playerPositionX = 100
    playerPositionY = 400
    playerPositionX2 = 1000
    playerPositionY2 = 400
    bullets = []


def reset_hp():
    global p1_current_hp, p2_current_hp
    p1_current_hp = p1_max_hp
    p2_current_hp = p2_max_hp


def draw_game_screen():
    scrn.blit(BgImage, (0, 0))
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

    if Player1Image: scrn.blit(Player1Image, (playerPositionX, playerPositionY))
    if Player2Image: scrn.blit(Player2Image, (playerPositionX2, playerPositionY2))

    for b in bullets:
        b_color = RED if b[2] == 1 else (100, 100, 255)
        pygame.draw.rect(scrn, b_color, b[0])


load = True
while load:
    scrn.blit(BgImage, (0, 0))
    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            load = False

        if game_state == GAME:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    b_rect = pygame.Rect(playerPositionX + ShapeX1, playerPositionY + ShapeY1 // 2 - 10, 20, 20)
                    bullets.append([b_rect, p1_b_spd, 1])

                if event.key == pygame.K_RSHIFT:
                    b_rect = pygame.Rect(playerPositionX2 - 20, playerPositionY2 + ShapeY2 // 2 - 10, 20, 20)
                    bullets.append([b_rect, -p2_b_spd, 2])

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == MENU:
                button_rect = pygame.Rect(scrn_width // 2 - 125, 450, 250, 100)
                if button_rect.collidepoint((mx, my)):
                    game_state = P1_SELECT

            elif game_state == P1_SELECT:
                for i in range(4):
                    x_pos = 100 + (i * 300)
                    if x_pos < mx < x_pos + 200 and 300 < my < 600:
                        p1_choice = i
                        pygame.time.delay(150)
                        game_state = P2_SELECT

            elif game_state == P2_SELECT:
                for i in range(4):
                    x_pos = 100 + (i * 300)
                    if x_pos < mx < x_pos + 200 and 300 < my < 600:
                        p2_choice = i

                        p1_stats = tank_stats[p1_choice]
                        p2_stats = tank_stats[p2_choice]

                        p1_max_hp = p1_stats['hp']
                        p1_spd = p1_stats['speed']
                        p1_b_spd = p1_stats['b_speed']

                        p2_max_hp = p2_stats['hp']
                        p2_spd = p2_stats['speed']
                        p2_b_spd = p2_stats['b_speed']

                        reset_hp()
                        reset_positions()

                        p1_imgs = [p1_img_1, p1_img_2, p1_img_3, p1_img_4]
                        p2_imgs = [p2_img_1, p2_img_2, p2_img_3, p2_img_4]

                        Player1Image = pygame.transform.scale(p1_imgs[p1_choice], (ShapeX1, ShapeY1))
                        Player2Image = pygame.transform.scale(p2_imgs[p2_choice], (ShapeX2, ShapeY2))

                        game_state = GAME

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

    elif game_state == P1_SELECT or game_state == P2_SELECT:
        if game_state == P1_SELECT:
            header = "PLAYER 1: CHOOSE YOUR TANK"
            header_color = (255, 100, 100)
            prev_imgs = [p1_img_1, p1_img_2, p1_img_3, p1_img_4]
        else:
            header = "PLAYER 2: CHOOSE YOUR TANK"
            header_color = (100, 100, 255)
            prev_imgs = [p2_img_1, p2_img_2, p2_img_3, p2_img_4]

        draw_text_with_shadow(header, subtitle_font, header_color, BLACK, scrn_width // 2, 100, center=True)

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
            draw_text(f"SPD: {stats['speed']}", smallfont, WHITE, x_base + 10, 380)
            draw_text(f"B.SPD: {stats['b_speed']}", smallfont, WHITE, x_base + 10, 410)

            prev = pygame.transform.scale(prev_imgs[i], (120, 120))
            img_x = x_base + (220 - 120) // 2
            scrn.blit(prev, (img_x, 460))

    elif game_state == GAME:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]: playerPositionX -= p1_spd
        if keys[pygame.K_d]: playerPositionX += p1_spd
        if keys[pygame.K_w]: playerPositionY -= p1_spd
        if keys[pygame.K_s]: playerPositionY += p1_spd

        if keys[pygame.K_LEFT]: playerPositionX2 -= p2_spd
        if keys[pygame.K_RIGHT]: playerPositionX2 += p2_spd
        if keys[pygame.K_UP]: playerPositionY2 -= p2_spd
        if keys[pygame.K_DOWN]: playerPositionY2 += p2_spd

        if playerPositionX < 0: playerPositionX = 0
        if playerPositionX > (scrn_width // 2) - ShapeX1 - 5: playerPositionX = (scrn_width // 2) - ShapeX1 - 5
        if playerPositionY < 0: playerPositionY = 0
        if playerPositionY > scrn_height - ShapeY1: playerPositionY = scrn_height - ShapeY1

        if playerPositionX2 < (scrn_width // 2) + 5: playerPositionX2 = (scrn_width // 2) + 5
        if playerPositionX2 > scrn_width - ShapeX2: playerPositionX2 = scrn_width - ShapeX2
        if playerPositionY2 < 0: playerPositionY2 = 0
        if playerPositionY2 > scrn_height - ShapeY2: playerPositionY2 = scrn_height - ShapeY2

        for b in bullets:
            b[0].x += b[1]

        round_over = False
        winner = 0

        for b in bullets[:]:
            if b[0].x < 0 or b[0].x > scrn_width:
                bullets.remove(b)
                continue

            p1_rect = pygame.Rect(playerPositionX, playerPositionY, ShapeX1, ShapeY1)
            p2_rect = pygame.Rect(playerPositionX2, playerPositionY2, ShapeX2, ShapeY2)

            hit = False
            if b[2] == 1 and b[0].colliderect(p2_rect):
                p2_current_hp -= 1
                bullets.remove(b)
                hit = True
                if p2_current_hp <= 0:
                    score1 += 1
                    round_over = True
                    winner = 1

            elif b[2] == 2 and b[0].colliderect(p1_rect):
                p1_current_hp -= 1
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
            pygame.time.delay(2000)

            if score1 >= 5 or score2 >= 5:
                if score1 >= 5:
                    win_msg = "PLAYER 1 WINS THE GAME!"
                    win_color = RED
                else:
                    win_msg = "PLAYER 2 WINS THE GAME!"
                    win_color = (100, 100, 255)

                draw_text_with_shadow(win_msg, subtitle_font, win_color, BLACK, scrn_width // 2, scrn_height // 2,
                                      center=True)
                pygame.display.flip()
                pygame.time.delay(3000)
                score1 = 0
                score2 = 0
                reset_positions()
                game_state = MENU
            else:
                reset_positions()
                reset_hp()
                game_state = P1_SELECT

    pygame.display.flip()

pygame.quit()
sys.exit()