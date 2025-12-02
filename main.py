import pygame
import random
import os

pygame.init()
width = 1200
height = 600
fps = 60
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

# FIX 1: Update highscore path to be inside the assets folder
highscore_file = os.path.join("assets", "highscore.txt")

# Ensure the file exists (using the new path)
if not os.path.exists(highscore_file):
    # Ensure assets directory exists before writing
    if not os.path.exists("assets"):
        os.makedirs("assets")
    with open(highscore_file, "w") as f:
        f.write("0")

def draw_text(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, (x, y))

def main():
    global gameWindow
    gameWindow = pygame.display.set_mode((width, height))
    pygame.display.set_caption("SpaceShip - Shoot the upcoming ones! ~ Ashutosh Tanguria")
    
    # FIX 2: Use os.path.join and remove the dot from ".assets"
    try:
        frimg = pygame.image.load(os.path.join("assets", "front.png"))
        frimg = pygame.transform.scale(frimg, (width, height))
    except:
        frimg = pygame.Surface((width, height))
        frimg.fill((10, 10, 50))
        draw_text("Press SPACE to Start", WHITE, width // 2 - 150, height // 2)
    
    try:
        pygame.mixer.music.load(os.path.join("assets", "start.mp3"))
        pygame.mixer.music.play()
    except:
        pass
        
    waiting = True
    while waiting:
        gameWindow.blit(frimg, (0, 0))
        draw_text("Press SPACE to Start", WHITE, width // 2 - 150, height // 2)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_setup()

def game_setup():
    global exit_game, highscore
    locate_x, locate_y = (width / 2) - 70, height - 90
    alien_images = []
    alien_positions = []
    alien_bullets = []
    player_bullets = []
    score = 0
    gap = -70
    exit_game = False
    
    # FIX 3: background.jpeg path
    try:
        brimg = pygame.image.load(os.path.join("assets", "background.jpeg"))
        brimg = pygame.transform.scale(brimg, (width, height))
    except:
        brimg = pygame.Surface((width, height))
        brimg.fill((0, 0, 0))
    
    # FIX 4: rocket.png path
    try:
        r = pygame.image.load(os.path.join("assets", "rocket.png"))
        r = pygame.transform.scale(r, (80, 80)).convert_alpha()
    except:
        r = pygame.Surface((80, 80))
        r.fill((255, 255, 255))
        
    with open(highscore_file, "r") as f:
        highscore = int(f.read())

    def game(score, c=1):
        global exit_game
        alien_images.clear()
        alien_positions.clear()
        nonlocal locate_x, locate_y, gap
        gap = -70
        for i in range(10):
            # FIX 5: alien.png path
            try:
                alien = pygame.image.load(os.path.join("assets", "alien.png"))
                alien = pygame.transform.scale(alien, (80, 80)).convert_alpha()
                alien = pygame.transform.rotate(alien, 180)
            except:
                alien = pygame.Surface((80, 80))
                alien.fill((100, 255, 100))
            alien_images.append(alien)
            alien_x = 80 + gap
            alien_positions.append([alien_x, 90])
            gap += 123
        
        # FIX 6: music.mp3 was missing the path prefix entirely in original code
        try:
            pygame.mixer.music.load(os.path.join("assets", "music.mp3"))
            pygame.mixer.music.play(loops=-1)
        except:
            pass
            
        while not exit_game:
            gameWindow.blit(brimg, (0, 0))
            gameWindow.blit(r, (locate_x, locate_y))
            for i in range(len(alien_images)):
                x, y = alien_positions[i]
                gameWindow.blit(alien_images[i], (x, y))
            if random.randint(1, 30) == 1:
                if len(alien_positions) > 0:
                    idx = random.randint(0, len(alien_positions) - 1)
                    shooting_alien = alien_positions[idx]
                    bullet_rect = pygame.Rect(shooting_alien[0] + 40, shooting_alien[1] + 80, 5, 10)
                    alien_bullets.append(bullet_rect)
            for bullet in alien_bullets[:]:
                bullet.y += (7 * c)
                pygame.draw.circle(gameWindow, RED, (bullet.x, bullet.y), 7)
                rocket_rect = pygame.Rect(locate_x, locate_y, 80, 80)
                if rocket_rect.collidepoint(bullet.x, bullet.y):
                    game_over(score, highscore)
                    return
                if bullet.y > height:
                    alien_bullets.remove(bullet)
            for bullet in player_bullets[:]:
                bullet.y -= 10
                pygame.draw.circle(gameWindow, GREEN, (bullet.x, bullet.y), 7)
                i = 0
                while i < len(alien_positions):
                    pos = alien_positions[i]
                    alien_rect = pygame.Rect(pos[0], pos[1], 80, 80)
                    if alien_rect.collidepoint(bullet.x, bullet.y):
                        alien_positions.pop(i)
                        alien_images.pop(i)
                        if bullet in player_bullets:
                            player_bullets.remove(bullet)
                        score += 10
                        break
                    else:
                        i += 1
                if bullet.y < 0 and bullet in player_bullets:
                    player_bullets.remove(bullet)
            if len(alien_images) == 0:
                game(score, c * 1.25)
                return
            draw_text(f"Score: {score}", WHITE, 20, 20)
            draw_text(f"Highscore: {highscore}", WHITE, 20, 50)
            keys = pygame.key.get_pressed()
            if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and locate_x < width - 100:
                locate_x += 8
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and locate_x > 10:
                locate_x -= 8
            if keys[pygame.K_SPACE]:
                if len(player_bullets) < 2:
                    bullet = pygame.Rect(locate_x + 40, locate_y, 5, 10)
                    player_bullets.append(bullet)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
            pygame.display.update()
            clock.tick(fps)

    game(score)
    pygame.display.update()
    clock.tick(fps)

def game_over(score, highscore):
    global exit_game
    if score > highscore:
        with open(highscore_file, "w") as f:
            f.write(str(score))
    while True:
        gameWindow.fill((0, 0, 0))
        draw_text("GAME OVER", YELLOW, width // 2 - 130, height // 2 - 50)
        draw_text(f"Your Score: {score}", WHITE, width // 2 - 130, height // 2)
        draw_text(f"High Score: {max(score, highscore)}", WHITE, width // 2 - 130, height // 2 + 40)
        draw_text("Press R to Restart or E to Exit", WHITE, width // 2 - 220, height // 2 + 80)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_setup()
                    return
                if event.key == pygame.K_e:
                    pygame.quit()
                    quit()

if __name__ == "__main__":
    main()

pygame.quit()
quit()