# ChronoDungeonMaster8.py

import copy
import sys # sus

import TrackableRandom
import BaseMap
import GameObjects
from Renderer import ConsoleRenderer

renderer = ConsoleRenderer() # один, пересоздавать не нужно

map_manager = None
random_generator = None


"""
В этом модуле хранится в целом состояние игры (карта, запас маны и пр), 
а также точка входа в игру.
"""

class GameStatus:
    def __init__(self):
        self.game_map = [] # 2D list of lists of objects
        self.acting_objects = []
        self.rand_seed = 123
        self.hero = None # Ссылка на текущего управляемого персонажа (Hero или Phantom)
        self.cur_mana = 100
        self.turn_counter = 0

    def count_nonempty_in_cell(self, x, y):
        return sum([1 for obj in self.game_map[y][x] if type(obj) not in GameObjects.EMPTY_OBJECTS])

    """
    Возвращает возможность помещения объекта в указанную клетку
    Если можно (True), то указывает сколько ещё объектов в клетке
    Если нельзя (False), то 0
    """
    def check_for_passability(self, x, y) -> (bool, int):
        # Проверка границ: вне поля — бан
        if not (0 <= y < len(self.game_map) and 0 <= x < len(self.game_map[0])):
            return False, 0

        # Проверка есть ли в клетке "жирный" (bold) объект, который не терпит соседства с другими на одной клетке
        # "Жирный" (bold) объект в клетке — бан
        for obj in self.game_map[y][x]:
            if obj.isBlocking:
                return False, 0

        # объект добавить можно
        return True, self.count_nonempty_in_cell(x, y)

    """
    Пытаемся добавить объект на поле.
    return: True/False
    """
    def add_object(self, obj: GameObjects.MapObject) -> bool:
        # Проверить границы
        if not (0 <= obj.y < len(self.game_map) and 0 <= obj.x < len(self.game_map[0])):
            return False

        # если в клетке что-то мешает (flag)
        # либо 
        # текущ объект "жирный" и ему что-то мешает
        flag, cnt = self.check_for_passability(obj.x, obj.y)

        if (not flag) or (obj.isBlocking and cnt > 0):
            return False

        self.game_map[obj.y][obj.x].append(obj)
        if isinstance(obj, GameObjects.ActingObject):
            self.acting_objects.append(obj)
        return True


    def remove_object(self, obj: GameObjects.MapObject) -> bool:
        if 0 <= obj.y < len(self.game_map) and 0 <= obj.x < len(self.game_map[0]):
            cell = self.game_map[obj.y][obj.x]
            if obj in cell:
                cell.remove(obj)
                # Удаляем из списка действующих, если он там есть
                if isinstance(obj, GameObjects.ActingObject) and obj in self.acting_objects:
                    self.acting_objects.remove(obj)
                return True
        return False

    def move_object(self, obj: GameObjects.MapObject, new_x, new_y) -> bool:
        # 1. Проверяем валидность новой позиции
        flag, _ = self.check_for_passability(new_x, new_y)
        if not flag:
            return False

        # 2. Удаляем из старой клетки (но НЕ из списка acting_objects)
        if 0 <= obj.y < len(self.game_map) and 0 <= obj.x < len(self.game_map[0]):
            if obj in self.game_map[obj.y][obj.x]:
                self.game_map[obj.y][obj.x].remove(obj)
            else:
                return False # Объект потерян?
        
        # 3. Обновляем координаты
        obj.x = new_x
        obj.y = new_y

        # 4. Кладем в новую клетку
        self.game_map[new_y][new_x].append(obj)
        return True

    def clone(self):
        # Глубокое копирование ВСЕГО состояния для истории
        # ВАЖНО: deepcopy корректно скопирует все объекты и ссылки внутри game_map
        return copy.deepcopy(self)

class MapManager:
    def __init__(self):
        self.history: list[GameStatus] = [] # История состояний

    def get_current(self) -> GameStatus:
        return self.history[-1]

    def save_turn(self):
        #TODO: состояние рандома откатить до сида того хода куда идём
        #      чтобы уровень также проходил

        # Сохраняем копию текущего состояния в историю
        current = self.get_current()
        # Важно: сохраняем состояние генератора случайных чисел, если хотим детерминизма
        # Но для MVP пока оставим просто копию данных
        self.history.append(current.clone())


