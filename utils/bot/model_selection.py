# AI generated file

import pygame

# Initialize Pygame
pygame.init()

# Set up display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("GPT4ALL Model Zoo")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (200, 200, 200)
green = (0, 255, 0)

# Fonts
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Define model information (expanded)
models = [
    {"name": "GPT-3.5 Small", "description": "A compact language model for various tasks.", "downloaded": False},
    {"name": "Image Captioning", "description": "Generate captions for images.", "downloaded": False},
    {"name": "ChatGPT", "description": "Engage in interactive conversations.", "downloaded": False},
    {"name": "Code Generation", "description": "Generate code snippets.", "downloaded": False},
    # Add more models here
]

# Define UI elements
model_list = pygame.Rect(50, 100, 300, 400)
scroll_bar = pygame.Rect(350, 100, 20, 400)
download_button = pygame.Rect(400, 500, 200, 50)

# Main loop
running = True
selected_model = None
scroll_offset = 0  # For scrolling the model list

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if download_button.collidepoint(event.pos):
                    if selected_model is not None and not models[selected_model]["downloaded"]:
                        model_name = models[selected_model]["name"]
                        print(f"Downloading {model_name}...")
                        models[selected_model]["downloaded"] = True  # Mark as downloaded
                        # Implement your download logic here

                elif model_list.collidepoint(event.pos):
                    clicked_model = (event.pos[1] - model_list.top + scroll_offset) // 50
                    if 0 <= clicked_model < len(models):
                        selected_model = clicked_model

    # Clear the screen
    screen.fill(white)

    # Draw model list
    pygame.draw.rect(screen, black, model_list, border_radius=10)
    for i, model in enumerate(models[scroll_offset:]):
        model_rect = pygame.Rect(model_list.left + 10, model_list.top + i * 50 - scroll_offset, model_list.width - 20, 50)
        if selected_model is not None and selected_model == i + scroll_offset:
            pygame.draw.rect(screen, gray, model_rect, border_radius=8)
        
        if model["downloaded"]:
            pygame.draw.rect(screen, green, (model_rect.left, model_rect.top, 5, model_rect.height))
            
        text = small_font.render(model["name"], True, white)  # Change font color to white
        screen.blit(text, (model_list.left + 10, model_list.top + i * 50 + 10 - scroll_offset))

    # Draw scroll bar
    pygame.draw.rect(screen, black, scroll_bar, border_radius=10)
    max_scroll = len(models) * 50 - model_list.height
    scroll_pos = (scroll_offset / max_scroll) * (model_list.height - scroll_bar.height)
    pygame.draw.rect(screen, gray, (scroll_bar.left, model_list.top + scroll_pos, scroll_bar.width, scroll_bar.height))

    # Draw download button
    pygame.draw.rect(screen, black, download_button, border_radius=10)
    text = font.render("Download", True, white)
    screen.blit(text, (download_button.centerx - 60, download_button.centery - 18))

    pygame.display.flip()

# Clean up
pygame.quit()
