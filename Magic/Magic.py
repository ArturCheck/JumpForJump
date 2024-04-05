import pygame
import sys
import random
import os

pygame.init()

width, height = 600, 400
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("JumpForJump")

# Функція для визначення шляху до файлу
def get_file_path(file_name, file_type):
    if getattr(sys, 'frozen', False):  # Перевіряємо, чи виконується програма з PyInstaller
        return os.path.join(sys._MEIPASS, file_name)  # Використовуємо спеціальний шлях PyInstaller
    else:
        return os.path.join(os.path.dirname(__file__), file_name)

def load_file(file_name, file_type):
    file_path = get_file_path(file_name, file_type)
    if file_type == "image":
        return pygame.image.load(file_path).convert_alpha()
    elif file_type == "sound":
        return pygame.mixer.Sound(file_path)
    else:
        raise ValueError("Invalid file type")

songs_directory = os.path.dirname(os.path.abspath(__file__))  

def select_random_song():
    mp3_files = [f for f in os.listdir(songs_directory) if f.endswith('.mp3')]

    random_song = random.choice(mp3_files)

    return os.path.join(songs_directory, random_song)

def play_random_song():
    song = select_random_song()
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(-1)

icon = load_file('emo.png', "image")
background_image = load_file("background.jpg", "image")
cloud_image = load_file('cloud.png', "image")
cloud_image = pygame.transform.scale(cloud_image, (200, 150))
tree_image = load_file('tree.png', "image")
tree_image = pygame.transform.scale(tree_image, (80, 160))
bush_image = load_file('brush.png', "image")
bush_image = pygame.transform.scale(bush_image, (80, 40))
sun_image = load_file('sun.png', "image")
sun_image = pygame.transform.scale(sun_image, (100, 100))
moon_image = load_file('moon.png', "image")
moon_image = pygame.transform.scale(moon_image, (120, 90))
player_image = load_file('emo.png', "image")
player_image = pygame.transform.scale(player_image, (50, 50))
pygame.display.set_icon(icon)

def smooth_color_transition(color):
    return (color[0] + 0.5) % 256, (color[1] + 1) % 256, (color[2] + 1.5) % 256

def smooth_text_color_transition(color):
    return (color[0] - 1) % 256, (color[1] - 1) % 256, (color[2] - 1) % 256

