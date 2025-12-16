class MapObject:
    def __init__(self, x, y, isBlocking = True):
        self.x = x
        self.y = y
        self.isBlocking = isBlocking

    def get_position(self):
        return self.x, self.y

    def move_to(self, x, y):
        self.x = x
        self.y = y


class ActingObject:
    def do_next_turn(self): #В этом методе для каждого активного объекта должен содержаться его "интеллект"
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
    def __init__(self, x, y, isBlocking=False):
        super().__init__(x, y)

class Wall(MapObject):
    def __init__(self, x, y):
        super().__init__(x, y)

class SpikeTrap(MapObject, ActingObject):
    def __init__(self, x, y, isBlocking=False):
        super().__init__(x, y)
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
