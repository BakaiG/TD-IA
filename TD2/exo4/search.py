"""Cost-based search algorithms for the Pokémon environment."""

from __future__ import annotations

import heapq
import random
from collections import deque
from itertools import count
from math import inf

from pokemon_game import (
    GameMap,
    State,
    movement_cost,
    successors,
)


def reconstruct_path(
    parents: dict[State, State | None],
    goal: State,
) -> list[State]:
    """Reconstruct a path from a parent dictionary."""
    path: list[State] = []
    current: State | None = goal

    while current is not None:
        path.append(current)
        current = parents[current]

    path.reverse()
    return path


def path_cost(
    game_map: GameMap,
    path: list[State],
) -> int:
    """Return the total cost of a path."""
    return sum(
        movement_cost(game_map, state)
        for state in path[1:]
    )


def manhattan_distance(
    state: State,
    goal: State,
) -> int:
    """Return the Manhattan distance between two states."""
    return (
        abs(state[0] - goal[0])
        + abs(state[1] - goal[1])
    )


def generate_random_path(
    game_map: GameMap,
    start: State,
    goal: State,
    seed: int | None = None,
) -> list[State]:
    """Generate a random valid path from start to goal.

    This function is provided only to demonstrate the visualization.
    It is not guaranteed to return a minimum-cost or shortest path.

    The function performs a randomized depth-first exploration: the valid
    successor states are shuffled before being added to the frontier.

    Parameters
    ----------
    game_map : GameMap
        Weighted Pokémon map.
    start : State
        Initial trainer position.
    goal : State
        Pokémon Center position.
    seed : int or None, default=None
        Random seed used to make the result reproducible.

    Returns
    -------
    list[State]
        A valid path beginning at ``start`` and ending at ``goal``.

    Raises
    ------
    RuntimeError
        If no path exists between the start and the goal.
    """
    rng = random.Random(seed)

    frontier = [start]

    parents: dict[State, State | None] = {
        start: None,
    }

    while frontier:
        current = frontier.pop()

        if current == goal:
            return reconstruct_path(parents, goal)

        next_states = successors(game_map, current)
        rng.shuffle(next_states)

        for next_state in next_states:
            if next_state in parents:
                continue

            parents[next_state] = current
            frontier.append(next_state)

    raise RuntimeError(
        "No path exists between the start and the goal."
    )

def dijkstra(
    game_map: GameMap,
    start: State,
    goal: State,
) -> tuple[list[State], int]:
    """Return a minimum-cost path using Dijkstra's algorithm.
    From Wikipedia's pseudocode (with heap queues as it was already imported)

    Returns
    -------
    path : list[State]
        Minimum-cost path from start to goal.
    considered_states : int
        Number of states removed from the priority queue.
    """
    considered_states=0
    Q = []
    dist = {start:0}
    prev = {}
    heapq.heappush(Q,(0,start))

    n = len(game_map)
    m = len(game_map[0])
    available_states:list[State] = [(i,j) for i in range(n) for j in range(m)]
    for s in available_states:
      if s != start:
        prev[s]=None
        dist[s]=inf
    while Q:
      u = heapq.heappop(Q)[1]
      for v in successors(game_map,u):
        considered_states+=1
        alt:int = dist[u] + movement_cost(game_map,v)
        if alt < dist[v]:
          prev[v] = u
          dist[v] = alt
          heapq.heappush(Q,(alt,v))
    path = deque()
    if goal==start:return ([start],considered_states) #untested
    if prev[goal]:
      while goal!=start:
        path.appendleft(goal)
        goal = prev[goal]
    path.appendleft(start)
    return (list(path),considered_states)


def a_star(
    game_map: GameMap,
    start: State,
    goal: State,
) -> tuple[list[State], int]:
    """Return a minimum-cost path using A* search.
    From pseudocode in Reinforcement Learning session 2 pdf

    The Manhattan distance is used as the heuristic.

    Returns
    -------
    path : list[State]
        Minimum-cost path from start to goal.
    considered_states : int
        Number of states removed from the priority queue.
    """
    s_open = {start} #States
    closed = {} #(point,f_cost)
    best_path_so_far:dict[State,list[State]] = {start:[start]}
    considered_states = 0

    while s_open:
      print(f"s_open vaut {s_open}")
      node:State = min([[path_cost(game_map,best_path_so_far[s]) + manhattan_distance(s,goal),s] for s in s_open ])[1]
      # Prend l'état dont le f(n) est le plus petit

      if node == goal: return (best_path_so_far[node][:-1],considered_states)
      s_open.remove(node)
      if node not in closed:
        closed[node]=inf
      for s in successors(game_map,node):
        considered_states+=1
        best_path_with_s = best_path_so_far[node]
        best_path_with_s.append(s)
        g_n = path_cost(game_map,best_path_with_s)
        h_n = manhattan_distance(s,goal)
        f_n = g_n + h_n
        if s not in closed or f_n <closed[s]:
          print(f"À partir de {node} qui vaut {closed[node]}, on trouve {f_n}")
          closed[s]=f_n
          best_path_so_far[s]=best_path_with_s
          s_open.add(s)
    return (best_path_so_far[goal],considered_states)
