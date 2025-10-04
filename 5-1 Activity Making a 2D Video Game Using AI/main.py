"""
A small 2D Pygame game:
- Player: square, moved with arrow keys or WASD.
- Enemy: moving circle that bounces around.
- Score: increases over time (seconds survived) and by collecting small coins.
- Challenge: avoid enemy; game over on collision or when timer reaches 0.
- Win: reach target score before timer runs out.
- On-screen instructions and score shown.

Controls:
- Arrow keys or WASD: move
- R: restart after game over/win
- ESC or window close: quit
"""

import pygame
import random
import sys
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_r

# ---------- Game settings ----------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

PLAYER_SIZE = 40
PLAYER_SPEED = 300  # pixels per second

ENEMY_RADIUS = 25
ENEMY_SPEED = 180  # pixels per second

COIN_RADIUS = 7
NUM_COINS = 5

START_TIME = 45  # seconds (countdown timer)
WIN_SCORE = 20   # score (seconds + coins) required to win

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_COLOR = (70, 130, 180)   # steelblue
ENEMY_COLOR = (200, 50, 50)     # red-ish
COIN_COLOR = (240, 200, 20)     # gold-ish
BG_COLOR = (30, 30, 30)         # dark background
TEXT_COLOR = (230, 230, 230)

# ---------- Helper functions ----------
def clamp(value, minv, maxv):
    return max(minv, min(value, maxv))

def rect_circle_collide(rect, circle_pos, circle_radius):
    # Find the closest point on the rect to the circle center
    closest_x = clamp(circle_pos[0], rect.left, rect.right)
    closest_y = clamp(circle_pos[1], rect.top, rect.bottom)
    dx = circle_pos[0] - closest_x
    dy = circle_pos[1] - closest_y
    return (dx*dx + dy*dy) <= (circle_radius * circle_radius)

# ---------- Game classes ----------
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(0, 0, PLAYER_SIZE, PLAYER_SIZE)
        self.rect.center = (x, y)

    def update(self, dt, keys):
        dx = 0
        dy = 0
        # Keyboard input (arrow keys + WASD)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += 1

        # normalize diagonal movement
        if dx != 0 and dy != 0:
            factor = 0.70710678  # 1/sqrt(2)
            dx *= factor
            dy *= factor

        self.rect.x += int(dx * PLAYER_SPEED * dt)
        self.rect.y += int(dy * PLAYER_SPEED * dt)

        # keep inside screen
        self.rect.left = clamp(self.rect.left, 0, SCREEN_WIDTH - self.rect.width)
        self.rect.top = clamp(self.rect.top, 0, SCREEN_HEIGHT - self.rect.height)

    def draw(self, surf):
        pygame.draw.rect(surf, PLAYER_COLOR, self.rect)

class Enemy:
    def __init__(self):
        self.x = random.randint(ENEMY_RADIUS, SCREEN_WIDTH - ENEMY_RADIUS)
        self.y = random.randint(ENEMY_RADIUS, SCREEN_HEIGHT - ENEMY_RADIUS)
        angle = random.random() * 2 * 3.14159265
        self.vx = ENEMY_SPEED * math_cos(angle)
        self.vy = ENEMY_SPEED * math_sin(angle)

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

        # bounce off walls
        if self.x <= ENEMY_RADIUS:
            self.x = ENEMY_RADIUS
            self.vx *= -1
        if self.x >= SCREEN_WIDTH - ENEMY_RADIUS:
            self.x = SCREEN_WIDTH - ENEMY_RADIUS
            self.vx *= -1
        if self.y <= ENEMY_RADIUS:
            self.y = ENEMY_RADIUS
            self.vy *= -1
        if self.y >= SCREEN_HEIGHT - ENEMY_RADIUS:
            self.y = SCREEN_HEIGHT - ENEMY_RADIUS
            self.vy *= -1

    def draw(self, surf):
        pygame.draw.circle(surf, ENEMY_COLOR, (int(self.x), int(self.y)), ENEMY_RADIUS)

class Coin:
    def __init__(self):
        self.respawn()

    def respawn(self):
        margin = 20
        self.x = random.randint(margin, SCREEN_WIDTH - margin)
        self.y = random.randint(margin, SCREEN_HEIGHT - margin)
        self.collected = False

    def draw(self, surf):
        if not self.collected:
            pygame.draw.circle(surf, COIN_COLOR, (self.x, self.y), COIN_RADIUS)

# ---------- math helpers (avoid importing math for two functions repeated many times) ----------
import math
def math_sin(a):
    return math.sin(a)
def math_cos(a):
    return math.cos(a)