# --- Новая функция для реализации механики времени ---
def perform_time_travel(current_state):
    global map_manager
    
    # 1. Спрашиваем игрока
    try:
        turns_back = int(input(f"Travel back (max {len(map_manager.history)-1} turns): "))
    except ValueError:
        print("Invalid number.")
        return False

    if turns_back <= 0 or turns_back >= len(map_manager.history):
        print("Cannot travel that far.")
        return False

    mana_cost = 5 + 2*turns_back # Пример формулы
    if current_state.cur_mana < mana_cost:
        print(f"Not enough mana! Need {mana_cost}, have {current_state.cur_mana}")
        return False

    # 2. Запоминаем текущую позицию героя (чтобы там появился Фантом)
    phantom_x, phantom_y = current_state.hero.x, current_state.hero.y
    current_mana_pool = current_state.cur_mana - mana_cost

    # 3. Загружаем прошлое
    # Отрезаем историю: всё, что было "после" момента прыжка, стирается (или создается ветка)
    target_index = len(map_manager.history) - 1 - turns_back
    # Восстанавливаем состояние
    loaded_state = map_manager.history[target_index].clone()
    
    # Обрезаем историю до этого момента
    map_manager.history = map_manager.history[:target_index+1]
    
    # 4. Настраиваем "Старого героя" (теперь он бот)
    old_hero = loaded_state.hero
    if old_hero:
        old_hero.is_controlled_by_player = False
        # Визуально помечаем старого героя иначе, если хотим (опционально)
        old_hero.char = 'h' 

    # 5. Создаем Фантома (нового игрока)
    phantom = GameObjects.Phantom(phantom_x, phantom_y)
    
    # Проверка: не занята ли клетка в прошлом?
    passable, _ = loaded_state.check_for_passability(phantom_x, phantom_y)
    if not passable:
        # Если занято, пробуем сдвинуть (простой хак для MVP)
        print("Target timeline location blocked! Shifting slightly...")
        phantom.x += 1 
    
    if loaded_state.add_object(phantom):
        loaded_state.hero = phantom # Передаем управление фантому
        loaded_state.cur_mana = current_mana_pool # Переносим ману (общая для всех времён)
        
        # Обновляем текущее состояние в менеджере
        map_manager.history.append(loaded_state)
 
        print(f"*** TIME TRAVEL SUCCESSFUL: -{turns_back} turns ***")
        return True
    else:
        print("Critical Paradox: Cannot spawn phantom anywhere!")
        return False

def player_interaction():
    current_state = map_manager.get_current()
    player = current_state.hero
    
    if not player or player.cur_hp <= 0:
        return False # Game Over handled in loop

    action_done = False
    while not action_done:
        cmd = input("Action: ").lower().strip()
        
        dx, dy = 0, 0
        if cmd == 'w': dy = -1
        elif cmd == 's': dy = 1
        elif cmd == 'a': dx = -1
        elif cmd == 'd': dx = 1
        elif cmd in ['wait', '']: 
            action_done = True
        elif cmd == 't':
            if perform_time_travel(current_state):
                # Если переместились во времени, текущий ход "обнуляется" 
                # и мы оказываемся в начале хода в прошлом.
                # Возвращаем False, чтобы не вызывать make_turn сразу же в старой реальности,
                # а дать игроку осмотреться (или True, если прыжок тратит ход).
                # Давайте считать, что прыжок перезапускает цикл ввода для новой реальности.
                return "TIME_JUMP" 
            else:
                continue # Travel failed/cancelled
        elif cmd in ["cls", "clear", "exit"]:
            sys.exit()
        else:
            print("Unknown command.")
            continue
        
        if dx != 0 or dy != 0:
            player.try_move(dx, dy, current_state)
            action_done = True
            
    return True

def make_turn():
    state = map_manager.get_current()
    state.turn_counter += 1
    
    # Очистка мертвых
    dead_objects = [obj for obj in state.acting_objects if hasattr(obj, 'cur_hp') and obj.cur_hp <= 0]
    for obj in dead_objects:
        state.remove_object(obj)
        if obj == state.hero:
            print("HERO DIED") # Game loop catch checking logic

    # Ход ИИ и других объектов
    # Делаем копию списка, так как внутри loop объекты могут удаляться/добавляться (теоретически)
    # Но НЕ копируем сами объекты!
    actors = list(state.acting_objects)
    actors.sort(key=lambda o: isinstance(o, GameObjects.Hero)) # Герои/Фантомы могут иметь приоритет или наоборот

    for obj in actors:
        # Проверка, жив ли еще объект (могли убить предыдущим в этом же цикле)
        if obj.cur_hp <= 0: continue
        if obj not in state.acting_objects: continue # Был удален

        # Игрок (Phantom или Hero) пропускает make_turn, т.к. сходил в player_interaction
        if isinstance(obj, (GameObjects.Hero, GameObjects.Phantom)) and obj.is_controlled_by_player:
            continue
            
        obj.do_next_turn(state)

    # После всех действий сохраняем это состояние как новую страницу истории
    map_manager.save_turn()

def start_game(seed = 42):
    global map_manager, random_generator

    map_manager = MapManager()
    random_generator = TrackableRandom.TrackableRandom(seed)

    start_state = BaseMap.create_base_map(seed)
    map_manager.history.append(start_state)

    print("Game started")
    game_loop()


def game_loop():
    """
    Здесь должен быть цикл, внутри которого будет обработка одного хода,
    т.е. начинаем с общения с игроком, когда игрок завершает ход - обрабатываем всю карту, и начинаем снова.
    """
    while True:
        current_state = map_manager.get_current()
        
        # Проверка условий поражения
        if not current_state.hero or current_state.hero.cur_hp <= 0:
            renderer.render(current_state)
            print("=== GAME OVER ===")
            break

        renderer.render(current_state)

        # Обработка ввода
        result = player_interaction()

        if result == "TIME_JUMP":
            # Если прыгнули во времени, не делаем ход мира сразу, 
            # а перерисовываем карту прошлого и ждем ввода
            continue
        elif result is True:
            # Игрок походил, теперь ходит мир
            make_turn()
            
            #TODO: обдумать восстановление HP, маны и прочего
            # Восстановление маны (опционально)
            current_state.cur_mana = min(100, current_state.cur_mana + 1)


if __name__ == '__main__':
    start_game()
