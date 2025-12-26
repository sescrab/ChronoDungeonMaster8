# Renderer.py

import os 

import GameObjects

class Renderer:
    def render(self, game_status):
        raise NotImplementedError

class ConsoleRenderer(Renderer):
    def clear_screen(self):
        CLEAR_COMMAND = 'cls' if os.name == 'nt' else 'clear'
        os.system(CLEAR_COMMAND)

    def render(self, game_status):
        self.clear_screen()
        print(f"Turn: {game_status.turn_counter} | Mana: {game_status.cur_mana}")
        print(f"Hero HP: {game_status.hero.cur_hp if game_status.hero else 'DEAD'}")
        
        # Определяем размер карты (предполагаем 10x10 как в BaseMap)
        height = len(game_status.game_map)
        width = len(game_status.game_map[0])

        board_str = ""
        for y in range(height):
            line = ""
            for x in range(width):
                cell_objs = game_status.game_map[y][x]
                # Приоритет отрисовки: ActingObject > Wall > Item > Empty
                symbol = '.'
                top_priority = -1
                
                for obj in cell_objs:
                    current_prio = 0
                    if isinstance(obj, GameObjects.EmptyCell): current_prio = 0
                    elif isinstance(obj, GameObjects.ItemOnGround): current_prio = 1
                    elif isinstance(obj, GameObjects.Wall): current_prio = 2
                    elif isinstance(obj, GameObjects.ActingObject): 
                        current_prio = 3
                        # Если в клетке несколько живых, показываем того, кто "важнее" (например Игрок)
                        if isinstance(obj, GameObjects.Phantom): current_prio = 5
                        elif isinstance(obj, GameObjects.Hero): current_prio = 4
                    
                    if current_prio > top_priority:
                        top_priority = current_prio
                        symbol = obj.char
                
                line += f" {symbol} "
            board_str += line + "\n"
        print(board_str)
        print("Controls: 'wasd' - Move/Attack | 'wait' or ''(just Enter) - Wait/Attack | 't' - Time Travel")
