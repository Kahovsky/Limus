import os
import sys

import pygame
import pygame_gui

import database
import levels

pygame.init()
clock = pygame.time.Clock()

manager = pygame_gui.UIManager((800, 500))

FPS = 50

pygame.mixer.music.load('data/ppk-voskreshenie (1).mp3')
pygame.mixer.music.set_volume(0.1)


def draw_text(surf, text, size, x, y, col, ):
    font = pygame.font.Font('data\konstanking.ttf', size)
    text_surface = font.render(text, True, col)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def record_screen(WIDTH, HEIGHT, screen):
    pygame.mixer.music.play(-1)
    manager = pygame_gui.UIManager((WIDTH, HEIGHT))
    fon = pygame.transform.scale(load_image('background_reiting.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    draw_text(screen, "РЕЙТИНГ ИГРОКОВ", HEIGHT // 7, WIDTH // 2, 5, (255, 255, 255))

    level = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 20),
                                                                    (WIDTH // 7, HEIGHT // 9)),
                                          text='уровни',
                                          manager=manager)
    res_my = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH - WIDTH // 7 - 20, 20),
                                                                    (WIDTH // 7 + 10, HEIGHT // 9)),
                                          text='отчистить меня',
                                          manager=manager)
    res_all = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH - WIDTH // 7 - 20, HEIGHT // 9 + 22),
                                                                     (WIDTH // 7 + 10, HEIGHT // 9)),
                                           text='отчистить всех',
                                           manager=manager)
    while True:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == level:
                        pygame.mixer.music.pause()
                        level_screen(WIDTH, HEIGHT, screen)
                        return
                    elif event.ui_element == res_my:
                        database.my_clear(levels.name)
                    elif event.ui_element == res_all:
                        database.clear_all()

            manager.process_events(event)
        screen.blit(fon, (0, 0))
        r = database.records()
        draw_text(screen, "РЕЙТИНГ ИГРОКОВ", HEIGHT // 7, WIDTH // 2, 5, (255, 255, 255))
        draw_text(screen, f"1: {r[0][0]} - {str(r[0][1])}", HEIGHT // 9, WIDTH // 2, HEIGHT // 25 * 4, (255, 255, 255))
        for i in range(2, len(r) + 1):
            draw_text(screen, f"{str(i)}: {r[i - 1][0]} - {str(r[i - 1][1])}",
                      HEIGHT // 12, WIDTH // 2,
                      HEIGHT // 13 * i + HEIGHT // 13 * 2, (255, 255, 255))

        manager.update(time_delta)

        manager.draw_ui(screen)

        pygame.display.update()


def level_screen(WIDTH, HEIGHT, screen):
    import levels
    pygame.mixer.music.play(-1)
    manager = pygame_gui.UIManager((WIDTH, HEIGHT))
    fon = pygame.transform.scale(load_image('background_levels.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    level1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH // 8 * 3, HEIGHT // 9),
                                                                    (WIDTH // 4, HEIGHT // 10)),
                                          text='уровень 1',
                                          manager=manager)
    level2 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH // 8 * 3, HEIGHT // 9 * 2.3),
                                                                    (WIDTH // 4, HEIGHT // 10)),
                                          text='уровень 2',
                                          manager=manager)
    level3 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH // 8 * 3, HEIGHT // 9 * 3.6),
                                                                    (WIDTH // 4, HEIGHT // 10)),
                                          text='уровень 3',
                                          manager=manager)
    level4 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH // 8 * 3, HEIGHT // 9 * 4.9),
                                                                    (WIDTH // 4, HEIGHT // 10)),
                                          text='уровень 4',
                                          manager=manager)
    level_b = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH // 8 * 2, HEIGHT // 9 * 6.5),
                                                                     (WIDTH // 2, HEIGHT // 10)),
                                           text='бесконечный режим',
                                           manager=manager)
    main_menu = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH // 4 * 3, HEIGHT // 4),
                                                                       (HEIGHT // 4, HEIGHT // 4)),
                                             text='в главное меню',
                                             manager=manager)
    records = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH // 4 - (HEIGHT // 4), HEIGHT // 4),
                                                                     (HEIGHT // 4, HEIGHT // 4)),
                                           text='рейтинг',
                                           manager=manager)
    while True:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == level_b:
                        pygame.mixer.music.pause()
                        levels.endless_level()
                        return
                    elif event.ui_element == level1:
                        pygame.mixer.music.pause()
                        levels.first_level()
                        return
                    elif event.ui_element == level2:
                        pygame.mixer.music.pause()
                        levels.second_level()
                        return
                    elif event.ui_element == level3:
                        pygame.mixer.music.pause()
                        levels.third_level()
                        return
                    elif event.ui_element == level4:
                        pygame.mixer.music.pause()
                        levels.fourth_level()
                        return
                    elif event.ui_element == main_menu:
                        pygame.mixer.music.pause()
                        start_screen(WIDTH, HEIGHT, screen)
                        return
                    elif event.ui_element == records:
                        pygame.mixer.music.pause()
                        record_screen(WIDTH, HEIGHT, screen)
                        return

            manager.process_events(event)

        manager.update(time_delta)

        manager.draw_ui(screen)

        pygame.display.update()


def final_screen(c, WIDTH, HEIGHT, screen, f):
    global levels
    pygame.mixer.music.play(-1)
    if c > database.my_record(levels.name):
        database.set_record(levels.name, c)
    manager = pygame_gui.UIManager((WIDTH, HEIGHT))
    fon = pygame.transform.scale(load_image('final_background.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    if f:
        draw_text(screen, "вы выйграли!", HEIGHT // 9, WIDTH // 2, HEIGHT // 8, (255, 255, 255))
    else:
        draw_text(screen, "вы проиграли!", HEIGHT // 9, WIDTH // 2, HEIGHT // 8, (255, 255, 255))
    mr = database.my_record(levels.name)
    lr = database.records()
    draw_text(screen, "счет игры:", HEIGHT // 19, WIDTH // 2, HEIGHT // 4, (255, 255, 255))
    draw_text(screen, str(c), HEIGHT // 19, WIDTH // 2, HEIGHT // 4 + HEIGHT // 19, (255, 255, 255))
    draw_text(screen, "ваш лучший счет:", HEIGHT // 19, WIDTH // 2, HEIGHT // 4 * 2 - HEIGHT // 15, (255, 255, 255))
    draw_text(screen, str(mr), HEIGHT // 19, WIDTH // 2, HEIGHT // 4 * 2, (255, 255, 255))
    draw_text(screen, "лучший счет игры:", HEIGHT // 19, WIDTH // 2, HEIGHT // 4 * 3 - HEIGHT // 10, (255, 255, 255))
    draw_text(screen, f'{lr[0][0]} - {str(lr[0][1])}', HEIGHT // 19, WIDTH // 2, HEIGHT // 4 * 3, (255, 255, 255))
    levels = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH // 4, HEIGHT // 9 * 8),
                                                                    (WIDTH // 7, HEIGHT // 9)),
                                          text='уровни',
                                          manager=manager)
    reiting = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH // 4 * 3 - WIDTH // 7, HEIGHT // 9 * 8),
                                                                     (WIDTH // 7, HEIGHT // 9)),
                                           text='рейтинг',
                                           manager=manager)
    while True:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == levels:
                        level_screen(WIDTH, HEIGHT, screen)
                        pygame.mixer.music.pause()
                        return
                    elif event.ui_element == reiting:
                        pygame.mixer.music.pause()
                        record_screen(WIDTH, HEIGHT, screen)
                        return
            manager.process_events(event)

        manager.update(time_delta)

        manager.draw_ui(screen)

        pygame.display.update()


def start_screen(WIDTH, HEIGHT, screen):
    pygame.mixer.music.play(-1)
    manager = pygame_gui.UIManager((WIDTH, HEIGHT))
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    text = ['На твой город напали пришельцы с планеты "Limus".',
            'Не дай им добраться до домов, уничтожь все летающие тарелки.',
            'Помни, что некоторые из них особо опасны',
            'и требуют двойных усилий.',
            ' Для начала игры выберете персонажа и уровень',
            'ПАУЗА НА ПРОБЕЛ']
    a = database.names()
    s = []
    for i in range(0, len(a), 3):
        ss = [a[i], a[i + 1], a[i + 2]]
        s.append(ss)

    s1 = []
    b = (HEIGHT // 3.3) * 2
    rx = (WIDTH // 2.5) // 3
    ry = (HEIGHT // 3) // 3
    for i in s:
        c = (WIDTH // 3.5) * 2
        for j in i:
            s1.append((pygame_gui.elements.UIButton(relative_rect=pygame.Rect((c, b), (rx, ry)),
                                                    text=j,
                                                    manager=manager)
                       , j))
            c += rx
        b += ry

    while True:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    for i in s1:
                        if event.ui_element == i[0]:
                            levels.name = i[1]
                            level_screen(WIDTH, HEIGHT, screen)
                            pygame.mixer.music.pause()
                            return

            manager.process_events(event)

        manager.update(time_delta)

        pygame.display.flip()
        clock.tick(FPS)

        screen.blit(fon, (0, 0))
        manager.draw_ui(screen)
        draw_text(screen, 'Limus', HEIGHT // 4, WIDTH // 4, HEIGHT // 10, (255, 255, 255))
        draw_text(screen, 'Выберете игрока', HEIGHT // 20, (WIDTH // 2.3) * 2, (HEIGHT // 3.3) * 2 - HEIGHT // 20,
                  (159, 150, 150))
        a = HEIGHT // 2
        for i in text:
            draw_text(screen, i, HEIGHT // 25, WIDTH // 4, a, (255, 255, 255))
            a += HEIGHT // 15
        draw_text(screen, 'проектная работа Наташи Соколовой и Ульяны Хромовой', HEIGHT // 30, WIDTH // 2, 0,
                  (255, 255, 255))


def pausa(WIDTH, HEIGHT, screen):
    pygame.mixer.music.play(-1)
    fon = pygame.transform.scale(load_image('background_pause.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    draw_text(screen, 'ну пауза и пауза че бубнить-то', 50, WIDTH // 2, HEIGHT // 2 - 50, (20, 20, 20))
    draw_text(screen, 'нажмите на любую кнопку для продолжения', 25, WIDTH // 2, HEIGHT // 5 * 3, (20, 20, 20))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.music.pause()
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)
