import algorithms
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
  dic_minmax_alphabeta = {
    "Minimax":{},
    "alphabeta":{}
  }
  for prof in [1,2,3,4,5]:
    dic_minmax_alphabeta["minmax"][f"{prof}"]=benchmark(create_board(),algorithms.minimax,depth=prof)
    dic_minmax_alphabeta["alphabeta"][f"{prof}"]=benchmark(create_board(),algorithms.alphabeta,depth=prof)
  dic_MCTS={}
  for N in (100,500,1000,2000):
    dic_MCTS[N]=benchmark(create_board(),algorithms.mcts,seed=3)
