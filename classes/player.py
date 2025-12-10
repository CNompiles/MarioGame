import pygame

GREEN = (0, 255, 0)

class Player(pygame.sprite.Sprite):
    """
    Κλαση που αναπαριστα τη φιγουρα του παικτη.
    """
    def __init__(self, screen_width, screen_height, image=None):
        super().__init__()
        
        # Ελεγχος αν περαστικε εικονα
        if image:
            self.image = image
            self.rect = self.image.get_rect() # Το ορθογωνιο παιζετε στο μεγεθος της εικονας 
        else:
            # Fallback: Πρασινο τετραγωνο
            self.image = pygame.Surface([32, 32])
            self.image.fill(GREEN)
            self.rect = self.image.get_rect()
        
        # Ορισμος αρχικης θεσης
        self.rect.x = screen_width // 10
        self.rect.y = screen_height // 2
        
        # Μταβλητες κινησης
        self.velocity = 0 # ταχυτητα καθετης μετατοπισης
        self.move_speed = 10 # ταχυτητα κινισης οταν πατηθει το βελακι

    def update(self):
        """Ενημερώνει τη θέση του παίκτη."""
        self.rect.y += self.velocity
        self.velocity = 0 # μηδενιζεται η ταχυτητα για να σταματησει η κινιση

    def move_up(self):
        """Θέτει την ταχύτητα για κίνηση προς τα πάνω."""
        self.velocity = -self.move_speed # Αρνητικο σημαινει πανω στην Pygame

    def move_down(self):
        """Θέτει την ταχύτητα για κίνηση προς τα κάτω."""
        self.velocity = self.move_speed # Θετικο σημαινει κατω