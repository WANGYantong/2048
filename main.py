import pygame
import sys
import random
import copy

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 750

GAMEBOX_LEFT = 50
GAMEBOX_TOP = 200
GAMEBOX_WIDTH = 500
UNIT_WIDTH = GAMEBOX_WIDTH / 33
BOLCK_WIDTH = UNIT_WIDTH * 7
SCOREBOARD_WIDTH = 120
SCOREBOARD_HEIGHT = 55
TITLE_SIZE = 60
SCORETITLE_SIZE = 14
SCORE_SIZE = 24

BROWN_DEEP = (119, 110, 101)
BROWN_NORMAL = (187, 173, 160)
BROWN_LIGHT = (205, 193, 180)
BROWN_MORE_LIGHT = (238, 228, 218)
YELLOW_LIGHT = (250, 248, 239)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

score = 0
best_score = 0


class numBlock:  # 数字块类
    def __init__(self):
        self.num = 0  # 数字
        self.rect = pygame.Rect(0, 0, BOLCK_WIDTH, BOLCK_WIDTH)  # 所在矩形

    def set_position(self, x, y):  # 根据数组下标设置矩形位置
        self.rect.x = GAMEBOX_LEFT + UNIT_WIDTH * (8 * x + 1)
        self.rect.y = GAMEBOX_TOP + UNIT_WIDTH * (8 * y + 1)


def main():
    global best_score
    pygame.init()  # 初始化pyamge库
    images = load_images()  # 载入数字块图片
    best_score = read_best()  # 读入历史最高分数
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # 新建窗口对象
    pygame.display.set_caption('2048')  # 设置窗口标题
    map = init_map()  # 初始化游戏地图二维列表
    map = add_randnum(map)  # 随机加入一个新数字块
    draw_all(screen, map, images)  # 绘制窗口
    # 主循环部分
    while True:
        game_over_label = game_over_check(map)
        for event in pygame.event.get():  # 获取事件(鼠标、键盘等)
            if event.type == pygame.QUIT:  # 如果按下关闭按钮
                pygame.quit()  # 退出pygame窗口
                sys.exit()  # 结束主循环
            elif not game_over_label:  # 游戏没有结束，继续进行
                if event.type == pygame.KEYDOWN:  # 键盘事件
                    if event.key == pygame.K_UP or event.key == pygame.K_w:  # 按下向上键或w键
                        map = move_up(screen, map, images)  # 获取移动后的地图，函数中完成移动动画效果（下同）
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:  # 按下向下键或s键
                        map = move_down(screen, map, images)
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:  # 按下向左键或a键
                        map = move_left(screen, map, images)
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:  # 按下向右键或d键
                        map = move_right(screen, map, images)
            else:  # 游戏结束
                screen.blit(write_text("游戏结束!", height=SCORE_SIZE * 2, color=RED),
                            (WINDOW_WIDTH / 2 - 150, WINDOW_HEIGHT / 2 - 48))
                screen.blit(write_text("按键n 再来一局", height=SCORE_SIZE * 2, color=RED),
                            (WINDOW_WIDTH / 2 - 150, WINDOW_HEIGHT / 2))
                screen.blit(write_text("按键q 退出游戏", height=SCORE_SIZE * 2, color=RED),
                            (WINDOW_WIDTH / 2 - 150, WINDOW_HEIGHT / 2 + 48))
                pygame.display.update()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:  # 按下n键重新开始一局
                        global score
                        score = 0  # 分数重新计算
                        game_over_label = False  # 重置游戏结束标识
                        map = init_map()  # 初始化游戏地图
                        map = add_randnum(map)  # 随即加入数字快
                        draw_all(screen, map, images)  # 绘制窗口
                    if event.key == pygame.K_q or event.type == pygame.QUIT:  # 退出游戏
                        pygame.quit()
                        sys.exit()


