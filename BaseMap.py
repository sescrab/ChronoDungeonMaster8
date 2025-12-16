from ChronoDungeonMaster8 import GameStatus
import GameObjects

MAP_WIDTH = 10
MAP_HEIGHT = 10


def create_base_map(seed) -> GameStatus:
    initial_game_status = GameStatus()
    initial_game_status.rand_seed = seed

    initial_game_status.game_map = []
    for h in range(MAP_HEIGHT):
        row = []
        for w in range(MAP_WIDTH):
            cell = [GameObjects.EmptyCell(w, h)]
            row.append(cell)
        initial_game_status.game_map.append(row)

    player = GameObjects.Hero(1, 1)
    initial_game_status.add_object(player)
    initial_game_status.hero = player

    for i in range(MAP_WIDTH):
        initial_game_status.add_object(GameObjects.Wall(i, 0))
        initial_game_status.add_object(GameObjects.Wall(i, MAP_HEIGHT-1))
    for i in range(1, MAP_HEIGHT-1):
        initial_game_status.add_object(GameObjects.Wall(0, i))
        initial_game_status.add_object(GameObjects.Wall(MAP_WIDTH-1, i))

    initial_game_status.add_object(GameObjects.Zombie(6, 6))

    return initial_game_status