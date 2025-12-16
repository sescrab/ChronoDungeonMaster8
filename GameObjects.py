"""
Тут всевозможные объекты, которые могут быть на игровом поле.
"""
class MapObject:
    """
    is_blocking - в одной клетке может быть сколько угодно объектов, где этот параметр = False,
    но не более одного, у которого True
    """
    def __init__(self, x, y, is_blocking = True):
        self.x = x
        self.y = y
        self.isBlocking = is_blocking

    def get_position(self):
        return self.x, self.y

    def move_to(self, x, y):
        self.x = x
        self.y = y


class ActingObject:
    """
    Интерфейс для объектов, которые могут выполнять какие-то действия самостоятельно.
    Сюда включаются как и монстры с возможным "интеллектом", так и ловушки, которые просто срабатывают при нажатии(и пр)
    """
    def do_next_turn(self):
        pass

class Hero(MapObject, ActingObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.is_controlled_by_player = True
        self.cur_hp = 123
        self.cur_dmg = 12

    def do_next_turn(self):
        pass

class Phantom(MapObject, ActingObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.is_controlled_by_player = True
        self.cur_hp = 123
        self.cur_dmg = 12

    def do_next_turn(self):
        pass

class Zombie(MapObject, ActingObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.cur_hp = 80
        self.cur_dmg = 8

    def do_next_turn(self):
        pass

class Spider(MapObject, ActingObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.cur_hp = 50
        self.cur_dmg = 5

    def do_next_turn(self):
        pass

class Dragon(MapObject, ActingObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.cur_hp = 500
        self.cur_dmg = 25

    def do_next_turn(self):
        pass

class EmptyCell(MapObject):
    def __init__(self, x, y, is_blocking=False):
        super().__init__(x, y, is_blocking)

class Wall(MapObject):
    def __init__(self, x, y):
        super().__init__(x, y)

class SpikeTrap(MapObject, ActingObject):
    def __init__(self, x, y, is_blocking=False):
        super().__init__(x, y, is_blocking)
    def do_next_turn(self):
        pass

class ItemOnGround(MapObject):
    def __init__(self, x, y, item):
        super().__init__(x, y, False)
        self.item = item

class Item:
    def __init__(self):
        self.name = "Базовый предмет (шаблон)"
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
