import pygame
import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Ініціалізація Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Робот-помічник")

# Завантаження зображення робота
robot_image = pygame.image.load('robot.png')
robot_rect = robot_image.get_rect()
robot_rect.topleft = (50, 50)

# Ініціалізація Selenium WebDriver
driver = webdriver.Chrome()

# Функція для виконання команд браузера
def execute_browser_command(command, driver):
    if "відкрити" in command:
        website = command.replace("відкрити", "").strip()
        driver.get(f"http://{website}.com")
    elif "знайти" in command:
        search_query = command.replace("знайти", "").strip()
        search_box = driver.find_element_by_name("q")
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)
    # Додати інші команди відповідно до потреб

# Функція для розпізнавання голосових команд
def voice_command(recognizer):
    with sr.Microphone() as source:
        print("Скажіть команду:")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio, language='uk-UA')
        print(f"Ви сказали: {command}")
        return command
    except sr.UnknownValueError:
        print("Не вдалося розпізнати голос")
        return None
    except sr.RequestError:
        print("Помилка сервісу розпізнавання")
        return None

# Основний цикл програми
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Оновлення позиції робота (приклад, рухається вправо)
    robot_rect.x += 1
    if robot_rect.x > 800:
        robot_rect.x = 0

    # Очищення екрану та малювання робота
    screen.fill((255, 255, 255))
    screen.blit(robot_image, robot_rect)
    pygame.display.flip()

    # Отримання голосової команди
    cmd = voice_command(sr.Recognizer())
    if cmd:
        execute_browser_command(cmd, driver)

# Завершення програми
pygame.quit()
driver.quit()
