import pygame
import random
import sys
import webbrowser

pygame.init()

WIDTH, HEIGHT = 1000, 800
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - 2 * player_size
player_speed = 5

enemy_min_size = 10
enemy_max_size = 50
enemy_size = random.randint(enemy_min_size, enemy_max_size)

friendly_min_size = 10
friendly_max_size = 30
friendly_rarity = 10
friendly_count = 5

max_red_squares = 3
max_green_squares = 2

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter Game")

clock = pygame.time.Clock()

def draw_player(x, y):
    pygame.draw.rect(screen, WHITE, [x, y, player_size, player_size])

def draw_enemy(x, y, size):
    pygame.draw.rect(screen, RED, [x, y, size, size])

def draw_friendly(x, y, size, color):
    pygame.draw.rect(screen, color, [x, y, size, size])

def draw_menu(last_score, high_score):
    font = pygame.font.Font(None, 36)
    text = font.render("Shooter Game", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 4))

    instructions = [
        "Use LEFT and RIGHT arrow keys to move",
        "Avoid red squares",
        "Collect green squares for extra points",
        "Press SPACE to start",
        "Press ` for a tutorial"
    ]

    for i, line in enumerate(instructions):
        text = font.render(line, True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + i * 30))

    if last_score is not None:
        text_last_score = font.render(f"Last Score: {last_score}", True, WHITE)
        screen.blit(text_last_score, (WIDTH // 2 - text_last_score.get_width() // 2, HEIGHT // 2 + 180))

    if high_score is not None:
        text_high_score = font.render(f"High Score: {high_score}", True, WHITE)
        screen.blit(text_high_score, (WIDTH // 2 - text_high_score.get_width() // 2, HEIGHT // 2 + 210))

def game_over(score, high_score):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return score, high_score

        screen.fill((0, 0, 0))
        draw_menu(score, high_score)
        pygame.display.flip()
        clock.tick(FPS)

def main_menu():
    while True:
        last_score = None
        high_score = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                last_score, high_score = main()
                break

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKQUOTE:

                webbrowser.open("https://your-tutorial-link.com")

        screen.fill((0, 0, 0))
        draw_menu(last_score, high_score)
        pygame.display.flip()
        clock.tick(FPS)

def main():
    player_x, player_y = WIDTH // 2 - player_size // 2, HEIGHT - 2 * player_size
    enemy_speed = 0
    enemy_x, enemy_y, enemy_size = 0, 0, 0

    friendlies = []

    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
            player_x += player_speed

        enemy_speed = random.uniform(10, 30) / 5
        enemy_y += enemy_speed

        #red squares
        if len([friendly for friendly in friendlies if friendly["color"] == RED]) < max_red_squares and random.randint(1, friendly_rarity) == 1:
            biggest_enemy_size = max((enemy_size, * [friendly["size"] for friendly in friendlies]), default=enemy_min_size)
            friendlies.append({
                "x": random.randint(0, WIDTH - biggest_enemy_size),
                "y": 0,
                "size": biggest_enemy_size,
                "speed": enemy_speed,
                "color": RED
            })

        #green squares
        if len([friendly for friendly in friendlies if friendly["color"] == GREEN]) < max_green_squares and random.randint(1, friendly_rarity) == 1:
            biggest_enemy_size = max((enemy_size, * [friendly["size"] for friendly in friendlies]), default=enemy_min_size)
            friendlies.append({
                "x": random.randint(0, WIDTH - biggest_enemy_size),
                "y": 0,
                "size": biggest_enemy_size,
                "speed": enemy_speed,
                "color": GREEN
            })

        for friendly in friendlies:
            friendly["y"] += friendly["speed"]

        friendlies = [friendly for friendly in friendlies if 0 <= friendly["y"] < HEIGHT]

        if enemy_y > HEIGHT:
            enemy_x = random.randint(0, WIDTH - player_size)
            enemy_y = 0
            enemy_size = random.randint(enemy_min_size, enemy_max_size)
            score += 1

        if (
            player_x < enemy_x + enemy_size
            and player_x + player_size > enemy_x
            and player_y < enemy_y + enemy_size
            and player_y + player_size > enemy_y
        ):
            return score, None

        for friendly in friendlies:
            if (
                player_x < friendly["x"] + friendly["size"]
                and player_x + player_size > friendly["x"]
                and player_y < friendly["y"] + friendly["size"]
                and player_y + player_size > friendly["y"]
            ):
                friendlies.remove(friendly)
                if friendly["color"] == RED:
                    return score, None
                elif friendly["color"] == GREEN:
                    score += 2

        screen.fill((0, 0, 0))
        draw_player(player_x, player_y)
        draw_enemy(enemy_x, enemy_y, enemy_size)
        for friendly in friendlies:
            draw_friendly(friendly["x"], friendly["y"], friendly["size"], friendly["color"])

        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main_menu()
