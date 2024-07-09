import pygame as pg

pg.init()

# ディスプレイの設定
SCREEN_WIDTH = pg.display.Info().current_w
SCREEN_HEIGHT = pg.display.Info().current_h
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.FULLSCREEN)
pg.display.set_caption("しゅぅてぃんぐげぇむ")

# 色の定義
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

class Player:
    """
    Playerの操作するキャラのクラス
    """
    def __init__(self):
        self.width = 50
        self.height = 50
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT // 2 - self.height // 2
        self.speed = 5

    def move(self, dx:int, dy:int):
        """
        自機を速度ベクトルself.x,self.yに基づき移動させる
        """
        self.x += dx * self.speed
        self.y += dy * self.speed

    def draw(self, screen: pg.Surface):
        """
        引数 screen：画面surface
        """
        pg.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))

def main():
    player = Player()
    clock = pg.time.Clock()

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False

        keys = pg.key.get_pressed()
        player.move(keys[pg.K_RIGHT] - keys[pg.K_LEFT], keys[pg.K_DOWN] - keys[pg.K_UP])

        screen.fill((0, 0, 0))
        player.draw(screen)
        pg.display.flip()
        clock.tick(60)

    pg.quit()
    

if __name__ == "__main__":
    main()

#敵の追加とゲームエリアの設定
#弾の追加と衝突判定
#HPとSPの追加、敵の動きの改善
#敵の弾の改善、ゲームオーバー条件の追加
