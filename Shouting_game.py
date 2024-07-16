import pygame as pg
import random
import math

pg.init()

# ディスプレイの設定
SCREEN_WIDTH = pg.display.Info().current_w
SCREEN_HEIGHT = pg.display.Info().current_h
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.FULLSCREEN)
pg.display.set_caption("しゅぅてぃんぐげぇむ")

# 色の定義
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# ゲームエリア
GAME_AREA_SIZE = min(SCREEN_WIDTH, SCREEN_HEIGHT) * 0.6
GAME_AREA_X = (SCREEN_WIDTH - GAME_AREA_SIZE) / 2
GAME_AREA_Y = (SCREEN_HEIGHT - GAME_AREA_SIZE) / 2


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
        self.hp = 100 # プレイヤーHPの追加（初期化）
        self.sp = 0 # プレイヤーSP(スキルポイント)の追加（初期化）

    def move(self, dx:int, dy:int):
        """
        自機を速度ベクトルself.x,self.yに基づき,
        new_x,new_yとして移動させる
        プレイヤーの行動範囲を制御する
        """
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        if (GAME_AREA_X < new_x < GAME_AREA_X + GAME_AREA_SIZE - self.width and
            GAME_AREA_Y < new_y < GAME_AREA_Y + GAME_AREA_SIZE - self.height):
            self.x = new_x
            self.y = new_y

    def draw(self, screen: pg.Surface):
        """
        引数 screen：画面surface
        """
        pg.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))


class Enemy:
    """
    敵キャラを表示するクラス
    """
    def __init__(self):
        self.width = 60
        self.height = 60
        self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.y = 50
        self.speed = random.uniform(2, 5)
        self.hp = 100 # 敵HPの追加（初期化）
        self.direction = random.choice([-1, 1])
        self.change_direction_counter = 0 # 敵の移動判定のカウンターの初期化
        self.change_direction_threshold = random.randint(60, 180) # 敵の停止時間をランダム値で設定

    def move(self):
        """
        敵キャラを速度ベクトルself.x,self.directionに基づき移動させる
        """
        self.x += self.speed * self.direction
        if self.x <= 0 or self.x >= SCREEN_WIDTH - self.width:
            self.direction *= -1

        self.change_direction_counter += 1 # 敵の移動判定のカウンターの更新
        if self.change_direction_counter >= self.change_direction_threshold: # 敵の停止時間超えたら敵を移動させる
            self.direction = random.choice([-1, 1]) # 敵の動くy軸+-の方向をランダムに設定
            self.speed = random.uniform(2, 5) # 敵の移動量をランダムに設定
            self.change_direction_counter = 0 # 敵の移動判定のカウンターのリセット
            self.change_direction_threshold = random.randint(60, 180) # 敵の停止時間をランダム値で設定

    def draw(self, screen: pg.Surface):
        """
        引数 screen：画面surface
        """
        pg.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))


class Bullet:
    """
    敵味方が攻撃を行う弾を表すクラス。

    変数:
        x : 弾の現在のx座標
        y : 弾の現在のy座標
        dx : x方向の移動速度
        dy : y方向の移動速度

    メソッド:
        move(): 弾を移動させる
        draw(screen): 弾を画面上に描画する
    """
    def __init__(self, x:float, y:float, target_x:float, target_y:float):
        """
        Bulletオブジェクトを初期化する。

        引数:
            x : 弾の初期x座標
            y : 弾の初期y座標
            target_x : プレイヤーのx座標
            target_y : プレイヤーのy座標
        """
        self.x = x
        self.y = y
        self.speed = 5
        angle = math.atan2(target_y - y, target_x - x)
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed
        self.is_enemy_bullet = True
        self.is_normal_enemy_bullet = False
        self.is_inside_square = False

    def move(self):
        """弾を現在の速度に基づいて移動させる。"""
        self.x += self.dx
        self.y += self.dy

    def bounce(self):
        angle = random.uniform(0, 2 * math.pi)
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed

    def draw(self, screen: pg.Surface):
        """
        弾を画面上に描画する。

        引数:
            screen (pygame.Surface): 描画対象の画面
        """
        if self.is_normal_enemy_bullet:
            color = WHITE  # 通常の敵の弾は白色
        elif self.is_enemy_bullet:
            color = YELLOW  # その他の敵の弾は黄色
        else:
            color = BLUE  # プレイヤーの弾は青色
        pg.draw.circle(screen, color, (int(self.x), int(self.y)), 5)

    @classmethod
    def create_normal_enemy_bullet(cls):
        side = random.choice(['top', 'bottom', 'left', 'right'])
        if side == 'top':
            x = random.randint(0, SCREEN_WIDTH)
            y = 0
        elif side == 'bottom':
            x = random.randint(0, SCREEN_WIDTH)
            y = SCREEN_HEIGHT
        elif side == 'left':
            x = 0
            y = random.randint(0, SCREEN_HEIGHT)
        else:  # right
            x = SCREEN_WIDTH
            y = random.randint(0, SCREEN_HEIGHT)

        target_x = GAME_AREA_X + GAME_AREA_SIZE // 2
        target_y = GAME_AREA_Y + GAME_AREA_SIZE // 2
        bullet = cls(x, y, target_x, target_y)
        bullet.is_normal_enemy_bullet = True
        return bullet

