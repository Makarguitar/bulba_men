import arcade
import arcade as bora
import random as ra

import animate
import animate as anime

SCREEN_TITLE = "BRUH"
CELL_WIDTH = 60
CELL_HEIGHT = 60
ROW_COUNT = 11
COLOUMN_COUNT = 11
SCREEN_WIDTH = CELL_WIDTH * COLOUMN_COUNT
SCREEN_HEIGHT = CELL_HEIGHT * ROW_COUNT


def justify_x(position_x):
    for x in range(COLOUMN_COUNT):
        cell_center_x = x * CELL_WIDTH - CELL_WIDTH / 2
        if position_x - cell_center_x <= CELL_WIDTH / 2:
            return cell_center_x

def justify_y(position_y):
    for y in range(ROW_COUNT):
        cell_center_y = y * CELL_HEIGHT - CELL_HEIGHT / 2
        if position_y - cell_center_y <= CELL_HEIGHT / 2:
            return cell_center_y


class BreakableBlock(bora.Sprite):
    def __init__(self):
        super().__init__("res/Blocks/ExplodableBlock.png", 1)


class SolidBlock(bora.Sprite):
    def __init__(self):
        super().__init__("res/Blocks/SolidBlock.png", 1)


class Bombastic(animate.Animate):
    def __init__(self):
        super().__init__("res/Bomb/Bomb_f00.png", 0.7)
        for i in range(3):
            self.append_texture(arcade.load_texture(f"res/Bomb/Bomb_f0{i}.png"))


class BulbaMan(anime.Animate):
    def __init__(self):
        self.speed = 3
        super().__init__("res/Bomberman/Front/Bman_F_f00.png", 0.5)
        # front
        self.walk_down_frames = []
        # back
        self.walk_up_frames = []
        # right
        self.walk_right_frames = []
        # left
        self.walk_left_frames = []
        for i in range(8):
            self.walk_down_frames.append(bora.load_texture(f"res/Bomberman/Front/Bman_F_f0{i}.png"))
            self.walk_up_frames.append(bora.load_texture(f"res/Bomberman/Back/Bman_B_f0{i}.png"))
            self.walk_right_frames.append(bora.load_texture(f"res/Bomberman/Side/Bman_S_f0{i}.png"))
            self.walk_left_frames.append(
                bora.load_texture(f"res/Bomberman/Side/Bman_S_f0{i}.png", flipped_horizontally=True))
        self.direction = 4
        self.motion = False
        self.bomb_count = 10

    def costum_change(self):
        if self.direction == 1:
            self.textures = self.walk_left_frames
        elif self.direction == 2:
            self.textures = self.walk_right_frames
        elif self.direction == 3:
            self.textures = self.walk_up_frames
        elif self.direction == 4:
            self.textures = self.walk_down_frames

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.right > SCREEN_WIDTH:
            self.right = SCREEN_WIDTH
        if self.left < 0:
            self.left = 0
        if self.top > SCREEN_HEIGHT:
            self.top = SCREEN_HEIGHT
        if self.bottom < 0:
            self.bottom = 0

        self.collisions(game.solid_blocks)
        self.collisions(game.breakable_blocks)

    def collisions(self, sprite_list):

        blockhit = bora.check_for_collision_with_list(self, sprite_list)

        for block in blockhit:
            if self.left < block.right and self.direction == 1:
                self.left = block.right
            if self.right > block.left and self.direction == 2:
                self.right = block.left
            if self.top > block.bottom and self.direction == 3:
                self.top = block.bottom
            if self.bottom < block.top and self.direction == 4:
                self.bottom = block.top

    def to_up(self):
        if self.motion == False:
            self.motion = True
            self.direction = 3
            self.change_y = self.speed

    def to_left(self):
        if self.motion == False:
            self.motion = True
            self.direction = 1
            self.change_x = -self.speed

    def to_right(self):
        if self.motion == False:
            self.motion = True
            self.direction = 2
            self.change_x = self.speed

    def to_down(self):
        if self.motion == False:
            self.motion = True
            self.direction = 4
            self.change_y = -self.speed

    def stop(self):
        self.change_x = 0
        self.change_y = 0
        self.motion = False


