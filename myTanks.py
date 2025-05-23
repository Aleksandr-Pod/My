import pygame
from random import randint
from time import sleep

pygame.init()
# Инициализация окна
mw = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Класс танка
class Tank():
    def __init__(self, filename, hp, ammo, defence, range, color, x, y, l, h, side = "left"):
        self.team = side
        self.maxHP = hp
        self.currentHP = hp
        if side == "left":
            self.maxHPBar = pygame.Rect(10, 80, 80, 20)
        else:
            self.maxHPBar = pygame.Rect(710, 80, 80, 20)
        self.currentHPBar = self.maxHPBar
        self.ammo = ammo
        self.defence = defence
        self.range = range
        self.color = color
        self.box = pygame.Rect(x, y, l, h)
        self.picture = pygame.image.load(filename)
        self.picture = pygame.transform.scale(self.picture, (l, h))
        self.currentView = self.picture
        self.moveDirection = ""
    def fill(self):
        pygame.draw.rect(mw, self.color, self.box)

    def draw(self):
        mw.blit(self.currentView, (self.box.x, self.box.y))

    def move(self, dx, dy):
        self.box.x += dx
        self.box.y += dy

    def writeHP(self):
        fontObj = pygame.font.SysFont('arial', 24, bold=True)
        textSurface = fontObj.render(f"HP: {self.currentHP}", True, ("#5f5f5f"))
        if self.team == "left":
            mw.blit(textSurface, (20, 50))
            # пишем текст слева
        else:
            mw.blit(textSurface, (720, 50))
            # пишем текст справа

    def drawHP(self):
        pygame.draw.rect(mw, "darkgray", self.maxHPBar)
        self.currentHPBar.width = 80 * (self.currentHP / self.maxHP)
        pygame.draw.rect(mw, "red", self.currentHPBar)

class Mines():
    def __init__(self, x, y):
        self.image = pygame.image.load("images/land-mine-64.png")
        self.picture = pygame.transform.scale(self.image, (30, 30))
        self.box = pygame.Rect(x, y, 30, 30)
    def fill(self):
        pygame.draw.rect(mw, "gray", self.box)
    def draw(self):
        mw.blit(self.picture, (self.box.x, self.box.y))
    def is_collide(self, rect):
        return self.box.colliderect(rect)

# Создаем поле с минами
fild = []
minefieldSprites = []
for x in range(20):
    xline = []
    for i in range(20):
        a = randint(1, 10)  # Генерация случайного значения для клетки
        if a == 1:
            xline.append(1)  # 1 - это мина
            minefieldSprites.append(Mines(i*30 + 100, x*30))
        else:
            xline.append(0)  # 0 - пустая клетка
    fild.append(xline)
    xline = []
print("total quantity of mines:", len(minefieldSprites))

def writeGameOver(tank):
    fontObj = pygame.font.SysFont('arial', 60, bold=True)
    textSurface = fontObj.render("GAME OVER - "+ tank.team + " loose", True, ("#5f5f5f"))
    mw.blit(textSurface, (100, 10))
    print(f"GameOver - {tank.team} loose")

firedMines = []
whoLoose = ""
in_game = True

tank1 = Tank("images/tank.png", 140, "pod", 60, 40, "gray", 40, 150, 40, 40, "left")
tank1.moveDirection = "right"
# tank2 = Tank("images/launcher.png", 200, "bp", 100, 30, "gray", 750, 550, 40, 40)
tank3 = Tank("images/tank-50.png", 150, "bp", 100, 30, "gray", 700, 350, 40, 40, "right")

# Функция для рисования мин
def draw_firedMines():
    for mine in firedMines:
        mine.draw()

# Проверка на столкновение с миной
def check_mines(tank, whoLoose):
    for mine in minefieldSprites:
        if mine.is_collide(tank.box):
            mine.draw()
            minefieldSprites.remove(mine)
            firedMines.append(mine)
            tank.currentHP -= 10
            if tank.currentHP <= 0:
                whoLoose = tank
                writeGameOver(whoLoose)
                break
    return whoLoose

# Функция для перемещения танка
def move_tank(tank, direction, rotation, move_x, move_y, boundary_check):
    if tank.moveDirection != direction:
        tank.currentView = pygame.transform.rotate(tank.picture, rotation)
        tank.moveDirection = direction
    if boundary_check:
        tank.move(move_x, move_y)

while in_game:
    mw.fill("green")

    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            in_game = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        if tank1.box.y > 0:
            tank1.move(0, -5)
    if keys[pygame.K_DOWN]:
        if tank1.box.y < 560:
            tank1.move(0, 5)
    if keys[pygame.K_LEFT]:
        if tank1.moveDirection != "left":
            tank1.currentView = pygame.transform.flip(tank1.picture, True, False)
            tank1.moveDirection = "left"
        if tank1.box.x > 0:
            tank1.move(-5, 0)
    if keys[pygame.K_RIGHT]:
        if tank1.moveDirection != "right":
            tank1.currentView = tank1.picture
            tank1.moveDirection = "right"
        if tank1.box.x < 760:
            tank1.move(5, 0)

    if keys[pygame.K_w]:
        move_tank(tank3, "up", 0, 0, -5, tank3.box.y > 0)
    if keys[pygame.K_s]:
        move_tank(tank3, "down", 180, 0, 5, tank3.box.y < 560)
    if keys[pygame.K_a]:
        move_tank(tank3, "left", 90, -5, 0, tank3.box.x > 0)
    if keys[pygame.K_d]:
        move_tank(tank3, "right", 270, 5, 0, tank3.box.x < 760)

    # Рисуем мины
    draw_firedMines()

    # Проверяем столкновения танков с минами
    whoLoose = check_mines(tank1, whoLoose)
    whoLoose = check_mines(tank3, whoLoose)
    # Проверяем, нужно ли завершить игру
    if whoLoose != "":
        in_game = False
    
    # Рисуем танки
    tank1.draw()
    # tank2.draw()
    tank3.draw()

    tank1.writeHP()
    tank1.drawHP()
    # tank2.writeHP("")
    tank3.writeHP()
    tank3.drawHP()
    
    pygame.display.update()
    clock.tick(30)

sleep(3)
waiting_for_key = True
while waiting_for_key:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:  # Check if a key is pressed
            waiting_for_key = False 
pygame.quit()
