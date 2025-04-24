import pygame
from config import *

def view_avatar(screen, user_data, current_user):
    if current_user is None:
        show_message(screen, "Please login first!")
        return
    
    viewing = True
    
    while viewing:
        screen.fill(WHITE)
        title = FONT_REGULAR.render(f"{current_user}'s Avatar", True, BLACK)
        screen.blit(title, (320, 50))
        
        # Draw base avatar
        pygame.draw.ellipse(screen, BLACK, AVATAR_BASE["head"])
        pygame.draw.rect(screen, BLACK, AVATAR_BASE["body"])
        pygame.draw.rect(screen, BLACK, AVATAR_BASE["arms"])
        pygame.draw.rect(screen, BLACK, AVATAR_BASE["legs"])
        
        # Draw purchased items
        if 'inventory' in user_data[current_user]:
            for item in user_data[current_user]['inventory']:
                if item.lower() in AVATAR_ITEMS:
                    item_rect = AVATAR_ITEMS[item.lower()]
                    pygame.draw.rect(screen, BLUE, item_rect)
        
        instruction = FONT_SMALL.render("Press ESC to go back", True, BLACK)
        screen.blit(instruction, (320, 500))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    viewing = False
    
    return True