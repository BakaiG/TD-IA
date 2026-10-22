import algorithms
import matplotlib.pyplot as plt
from game import (
  AI,
  HUMAN,
  create_board,
  get_valid_moves,
  get_winner,
  is_terminal,
  make_move,
)


def benchmark(board,algo,**kwargs):
  d = {}
  a = algo(board,**kwargs)
  d['move']=a['move']
  d['score']=a['score']
  d['nodes_explored']=a['nodes_explored']
  d['time']=a['time']
  return d


def benchmark_full():
  tableau=[]
  for prof in [1,2,3,4,5]:
    b=benchmark(create_board(),algorithms.minimax,depth=prof)
    tableau.append(["Minimax",f"Depth {prof}",b['move'],b['nodes_explored'],b['time']])
  for prof in [1,2,3,4,5]:
    b=benchmark(create_board(),algorithms.alphabeta,depth=prof)
    tableau.append(["Alpha-Beta",f"Depth {prof}",b['move'],b['nodes_explored'],b['time']])
  for N in (100,500,1000,2000):
    b=benchmark(create_board(),algorithms.mcts,seed=3)
    tableau.append(["Alpha-Beta",f"{N} simulations",b['move'],b['nodes_explored'],b['time']])

  return tableau

print(benchmark_full())

fig = plt.figure(figsize=(2, 1))
fig.add_subplot(1,2,1)
