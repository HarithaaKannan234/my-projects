# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first (graph search).
    """
    from util import Stack

    start = problem.getStartState()
    if problem.isGoalState(start):
        return []

    frontier = Stack()
    frontier.push((start, []))
    frontier_states = {start}   # track states currently in frontier
    visited = set()

    while not frontier.isEmpty():
        state, path = frontier.pop()
        frontier_states.remove(state)  # no longer in frontier

        if state in visited:
            continue
        visited.add(state)

        if problem.isGoalState(state):
            return path

        successors = problem.getSuccessors(state)
        # Push in reverse so the first successor is expanded first
        for succ, action, cost in reversed(successors):
            if succ not in visited and succ not in frontier_states:
                frontier.push((succ, path + [action]))
                frontier_states.add(succ)

    return []


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first (graph search).
    """
    from util import Queue

    start = problem.getStartState()
    if problem.isGoalState(start):
        return []

    frontier = Queue()
    frontier.push((start, []))
    frontier_states = {start}
    visited = set()

    while not frontier.isEmpty():
        state, path = frontier.pop()
        frontier_states.remove(state)

        if state in visited:
            continue
        visited.add(state)

        if problem.isGoalState(state):
            return path

        for succ, action, cost in problem.getSuccessors(state):
            if succ not in visited and succ not in frontier_states:
                frontier.push((succ, path + [action]))
                frontier_states.add(succ)

    return []


def uniformCostSearch(problem):
    """
    Search the node of least total cost first (graph search).
    """
    from util import PriorityQueue

    start = problem.getStartState()
    if problem.isGoalState(start):
        return []

    frontier = PriorityQueue()                 # items: (state, path, g_cost)
    frontier.push((start, [], 0), 0)
    best_g = {start: 0}                        # best known cost to each state
    closed = set()

    while not frontier.isEmpty():
        state, path, g = frontier.pop()

        if state in closed:
            continue
        closed.add(state)

        if problem.isGoalState(state):
            return path

        for succ, action, stepCost in problem.getSuccessors(state):
            new_g = g + stepCost
            if succ not in closed and (succ not in best_g or new_g < best_g[succ]):
                best_g[succ] = new_g
                frontier.push((succ, path + [action], new_g), new_g)

    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """
    Search the node that has the lowest combined cost and heuristic first (graph search).
    """
    from util import PriorityQueue

    start = problem.getStartState()
    if problem.isGoalState(start):
        return []

    frontier = PriorityQueue()
    frontier.push((start, [], 0), heuristic(start, problem))
    frontier_states = {start}
    visited = set()
    best_g = {start: 0}

    while not frontier.isEmpty():
        state, path, g = frontier.pop()
        frontier_states.discard(state)

        if state in visited:
            continue
        visited.add(state)

        if problem.isGoalState(state):
            return path

        for succ, action, stepCost in problem.getSuccessors(state):
            new_g = g + stepCost
            f = new_g + heuristic(succ, problem)
            if succ not in visited and (succ not in best_g or new_g < best_g[succ]):
                best_g[succ] = new_g
                frontier.push((succ, path + [action], new_g), f)
                frontier_states.add(succ)

    return []




#####################################################
# EXTENSIONS TO BASE PROJECT
#####################################################

# Extension Q1e
def iterativeDeepeningSearch(problem):
    """
    Iterative Deepening Tree Search (AIMA Fig. 3.12).
    - Tree search (no explored set).
    - Runs Depth-Limited Search (DLS) with depth bound d = 0,1,2,...
    - DLS returns: solution | 'cutoff' | None
    """
    start = problem.getStartState()
    if problem.isGoalState(start):
        return []

    def dls(state, limit):
        """
        Depth-Limited Search.
        Args:
            state: current node (problem state)
            limit: remaining depth allowed (int)
        Returns:
            list[str] | 'cutoff' | None
        """
        # Goal test before expanding children
        if problem.isGoalState(state):
            return []

        # Depth bound reached
        if limit == 0:
            return 'cutoff'

        cutoff_occurred = False
        for successor, action, stepCost in problem.getSuccessors(state):
            result = dls(successor, limit - 1)
            if result == 'cutoff':
                cutoff_occurred = True
            elif result is not None:
                # prepend this action to the returned plan
                return [action] + result

        return 'cutoff' if cutoff_occurred else None

    # Increase depth until solution found
    depth = 0
    while True:
        result = dls(start, depth)
        if result != 'cutoff':
            # If None: failure (e.g., no goal reachable); return empty list per project conventions
            return result if result is not None else []
        depth += 1

def ids(problem):
    """Alias so you can run: -a fn=ids"""
    return iterativeDeepeningSearch(problem)




#####################################################
# Abbreviations
#####################################################
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
ids = iterativeDeepeningSearch
