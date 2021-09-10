"""
- use move ordering!
- Iterative depth -> dynamic depth depending on time left
- store 2 killer moves
- transition table TT

- 2D container to keep track of the good moves (history heuristic)


"""

from typing import Dict
from stupid_engine.cannon.ai.ai import BaseAI


# table: history_table[player white|dark][x][y]
history_table = [[[None for _ in range(10)] for _ in range(10)] for player in range(2)]

class AlphaBeta(BaseAI):
    def play_turn(self, state: Dict) -> bool:
        pass
