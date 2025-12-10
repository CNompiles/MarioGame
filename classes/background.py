import pygame

class Background:
    """
    Κλαση που διαχειριζεται το κινουμενο φοντο (scrolling background) 
    χρησιμοποιωντας δυο αντιγραφα της εικονας.
    """
    def __init__(self, screen_width, screen_height, image):
        self.image = image
        
        # Προσαρμοζουμε το υψος της εικονας στο υψος της οθονης
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * screen_height // self.image.get_height(), screen_height))
        
        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.height = screen_height
        
        # Θεσεις των δυο αντιγραφων της εικονας
        self.x1 = 0
        # Θεση του δευτερου αντιγραφου (ακριβως μετα το πρωτο)
        self.x2 = self.width
        
        # Ταχυτητα κυλισης
        self.scroll_speed = 3 

    def update(self):
        """Ενημερώνει τη θέση του φόντου."""
        self.x1 -= self.scroll_speed
        self.x2 -= self.scroll_speed

        # Επανατοποθετηση του πρωτου αντιγραφου
        if self.x1 < -self.width:
            self.x1 = self.width
        
        # Επανατοποθετηση του δευτερου αντιγρφου
        if self.x2 < -self.width:
            self.x2 = self.width

    def draw(self, screen):
        """Σχεδιάζει και τα δύο αντίγραφα του φόντου."""
        screen.blit(self.image, (self.x1, 0))
        screen.blit(self.image, (self.x2, 0))