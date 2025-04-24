import pygame
from config import *

def marketplace(screen, user_data, current_user):
    if current_user is None:
        show_message(screen, "Please login first!")
        return
    
    items = MARKET_ITEMS + [{"name": "Back", "price": 0, "description": "Return to the main menu"}]
    selected_index = 0
    shopping = True
    
    while shopping:
        screen.fill(WHITE)
        title = FONT_REGULAR.render("Marketplace", True, BLACK)
        screen.blit(title, (320, 50))
        
        coins_text = FONT_REGULAR.render(f"Your Coins: {user_data[current_user]['coins']}", True, BLUE)
        screen.blit(coins_text, (320, 100))
        
        for i, item in enumerate(items):
            color = GREEN if i == selected_index else BLACK
            item_text = FONT_REGULAR.render(f"{item['name']} - {item['price']} coins", True, color)
            screen.blit(item_text, (150, 180 + i * 70))
            
            desc_text = FONT_SMALL.render(item['description'], True, BLACK)
            screen.blit(desc_text, (150, 210 + i * 70))
        
        instruction1 = FONT_SMALL.render("UP/DOWN to navigate", True, BLACK)
        instruction2 = FONT_SMALL.render("ENTER to buy, ESC to exit", True, BLACK)
        screen.blit(instruction1, (320, 480))
        screen.blit(instruction2, (320, 510))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = max(0, selected_index - 1)
                elif event.key == pygame.K_DOWN:
                    selected_index = min(len(items) - 1, selected_index + 1)
                elif event.key == pygame.K_RETURN:
                    if items[selected_index]['name'] == "Back":
                        shopping = False
                    else:
                        selected_item = items[selected_index]
                        if user_data[current_user]['coins'] >= selected_item['price']:
                            user_data[current_user]['coins'] -= selected_item['price']
                            if 'inventory' not in user_data[current_user]:
                                user_data[current_user]['inventory'] = []
                            user_data[current_user]['inventory'].append(selected_item['name'].lower())
                            save_user_data(user_data)
                            show_message(screen, f"Purchased {selected_item['name']}!")
                        else:
                            show_message(screen, "Not enough coins!")
                elif event.key == pygame.K_ESCAPE:
                    shopping = False
    
    return True