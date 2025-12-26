# TrackableRandom.py

import random

"""
Тут класс, который позволяет отслеживать текущий сид для рандома.
Это нужно хотя бы для возможности задавать сид на начало хода, 
чтобы при переносе в прошлое рандом не менялся
"""

class TrackableRandom:
    def __init__(self, seed_val):
        self._rng = random.Random(seed_val)  # Создаем изолированный генератор!
        # self._initial_seed = seed_val # вдруг понадобится позже?
        self._current_seed = seed_val
    
    def seed(self, seed_val):
        self._current_seed = seed_val
        self._rng.seed(seed_val)  # Работаем с локальным генератором
        return seed_val
    
    def random(self):
        return self._rng.random()  # Используем локальный генератор
    
    def randint(self, a, b):
        return self._rng.randint(a, b)  # Используем локальный генератор
    
    def get_current_seed(self):
        return self._current_seed