def fade_in_out(image, text1, text2, font, start_text, end_text):
    pygame.mixer.music.load(get_file_path("menu.mp3", "sound"))
    pygame.mixer.music.play(0)
    alpha = 0
    fade_speed = 3
    screen.fill((0, 0, 0))
    
    while alpha < 255:
        screen.fill((0, 0, 0))
        image.set_alpha(alpha)
        screen.blit(image, (0, 0))
        
        text1.set_alpha(alpha)
        text2.set_alpha(alpha)
        screen.blit(text1, (width // 2 - text1.get_width() // 2, height // 5))
        screen.blit(text2, (width // 2 - text2.get_width() // 2, height // 3))
        
        alpha += fade_speed
        pygame.display.update()
        clock.tick(50)
    
    start_button = pygame.Rect(width // 2 - 100, height // 2 + 50, 200, 50)
    color = (50, 50, 200)
    pygame.draw.rect(screen, color, start_button, border_radius=10)
    start_font = pygame.font.Font(None, 36)
    start_text_surface = start_font.render("Start Game", True, (255, 255, 255))
    screen.blit(start_text_surface, (width // 2 - start_text_surface.get_width() // 2, height // 2 + 65))
    
    pygame.display.update()

    text_color = (255, 255, 255)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if start_button.collidepoint(mouse_pos):
                    pygame.mixer.music.stop()
                    play_random_song()
                    pygame.mouse.set_visible(False)
                    return

        # Плавно змінюємо колір кнопки
        color = smooth_color_transition(color)
        # Плавно змінюємо колір тексту кнопки
        text_color = smooth_text_color_transition(text_color)
        pygame.draw.rect(screen, color, start_button, border_radius=10)
        start_text_surface = start_font.render("Start Game", True, text_color)
        screen.blit(start_text_surface, (width // 2 - start_text_surface.get_width() // 2, height // 2 + 65))
        pygame.display.update()
        clock.tick(60)

background_image = pygame.transform.scale(background_image, (width, height))
font = pygame.font.Font(None, 48)
text1_surface = font.render("Artur Games", True, (173, 216, 230))
text2_surface = font.render("Presents", True, (173, 216, 230))

fade_in_out(background_image, text1_surface, text2_surface, font, "Artur Games Presents", "Start Game")

# Основний цикл гри або функція, яка викликає головний цикл гри
def main_game():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
    pygame.quit()

player_radius = 25
player_x = 50
player_y = height - 2 * player_radius
player_speed = 5
jump_height = 7
jumping = False
jump_count = 10
game_over = False
score = 0
high_score = 0

obstacles = []
obstacle_speed = 5
min_obstacle_distance = 150
obstacle_frequency = 30

clouds = []  
cloud_speed = 2
cloud_frequency = 100

tree_images = []  
tree_speed = 3
tree_frequency = 80

bush_images = []  
bush_speed = 4
bush_frequency = 120

sun_angle = 0
sun_rotation_speed = 1

moon_angle = 0
moon_rotation_speed = 1

player_rotation_angle = 0
jump_start_angle = 0

cloud_width = 200
tree_width = 80
bush_width = 80

clock = pygame.time.Clock()

white = (255, 255, 255)
blue = (0, 128, 255)
green = (34, 177, 76)
sky_blue = (135, 206, 235)
yellow = (255, 255, 0)
gray = (169, 169, 169)
red = (255, 0, 0)
purpule = (148, 0, 211) 
black = (0, 0, 0)

day_background_color = (135, 206, 250)
night_background_color = (25, 25, 112)
sunset_color = (255, 165, 0)
sunrise_color = (148, 0, 211)

current_background_color = day_background_color
current_sunset_color = sunset_color
current_sunrise_color = sunrise_color

score_to_change_time = 100
is_night = False

# Змінні для кольорів фону та перехідного кольору
transition_duration = 1000
transition_step = 1 

current_transition = 0  # Змінна для відстеження поточного кроку переходу

def stop_song():
    pygame.mixer.music.stop()

def generate_cloud():
    cloud_x = width
    cloud_y = random.randint(10, height // 4)
    clouds.append((cloud_x, cloud_y))
    
def generate_tree():
    tree_x = width
    tree_y = height - random.randint(160, 170)
    tree_images.append((tree_x, tree_y))
    
def generate_bush():
    bush_x = width
    bush_y = height - random.randint(50, 60)
    bush_images.append((bush_x, bush_y))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not jumping and not game_over:
            jumping = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over:
            play_random_song()
            pygame.mouse.set_visible(False)
            game_over = False
            jumping = False
            jump_count = 10
            player_y = height - 2 * player_radius
            obstacles = []
            clouds = []
            bush_images = []
            tree_images = []
            score = 0

    keys = pygame.key.get_pressed()
    if not game_over:
        if not jumping:
            if keys[pygame.K_UP]:
                jumping = True
                jump_start_angle = player_rotation_angle
        else:
            if jump_count >= -10:
                neg = 1
                if jump_count < 0:
                    neg = -1
                player_y -= (jump_count ** 2) * 0.3 * neg
                jump_count -= 1
                rotated_player = pygame.transform.rotate(player_image, jump_start_angle + player_rotation_angle)
                player_rect = rotated_player.get_rect(center=(player_x, player_y))
                screen.blit(rotated_player, player_rect.topleft)
                player_rotation_angle += 10
            else:
                jumping = False
                jump_count = 10

        if random.randint(1, obstacle_frequency) == 1:
            obstacle_x = width
            obstacle_y = height - random.randint(30, 60)
            if not obstacles or obstacle_x - obstacles[-1][0] > min_obstacle_distance:
                obstacles.append((obstacle_x, obstacle_y))

        for i in range(len(obstacles)):
            obstacles[i] = (obstacles[i][0] - obstacle_speed, obstacles[i][1])

        obstacles = [obs for obs in obstacles if obs[0] > 0]

        for obs in obstacles:
            if (
                player_x - player_radius < obs[0] < player_x + player_radius
                and player_y - player_radius < obs[1] < player_y + player_radius
            ):
                game_over = True
            elif obs[0] < player_x and not game_over:
                score += 1
                if score >= score_to_change_time:
                    is_night = not is_night
                    score_to_change_time += 100
                
        # Облака
        if random.randint(1, cloud_frequency) == 1:
            generate_cloud()

        for i in range(len(clouds)):
            clouds[i] = (clouds[i][0] - cloud_speed, clouds[i][1])

        clouds = [cloud for cloud in clouds if cloud[0] + cloud_width > 0]

        for cloud in clouds:
            screen.blit(cloud_image, (int(cloud[0]), int(cloud[1])))

        # Дерева
        if random.randint(1, tree_frequency) == 1:
            generate_tree()

        for i in range(len(tree_images)):
            tree_images[i] = (tree_images[i][0] - tree_speed, tree_images[i][1])

        tree_images = [tree for tree in tree_images if tree[0] + tree_width > 0]
        for tree in tree_images:
            screen.blit(tree_image, (int(tree[0]), int(tree[1])))

        # Кущі
        if random.randint(1, bush_frequency) == 1:
            generate_bush()

        for i in range(len(bush_images)):
            bush_images[i] = (bush_images[i][0] - bush_speed, bush_images[i][1])

        bush_images = [bush for bush in bush_images if bush[0] + bush_width > 0]

        for bush in bush_images:
            screen.blit(bush_image, (int(bush[0]), int(bush[1])))

    if is_night:
        if current_transition < transition_duration:
            # Зміна колірних компонентів фону в напрямку до ночі
            current_background_color = (
                max(current_background_color[0] - transition_step, night_background_color[0]),
                max(current_background_color[1] - transition_step, night_background_color[1]),
                max(current_background_color[2] - transition_step, night_background_color[2])
            )
            # Зміна колірних компонентів закату в напрямку до ночі
            current_sunset_color = (
                max(current_sunset_color[0] - transition_step, night_background_color[0]),
                max(current_sunset_color[1] - transition_step, night_background_color[1]),
                max(current_sunset_color[2] - transition_step, night_background_color[2])
            )
            # Зміна колірних компонентів сходу в напрямку до ночі
            current_sunrise_color = (
                max(current_sunrise_color[0] - transition_step, night_background_color[0]),
                max(current_sunrise_color[1] - transition_step, night_background_color[1]),
                max(current_sunrise_color[2] - transition_step, night_background_color[2])
            )
            current_transition += 1
        else:
            current_transition = 0  # Скидання кроку переходу

        screen.fill(current_background_color)  # Ніч
        rotated_moon = pygame.transform.rotate(moon_image, moon_angle)
        moon_rect = rotated_moon.get_rect(center=(60, 60))
        screen.blit(rotated_moon, moon_rect.topleft)
        moon_angle += moon_rotation_speed
    else:
        if current_transition < transition_duration:
            # Зміна колірних компонентів фону в напрямку до дня
            current_background_color = (
                min(current_background_color[0] + transition_step, day_background_color[0]),
                min(current_background_color[1] + transition_step, day_background_color[1]),
                min(current_background_color[2] + transition_step, day_background_color[2])
            )
            # Зміна колірних компонентів закату в напрямку до закату
            current_sunset_color = (
                min(current_sunset_color[0] + transition_step, sunset_color[0]),
                min(current_sunset_color[1] + transition_step, sunset_color[1]),
                min(current_sunset_color[2] + transition_step, sunset_color[2])
            )
            # Зміна колірних компонентів сходу в напрямку до сходу
            current_sunrise_color = (
                min(current_sunrise_color[0] + transition_step, sunrise_color[0]),
                min(current_sunrise_color[1] + transition_step, sunrise_color[1]),
                min(current_sunrise_color[2] + transition_step, sunrise_color[2])
            )
            current_transition += 1
        else:
            current_transition = 0  # Скидання кроку переходу

        screen.fill(current_background_color)  # День
        rotated_sun = pygame.transform.rotate(sun_image, sun_angle)
        sun_rect = rotated_sun.get_rect(center=(60, 60))
        screen.blit(rotated_sun, sun_rect.topleft)
        sun_angle += sun_rotation_speed

    for cloud in clouds:
        screen.blit(cloud_image, (int(cloud[0]), int(cloud[1])))
        
    for tree in tree_images:
            screen.blit(tree_image, (int(tree[0]), int(tree[1])))
            
    for bush in bush_images:
        screen.blit(bush_image, (int(bush[0]), int(bush[1])))

    pygame.draw.rect(screen, green, (0, height - player_radius, width, player_radius))

    rotated_player = pygame.transform.rotate(player_image, jump_start_angle + player_rotation_angle)
    player_rect = rotated_player.get_rect(center=(player_x, player_y))
    screen.blit(rotated_player, player_rect.topleft)

    for obs in obstacles:
        pygame.draw.rect(screen, red, (obs[0], obs[1], 20, 20))

    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: {}".format(score), True, (148, 0, 211))
    screen.blit(score_text, (width - score_text.get_width() - 10, 10))

    if game_over:
        stop_song()
        pygame.mouse.set_visible(True)
        font_big = pygame.font.Font(None, 72)
        font_small = pygame.font.Font(None, 36)
        game_over_text = font_big.render("Game Over", True, (0, 0, 0))
        restart_text = font_small.render("Press R to Restart", True, (0, 255, 0))
        score_text_game_over = font_small.render("Your Score: {}".format(score), True, (173, 216, 230))
        if score > high_score:
            high_score = score
        record_text = font_small.render("Record Score: {}".format(high_score), True, (255, 165, 0))

        # Отримання прямокутників для надписів
        game_over_rect = game_over_text.get_rect(center=(width // 2, height // 4))
        restart_rect = restart_text.get_rect(center=(width // 2, height // 2 - 15))
        score_rect = score_text_game_over.get_rect(center=(width // 2, height // 2 + 20))
        record_rect = record_text.get_rect(center=(width // 2, height // 2 + 55))

        # Створення фону під надписами з заокругленими кутами
        background_surface = pygame.Surface((width // 2, height // 2 + 50), pygame.SRCALPHA)
        pygame.draw.rect(background_surface, (0, 0, 0, 100), (0, 0, width // 2, height // 2 + 50), border_radius=25)  # Заокруглені кути

        # Відображення фону
        screen.blit(background_surface, (width // 4, height // 8))

        # Відображення надписів на фоні
        screen.blit(game_over_text, game_over_rect)
        screen.blit(restart_text, restart_rect)
        screen.blit(score_text_game_over, score_rect)
        screen.blit(record_text, record_rect)

        sun_angle = 0
        sun_rotation_speed = 1
        
        moon_angle = 0
        moon_rotation_speed = 1
        score_to_change_time = 100
        
        player_rotation_angle = 0
        jump_start_angle = 0

    pygame.display.flip()

    clock.tick(60)