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
    print("----------------SATRT_TESTttt-----")
    print()
    # print(problem.__dict__)

    print(problem.walls)
    ws = problem.walls
    print('-------')
    print('start ',problem.startState)
    print('goal ',problem.goal)
    print(problem.visualize)
    print(problem._visited)
    print(problem._visitedlist)
    print(problem._expanded)
    print()
    print()
    print()
    print("---------TEST------------------")

    walls = problem.walls

    visited = set()
    start = problem.startState

    from util import Stack
    stack = Stack()

    stack.push(start)

    storage = dict()

    while not stack.isEmpty():
        element = stack.pop()

        if element in visited:
            continue
        visited.add(element)
        # print(f'--->{element}')
        if(element == problem.goal):
            print('goal found')
            break
        col, row = element
        if walls[col+1][row] == False and ((col+1, row) not in visited):
            stack.push(((col+1, row)))
            storage[(col+1, row)] = (col, row)
        if walls[col-1][row] == False and ((col-1, row) not in visited):
            stack.push(((col-1, row)))
            storage[(col-1, row)] = (col, row)
        if walls[col][row+1] == False and ((col, row+1) not in visited):
            stack.push(((col, row+1)))
            storage[(col, row+1)] = (col, row)
        if walls[col][row-1] == False and ((col, row-1) not in visited):
            stack.push(((col, row-1)))
            storage[(col, row-1)] = (col, row)

    from game import Directions

    s = Directions.SOUTH
    w = Directions.WEST
    e = Directions.EAST
    n = Directions.NORTH

    goal_path =[]
    curr_node = problem.goal
    goal_path.append(curr_node)
    while True:
        #node that we use to come to the curr_node,
        node = storage[curr_node]

        col,row = node
        #means column of node is greater than column of current node(curr_node), the agent should go to the west
        if  (col-1,row) == curr_node:
            goal_path.append(w)
        # if column of node is less than curr_node
        elif (col+1,row) == curr_node:
            goal_path.append(e)
        #means row of node is greater than column of current node(curr_node), the agent should go to the south
        elif (col,row-1) == curr_node:
            goal_path.append(s)
        # if row of node is less than curr_node
        elif (col,row+1) == curr_node:
            goal_path.append(n)
        
        curr_node = node
        
        # goal_path.append(node)

        #reach the start state
        if(node == start):
            break
    print('-------------')
    print(len(goal_path))
   

    # import time
    # time.sleep(100)

    #reverse the path by slicing
    return goal_path[::-1]

    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