def main():
    player = Player()
    enemy = Enemy() # enemy関数の呼び出し
    player_bullets = [] #プレイヤーと敵の弾を保持するリスト
    enemy_bullets = []
    clock = pg.time.Clock()

    red_bullet_timer = 0  # 赤い弾のタイマーを初期化
    red_bullet_interval = 10 * 60  # 30秒 * 60フレーム/秒 = 1800フレーム

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_SPACE: # スペースキーで弾の発射
                    bullet = Bullet(player.x + player.width // 2, player.y,
                                    player.x + player.width // 2, 0)
                    bullet.is_enemy_bullet = False
                    player_bullets.append(bullet)

        keys = pg.key.get_pressed()
        player.move(keys[pg.K_RIGHT] - keys[pg.K_LEFT], keys[pg.K_DOWN] - keys[pg.K_UP])

        enemy.move()

         # 敵の通常攻撃（白い弾）
        # 敵の通常攻撃（白い弾）
        if random.random() < 0.02:
            enemy_bullets.append(Bullet.create_normal_enemy_bullet())
            
        # 赤い弾の生成（30秒に1回）
        red_bullet_timer += 1
        if red_bullet_timer >= red_bullet_interval:
            # 画面の四辺からランダムに弾を発射
            side = random.choice(['top', 'bottom', 'left', 'right'])
            if side == 'top':
                x = random.randint(0, SCREEN_WIDTH)
                y = 0
            elif side == 'bottom':
                x = random.randint(0, SCREEN_WIDTH)
                y = SCREEN_HEIGHT
            elif side == 'left':
                x = 0
                y = random.randint(0, SCREEN_HEIGHT)
            else:  # right
                x = SCREEN_WIDTH
                y = random.randint(0, SCREEN_HEIGHT)

            target_x = GAME_AREA_X + GAME_AREA_SIZE // 2
            target_y = GAME_AREA_Y + GAME_AREA_SIZE // 2
            red_bullet = Bullet(x, y, target_x, target_y)
            red_bullet.is_enemy_bullet = True
            red_bullet.is_normal_enemy_bullet = False
            enemy_bullets.append(red_bullet)

            red_bullet_timer = 0
        
        # プレイヤーの弾の移動と当たり判定
        for bullet in player_bullets[:]: # 弾の動きと衝突
            bullet.move()
            if bullet.y < 0:
                player_bullets.remove(bullet)
            elif (enemy.x < bullet.x < enemy.x + enemy.width and
                  enemy.y < bullet.y < enemy.y + enemy.height):
                enemy.hp -= 10 # 敵HPの更新
                player.sp += 5 # プレイヤーSPの更新
                player_bullets.remove(bullet)

        # 敵の弾の移動と当たり判定
        for bullet in enemy_bullets[:]:
            bullet.move()
            if (bullet.x < 0 or bullet.x > SCREEN_WIDTH or
                bullet.y < 0 or bullet.y > SCREEN_HEIGHT):
                enemy_bullets.remove(bullet)
            elif (player.x < bullet.x < player.x + player.width and
                  player.y < bullet.y < player.y + player.height):
                player.hp -= 1
                enemy_bullets.remove(bullet)
            elif not bullet.is_normal_enemy_bullet:  # 通常の敵の弾でない場合のみバウンド処理
                if not bullet.is_inside_square:
                    if (GAME_AREA_X < bullet.x < GAME_AREA_X + GAME_AREA_SIZE and
                        GAME_AREA_Y < bullet.y < GAME_AREA_Y + GAME_AREA_SIZE):
                        bullet.is_inside_square = True
                        bullet.bounce()
                else:
                    if (bullet.x < GAME_AREA_X or bullet.x > GAME_AREA_X + GAME_AREA_SIZE or
                        bullet.y < GAME_AREA_Y or bullet.y > GAME_AREA_Y + GAME_AREA_SIZE):
                        bullet.bounce()
                        # 中央の四角形内に戻す
                        bullet.x = max(GAME_AREA_X, min(bullet.x, GAME_AREA_X + GAME_AREA_SIZE))
                        bullet.y = max(GAME_AREA_Y, min(bullet.y, GAME_AREA_Y + GAME_AREA_SIZE))

        if player.hp <= 0 or enemy.hp <= 0: # ゲームの終了判定
            running = False # ゲームを終了させる

        screen.fill((0, 0, 0))
        # プレイヤーの行動範囲を視覚的に表示する
        pg.draw.rect(screen, WHITE, (GAME_AREA_X, GAME_AREA_Y, GAME_AREA_SIZE, GAME_AREA_SIZE), 2)
        player.draw(screen)
        # 敵キャラを表示
        enemy.draw(screen)
        for bullet in player_bullets + enemy_bullets: # 弾の描画
            bullet.draw(screen)

        pg.draw.rect(screen, RED, (10, SCREEN_HEIGHT - 30, player.hp * 2, 20)) # プレイヤーHPのゲージを表示
        pg.draw.rect(screen, GREEN, (10, 10, enemy.hp * 2, 20)) # 敵HPのゲージを表示
        pg.draw.rect(screen, BLUE, (SCREEN_WIDTH - 210, SCREEN_HEIGHT - 30, player.sp * 2, 20)) # プレイヤーSPのゲージを表示

        pg.display.flip()
        clock.tick(60)

    pg.quit()


if __name__ == "__main__":
    main()