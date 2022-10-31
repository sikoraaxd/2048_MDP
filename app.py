import pygame as pg
import config

class Tile(pg.sprite.Sprite):
    def __init__(self, width, height, center_x, center_y, number):
        pg.sprite.Sprite.__init__(self)
        self.number = number
        self.width = width
        self.bg = pg.Rect(0, 0, width-10, height-10)
        self.bg.center = (center_x, center_y)
        self.GAME_FONT = pg.font.Font(config.FONT, 24)

    def draw(self, screen):
        pg.draw.rect(screen, (242, 237, 173), self.bg) if self.number != 0 else pg.draw.rect(
            screen, (223, 222, 210), self.bg)
        if self.number < 64:
            text_surface = self.GAME_FONT.render(
                f"{self.number}", True, (249, 178, 108))
        elif self.number < 128:
            text_surface = self.GAME_FONT.render(
                f"{self.number}", True, (237, 137, 31))
        else:
            text_surface = self.GAME_FONT.render(
                f"{self.number}", True, (255, 0, 0))
        if self.number != 0:
            screen.blit(
                text_surface,
                (
                    self.bg.centerx-text_surface.get_width()/2,
                    self.bg.centery-text_surface.get_height()/2
                )
            )

class App2048(pg.sprite.Sprite):
    def __init__(self, tiles_count=4):
        pg.sprite.Sprite.__init__(self)
        self.start_x = 10
        self.start_y = 10
        self.tiles_count = tiles_count
        self.width = config.HEIGHT-20
        self.height = config.HEIGHT-20
        self.tileWidth = self.width/self.tiles_count
        self.tiles = []
        self.bg = pg.Rect(self.start_x, self.start_y, self.width, self.height)

        self.game_over = False
        self.max = 2

    def init(self):
        self.tiles = []
        for x in range(self.tiles_count):
            row = []
            for y in range(self.tiles_count):
                row.append(
                    Tile(
                        width=self.tileWidth,
                        height=self.tileWidth,
                        center_x=(self.start_x + self.tileWidth/2) +
                        self.tileWidth*x,
                        center_y=(self.start_y+self.tileWidth/2) +
                        self.tileWidth*y,
                        number=0)
                )
            self.tiles.append(row)
        self.game_over = False

    def draw(self, screen):
        pg.draw.rect(screen, (171, 180, 172), self.bg)
        for row in self.tiles:
            for tile in row:
                tile.draw(screen)

    def update(self, game_state):
        for row in range(self.tiles_count):
            for col in range(self.tiles_count):
                self.tiles[row][col].number = game_state[row][col]

class App:
    def __init__(self, environment):
        pg.init()
        pg.font.init()
        self.font = pg.font.Font(config.FONT, 16)
        self.screen = pg.display.set_mode((config.WIDTH, config.HEIGHT))
        pg.display.set_caption("2048")

        self.clock = pg.time.Clock()
        self.run = True

        self.game = App2048(environment.rows)
        self.game.init()

    def update(self, environment):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.run = False

        self.game.update(environment.game)

    def draw(self, value, action):
        self.clock.tick(config.FPS)
        self.screen.fill((255, 255, 255))
        value_surface = self.font.render(
                f"Ценность состояния: {value}", True, (0, 0, 0))
        action_surface = self.font.render(
                "Действие: " + action, True, (0, 0, 0))
        
        self.screen.blit(
            value_surface,
            (
                self.game.width + 20,
                60
            )
        )
        self.screen.blit(
            action_surface,
            (
                self.game.width + 20,
                80
            )
        )
        self.game.draw(self.screen)
        pg.display.flip()