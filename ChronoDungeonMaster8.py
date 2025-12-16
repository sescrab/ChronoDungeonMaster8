import TrackableRandom
import BaseMap
import GameObjects
class GameStatus:
    def __init__(self):
        self.game_map = []
        self.acting_objects = []
        self.rand_seed = 123
        self.hero = None


    def check_for_passability(self, x, y) -> bool:
        for obj in self.game_map[y][x]:
            if obj.isBlocking:
                return False
        return True
    def add_object(self, obj: GameObjects.MapObject) -> bool:
        if obj.isBlocking and self.check_for_passability(obj.x, obj.y):
            return False
        self.game_map[obj.y][obj.x].append(obj)
        if isinstance(obj, GameObjects.ActingObject):
            self.acting_objects.append(obj)
        return True
    def remove_object(self, obj: GameObjects.MapObject) -> bool:
        for cell_object in self.game_map[obj.y][obj.x]:
            if cell_object == obj:
                if isinstance(obj, GameObjects.ActingObject):
                    self.acting_objects.remove(obj)
                self.game_map[obj.y][obj.x].remove(obj)
                return True
        return False


class MapManager:
    def __init__(self):
        self.game_turn_statuses: list[GameStatus] = []

    def add_object(self, obj: GameObjects.MapObject):
        return self.game_turn_statuses[-1].add_object(obj)

    def remove_object(self, obj: GameObjects.MapObject):
        return self.game_turn_statuses[-1].remove_object(obj)

class ChronoStatus:
    def __init__(self):
        self.cur_mana = 123

def player_interaction():
    pass

def make_turn():
    pass

random_generator = TrackableRandom.TrackableRandom(123)
map_manager = MapManager()



def start_game():
    seed = 0.123
    random_generator.seed(seed)
    start_status = BaseMap.create_base_map(seed)
    map_manager.game_turn_statuses.append(start_status)

    print("Game started")
    game_loop()

def game_loop():
    while map_manager.game_turn_statuses[-1].hero.cur_hp > 0:
        player_interaction()
        make_turn()


if __name__ == '__main__':
    start_game()