def load_images():
    images = [0]
    for i in range(1, 16):
        images.append(pygame.image.load("block/" + str(i) + ".png"))
        images[i] = pygame.transform.scale(images[i], (int(BOLCK_WIDTH), int(BOLCK_WIDTH)))
    return images


def draw_bg(screen):
    screen.fill(YELLOW_LIGHT)
    gamebox_rect = pygame.Rect(GAMEBOX_LEFT, GAMEBOX_TOP, GAMEBOX_WIDTH, GAMEBOX_WIDTH)
    pygame.draw.rect(screen, BROWN_NORMAL, gamebox_rect, 0, 5)
    for i in range(4):
        for j in range(4):
            block_rect = pygame.Rect(GAMEBOX_LEFT + UNIT_WIDTH * (8 * i + 1), GAMEBOX_TOP + UNIT_WIDTH * (8 * j + 1),
                                     BOLCK_WIDTH, BOLCK_WIDTH)
            pygame.draw.rect(screen, BROWN_LIGHT, block_rect, 0, 5)


def draw_titlebar(screen):
    # 绘制2048标题
    title_font = pygame.font.Font('font/ClearSansBold.woff.ttf', TITLE_SIZE)
    title_text = title_font.render('2048', True, BROWN_DEEP)
    screen.blit(title_text, (GAMEBOX_LEFT, GAMEBOX_TOP / 2 - TITLE_SIZE * 3 / 4))
    # 绘制记分牌背板
    scoreboard_rect = pygame.Rect(WINDOW_WIDTH - GAMEBOX_LEFT - SCOREBOARD_WIDTH * 15 / 7,
                                  GAMEBOX_TOP / 2 - SCOREBOARD_HEIGHT * 3 / 4, SCOREBOARD_WIDTH, SCOREBOARD_HEIGHT)
    pygame.draw.rect(screen, BROWN_NORMAL, scoreboard_rect, 0, 3)
    bestboard_rect = pygame.Rect(WINDOW_WIDTH - GAMEBOX_LEFT - SCOREBOARD_WIDTH,
                                 GAMEBOX_TOP / 2 - SCOREBOARD_HEIGHT * 3 / 4, SCOREBOARD_WIDTH, SCOREBOARD_HEIGHT)
    pygame.draw.rect(screen, BROWN_NORMAL, bestboard_rect, 0, 3)
    # 绘制记分牌标题文字
    scoretitle_font = pygame.font.SysFont('Arial', SCORETITLE_SIZE, True)
    scoretitle_text = scoretitle_font.render('SCORE', True, BROWN_MORE_LIGHT)
    scoretitle_rect = scoretitle_text.get_rect()
    scoretitle_rect.center = (
        WINDOW_WIDTH - GAMEBOX_LEFT - SCOREBOARD_WIDTH * (15 / 7 - 1 / 2), GAMEBOX_TOP / 2 - SCOREBOARD_HEIGHT / 2)
    screen.blit(scoretitle_text, scoretitle_rect)

    besttitle_font = pygame.font.SysFont('Arial', SCORETITLE_SIZE, True)
    besttitle_text = besttitle_font.render('BEST', True, BROWN_MORE_LIGHT)
    besttitle_rect = besttitle_text.get_rect()
    besttitle_rect.center = (
        WINDOW_WIDTH - GAMEBOX_LEFT - SCOREBOARD_WIDTH / 2, GAMEBOX_TOP / 2 - SCOREBOARD_HEIGHT / 2)
    screen.blit(besttitle_text, besttitle_rect)

    # 绘制分数
    global score, best_score

    score_font = pygame.font.Font('font/ClearSansBold.woff.ttf', SCORE_SIZE)
    score_text = score_font.render(str(score), True, WHITE)
    score_rect = score_text.get_rect()
    score_rect.center = (
        WINDOW_WIDTH - GAMEBOX_LEFT - SCOREBOARD_WIDTH * (15 / 7 - 1 / 2), GAMEBOX_TOP / 2 - SCOREBOARD_HEIGHT / 10)
    screen.blit(score_text, score_rect)

    best_font = pygame.font.Font('font/ClearSansBold.woff.ttf', SCORE_SIZE)
    best_text = best_font.render(str(best_score), True, WHITE)
    best_rect = best_text.get_rect()
    best_rect.center = (WINDOW_WIDTH - GAMEBOX_LEFT - SCOREBOARD_WIDTH / 2, GAMEBOX_TOP / 2 - SCOREBOARD_HEIGHT / 10)
    screen.blit(best_text, best_rect)


