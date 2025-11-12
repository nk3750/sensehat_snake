import time
import random
import threading
from sense_hat import SenseHat

sense = SenseHat()
sense.set_rotation(180)
sense.clear()

WIDTH, HEIGHT = 8, 8
COLOR_BG = [0, 0, 0]
DEFAULT_COLOR = [0, 255, 0]

# Brightness and display state
brightness = 1.0
previous_brightness = brightness
display_enabled = True

# 15 vivid food colors
FOOD_COLORS = [
    [255, 0, 0], [255, 128, 0], [255, 255, 0],
    [0, 255, 0], [0, 255, 128], [0, 255, 255],
    [0, 128, 255], [0, 0, 255], [128, 0, 255],
    [255, 0, 255], [255, 0, 128], [128, 128, 0],
    [0, 128, 128], [255, 255, 255], [192, 0, 255]
]

DIRS = {
    "UP": (0, -1), "DOWN": (0, 1),
    "LEFT": (-1, 0), "RIGHT": (1, 0)
}

def scale_color(color, b):
    return [min(255, int(c * b)) for c in color]

def color_distance(c1, c2):
    return sum((a - b) ** 2 for a, b in zip(c1, c2)) ** 0.5

def place_food(snake, snake_head_color):
    options = [(x, y) for x in range(WIDTH) for y in range(HEIGHT) if (x, y) not in snake]
    if not options:
        return None, None

    food_color = random.choice(FOOD_COLORS)
    tries = 0
    while color_distance(food_color, snake_head_color) < 100 and tries < 10:
        food_color = random.choice(FOOD_COLORS)
        tries += 1

    return random.choice(options), food_color

def draw(snake, snake_colors, food, food_color):
    if not display_enabled:
        sense.clear()
        return

    grid = []
    for y in range(HEIGHT):
        for x in range(WIDTH):
            pos = (x, y)
            if pos == food:
                grid.append(scale_color(food_color, brightness))
            elif pos in snake:
                idx = snake.index(pos)
                color = snake_colors[idx] if idx < len(snake_colors) else DEFAULT_COLOR
                grid.append(scale_color(color, brightness))
            else:
                grid.append(scale_color(COLOR_BG, brightness))
    sense.set_pixels(grid)

def move_snake(snake, snake_colors, direction, food, food_color):
    dx, dy = DIRS[direction]
    head_x, head_y = snake[0]
    new_head = ((head_x + dx) % WIDTH, (head_y + dy) % HEIGHT)

    if new_head in snake:
        return False, snake, snake_colors, food, food_color

    snake.insert(0, new_head)

    if new_head == food:
        snake_colors.insert(0, food_color)
        head_color = food_color
        food, food_color = place_food(snake, head_color)
    else:
        if snake: snake.pop()
        if snake_colors: snake_colors.pop()

    if len(snake_colors) != len(snake):
        fallback = snake_colors[0] if snake_colors else DEFAULT_COLOR
        snake_colors = [fallback] * len(snake)

    return True, snake, snake_colors, food, food_color

def choose_direction(snake, food, current_direction):
    head_x, head_y = snake[0]
    fx, fy = food

    candidates = []
    if fx > head_x: candidates.append("RIGHT")
    if fx < head_x: candidates.append("LEFT")
    if fy > head_y: candidates.append("DOWN")
    if fy < head_y: candidates.append("UP")
    random.shuffle(candidates)

    for d in candidates:
        dx, dy = DIRS[d]
        nx, ny = (head_x + dx) % WIDTH, (head_y + dy) % HEIGHT
        if (nx, ny) not in snake:
            return d

    fallback = []
    for d, (dx, dy) in DIRS.items():
        nx, ny = (head_x + dx) % WIDTH, (head_y + dy) % HEIGHT
        if (nx, ny) not in snake:
            fallback.append(d)

    return random.choice(fallback) if fallback else current_direction

def joystick_listener():
    global brightness, previous_brightness, display_enabled
    while True:
        for event in sense.stick.get_events():
            if event.action != "pressed":
                continue
            if event.direction == "up":
                if display_enabled:
                    brightness = max(0.1, round(brightness - 0.1, 2))
            elif event.direction == "down":
                if display_enabled:
                    brightness = min(1.0, round(brightness + 0.1, 2))
            elif event.direction == "middle":
                if display_enabled:
                    previous_brightness = brightness
                    brightness = 0.0
                    display_enabled = False
                    sense.clear()
                else:
                    brightness = previous_brightness or 1.0
                    display_enabled = True

# Start joystick handling thread
threading.Thread(target=joystick_listener, daemon=True).start()

# === Main Game Loop ===
while True:
    snake = [(4, 4)]
    direction = "RIGHT"
    head_color = DEFAULT_COLOR
    food, food_color = place_food(snake, head_color)
    snake_colors = [DEFAULT_COLOR] * len(snake)

    sense.clear()
    draw(snake, snake_colors, food, food_color)
    time.sleep(1)

    while True:
        direction = choose_direction(snake, food, direction)
        alive, snake, snake_colors, food, food_color = move_snake(
            snake, snake_colors, direction, food, food_color
        )
        draw(snake, snake_colors, food, food_color)
        time.sleep(0.25)

        if not alive:
            if display_enabled:
                sense.show_message("GAME OVER", scroll_speed=0.05, text_colour=[255, 0, 0])
            break
