import pygame
import random
import math
import time

pygame.init()

FPS = 60

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
GRID_ROWS = 4
GRID_COLS = 4

TILE_HEIGHT = SCREEN_HEIGHT // GRID_ROWS
TILE_WIDTH = SCREEN_WIDTH // GRID_COLS

GRID_OUTLINE_COLOR = (150, 150, 150)  # Changed color
GRID_OUTLINE_THICKNESS = 10
SCREEN_BACKGROUND_COLOR = (170, 170, 170)  # Changed color
TILE_FONT_COLOR = (100, 100, 100)  # Changed color

TILE_FONT = pygame.font.SysFont("comicsans", 60, bold=True)
TIMER_FONT = pygame.font.SysFont("comicsans", 40, bold=True)
TILE_MOVE_VEL = 20

GAME_WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2048 by Mohammed Kashif Ahmed")  # Added author's name


class GameTile:
    TILE_COLORS = [
        (239, 222, 205),  # 2
        (240, 215, 186),  # 4
        (245, 160, 122),  # 8
        (246, 135, 101),  # 16
        (247, 110, 95),   # 32
        (248, 85, 59),    # 64
        (237, 195, 110),  # 128
        (237, 191, 94),   # 256
        (236, 189, 75),   # 512
        (235, 170, 60),   # 1024
        (234, 150, 40)    # 2048
    ]

    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col
        self.x = col * TILE_WIDTH
        self.y = row * TILE_HEIGHT

    def get_color(self):
        color_index = int(math.log2(self.value)) - 1
        color = self.TILE_COLORS[color_index]
        return color

    def draw(self, window):
        color = self.get_color()
        pygame.draw.rect(window, color, (self.x, self.y, TILE_WIDTH, TILE_HEIGHT))

        text = TILE_FONT.render(str(self.value), 1, TILE_FONT_COLOR)
        window.blit(
            text,
            (
                self.x + (TILE_WIDTH / 2 - text.get_width() / 2),
                self.y + (TILE_HEIGHT / 2 - text.get_height() / 2),
            ),
        )

    def set_pos(self, ceil=False):
        if ceil:
            self.row = math.ceil(self.y / TILE_HEIGHT)
            self.col = math.ceil(self.x / TILE_WIDTH)
        else:
            self.row = math.floor(self.y / TILE_HEIGHT)
            self.col = math.floor(self.x / TILE_WIDTH)

    def move(self, delta):
        self.x += delta[0]
        self.y += delta[1]


def draw_grid(window):
    for row in range(1, GRID_ROWS):
        y = row * TILE_HEIGHT
        pygame.draw.line(window, GRID_OUTLINE_COLOR, (0, y), (SCREEN_WIDTH, y), GRID_OUTLINE_THICKNESS)

    for col in range(1, GRID_COLS):
        x = col * TILE_WIDTH
        pygame.draw.line(window, GRID_OUTLINE_COLOR, (x, 0), (x, SCREEN_HEIGHT), GRID_OUTLINE_THICKNESS)

    pygame.draw.rect(window, GRID_OUTLINE_COLOR, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), GRID_OUTLINE_THICKNESS)


