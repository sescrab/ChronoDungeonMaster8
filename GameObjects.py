# GameObjects.py

import math

# в конце файла определены
PLAYER_OBJECTS = None
ENEMY_OBJECTS  = None
TRAP_OBJECTS   = None
OTHER_OBJECTS  = None
EMPTY_OBJECTS  = None

ALL_NONEMPTY_OBJECTS = None
ALL_OBJECTS = None


"""
Тут всевозможные объекты, которые могут быть на игровом поле.
"""
class MapObject:
    """
    is_blocking - в одной клетке может быть сколько угодно объектов, где этот параметр = False,
    но не более одного, у которого True
    """
    def __init__(self, x, y, is_blocking = True, char='?'):
        self.x = x
        self.y = y
        self.isBlocking = is_blocking
        self.char = char  # Символ для консоли

    def get_position(self):
        return self.x, self.y

    def move_to(self, x, y):
        self.x = x
        self.y = y


class ActingObject:
    """
    Интерфейс для объектов, которые могут выполнять какие-то действия самостоятельно.
    Сюда включаются как и монстры с возможным "интеллектом", так и ловушки, которые просто срабатывают при нажатии (и прочее)
    """
    def do_next_turn(self):
        pass

    def try_move(self, dx, dy, game_state):
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Проверка границ и блокировки
        if not (0 <= new_y < len(game_state.game_map) and 0 <= new_x < len(game_state.game_map[0])):
            return

        # Ищем, есть ли там кто-то, кого можно ударить
        target = None
        for obj in game_state.game_map[new_y][new_x]:
            if isinstance(obj, ActingObject) and obj != self:
                # Монстры бьют героев, Герои бьют монстров
                if isinstance(self, (Zombie, Spider, Dragon)) and isinstance(obj, (Hero, Phantom)):
                    target = obj
                elif isinstance(self, (Hero, Phantom)) and isinstance(obj, (Zombie, Spider, Dragon)):
                    target = obj
                elif isinstance(self, Hero) and self.is_controlled_by_player is False and isinstance(obj, (Zombie, Spider, Dragon)):
                    target = obj # ИИ-герой бьет монстров

        # двигаемся и затем атакуем
        if game_state.check_for_passability(new_x, new_y):
            game_state.move_object(self, new_x, new_y)
        if target:
            self.attack(target)

    def attack(self, target):
        dmg = getattr(self, 'cur_dmg', 0)
        target.cur_hp -= dmg
        # Сообщения об атаке можно выводить в лог, если добавить менеджер логов

    def find_nearest_enemy(self, game_state):
        # Простой поиск ближайшего врага
        targets = []
        is_monster = isinstance(self, (Zombie, Spider, Dragon))
        
        for obj in game_state.acting_objects:
            if obj == self: continue
            
            is_hero_side = isinstance(obj, (Hero, Phantom))
            
            if is_monster and is_hero_side:
                targets.append(obj)
            elif not is_monster and isinstance(obj, (Zombie, Spider, Dragon)):
                targets.append(obj)

        if not targets:
            return None

        # Сортируем по расстоянию
        targets.sort(key=lambda t: math.dist((self.x, self.y), (t.x, t.y)))
        return targets[0]

    def move_towards(self, target, game_state):
        if not target: return
        dx = 0
        dy = 0
        if target.x > self.x: dx = 1
        elif target.x < self.x: dx = -1
        
        if target.y > self.y: dy = 1
        elif target.y < self.y: dy = -1
        
        # Примитивный поиск пути: сначала пробуем по одной оси, если занято - не идем (можно улучшить)
        # Для простоты: пробуем пойти по X, если 0, то по Y
        if dx != 0 and dy != 0:
            # Выбираем случайно или приоритет (пусть будет X)
            self.try_move(dx, 0, game_state)
        elif dx != 0:
            self.try_move(dx, 0, game_state)
        elif dy != 0:
            self.try_move(0, dy, game_state)

class Hero(MapObject, ActingObject):
    def __init__(self, x, y):
        super().__init__(x, y, char='H')
        self.is_controlled_by_player = True # Если False, управляется ИИ (бывший игрок)
        self.cur_hp = 100
        self.cur_dmg = 15

    def do_next_turn(self, game_state):
        if not self.is_controlled_by_player:
            # Логика "прошлого меня": атаковать врагов
            target = self.find_nearest_enemy(game_state)
            self.move_towards(target, game_state)

class Phantom(MapObject, ActingObject):
    def __init__(self, x, y):
        super().__init__(x, y, char='P')
        self.is_controlled_by_player = True

        # Фантом хилее и слабее
        self.cur_hp = 50
        self.cur_dmg = 15

    def do_next_turn(self, game_state):
        pass # Управляется игроком напрямую в input loop

class Zombie(MapObject, ActingObject):
    def __init__(self, x, y):
        super().__init__(x, y, char='Z')
        self.cur_hp = 80
        self.cur_dmg = 8

    def do_next_turn(self, game_state):
        target = self.find_nearest_enemy(game_state)
        self.move_towards(target, game_state)

class Spider(MapObject, ActingObject):
    def __init__(self, x, y):
        super().__init__(x, y, char='S')
        self.cur_hp = 50
        self.cur_dmg = 5

    def do_next_turn(self, game_state):
        pass # Паук мирнич ^_^

class Dragon(MapObject, ActingObject):
    def __init__(self, x, y):
        super().__init__(x, y, char='D')
        self.cur_hp = 500
        self.cur_dmg = 25

    def do_next_turn(self, game_state):
        pass # Дракон ленивый: парит на месте

class EmptyCell(MapObject):
    def __init__(self, x, y, is_blocking=False):
        super().__init__(x, y, is_blocking, char='.')

class Wall(MapObject):
    def __init__(self, x, y):
        super().__init__(x, y, char='#')

class SpikeTrap(MapObject, ActingObject):
    def __init__(self, x, y, is_blocking=False):
        super().__init__(x, y, is_blocking, char='^')
    def do_next_turn(self, game_state):
        pass # Логика срабатывания при наступании

class ItemOnGround(MapObject):
    def __init__(self, x, y, item):
        super().__init__(x, y, False, char='!')
        self.item = item

class Item:
    def __init__(self):
        self.name = "Базовый предмет (шаблон, делает ничего)"

    def use(self, user, target):
        return False

    def on_take(self, user):
        return False

    def on_drop(self, user):
        return False

class SmallHealingPotion(Item):
    def __init__(self):
        super().__init__()
        self.name = "Малое зелье лечения"
        self.healing_amount = 50

    def use(self, user, target):
        user.cur_hp += self.healing_amount
        return True

class SmallAmuletOfDamage(Item):
    def __init__(self):
        super().__init__()
        self.name = "Малый амулет урона"
        self.bonus_dmg = 5

    def on_take(self, user):
        user.cur_dmg += self.bonus_dmg
        return True

    def on_drop(self, user):
        user.cur_dmg -= self.bonus_dmg
        return True



PLAYER_OBJECTS = {Hero, Phantom}
ENEMY_OBJECTS  = {Zombie, Spider, Dragon}
TRAP_OBJECTS   = {SpikeTrap}
OTHER_OBJECTS  = {Wall}
EMPTY_OBJECTS  = {EmptyCell, ItemOnGround}

ALL_NONEMPTY_OBJECTS = PLAYER_OBJECTS | ENEMY_OBJECTS | TRAP_OBJECTS | OTHER_OBJECTS
ALL_OBJECTS = ALL_NONEMPTY_OBJECTS | EMPTY_OBJECTS
