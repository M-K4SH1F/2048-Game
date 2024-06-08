## Overview
  This is a Python implementation of the popular 2048 game using the Pygame library. The objective of the game is to slide numbered tiles on a grid to combine them to create a tile with the number 2048.

## Author
Mohammed Kashif Ahmed

## Features
  - Smooth sliding tile animation
  - Tile merging based on the 2048 game rules
  - Timer to keep track of the game duration
  - Colorful tile representation based on their values
  - Simple and intuitive keyboard controls

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/Parking-Payment-Management-System.git
   cd Parking-Payment-Management-System
   
2. **Install Dependencies:**
   - Ensure you have Python and Pygame installed. You can install Pygame using pip:
     ```bash
     pip install pygame

## How To Play:
**1. Run The Game:**
  - Execute the following command in your terminal:
    ```bash
    python 2048_Game.py

**2. Controls:**
  - Use the arrow keys to move the tiles:
      - **Left Arrow:** Slide tiles to the left.
      - **Right Arrow:** Slide tiles to the right.
      - **Up Arrow:** Slide tiles upwards.
      - **Down Arrow:** Slide tiles downwards.
   
**3. Objective:**
  Combine tiles with the same number to create a tile with the number 2048.

## Game Logic

**Components:**

1. Initialization:
  - **Libraries:** Import necessary libraries (pygame, random, math, time).
  - **Pygame Initialization:** Initialize Pygame and set up constants (e.g., FPS, SCREEN_WIDTH, SCREEN_HEIGHT).

2. Window Setup:
  - **Display:** Create the game window and set the caption.
  - **Grid and Colors:** Define colors and fonts.

3.GameTile Class:
  - **Attributes:** Initialize tile value, position, and color.
  - Methods:
     - **get_color():** Get the color based on the tile value.
     - **draw():** Draw the tile on the window.
     - **set_pos():** Set the tile's position.
     - **move():** Move the tile based on a delta value.

4. Utility Functions:
  - **draw_grid(window):** Draw the grid lines on the window.
  - **draw_game(window, tiles, elapsed_time):** Draw the entire game including tiles and timer.
  - **get_random_position(tiles):** Generate a random position for a new tile.
  - **move_game_tiles(window, tiles, clock, direction):** Handle tile movement and merging based on direction.
  - **end_move(tiles):** End the move and add a new tile if the board is not full.
  - **update_game_tiles(window, tiles, sorted_tiles):** Update the tiles' positions and redraw the game.
  - **generate_initial_tiles():** Generate the initial tiles at the start of the game.

5. Main Function:   
  - **Game Loop:**
     - Handle events (e.g., quit, keypresses).
     - Move tiles based on keypresses.
     - Update and draw the game window.
  - **Quit:** Quit the game when the loop ends.

## Logic Flow Diagram:

![image](https://github.com/M-K4SH1F/2048-Game/assets/159590221/0e4dd38e-b3e2-4aaf-ae8b-2664452585c1)

## Contributing
I want you to know that contributions to enhance this game are always welcome. Please follow these steps:

   1. Fork the repository.
   2. Create a new branch for your feature or bug fix.
   3. Commit your changes and push the branch to your fork.
   3. Create a pull request with a detailed description of your changes.