def draw_game(window, tiles, elapsed_time):
    window.fill(SCREEN_BACKGROUND_COLOR)

    for tile in tiles.values():
        tile.draw(window)

    draw_grid(window)

    timer_text = TIMER_FONT.render(f"Time: {elapsed_time:.1f} sec", 1, TILE_FONT_COLOR)
    window.blit(timer_text, (SCREEN_WIDTH // 2 - timer_text.get_width() // 2, 20))

    pygame.display.update()


def get_random_position(tiles):
    row = None
    col = None
    while True:
        row = random.randrange(0, GRID_ROWS)
        col = random.randrange(0, GRID_COLS)

        if f"{row}{col}" not in tiles:
            break

    return row, col


def move_game_tiles(window, tiles, clock, direction):
    updated = True
    merged_tiles = set()

    if direction == "left":
        sort_func = lambda x: x.col
        reverse = False
        delta = (-TILE_MOVE_VEL, 0)
        boundary_check = lambda tile: tile.col == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col - 1}")
        merge_check = lambda tile, next_tile: tile.x > next_tile.x + TILE_MOVE_VEL
        move_check = (
            lambda tile, next_tile: tile.x > next_tile.x + TILE_WIDTH + TILE_MOVE_VEL
        )
        ceil = True
    elif direction == "right":
        sort_func = lambda x: x.col
        reverse = True
        delta = (TILE_MOVE_VEL, 0)
        boundary_check = lambda tile: tile.col == GRID_COLS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col + 1}")
        merge_check = lambda tile, next_tile: tile.x < next_tile.x - TILE_MOVE_VEL
        move_check = (
            lambda tile, next_tile: tile.x + TILE_WIDTH + TILE_MOVE_VEL < next_tile.x
        )
        ceil = False
    elif direction == "up":
        sort_func = lambda x: x.row
        reverse = False
        delta = (0, -TILE_MOVE_VEL)
        boundary_check = lambda tile: tile.row == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row - 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y > next_tile.y + TILE_MOVE_VEL
        move_check = (
            lambda tile, next_tile: tile.y > next_tile.y + TILE_HEIGHT + TILE_MOVE_VEL
        )
        ceil = True
    elif direction == "down":
        sort_func = lambda x: x.row
        reverse = True
        delta = (0, TILE_MOVE_VEL)
        boundary_check = lambda tile: tile.row == GRID_ROWS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row + 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y < next_tile.y - TILE_MOVE_VEL
        move_check = (
            lambda tile, next_tile: tile.y + TILE_HEIGHT + TILE_MOVE_VEL < next_tile.y
        )
        ceil = False

    while updated:
        clock.tick(FPS)
        updated = False
        sorted_tiles = sorted(tiles.values(), key=sort_func, reverse=reverse)

        for i, tile in enumerate(sorted_tiles):
            if boundary_check(tile):
                continue

            next_tile = get_next_tile(tile)
            if not next_tile:
                tile.move(delta)
            elif (
                tile.value == next_tile.value
                and tile not in merged_tiles
                and next_tile not in merged_tiles
            ):
                if merge_check(tile, next_tile):
                    tile.move(delta)
                else:
                    next_tile.value *= 2
                    sorted_tiles.pop(i)
                    merged_tiles.add(next_tile)
            elif move_check(tile, next_tile):
                tile.move(delta)
            else:
                continue

            tile.set_pos(ceil)
            updated = True

        update_game_tiles(window, tiles, sorted_tiles)

    return end_move(tiles)


def end_move(tiles):
    if len(tiles) == 16:
        return "lost"

    row, col = get_random_position(tiles)
    tiles[f"{row}{col}"] = GameTile(random.choice([2, 4]), row, col)
    return "continue"


def update_game_tiles(window, tiles, sorted_tiles):
    tiles.clear()
    for tile in sorted_tiles:
        tiles[f"{tile.row}{tile.col}"] = tile

    draw_game(window, tiles, 0)  # Initial draw to reset the screen


def generate_initial_tiles():
    tiles = {}
    for _ in range(2):
        row, col = get_random_position(tiles)
        tiles[f"{row}{col}"] = GameTile(2, row, col)

    return tiles


def main(window):
    clock = pygame.time.Clock()
    run = True

    tiles = generate_initial_tiles()
    start_time = time.time()

    while run:
        clock.tick(FPS)
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_game_tiles(window, tiles, clock, "left")
                if event.key == pygame.K_RIGHT:
                    move_game_tiles(window, tiles, clock, "right")
                if event.key == pygame.K_UP:
                    move_game_tiles(window, tiles, clock, "up")
                if event.key == pygame.K_DOWN:
                    move_game_tiles(window, tiles, clock, "down")

        draw_game(window, tiles, elapsed_time)

    pygame.quit()


if __name__ == "__main__":
    main(GAME_WINDOW)