# ---------- Main game function ----------
def run_game():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Avoid the Enemy - Simple Pygame Demo")
    clock = pygame.time.Clock()

    # fonts
    pygame.font.init()
    font_small = pygame.font.SysFont(None, 24)
    font_mid = pygame.font.SysFont(None, 36)
    font_big = pygame.font.SysFont(None, 72)

    # Initialize game objects
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    enemy = Enemy()
    coins = [Coin() for _ in range(NUM_COINS)]

    score = 0
    elapsed_survival = 0.0
    time_left = START_TIME
    game_over = False
    game_won = False

    # For stable coin placement not overlapping player at spawn, respawn coins if too close
    def fix_coins_initial():
        for c in coins:
            while abs(c.x - player.rect.centerx) < 60 and abs(c.y - player.rect.centery) < 60:
                c.respawn()
    fix_coins_initial()

    # Game loop
    while True:
        dt = clock.tick(FPS) / 1000.0  # delta time in seconds

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_r and (game_over or game_won):
                    # Restart game
                    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                    enemy = Enemy()
                    coins = [Coin() for _ in range(NUM_COINS)]
                    score = 0
                    elapsed_survival = 0.0
                    time_left = START_TIME
                    game_over = False
                    game_won = False
                    fix_coins_initial()

        keys = pygame.key.get_pressed()

        if not (game_over or game_won):
            # Update player and enemy
            player.update(dt, keys)
            enemy.update(dt)

            # Update timer and score by time survived
            elapsed_survival += dt
            time_left -= dt
            # Increase score by full seconds survived (we add fractional and convert for display)
            # To make score increase smoothly, we add dt to score_rate and then integer part goes to score.
            # Simpler: add dt to a survival counter and when survival reaches an integer boundary, increment score.
            # We'll add 1 score for each second survived (rounded down).
            # Keep score as integer: floor(elapsed_survival)
            score = int(elapsed_survival) + sum(1 for c in coins if c.collected)

            # Coin collection (circle-rect approximate)
            for c in coins:
                if not c.collected:
                    # distance between player center and coin
                    px, py = player.rect.center
                    dx = px - c.x
                    dy = py - c.y
                    if dx*dx + dy*dy <= (COIN_RADIUS + PLAYER_SIZE//2)**2:
                        c.collected = True

            # If all coins collected, optionally respawn them after a short while
            if all(c.collected for c in coins):
                # respawn after collecting all (simple behavior)
                for c in coins:
                    c.respawn()

            # Collision detection player vs enemy
            if rect_circle_collide(player.rect, (enemy.x, enemy.y), ENEMY_RADIUS):
                game_over = True

            # Timer-based loss
            if time_left <= 0:
                # If time is up, you lose unless you already met WIN_SCORE
                if score >= WIN_SCORE:
                    game_won = True
                else:
                    game_over = True

            # Win condition by score
            if score >= WIN_SCORE:
                game_won = True

        # ---------- Drawing ----------
        screen.fill(BG_COLOR)

        # Draw coins
        for c in coins:
            c.draw(screen)

        # Draw player and enemy
        player.draw(screen)
        enemy.draw(screen)

        # HUD: score, time left
        score_text = font_mid.render(f"Score: {score}", True, TEXT_COLOR)
        time_text = font_mid.render(f"Time: {int(max(0, time_left))}", True, TEXT_COLOR)
        screen.blit(score_text, (10, 10))
        screen.blit(time_text, (10, 10 + score_text.get_height() + 6))

        # Instructions
        instructions = [
            "Move: Arrow keys or WASD",
            "Avoid the red circle (enemy).",
            f"Collect coins (+1 each). Reach score {WIN_SCORE} to win before timer ends.",
            "R to restart after game over. ESC to quit."
        ]
        y = SCREEN_HEIGHT - 20 * len(instructions) - 10
        for line in instructions:
            txt = font_small.render(line, True, TEXT_COLOR)
            screen.blit(txt, (10, y))
            y += txt.get_height() + 4

        # Center messages for win/lose
        if game_over:
            over_text = font_big.render("GAME OVER", True, (240, 80, 80))
            info_text = font_mid.render("Press R to retry or ESC to quit", True, TEXT_COLOR)
            screen.blit(over_text, over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 30)))
            screen.blit(info_text, info_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30)))
        if game_won:
            win_text = font_big.render("YOU WIN!", True, (80, 240, 120))
            info_text = font_mid.render("Press R to play again or ESC to quit", True, TEXT_COLOR)
            screen.blit(win_text, win_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 30)))
            screen.blit(info_text, info_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30)))

        pygame.display.flip()


if __name__ == "__main__":
    run_game()