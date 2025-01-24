import pygame
from random import randint



# for i in range(10):
#     print(fild[i])  # Выводим поле в консоль для проверки

pygame.init()
# Инициализация окна
mw = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Класс танка
class Tank():
    def __init__(self, filename, hp, ammo, defence, range, color, x, y, l, h):
        self.hp = hp
        self.hp
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

    def writeHP(self, side):
        fontObj = pygame.font.SysFont('arial', 24, bold=True)
        textSurface = fontObj.render(f"HP: {str(self.hp)}", True, ("#5f5f5f"))
        if side == "left":
            mw.blit(textSurface, (20, 50))
            # пишем текст слева
        else:
            mw.blit(textSurface, (720, 50))
            # пишем текст справа
    def drawHP(self):



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

firedMines = []

in_game = True

tank1 = Tank("images/tank.png", 140, "pod", 60, 40, "gray", 40, 150, 40, 40)
tank1.moveDirection = "right"
tank2 = Tank("images/launcher.png", 200, "bp", 100, 30, "gray", 750, 550, 40, 40)
tank3 = Tank("images/tank-50.png", 150, "bp", 100, 30, "gray", 40, 350, 40, 40)

# Функция для рисования мин
def draw_firedMines():
    for mine in firedMines:
        mine.draw()

# Проверка на столкновение с миной
def check_mines(tank):
    for mine in minefieldSprites:
        if mine.is_collide(tank.box):
            mine.draw()
            minefieldSprites.remove(mine)
            firedMines.append(mine)
            tank.hp -= 10

# Функция для перемещения танка
def move_tank(tank, direction, rotation, move_x, move_y, boundary_check):
    if tank.moveDirection != direction:
        tank.currentView = pygame.transform.rotate(tank.picture, rotation)
        tank.moveDirection = direction
    if boundary_check:
        tank.move(move_x, move_y)

while in_game:
    mw.fill("gray")

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

    # if keys[pygame.K_w]:
    #     if tank3.moveDirection != "up":
    #         tank3.currentView = pygame.transform.rotate(tank3.picture, 0)
    #         tank3.moveDirection = "up"
    #     if tank3.box.y > 0:
    #         tank3.move(0, -5)
    # if keys[pygame.K_s]:
    #     if tank3.moveDirection != "down":
    #         tank3.currentView = pygame.transform.rotate(tank3.picture, 180)
    #         tank3.moveDirection = "down"
    #     if tank3.box.y < 560:
    #         tank3.move(0, 5)
    # if keys[pygame.K_a]:
    #     if tank3.moveDirection != "left":
    #         tank3.currentView = pygame.transform.rotate(tank3.picture, 90)
    #         tank3.moveDirection = "left"
    #     if tank3.box.x > 0:
    #         tank3.move(-5, 0)
    # if keys[pygame.K_d]:
    #     if tank3.moveDirection != "right":
    #         tank3.currentView = pygame.transform.rotate(tank3.picture, 270)
    #         tank3.moveDirection = "right"
    #     if tank3.box.x < 760:
    #         tank3.move(5, 0)

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
    check_mines(tank1)
    check_mines(tank2)
    
    # Рисуем танки
    tank1.draw()
    tank2.draw()
    tank3.draw()

    tank1.writeHP("left")
    tank2.writeHP("")
    
    pygame.display.update()
    clock.tick(30)

pygame.quit()
