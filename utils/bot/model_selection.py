import pygame, textwrap, os
from gpt4all import GPT4All
import html2text

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
red = (255, 0, 0)

# Fonts
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Get a list of models from GPT4All
gotten_models = GPT4All.list_models()

# Check if each model exists in the 'models' folder
models = []
for m in gotten_models:
    model_filename = m["filename"]
    model_path = os.path.join("models", model_filename)
    downloaded = os.path.exists(model_path)
    models.append({
        "name": m["name"],
        "description": m["description"],
        "filename": m["filename"],
        "downloaded": downloaded
    })

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
            if event.button == 1:
                for i, model in enumerate(models):
                    model_rect = pygame.Rect(
                        model_list.left + 10,
                        model_list.top + i * 50 - scroll_offset * 50,
                        model_list.width - 20,
                        50
                    )
                    if model_rect.collidepoint(event.pos):
                        selected_model = i
                        break
                if download_button.collidepoint(event.pos):
                    if selected_model is not None and not models[selected_model]["downloaded"]:
                        model_name = models[selected_model]["name"]
                        model_filename = models[selected_model]["filename"]
                        model_path = os.path.join("models", model_filename)
                        if os.path.exists(model_path):
                            print(f"{model_name} already downloaded.")
                            models[selected_model]["downloaded"] = True
                        else:
                            print(f"Downloading {model_name}...")
                            GPT4All.retrieve_model(model_filename, model_path)
                            models[selected_model]["downloaded"] = True
            if event.button == 4:  # Scroll up
                scroll_offset = max(0, scroll_offset - 1)
            if event.button == 5:  # Scroll down
                max_scroll = max(0, len(models) - model_list.height // 50)
                scroll_offset = min(max_scroll, scroll_offset + 1)

    # Clear the screen
    screen.fill(white)

    # Draw model list
    pygame.draw.rect(screen, black, model_list, border_radius=10)
    for i, model in enumerate(models):
        model_rect = pygame.Rect(
            model_list.left + 10,
            model_list.top + i * 50 - scroll_offset * 50,
            model_list.width - 20,
            50
        )
        if selected_model is not None and selected_model == i:
            pygame.draw.rect(screen, gray, model_rect, border_radius=8)
        if model["downloaded"]:
            pygame.draw.rect(screen, green, (model_rect.left, model_rect.top, 5, model_rect.height))
        text = small_font.render(model["name"], True, white)
        screen.blit(text, (model_list.left + 10, model_list.top + i * 50 + 10 - scroll_offset * 50))

    # Draw uninstall button
    if selected_model is not None and models[selected_model]["downloaded"]:
        uninstall_button = pygame.Rect(400, 560, 200, 30)
        pygame.draw.rect(screen, red, uninstall_button, border_radius=8)
        text = small_font.render("Uninstall", True, white)
        screen.blit(text, (uninstall_button.centerx - 45, uninstall_button.centery - 10))
        if uninstall_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, white, (400, 300, 350, 150), border_radius=10)
            pygame.draw.rect(screen, gray, (400, 300, 350, 150), border_radius=10)
            confirmation_text = "Are you sure you want to uninstall?"
            confirm_text = small_font.render(confirmation_text, True, black)
            screen.blit(confirm_text, (420, 320))
            yes_button = pygame.Rect(420, 380, 80, 30)
            no_button = pygame.Rect(530, 380, 80, 30)
            pygame.draw.rect(screen, red, yes_button, border_radius=8)
            pygame.draw.rect(screen, green, no_button, border_radius=8)
            yes_text = small_font.render("Yes", True, white)
            no_text = small_font.render("No", True, white)
            screen.blit(yes_text, (yes_button.centerx - 15, yes_button.centery - 10))
            screen.blit(no_text, (no_button.centerx - 15, no_button.centery - 10))
            pygame.display.flip()
            confirm_waiting = True
            while confirm_waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        confirm_waiting = False
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if yes_button.collidepoint(event.pos):
                            models[selected_model]["downloaded"] = False
                            confirm_waiting = False
                        elif no_button.collidepoint(event.pos):
                            confirm_waiting = False

    # Draw info section
    info_section = pygame.Rect(400, 100, 350, 400)
    pygame.draw.rect(screen, gray, info_section, border_radius=10)
    if selected_model is not None:
        selected_info = models[selected_model]["description"]
        l = html2text.html2text(selected_info).replace(' * ', ' • ').split('\n')
        lines = []
        for i in l:
            lines.extend(textwrap.wrap(i, width=40))  # Wrap the text
        top = 0
        for i in range(len(lines)):
            prev = small_font.render(lines[i], True, white)
            if i != 0: top += prev.get_size()[1] + 10
            screen.blit(prev, (info_section.left + 10, info_section.top + 10 + top))

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