def draw_blocks(screen, map, images):
    for i in range(4):
        for j in range(4):
            if map[i][j].num != 0:
                screen.blit(images[map[i][j].num], (map[i][j].rect.x, map[i][j].rect.y))


def draw_all(screen, map, images):
    draw_bg(screen)
    draw_titlebar(screen)
    draw_blocks(screen, map, images)
    pygame.display.update()


def init_map():
    map = []
    for i in range(4):
        line = []
        for j in range(4):
            line.append(numBlock())
        map.append(line)
    return map


def add_randnum(map):
    x = random.randint(0, 3)
    y = random.randint(0, 3)
    while map[y][x].num != 0:
        x = random.randint(0, 3)
        y = random.randint(0, 3)
    map[y][x].num = random.randint(1, 2)
    map[y][x].set_position(x, y)
    return map


def print_map(map):
    for i in range(4):
        for j in range(4):
            print(map[i][j].num, end=" ")
        print()


def equal_map(map1, map2):
    equal = True
    for i in range(4):
        for j in range(4):
            if map1[i][j].num != map2[i][j].num:
                equal = False
                break
    return equal


def move_up(screen, map, images):
    global score, best_score
    pre_map = copy.deepcopy(map)
    map = copy.deepcopy(map)
    move_step = [[0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]]
    for j in range(4):
        k = 0
        pre_num = numBlock()
        for i in range(4):
            if map[i][j].num == 0:
                k += 1
            else:
                if map[i][j].num == pre_num.num:
                    pre_num.num += 1
                    score += pow(2, pre_num.num)
                    if best_score < score:
                        best_score = score
                        write_best(score)
                    map[i][j] = numBlock()
                    k += 1
                    move_step[i][j] = k
                else:
                    t = map[i][j]
                    map[i][j] = numBlock()
                    map[i - k][j] = t
                    map[i - k][j].set_position(j, i - k)
                    move_step[i][j] = k
                pre_num = map[i - k][j]
    is_moving = True
    k = 0
    while is_moving:
        is_moving = False
        k += 1
        for i in range(4):
            for j in range(4):
                if move_step[i][j] > 0.1:
                    is_moving = True
                    move_step[i][j] -= 1 / 10
                    pre_map[i][j].set_position(j, i - k * 1 / 10)
        draw_all(screen, pre_map, images)

    if not equal_map(map, pre_map):
        add_randnum(map)
    draw_all(screen, map, images)
    return map


def move_down(screen, map, images):
    global score, best_score
    pre_map = copy.deepcopy(map)
    map = copy.deepcopy(map)
    move_step = [[0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]]
    for j in range(4):
        k = 0
        pre_num = numBlock()
        for i in range(3, -1, -1):
            if map[i][j].num == 0:
                k += 1
            else:
                if map[i][j].num == pre_num.num:
                    pre_num.num += 1
                    score += pow(2, pre_num.num)
                    if best_score < score:
                        best_score = score
                        write_best(score)
                    map[i][j] = numBlock()
                    k += 1
                    move_step[i][j] = k
                else:
                    t = map[i][j]
                    map[i][j] = numBlock()
                    map[i + k][j] = t
                    map[i + k][j].set_position(j, i + k)
                    move_step[i][j] = k
                pre_num = map[i + k][j]
    is_moving = True
    k = 0
    while is_moving:
        is_moving = False
        k += 1
        for i in range(4):
            for j in range(4):
                if move_step[i][j] > 0.1:
                    is_moving = True
                    move_step[i][j] -= 1 / 10
                    pre_map[i][j].set_position(j, i + k * 1 / 10)
        draw_all(screen, pre_map, images)

    if not equal_map(map, pre_map):
        add_randnum(map)
    draw_all(screen, map, images)
    return map


