import pygame
import random

from NeuralNetwork import NeuralNetwork
from GeneticAlgorithm import GeneticAlgorithm
from Data import *

# Создаем игру и окно
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird NN")
clock = pygame.time.Clock()

# Необходиные переменные для отрисовки фона
bg_surf = pygame.image.load("Images/bg1.png")
bg_rect = bg_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Необходиные переменные для отрисовки земли
ground_surf = pygame.image.load("Images/ground.png")
ground_rect = (0, HEIGHT - 20, WIDTH, HEIGHT)

font1 = pygame.font.Font(None, 65) # Создаем шрифт, для вывода счета

# Группы спрайтов
bird_sprites = pygame.sprite.Group()
tower_sprites = pygame.sprite.Group()


# Класс птички
class Bird(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, image, index, tower_dist, tower_interval):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height

        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.jump = False
        self.count = 0
        self.gravity = GRAVITY
        self.acceleration = 0.3

        self.life = True
        self.score = 0
        self.fit = 0
        self.index = index

        self.tower_dist = tower_dist
        self.tower_interval = tower_interval

    def normalization(self, x, y):
        for tower in tower_sprites:
            if tower.rect.x + 3 * TOWER_WIDTH // 2 > x:
                tower_x = tower.rect.x
                top_tower_y = tower.rect.y
                bottom_tower_y = tower.rect.y - self.tower_dist
                break
        self.x_dist = (tower_x + TOWER_WIDTH - x) / (WIDTH + TOWER_WIDTH - x)
        self.y_top_dist = (top_tower_y - y) / HEIGHT
        self.y_bottom_dist = (bottom_tower_y - y) / HEIGHT

        # Отрисовка расстояний для наглядности
        # pygame.draw.line(screen, RED, [self.rect.x, self.rect.y], [tower_x + 3 * TOWER_WIDTH // 2, self.rect.y])
        # pygame.draw.line(screen, RED, [self.rect.x, self.rect.y], [self.rect.x, top_tower_y])
        # pygame.draw.line(screen, RED, [self.rect.x, self.rect.y], [self.rect.x, bottom_tower_y])

        return self.x_dist, self.y_top_dist, self.y_bottom_dist

    def get_score(self):
        for tower in tower_sprites:
            if tower.rect.x < self.rect.x:
                current_birds_count = len([i for i in bird_sprites])
                if tower.is_counted < current_birds_count and tower.tag == "bottom":
                    self.score += 1
                    tower.is_counted += 1

    def dead(self):
        self.fit = (
            self.score * self.tower_interval - (self.x_dist + 3 * TOWER_WIDTH // 2)
        ) / 10
        BIRDS_RESULTS.append((self.fit, self.index))
        self.kill()

    def update(self, *args):
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     if event.button == 1:
        #         self.jump = True
        #         self.count = self.jump_power
        #         self.gravity = GRAVITY

        if (
            Networks[self.index].query(self.normalization(self.rect.x, self.rect.y))
            > 0.6
        ):
            self.jump = True
            self.count = JUMP_POWER
            self.gravity = GRAVITY
        # Стлокновение с трубой
        hits = pygame.sprite.spritecollide(self, tower_sprites, False)
        if hits:
            self.life = False
        if self.life:
            self.get_score()
            if 0 < self.rect.y and self.rect.y + self.height < HEIGHT:
                if self.count >= -JUMP_POWER and self.jump:
                    self.rect.y -= self.count
                    self.count -= 1
                else:
                    self.rect.y += self.gravity
                    self.gravity += self.acceleration
                    self.jump = False
            else:
                self.life = False
        else:
            self.dead()


# Класс препятствия
class Tower(pygame.sprite.Sprite):
    def __init__(self, width, y, speed, image, tag):
        pygame.sprite.Sprite.__init__(self)
        self.width = width

        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + self.width
        self.rect.y = y

        self.speed = speed

        self.is_counted = 0
        self.tag = tag

    def update(self, *args):
        self.rect.x -= self.speed

        if self.rect.x < -self.width:
            self.kill()


# Класс в котором содержаться все функции, отвечающие за игру в целом
class GameController:
    def __init__(
        self,
        bird_count,
        mutation_chance,
        cross_count,
        tower_dist,
        tower_interval,
        is_random_generated,
    ):

        self.BIRD_COUNT = bird_count
        self.TOWER_DIST = tower_dist
        self.TOWER_INTERVAL = tower_interval
        self.IS_RANDOM_GENERATED = is_random_generated

        # Создаем генетический алгоритм, как объет
        self.genetic = GeneticAlgorithm(
            bird_count=self.BIRD_COUNT,
            mutation_chance=mutation_chance,
            cross_count=cross_count,
            network=Networks,
        )

    """ Создание препятствий """

    def new_towers(self):
        # Слачайная высота, на которой появится новая труба
        Y = random.randint(HEIGHT // 2, 4 * HEIGHT // 5)
        # Нижняя труба
        tower_bottom = Tower(
            width=TOWER_WIDTH,
            y=Y,
            speed=TOWER_SPEED,
            image="Images/tower1.png",
            tag="bottom",
        )
        # Верхняя труба
        tower_top = Tower(
            width=TOWER_WIDTH,
            y=Y - (self.TOWER_DIST + TOWER_HEIGHT),
            speed=TOWER_SPEED,
            image="Images/tower2.png",
            tag="top",
        )
        # Добавляем в группу
        tower_sprites.add(tower_bottom, tower_top)

    """ Генерация новых припятствий """

    def generate_towers(self):
        # Выбираем самую последнюю трубу и проверяем, нужно ли генерировать новую
        tower = [i for i in tower_sprites][-1]
        if tower.rect.x <= WIDTH - self.TOWER_INTERVAL:
            self.new_towers()

    """ Создаем птичек """

    def create_birds(self, count):
        for i in range(1, count + 1):
            # Создаем птичку
            bird = Bird(
                width=BIRD_SIZE,
                height=BIRD_SIZE,
                x=X + 5 * i,
                y=50 + 30 * i,
                image=f"Birds/Bird{i}/bird.png",
                index=i - 1,
                tower_dist=self.TOWER_DIST,
                tower_interval=self.TOWER_INTERVAL,
            )
            bird_sprites.add(bird)

    """ Перезапуск игры """

    def restart(self):
        self.genetic.new_generation(BIRDS_RESULTS)

        Networks.clear()
        # Если максимальный результат текущй популяции меньше, чем -4,
        # то задаем всем птицам случайные весовые коэффициенты
        max_fit = max([i[0] for i in BIRDS_RESULTS])
        if max_fit < -4:
            is_random_generated = True
        else:
            is_random_generated = False
        # Создаем для каждой птички собственную нейросеть
        for i in range(10):
            n = NeuralNetwork(
                input_nodes, hidden_nodes, output_nodes, i + 1, is_random_generated
            )
            Networks.append(n)
        BIRDS_RESULTS.clear()
        self.create_birds(self.BIRD_COUNT)

        tower_sprites.empty()
        self.new_towers()

    def start_game(self):
        # Создаем для каждой птички собственную нейросеть
        for i in range(10):
            n = NeuralNetwork(
                input_nodes, hidden_nodes, output_nodes, i + 1, self.IS_RANDOM_GENERATED
            )
            Networks.append(n)
        self.create_birds(self.BIRD_COUNT)
        self.new_towers()

        run = True
        while run:
            screen.blit(bg_surf, bg_rect)  # Фон
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
            # Счет
            if bird_sprites:
                self.generate_towers()
                # Птички
                bird_sprites.update()
                bird_sprites.draw(screen)
                # Препятствия
                tower_sprites.update()
                tower_sprites.draw(screen)
                # Земля
                screen.blit(ground_surf, ground_rect)
                screen.blit(ground_surf, (WIDTH // 2, HEIGHT - 20))

                try:
                    text = str(max([i.score for i in bird_sprites]))
                except ValueError:
                    text = "0"
                text_render = font1.render(text, 1, BLACK)
                place = text_render.get_rect(center=(WIDTH // 2, HEIGHT // 4))
                screen.blit(text_render, place)
            # Рестарт
            else:
                self.restart()
            pygame.display.flip()
