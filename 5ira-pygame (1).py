import os
from pprint import pprint

import numpy as np
import pygame
from pygame.locals import K_ESCAPE, KEYDOWN, MOUSEBUTTONUP, QUIT


WHITE = (255, 255, 255)
BOARDCOLOR = (206, 148, 90)
BLACK = (0, 0, 0)
SHOW_HITBOXES = False


class Spot(pygame.sprite.Sprite):
    def __init__(self, array_indexes: list[int], location: list[int], size: list[int], color: tuple[int, int, int]) -> None:
        super(Spot, self).__init__()
        self.surf = pygame.Surface(size)
        self.surf.fill(color)

        self.location = location
        self.array_indexes = array_indexes
        self.occupied = False
        self.color = None

    def __repr__(self) -> str:
        return f"<Spot Sprite, index {self.array_indexes}, color {self.color}, occupied {self.occupied}>"


class Main:
    def __init__(self):
        pygame.init()

        SCREEN_WIDTH = 621
        SCREEN_HEIGHT = 621

        self.sprites = pygame.sprite.Group()
        self.sprite_array = [[0 for _ in range(16)] for _ in range(16)]

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        pygame.display.set_caption("5 in a Row | It's White's move!")
        pygame.display.set_allow_screensaver(True)

        if os.path.exists("./iconFile.png"):
            pygame.display.set_icon(pygame.image.load("./iconFile.png"))

        self.move = -1

        self.gameover = False

        self.required_in_a_row = 5

    def printLog(self, message, message_type="info"):
        if self.gameover:
            return

        match message_type:
            case "info":
                msg = f"[INFO]    {message}"
            case "error":
                msg = f"[ERROR]   {message}"
            case "config":
                msg = f"[CONFIG]  {message}"
            case _:
                msg = f"[ERROR]   No message recieved"

        print(msg)

    def run(self):
        clock = pygame.time.Clock()

        self.generateSpriteLocations()
        self.addSprites()

        running = True

        while running:
            clock.tick(30)

            self.screen.fill(BOARDCOLOR)

            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    self.printLog(f"Position clicked: {pos}", "info")

                    clicked_sprites = [
                        sprite
                        for sprite in self.sprites
                        if self.spriteCollided(sprite.location, pos)
                    ]

                    if clicked_sprites and not self.gameover:
                        self.printLog("Sprite detected.", "info")
                        clicked_sprite = clicked_sprites[0]

                        if not clicked_sprite.occupied:
                            self.move += 1
                            color = BLACK if self.move % 2 else WHITE

                            self.printLog(
                                f"Clicked sprite's location: {clicked_sprite.location}",
                                "info",
                            )

                            x, y = clicked_sprite.location
                            loc = (x + 1, y)

                            pygame.draw.circle(self.screen, color, loc, 15, 0)

                            clicked_sprite.occupied = True
                            clicked_sprite.color = color

                            person = "Black" if not self.move % 2 else "White"
                            pygame.display.set_caption(
                                f"5 in a Row | It's {person}'s move!"
                            )

                            if self.checkWon(clicked_sprite.array_indexes[::-1]):
                                person_won = "Black" if self.move % 2 else "White"
                                won_string = f"5 in a Row | {person_won} won!"

                                pygame.display.set_caption(won_string)

                                self.gameover = True

                    else:
                        self.printLog("No sprite detected.", "info")

                    print()

                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                elif event.type == QUIT:
                    running = False

            self.drawGrid()
            self.drawSprites()

            pygame.display.update()

        pygame.quit()

    def drawGrid(self):
        for y_pos in range(10, 611, 40):
            pygame.draw.line(self.screen, BLACK, (10, y_pos), (611, y_pos), width=2)

        for x_pos in range(10, 611, 40):
            pygame.draw.line(self.screen, BLACK, (x_pos, 10), (x_pos, 611), width=2)

    def drawSprites(self):
        for entity in self.sprites:
            if SHOW_HITBOXES:
                self.screen.blit(entity.surf, entity.location)

            if entity.occupied:
                x, y = entity.location
                loc = (x + 1, y)
                pygame.draw.circle(self.screen, entity.color, loc, 15, 0)

    def generateSpriteLocations(self):
        locations = []

        for y_index, y_pos in enumerate(range(10, 611, 40)):
            for x_index, x_pos in enumerate(range(10, 611, 40)):
                locations.append([[y_index, x_index], [y_pos, x_pos]])

        self.locations = locations

    def addSprites(self):
        row = 0
        item = 0

        for location in self.locations:
            if item > 15:
                row += 1
                item = 0
            if row > 15:
                break

            sprite = Spot(location[0], location[1], (10, 10), (255, 32, 1))
            self.sprites.add(sprite)
            self.sprite_array[row][item] = sprite

            item += 1

    def spriteCollided(self, sprite_location, clicked_location):
        sprite_y, sprite_x = sprite_location
        clicked_y, clicked_x = clicked_location

        if sprite_y - 10 < clicked_y < sprite_y + 10:
            if sprite_x - 10 < clicked_x < sprite_x + 10:
                return True

        return False

    def checkWonDiagonalLeft(self, current_color, location):
        diagonal_left = 1
        current_index_x, current_index_y = location

        while True:
            try:
                up_left_x = current_index_x - 1
                up_left_y = current_index_y - 1

                if up_left_x < 0 or up_left_y < 0:
                    break

                next_sprite = self.sprite_array[up_left_y][up_left_x]

                if not next_sprite.occupied:
                    break

                if next_sprite.color == current_color:
                    diagonal_left += 1

                    current_index_x -= 1
                    current_index_y -= 1
                else:
                    break

            except IndexError:
                break

        current_index_x, current_index_y = location

        while True:
            try:
                down_right_x = current_index_x + 1
                down_right_y = current_index_y + 1

                if down_right_x < 0 or down_right_y < 0:
                    break

                next_sprite = self.sprite_array[down_right_y][down_right_x]

                if not next_sprite.occupied:
                    break

                if next_sprite.color == current_color:
                    diagonal_left += 1

                    current_index_x -= 1
                    current_index_y -= 1
                else:
                    break

            except IndexError:
                break

        return diagonal_left

    def checkWonDiagonalRight(self, current_color, location):
        diagonal_right = 1
        current_index_x, current_index_y = location

        while True:
            try:
                up_right_x = current_index_x + 1
                up_right_y = current_index_y - 1

                if up_right_x < 0 or up_right_y < 0:
                    break

                next_sprite = self.sprite_array[up_right_y][up_right_x]

                if not next_sprite.occupied:
                    break

                if next_sprite.color == current_color:
                    diagonal_right += 1

                    current_index_x += 1
                    current_index_y -= 1
                else:
                    break

            except IndexError:
                break

        current_index_x, current_index_y = location

        while True:
            try:
                down_right_x = current_index_x - 1
                down_right_y = current_index_y + 1

                if down_right_x < 0 or down_right_y < 0:
                    break

                next_sprite = self.sprite_array[down_right_y][down_right_x]

                if not next_sprite.occupied:
                    break

                if next_sprite.color == current_color:
                    diagonal_right += 1

                    current_index_x -= 1
                    current_index_y += 1
                else:
                    break

            except IndexError:
                break

        return diagonal_right

    def checkWonUpDown(self, current_color, location):
        up_down = 1
        current_index_x, current_index_y = location

        while True:
            try:
                up_x = current_index_x + 0
                up_y = current_index_y - 1

                if up_x < 0 or up_y < 0:
                    break

                next_sprite = self.sprite_array[up_y][up_x]
                print(next_sprite)

                if not next_sprite.occupied:
                    break

                if next_sprite.color == current_color:
                    up_down += 1

                    current_index_x += 0
                    current_index_y -= 1
                else:
                    break

            except IndexError:
                break

        current_index_x, current_index_y = location

        while True:
            try:
                down_x = current_index_x + 0
                down_y = current_index_y + 1

                if down_x < 0 or down_y < 0:
                    break

                next_sprite = self.sprite_array[down_y][down_x]
                print(f"jugs, {next_sprite.color}, {current_color}")

                if not next_sprite.occupied:
                    break

                if next_sprite.color == current_color:
                    up_down += 1

                    current_index_x += 0
                    current_index_y += 1
                else:
                    break

            except IndexError:
                break

        return up_down

    def checkWonLeftRight(self, current_color, location):
        left_right = 1
        current_index_x, current_index_y = location

        while True:
            try:
                left_x = current_index_x - 1
                left_y = current_index_y - 0

                if left_x < 0 or left_y < 0:
                    break

                next_sprite = self.sprite_array[left_y][left_x]
                # print(next_sprite)
                # print(current_color, next_sprite.color)
                if not next_sprite.occupied:
                    break

                if next_sprite.color == current_color:
                    left_right += 1

                    current_index_x -= 1
                    current_index_y += 0
                else:
                    break

            except IndexError:
                break

        current_index_x, current_index_y = location

        while True:
            try:
                down_x = current_index_x + 1
                down_y = current_index_y - 0

                if down_x < 0 or down_y < 0:
                    break

                next_sprite = self.sprite_array[down_y][down_x]

                if not next_sprite.occupied:
                    break

                if next_sprite.color == current_color:
                    left_right += 1

                    current_index_x += 1
                    current_index_y -= 0
                else:
                    break

            except IndexError:
                break

        return left_right

    def checkWon(self, piece_location):
        pprint(self.sprite_array)
        print(piece_location)

        current_color = [
            i for i in self.sprites if i.array_indexes == piece_location[::-1]
        ][0].color

        diagonal_left = self.checkWonDiagonalLeft(current_color, piece_location)
        diagonal_right = self.checkWonDiagonalRight(current_color, piece_location)
        up_down = self.checkWonUpDown(current_color, piece_location)
        left_right = self.checkWonLeftRight(current_color, piece_location)

        print(f"{diagonal_left=}, {diagonal_right=}, {up_down=}, {left_right=}")
        if (
            diagonal_left >= self.required_in_a_row
            or diagonal_right >= self.required_in_a_row
        ):
            return True
        if up_down >= self.required_in_a_row or left_right >= self.required_in_a_row:
            return True

        return False


if __name__ == "__main__":
    app = Main()
    app.run()
