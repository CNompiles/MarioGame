import pygame
import random
import os # Για την σωστη χρηση αρχειων
from classes.player import Player
from classes.obstacle import Obstacle
from classes.background import Background 

# Ρυθμισεις Παιχνιδιου
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60 # frames per seconds 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND_COLOR = (108, 137, 255) # Χρωμα ουρανου (αν δεν φορτωθει εικονα)

# Εκκινηση Pygame
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Mario Runner")
clock = pygame.time.Clock()

# Φορτωση εικονων
PLAYER_IMG = None
OBSTACLE_IMG = None
BACKGROUND_IMG = None 

try:
    # 1. Mario Sprite
    PLAYER_IMG_ORIGINAL = pygame.image.load(os.path.join('assets', 'mario_sprite.png')).convert_alpha()
    PLAYER_IMG = pygame.transform.scale(PLAYER_IMG_ORIGINAL, (32, 32)) 
    
    # 2. Εμποδιο Sprite
    OBSTACLE_IMG_ORIGINAL = pygame.image.load(os.path.join('assets', 'obstacle_sprite.png')).convert_alpha()
    OBSTACLE_IMG = pygame.transform.scale(OBSTACLE_IMG_ORIGINAL, (40, 40))
    
    # 3. Φοντο Sprite
    BACKGROUND_IMG = pygame.image.load(os.path.join('assets', 'background_scrolling.png')).convert()

except pygame.error as e:
    print(f"Δεν ήταν δυνατή η φόρτωση εικόνας. Χρησιμοποιούνται fallback χρώματα/σχήματα.")
    print(f"Σφάλμα: {e}")
    # Τα objects Παραμενουν none

# Custom Events (Για τη δημιουργια εμποδιων)
NEW_OBSTACLE = pygame.USEREVENT + 1
# Δημιουργια εμποδιου καθε 1.5 δευτερολεπτο
pygame.time.set_timer(NEW_OBSTACLE, 1500) 


def draw_text(surf, text, size, x, y):
    """Βοηθητική συνάρτηση για τη σχεδίαση σκορ/μηνυμάτων."""
    font = pygame.font.Font(pygame.font.match_font('arial'), size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def reset_game():
    """Επαναφορά παιχνιδιού, δημιουργία αντικειμένων."""
    global score
    score = 0
    
    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    
    # Δημιουργια παικτη παιρνοντας την εικονα
    player = Player(SCREEN_WIDTH, SCREEN_HEIGHT, image=PLAYER_IMG) 
    all_sprites.add(player)
    
    # Δημιουργια Background
    bg = None
    if BACKGROUND_IMG:
        bg = Background(SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_IMG)
        
    # Επιστροφη ολων των αντικειμενων
    return all_sprites, obstacles, player, bg


# Κυριο Game Loop
all_sprites, obstacles, player, bg = reset_game() # <-- Δεχεται και το bg
running = True
game_over = False

while running:
    # --- Χειρισμος Εισοδου (Events) ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if not game_over:
            if event.type == pygame.KEYDOWN:
                # Ελεγχος βελακιων για κινιση
                if event.key == pygame.K_UP:
                    player.move_up()
                if event.key == pygame.K_DOWN:
                    player.move_down()
            
            # Δημιουργια νεου εμποδιου
            if event.type == NEW_OBSTACLE:
                new_obs = Obstacle(SCREEN_WIDTH, SCREEN_HEIGHT, image=OBSTACLE_IMG) 
                all_sprites.add(new_obs)
                obstacles.add(new_obs)
        
        # Επανεκκινηση με SPACE
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                all_sprites, obstacles, player, bg = reset_game() # <-- Επαναφορά
                game_over = False

        # Ενημερωση (Update) 
    if not game_over:
        
        # Ενημερωση κινησης φοντου
        if bg:
            bg.update()
        
        all_sprites.update() 
        
        # Ελεγχος αν καποιο εμποδιο περασε
        for obs in obstacles:
            if obs.update():
                score += 1 
        
        # Ελεγχος Συγκρουσεων 
        
        # 1. Συγκρουση Παικτη με Εμποδιο
        hits = pygame.sprite.spritecollide(player, obstacles, False) 
        if hits:
            game_over = True
        
        # 2. Σύγκρουση Παίκτη με Ορια Οθονης
        if player.rect.top < 0 or player.rect.bottom > SCREEN_HEIGHT:
            game_over = True

    # Σχεδιαση (Draw)
    
    # 1. Σχεδιαση Φοντου
    if bg:
        bg.draw(screen)
    else:
        # Fallback χρωμα φοντου (μπλε ουρανος)
        screen.fill(BACKGROUND_COLOR) 
        
    # 2. Σχεδιαση Sprites (πανω απο το φοντο)
    all_sprites.draw(screen) 

    # 3. Σχεδιαση Σκορ και Μηνυματων
    draw_text(screen, f"Score: {score}", 24, SCREEN_WIDTH // 2, 10)
    
    if game_over:
        draw_text(screen, "GAME OVER", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        draw_text(screen, "Press SPACE to Restart", 30, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 130)

    # Ενημερωση της οθονης
    pygame.display.flip()
    #ορισμος ρυθμου καρε 
    clock.tick(FPS)

# Εξοδος απο την Pygame
pygame.quit()