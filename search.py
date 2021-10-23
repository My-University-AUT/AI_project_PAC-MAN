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

    # walls = problem.walls
    start_state = problem.getStartState()
    goal_state = None
    visited = set()  # explored nodes
    from util import Stack
    fringe = Stack()  # stack
    fringe.push(start_state)

    storage = dict()

    while not fringe.isEmpty():
        element = fringe.pop()

        if element in visited:
            continue
        visited.add(element)

        if problem.isGoalState(element):
            goal_state = element
            print('goal found')
            break

        successors = problem.getSuccessors(element)
        for successor in successors:
            node = successor[0]
            direction = successor[1]
            if(node not in visited):
                fringe.push(node)
                storage[node] = [element, direction]

    goal_path = []
    curr_node = goal_state
    while True:
        # node that we use to go to the curr_node,
        # means: node----->curr_node
        node = storage[curr_node]

        # 1th element contains the direction
        goal_path.append(node[1])

        # update current node
        curr_node = node[0]

        # reach the start state
        if(node[0] == start_state):
            break

    print('steps length: ', len(goal_path))

    # import time
    # time.sleep(100)

    # reverse the path by slicing
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

    start_state = problem.getStartState()
    goal_state = None
    visited = set()  # explored nodes
    visited.add(start_state)
    from util import Queue
    fringe = Queue()  # Queue
    fringe.push(start_state)

    storage = dict()

    while not fringe.isEmpty():
        element = fringe.pop()

        if problem.isGoalState(element):
            goal_state = element
            print('goal found')
            break
        successors = problem.getSuccessors(element)
        for successor in successors:
            node = successor[0]
            direction = successor[1]
            if(node not in visited):
                fringe.push(node)
                storage[node] = [element, direction]
                visited.add(node)

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


def uniformCostSearch(problem):
    start_state = problem.getStartState()
    goal_state = None

    visited = set()  # explored nodes
    # visited.add(start_state)

    from util import PriorityQueue
    fringe = PriorityQueue()  # Queue
    # cost for starting node to reach to start is zero :))
    fringe.push(start_state, 0)

    storage = dict()
    print('------------------start ucs----------------------')
    while not fringe.isEmpty():
        priority, element = fringe.pop()
        print('poped element: ', element, priority)
        if problem.isGoalState(element):
            goal_state = element
            print('goal found')
            break

        visited.add(element)

        successors = problem.getSuccessors(element)
        
        for successor in successors:
            node = successor[0]
            direction = successor[1]

            # we should add comulative costs as priority
            # TODO: how sould i get comulative cost from starting node to this node(successor[0])
            cost = successor[2]
            # print(node, priority+cost)
            if(node not in visited):
                updated = fringe.update(node, priority+cost)

                # در اینجا چک کنیم که اگر هزینه ی نودی که قرار است به تابع اپدیت داده شود بیشتر از هزینه ی قبلی بود، 
                # آنگاه نود جدید را به استوریج اضافه نکنیم
                if updated:
                    storage[node] = [element, direction]
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
    print('=======================end testing----------------------------')
    print('steps length: ', len(goal_path))

    print('cost of path: ', problem.getCostOfActions(goal_path[::-1]))

    # import time
    # time.sleep(100)

    # reverse the path by slicing
    return goal_path[::-1]


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