def move_left(screen, map, images):
    global score, best_score
    pre_map = copy.deepcopy(map)
    map = copy.deepcopy(map)
    move_step = [[0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]]
    for i in range(4):
        k = 0
        pre_num = numBlock()
        for j in range(4):
            if map[i][j].num == 0:
                k += 1
            else:
                if map[i][j].num == pre_num.num:
                    pre_num.num += 1
                    score += pow(2, pre_num.num)
                    if best_score < score:
                        best_score = score
                        write_best(score)
                    map[i][j] = numBlock()
                    k += 1
                    move_step[i][j] = k
                else:
                    t = map[i][j]
                    map[i][j] = numBlock()
                    map[i][j - k] = t
                    map[i][j - k].set_position(j - k, i)
                    move_step[i][j] = k
                pre_num = map[i][j - k]
    is_moving = True
    k = 0
    while is_moving:
        is_moving = False
        k += 1
        for i in range(4):
            for j in range(4):
                if move_step[i][j] > 0.1:
                    is_moving = True
                    move_step[i][j] -= 1 / 10
                    pre_map[i][j].set_position(j - k * 1 / 10, i)
        draw_all(screen, pre_map, images)

    if not equal_map(map, pre_map):
        add_randnum(map)
    draw_all(screen, map, images)
    return map


def move_right(screen, map, images):
    global score, best_score
    pre_map = copy.deepcopy(map)
    map = copy.deepcopy(map)
    move_step = [[0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]]
    for i in range(4):
        k = 0
        pre_num = numBlock()
        for j in range(3, -1, -1):
            if map[i][j].num == 0:
                k += 1
            else:
                if map[i][j].num == pre_num.num:
                    pre_num.num += 1
                    score += pow(2, pre_num.num)
                    if best_score < score:
                        best_score = score
                        write_best(score)
                    map[i][j] = numBlock()
                    k += 1
                    move_step[i][j] = k
                else:
                    t = map[i][j]
                    map[i][j] = numBlock()
                    map[i][j + k] = t
                    map[i][j + k].set_position(j + k, i)
                    move_step[i][j] = k
                pre_num = map[i][j + k]
    is_moving = True
    k = 0
    while is_moving:
        is_moving = False
        k += 1
        for i in range(4):
            for j in range(4):
                if move_step[i][j] > 0.1:
                    is_moving = True
                    move_step[i][j] -= 1 / 10
                    pre_map[i][j].set_position(j + k * 1 / 10, i)
        draw_all(screen, pre_map, images)

    if not equal_map(map, pre_map):
        add_randnum(map)
    draw_all(screen, map, images)
    return map


def read_best():
    f = open('best', 'r')
    score = int(f.read())
    return score


def write_best(score):
    f = open('best', 'w')
    f.write(str(score))


def write_text(message="testing", color=(255, 255, 0), height=14):
    text_font = pygame.font.Font('font/simhei.ttf', height)
    text = text_font.render(message, True, color)
    text = text.convert_alpha()
    return text


def game_over_check(map):
    for i in range(4):
        for j in range(4):
            if map[i][j].num == 0:  # 还有空白
                return False
    for i in range(4):
        for j in range(3):
            if map[i][j].num == map[i][j + 1].num:  # 可以左右合并
                return False
    for i in range(3):
        for j in range(4):
            if map[i][j].num == map[i + 1][j].num:  # 可以上下合并
                return False
    return True  # 游戏失败


main()
