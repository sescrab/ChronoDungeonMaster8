# BaseMap.py

from ChronoDungeonMaster8 import GameStatus
import GameObjects

"""
Тут будет заранее заданная карта, которую в будущем можно заменить генерацией
"""

MAP_WIDTH = 10
MAP_HEIGHT = 10


def create_base_map(seed) -> GameStatus:
    initial_game_state = GameStatus()
    initial_game_state.rand_seed = seed

    # Инициализация сетки
    initial_game_state.game_map = []
    for h in range(MAP_HEIGHT):
        row = []
        for w in range(MAP_WIDTH):
            cell = [GameObjects.EmptyCell(w, h)]
            row.append(cell)
        initial_game_state.game_map.append(row)

    # Создание героя
    player = GameObjects.Hero(1, 1)
    initial_game_state.hero = player
    initial_game_state.add_object(player)

    # Стены
    for i in range(MAP_WIDTH):
        initial_game_state.add_object(GameObjects.Wall(i, 0))
        initial_game_state.add_object(GameObjects.Wall(i, MAP_HEIGHT-1))
    for i in range(1, MAP_HEIGHT-1):
        initial_game_state.add_object(GameObjects.Wall(0, i))
        initial_game_state.add_object(GameObjects.Wall(MAP_WIDTH-1, i))

    # Монстры
    initial_game_state.add_object(GameObjects.Zombie(6, 6))
    initial_game_state.add_object(GameObjects.Spider(3, 7))
    
    return initial_game_state