class Game(bora.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.bg_item = bora.load_texture("res/Blocks/BackgroundTile.png")
        self.solid_blocks = bora.SpriteList()
        self.breakable_blocks = bora.SpriteList()
        self.bulba_man = BulbaMan()
        self.bulba_man_2 = BulbaMan()
        self.bombs_player_1 = bora.SpriteList()
        self.explosions = bora.SpriteList()


    def draw_bg(self):
        for y in range(ROW_COUNT):
            for x in range(COLOUMN_COUNT):
                bora.draw_texture_rectangle(x * CELL_WIDTH + CELL_WIDTH / 2, y * CELL_HEIGHT + CELL_HEIGHT / 2,
                                            CELL_WIDTH, CELL_HEIGHT, self.bg_item)

    def setup(self):
        for y in range(ROW_COUNT):
            for x in range(COLOUMN_COUNT):
                if x % 2 == 1 and y % 2 == 1:
                    solid_block = SolidBlock()
                    solid_block.center_x = x * CELL_WIDTH + CELL_WIDTH / 2
                    solid_block.center_y = y * CELL_HEIGHT + CELL_HEIGHT / 2
                    self.solid_blocks.append(solid_block)
                elif ra.randint(0, 2) == 1:
                    if (not (x == 0 and y <= 2)
                            and not (y == 0 and x <= 2)
                            and not (x == ROW_COUNT - 1 and y >= COLOUMN_COUNT - 3)
                            and not (y == COLOUMN_COUNT - 1 and x >= ROW_COUNT - 3)):
                        breakable_block = BreakableBlock()
                        breakable_block.center_x = x * CELL_WIDTH + CELL_WIDTH / 2
                        breakable_block.center_y = y * CELL_HEIGHT + CELL_HEIGHT / 2
                        self.breakable_blocks.append(breakable_block)
        x = SCREEN_WIDTH / COLOUMN_COUNT - CELL_WIDTH / 2
        y = SCREEN_HEIGHT / ROW_COUNT - CELL_HEIGHT / 2
        x2 = SCREEN_WIDTH - CELL_WIDTH / 2
        y2 = SCREEN_HEIGHT - CELL_HEIGHT / 2
        self.bulba_man.set_position(x, y)
        self.bulba_man_2.set_position(x2, y2)
        self.bulba_man_2.color = (255, 0, 0)

    def update(self, delta_time: float):
        self.bulba_man.update()
        self.bulba_man.update_animation(delta_time)
        self.bulba_man_2.update()
        self.bulba_man_2.update_animation(delta_time)
        self.bombs_player_1.update()
        self.bombs_player_1.update_animation()
        self.explosions.update()
        self.explosions.update_animation()

    def on_draw(self):
        self.clear((255, 255, 255))
        self.draw_bg()
        self.solid_blocks.draw()
        self.breakable_blocks.draw()
        self.bulba_man.draw()
        self.bulba_man_2.draw()
        self.bombs_player_1.draw()
        self.explosions.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == bora.key.A:
            self.bulba_man.to_left()
        elif symbol == bora.key.D:
            self.bulba_man.to_right()
        elif symbol == bora.key.W:
            self.bulba_man.to_up()
        elif symbol == bora.key.S:
            self.bulba_man.to_down()
        self.bulba_man.costum_change()

        if symbol == bora.key.LEFT:
            self.bulba_man_2.to_left()
        elif symbol == bora.key.RIGHT:
            self.bulba_man_2.to_right()
        elif symbol == bora.key.UP:
            self.bulba_man_2.to_up()
        elif symbol == bora.key.DOWN:
            self.bulba_man_2.to_down()
        self.bulba_man_2.costum_change()

        if symbol == bora.key.SPACE:
            if len(self.bombs_player_1) < self.bulba_man.bomb_count:
                bomb = Bombastic()
                bomb.set_position(justify_x(self.bulba_man.center_x), justify_y(self.bulba_man.center_y))
                self.bombs_player_1.append(bomb)

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == bora.key.A or symbol == bora.key.D or symbol == bora.key.W or symbol == bora.key.S:
            self.bulba_man.stop()
        if symbol == bora.key.LEFT or symbol == bora.key.RIGHT or symbol == bora.key.UP or symbol == bora.key.DOWN:
            self.bulba_man_2.stop()


game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
game.setup()

bora.run()
