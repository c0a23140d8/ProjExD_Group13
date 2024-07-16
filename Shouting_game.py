import pygame as pg
import random
import math
import os
import time
from typing import List, Optional

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
        angle = math.atan2(target_y - y, target_x - x)
        speed = 5
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed

    def move(self):
        """弾を現在の速度に基づいて移動させる。"""
        self.x += self.dx
        self.y += self.dy

    def draw(self, screen: pg.Surface):
        """
        弾を画面上に描画する。

        引数:
            screen (pygame.Surface): 描画対象の画面
        """
        pg.draw.circle(screen, WHITE, (int(self.x), int(self.y)), 5)


class SoundManager:
    """
    ゲーム内のサウンドを管理するクラス
    """
    def __init__(self):
        self.bgm = None
        self.load_bgm()

    def load_bgm(self):
        """BGMファイルをロードする"""
        bgm_path = os.path.join(os.path.dirname(__file__), '..\ex5\BGM\maou_bgm_8bit27.mp3')
        try:
            self.bgm = pg.mixer.Sound(bgm_path)
        except pg.error:
            print(f"警告: BGMファイル '{bgm_path}' をロードできませんでした。")

    def play_bgm(self):
        """BGMを再生する"""
        if self.bgm:
            self.bgm.play(loops=-1)  # ループ再生

    def stop_bgm(self):
        """BGMを停止する"""
        if self.bgm:
            self.bgm.stop()
            

class GameEndScreen:
    """
    ゲーム終了画面を管理するクラス。
    ゲームクリアまたはゲームオーバー時に表示される。
    """

    def __init__(self, screen: pg.Surface, is_win: bool):  # 型ヒントを追加
        """
        GameEndScreenオブジェクトを初期化する。

        Args:
            screen (pg.Surface): 描画対象の画面
            is_win (bool): ゲームクリアの場合True、ゲームオーバーの場合False
        """
        self.screen = screen
        self.is_win = is_win
        self.font = pg.font.Font(None, 74)
        self.start_time = time.time()

    def draw(self) -> None:
        """
        ゲーム終了画面を描画する。
        """
        self.screen.fill((0, 0, 0))
        if self.is_win:
            text = self.font.render("GAME CLEAR", True, (255, 255, 0))
        else:
            text = self.font.render("GAME OVER", True, (255, 0, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        self.screen.blit(text, text_rect)
        pg.display.flip()

    def should_exit(self) -> bool:  
        """
        ゲーム終了画面を表示してから3秒経過したかどうかを判定する。

        Returns:
            bool: 3秒経過していればTrue、そうでなければFalse
        """
        return time.time() - self.start_time > 3


def main():
    player = Player()
    enemy = Enemy() # enemy関数の呼び出し
    player_bullets = [] #プレイヤーと敵の弾を保持するリスト
    enemy_bullets = []
    clock = pg.time.Clock()
    
    # SoundManagerのインスタンスを作成
    sound_manager = SoundManager()
    
    # BGMを再生
    sound_manager.play_bgm()

    running = True
    game_end_screen: Optional[GameEndScreen] = None
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_SPACE and not game_end_screen: # スペースキーで弾の発射
                    player_bullets.append(Bullet(player.x + player.width // 2, player.y,
                                                 player.x + player.width // 2, 0))

        if not game_end_screen:
            keys = pg.key.get_pressed()
            player.move(keys[pg.K_RIGHT] - keys[pg.K_LEFT], keys[pg.K_DOWN] - keys[pg.K_UP])

            enemy.move()

            if random.random() < 0.02: # 弾の発生
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
                enemy_bullets.append(Bullet(x, y, target_x, target_y))
            
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
                    player.hp -= 1 # プレイヤーHPの更新
                    enemy_bullets.remove(bullet)

            if player.hp <= 0:
                game_end_screen = GameEndScreen(screen, False)  # GameEndScreen の生成を追加
                sound_manager.stop_bgm()
            elif enemy.hp <= 0:
                game_end_screen = GameEndScreen(screen, True)  # GameEndScreen の生成を追加
                sound_manager.stop_bgm()

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

        else:
            game_end_screen.draw()  
            if game_end_screen.should_exit():  
                running = False
                
        pg.display.flip()
        clock.tick(60)

    pg.quit()


if __name__ == "__main__":
    main()
