# Raspberry Pi Sense HAT Snake Game

An autonomous Snake game that runs on the Raspberry Pi Sense HAT LED matrix. Watch as the snake automatically navigates to find food, with colorful visuals and interactive brightness controls.

## Demo

![Snake Game Demo](Image%200168.gif)

## Features

- **Autonomous Gameplay**: The snake uses AI pathfinding to automatically chase food
- **Colorful Display**: 15 vibrant food colors that the snake absorbs
- **Joystick Controls**:
  - **Up**: Decrease brightness
  - **Down**: Increase brightness
  - **Middle**: Toggle display on/off
- **Wrapping Gameplay**: Snake wraps around the edges of the 8x8 LED matrix
- **Auto-restart**: Game automatically restarts after game over

## Requirements

- Raspberry Pi (any model with GPIO pins)
- Sense HAT board
- Python 3.x

## Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd sensehat_snake
```

### 2. Set Up Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Raspberry Pi OS
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: The `sense-hat` library requires system dependencies. On Raspberry Pi OS, you may need to install:

```bash
sudo apt-get update
sudo apt-get install sense-hat
sudo pip3 install sense-hat
```

## Usage

### Running the Game

Simply run the Python script:

```bash
python3 snake_game.py
```

The game will start automatically. The snake (green initially) will begin moving and chasing the colorful food items.

### Controls

While the game is running, use the Sense HAT joystick:

- **Push Up**: Decrease display brightness (min: 0.1)
- **Push Down**: Increase display brightness (max: 1.0)
- **Push Middle**: Turn the display on/off (preserves brightness setting)

### Stopping the Game

Press `Ctrl+C` in the terminal to exit.

## How It Works

The game features:
- An 8x8 LED grid where the snake moves automatically
- Smart pathfinding algorithm that guides the snake toward food
- Color inheritance: the snake's head takes on the color of the food it eats
- Collision detection: game ends if the snake runs into itself
- Automatic restart after game over with a "GAME OVER" message

## Customization

You can modify various parameters in `snake_game.py`:

- `WIDTH`, `HEIGHT`: Grid dimensions (default: 8x8)
- `DEFAULT_COLOR`: Initial snake color (default: green `[0, 255, 0]`)
- `FOOD_COLORS`: List of possible food colors
- `time.sleep(0.25)`: Game speed (line 163)
- `sense.set_rotation(180)`: Display rotation (line 7)

## Troubleshooting

### "No module named 'sense_hat'"

Make sure you've installed the sense-hat library:
```bash
sudo pip3 install sense-hat
```

### Display is rotated incorrectly

Adjust the rotation value on line 7:
```python
sense.set_rotation(180)  # Try 0, 90, 180, or 270
```

### Game runs too fast/slow

Modify the sleep duration on line 163:
```python
time.sleep(0.25)  # Increase for slower, decrease for faster
```

## License

This project is open source and available for personal and educational use.

## Contributing

Feel free to open issues or submit pull requests with improvements!
