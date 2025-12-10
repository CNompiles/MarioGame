import pygame
import random

RED = (255, 0, 0) # χρωμα για το fallback

class Obstacle(pygame.sprite.Sprite):
    """
    Κλάση που αναπαριστά ένα εμπόδιο.
    """
    def __init__(self, screen_width, screen_height, image=None): 
        super().__init__()
        
        if image:
            self.image = image
            self.rect = self.image.get_rect()
            # Τυχαιο υψος
            self.rect.y = random.randint(0, screen_height - self.rect.height)
            
        else:
            # Fallback (Δημιουργια τυχαιου μεγεθους κοκκινου τετραγωνου)
            width = random.randint(20, 50)
            height = random.randint(50, 150)
            self.image = pygame.Surface([width, height])
            self.image.fill(RED)
            self.rect = self.image.get_rect()
            self.rect.y = random.randint(0, screen_height - self.rect.height)
        
        # Αρχικη θεση και ταχυτητα
        self.rect.x = screen_width 
        self.speed = 5 # κινηση προς τα αριστερα 

    def update(self):
        """Ενημερώνει τη θέση του εμποδίου."""
        self.rect.x -= self.speed
        
        # Ελεγχος αν το εμποδιο βγηκε τελειως αριστερα 
        if self.rect.right < 0:
            self.kill() # Αφαιρει το sprite απο τις ομαδες
            return True # Επιστρεφει True για αυξηση σκορ
        return False