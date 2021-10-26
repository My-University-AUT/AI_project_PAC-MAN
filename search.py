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
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    return custom_search(problem, nullHeuristic, 'max')


def breadthFirstSearch(problem):
    return custom_search(problem, nullHeuristic, 'min')


def uniformCostSearch(problem):
    return custom_search(problem, nullHeuristic, 'min')


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    return custom_search(problem, heuristic, 'min')
    """Search the node that has the lowest combined cost and heuristic first."""


def custom_search(problem, heuristic=nullHeuristic, heapType='min'):

    prioritySign = 1
    # heaptype shows that our priority queue should be maxheap or minheap
    # by default our priority queue use minHeap
    # if we want priority queue as a maxHaep, multiply each priority by -1
    if heapType == 'max':
        prioritySign = -1

    start_state = problem.getStartState()
    goal_state = None

    visited = set()  # explored nodes
    # visited.add(start_state)

    from util import PriorityQueue
    fringe = PriorityQueue()  # Queue

    F_value = heuristic(start_state, problem)  # at starting state: f(S) = h(S)
    fringe.push(start_state, F_value)

    g_vals = dict()  # stores all g_value of nodes

    # cost for starting node to reach to start is zero :))
    g_vals[start_state] = 0

    storage = dict()

    while not fringe.isEmpty():
        curr_node = fringe.pop()
        if problem.isGoalState(curr_node):
            goal_state = curr_node
            print('goal found')
            break

        visited.add(curr_node)

        current_node_g_value = g_vals[curr_node]

        successors = problem.getSuccessors(curr_node)
        for successor in successors:
            node = successor[0]
            
            if(node not in visited):
                direction = successor[1]
                cost_from_curr_node_to_this_node = successor[2]

                h_value = heuristic(node, problem)

                node_g_value = cost_from_curr_node_to_this_node + current_node_g_value

                # node_g_value is the real backward cost
                # h_value is the estimated forward cost
                updated = fringe.update(
                    node, prioritySign*(node_g_value+h_value))

                # if priorityQueue was updated sucessfully, then update that path(storage) and update node g_value
                if updated:
                    storage[node] = [curr_node, direction]
                    g_vals[node] = node_g_value

                # visited.add(node)
            # else:
            #     fringe.update(node, priority+cost)

    goal_path = []
    curr_node = goal_state
    while True:
        # node that we use to go to the curr_node,
        # means: node----->curr_node
        node = storage[curr_node]

        # 1th element contains the direction that we us to go to the current node
        goal_path.append(node[1])

        # update current node
        curr_node = node[0]

        # reach the start state
        if(node[0] == start_state):
            break
    print('steps length: ', len(goal_path))

    print('cost of path: ', problem.getCostOfActions(goal_path[::-1]))

    # import time
    # time.sleep(100)

    # reverse the path by slicing
    return goal_path[::-1]


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
