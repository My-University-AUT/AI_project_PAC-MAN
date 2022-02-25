# multiAgents.py
# --------------
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


from sys import maxsize
from util import manhattanDistance
from game import Directions
import random
import util

from game import Agent


class ReflexAgent(Agent):
	"""
	A reflex agent chooses an action at each choice point by examining
	its alternatives via a state evaluation function.
	The code below is provided as a guide.  You are welcome to change
	it in any way you see fit, so long as you don't touch our method
	headers.
	"""

	def getAction(self, gameState):
		"""
		You do not need to change this method, but you're welcome to.
		getAction chooses among the best options according to the evaluation function.
		Just like in the previous project, getAction takes a GameState and returns
		some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
		"""
		# Collect legal moves and successor states
		legalMoves = gameState.getLegalActions()

		# Choose one of the best actions
		scores = [self.evaluationFunction(
			gameState, action) for action in legalMoves]
		bestScore = max(scores)
		bestIndices = [index for index in range(
			len(scores)) if scores[index] == bestScore]
		# Pick randomly among the best
		chosenIndex = random.choice(bestIndices)

		"Add more of your code here if you want to"

		return legalMoves[chosenIndex]

	def evaluationFunction(self, currentGameState, action):
		"""
		Design a better evaluation function here.
		The evaluation function takes in the current and proposed successor
		GameStates (pacman.py) and returns a number, where higher numbers are better.
		The code below extracts some useful information from the state, like the
		remaining food (newFood) and Pacman position after moving (newPos).
		newScaredTimes holds the number of moves that each ghost will remain
		scared because of Pacman having eaten a power pellet.
		Print out these variables to see what you're getting, then combine them
		to create a masterful evaluation function.
		"""
		# Useful information you can extract from a GameState (pacman.py)
		successorGameState = currentGameState.generatePacmanSuccessor(action)
		pacman_newPos = successorGameState.getPacmanPosition()
		newFood = successorGameState.getFood()
		newGhostStates = successorGameState.getGhostStates()
		newScaredTimes = [
			ghostState.scaredTimer for ghostState in newGhostStates]

		from sys import maxsize
		minimum_dist_from_ghosts = maxsize
		from util import manhattanDistance

		zip_object = zip(newGhostStates, newScaredTimes)
		for ghost, ghost_ScaredTime in zip_object:
			ghost_new_pos = ghost.getPosition()
			dist = manhattanDistance(ghost_new_pos, pacman_newPos)
			if ghost_ScaredTime == 0 and dist < minimum_dist_from_ghosts:
				minimum_dist_from_ghosts = dist

		food_list = currentGameState.getFood().asList()
		# food_list = newFood.asList()
		# number_of_foods = len(food_list)
		minimum_food_dist = maxsize
		for food_pos in food_list:
			dist_from_food = manhattanDistance(pacman_newPos, food_pos)
			if dist_from_food < minimum_food_dist:
				minimum_food_dist = dist_from_food

		if minimum_dist_from_ghosts <= 1:
			return -maxsize
		if minimum_food_dist == 0:
			return maxsize

		# return minimum_dist_from_ghosts - minimum_food_dist
		return 1/minimum_food_dist


def scoreEvaluationFunction(currentGameState):
	"""
	This default evaluation function just returns the score of the state.
	The score is the same one displayed in the Pacman GUI.
	This evaluation function is meant for use with adversarial search agents
	(not reflex agents).
	"""
	return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
	"""
	This class provides some common elements to all of your
	multi-agent searchers.  Any methods defined here will be available
	to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.
	You *do not* need to make any changes here, but you can if you want to
	add functionality to all your adversarial search agents.  Please do not
	remove anything, however.
	Note: this is an abstract class: one that should not be instantiated.  It's
	only partially specified, and designed to be extended.  Agent (game.py)
	is another abstract class.
	"""

	def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
		self.index = 0  # Pacman is always agent index 0
		self.evaluationFunction = util.lookup(evalFn, globals())
		self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
	"""
	Your minimax agent (question 2)
	"""

	def value(self, gameState, depth, agentIndex):
		if gameState.isWin() or gameState.isLose():
			return self.evaluationFunction(gameState)

		agentsNum = gameState.getNumAgents()
		agentIndex = (agentIndex+1) % (agentsNum)
		if not gameState.getLegalActions(agentIndex):
			return self.evaluationFunction(gameState)

		if agentIndex == 0:
			if self.depth == depth+1:
				return self.evaluationFunction(gameState)
			return self.maxValue(gameState=gameState, depth=depth+1, agentIndex=agentIndex)
		else:
			return self.minValue(gameState=gameState, depth=depth, agentIndex=agentIndex)

	def maxValue(self, gameState, depth, agentIndex):
		value = -maxsize

		# agentsNum = gameState.getNumAgents()

		# agentIndex = index % (agentsNum)

		for action in gameState.getLegalActions(agentIndex):
			successorGameState = gameState.generateSuccessor(
				agentIndex, action)

			value = max(value, self.value(
				gameState=successorGameState,
				depth=depth,
				agentIndex=agentIndex
			))
		return value

	def minValue(self, gameState, depth, agentIndex):
		value = maxsize

		# agentIndex = self.index
		for action in gameState.getLegalActions(agentIndex):
			successorGameState = gameState.generateSuccessor(
				agentIndex, action)

			value = min(value, self.value(
				gameState=successorGameState,
				depth=depth,
				agentIndex=agentIndex
			))
		return value

	def getAction(self, gameState):
		"""
		Returns the minimax action from the current gameState using self.depth
		and self.evaluationFunction.
		Here are some method calls that might be useful when implementing minimax.
		gameState.getLegalActions(agentIndex):
		Returns a list of legal actions for an agent
		agentIndex=0 means Pacman, ghosts are >= 1
		gameState.generateSuccessor(agentIndex, action):
		Returns the successor game state after an agent takes an action
		gameState.getNumAgents():
		Returns the total number of agents in the game
		gameState.isWin():
		Returns whether or not the game state is a winning state
		gameState.isLose():
		Returns whether or not the game state is a losing state
		"""
		from sys import maxsize

		maxValue = -maxsize
		agentIndex = self.index
		actions = gameState.getLegalActions(agentIndex)
		from game import Directions
		returned_action = Directions.STOP
		for action in actions:
			successorGameState = gameState.generateSuccessor(
				agentIndex, action)
			value = self.value(gameState=successorGameState,
							   depth=0,
							   agentIndex=agentIndex)
			if value > maxValue:
				maxValue = value
				returned_action = action

		return returned_action


class AlphaBetaAgent(MultiAgentSearchAgent):
	"""
	Your minimax agent with alpha-beta pruning (question 3)
	"""

	def value(self, gameState, depth, agentIndex, alpha, beta):
		if gameState.isWin() or gameState.isLose():
			return self.evaluationFunction(gameState)

		agentsNum = gameState.getNumAgents()
		agentIndex = (agentIndex+1) % (agentsNum)
		if not gameState.getLegalActions(agentIndex):
			return self.evaluationFunction(gameState)

		if agentIndex == 0:
			if self.depth == depth+1:
				return self.evaluationFunction(gameState)
			return self.maxValue(gameState=gameState,
								 depth=depth+1,
								 agentIndex=agentIndex,
								 alpha=alpha, beta=beta)
		else:
			return self.minValue(gameState=gameState,
								 depth=depth,
								 agentIndex=agentIndex,
								 alpha=alpha, beta=beta)

	def maxValue(self, gameState, depth, agentIndex, alpha, beta):
		value = -maxsize

		for action in gameState.getLegalActions(agentIndex):
			successorGameState = gameState.generateSuccessor(
				agentIndex, action)

			value = max(value, self.value(
				gameState=successorGameState,
				depth=depth,
				agentIndex=agentIndex,
				alpha=alpha, beta=beta
			))
			if value > beta:
				return value
			alpha = max(alpha, value)

		return value

	def minValue(self, gameState, depth, agentIndex, alpha, beta):
		value = maxsize

		for action in gameState.getLegalActions(agentIndex):
			successorGameState = gameState.generateSuccessor(
				agentIndex, action)

			value = min(value, self.value(
				gameState=successorGameState,
				depth=depth,
				agentIndex=agentIndex,
				alpha=alpha, beta=beta
			))
			if value < alpha:
				return value
			beta = min(beta, value)

		return value

	def getAction(self, gameState):
		"""
		Returns the minimax action from the current gameState using self.depth
		and self.evaluationFunction.
		Here are some method calls that might be useful when implementing minimax.
		gameState.getLegalActions(agentIndex):
		Returns a list of legal actions for an agent
		agentIndex=0 means Pacman, ghosts are >= 1
		gameState.generateSuccessor(agentIndex, action):
		Returns the successor game state after an agent takes an action
		gameState.getNumAgents():
		Returns the total number of agents in the game
		gameState.isWin():
		Returns whether or not the game state is a winning state
		gameState.isLose():
		Returns whether or not the game state is a losing state
		"""
		from sys import maxsize

		maxValue = -maxsize
		agentIndex = self.index
		actions = gameState.getLegalActions(agentIndex)
		from game import Directions
		returned_action = Directions.STOP
		alpha = -maxsize
		beta = maxsize
		for action in actions:
			successorGameState = gameState.generateSuccessor(
				agentIndex, action)
			value = self.value(gameState=successorGameState,
							   depth=0,
							   agentIndex=agentIndex,
							   alpha=alpha, beta=beta
							   )
			if value > maxValue:
				maxValue = value
				returned_action = action

			if value > beta:
				break
			alpha = max(alpha, value)

		return returned_action


class ExpectimaxAgent(MultiAgentSearchAgent):
	"""
	  Your expectimax agent (question 4)
	"""

	def value(self, gameState, depth, agentIndex):
		if gameState.isWin() or gameState.isLose():
			return self.evaluationFunction(gameState)

		agentsNum = gameState.getNumAgents()
		agentIndex = (agentIndex+1) % (agentsNum)
		if not gameState.getLegalActions(agentIndex):
			return self.evaluationFunction(gameState)

		if agentIndex == 0:
			if self.depth == depth+1:
				return self.evaluationFunction(gameState)
			return self.maxValue(gameState=gameState, depth=depth+1, agentIndex=agentIndex)
		else:
			return self.expectedValue(gameState=gameState, depth=depth, agentIndex=agentIndex)

	def maxValue(self, gameState, depth, agentIndex):
		value = -maxsize

		# agentsNum = gameState.getNumAgents()

		# agentIndex = index % (agentsNum)

		for action in gameState.getLegalActions(agentIndex):
			successorGameState = gameState.generateSuccessor(
				agentIndex, action)

			value = max(value, self.value(
				gameState=successorGameState,
				depth=depth,
				agentIndex=agentIndex
			))
		return value

	def expectedValue(self, gameState, depth, agentIndex):
		value = 0

		# agentIndex = self.index
		for action in gameState.getLegalActions(agentIndex):
			successorGameState = gameState.generateSuccessor(
				agentIndex, action)

			value += self.value(
				gameState=successorGameState,
				depth=depth,
				agentIndex=agentIndex
			)

		return value/len(gameState.getLegalActions(agentIndex))

	def getAction(self, gameState):
		"""
		Returns the minimax action from the current gameState using self.depth
		and self.evaluationFunction.
		Here are some method calls that might be useful when implementing minimax.
		gameState.getLegalActions(agentIndex):
		Returns a list of legal actions for an agent
		agentIndex=0 means Pacman, ghosts are >= 1
		gameState.generateSuccessor(agentIndex, action):
		Returns the successor game state after an agent takes an action
		gameState.getNumAgents():
		Returns the total number of agents in the game
		gameState.isWin():
		Returns whether or not the game state is a winning state
		gameState.isLose():
		Returns whether or not the game state is a losing state
		"""
		from sys import maxsize

		maxValue = -maxsize
		agentIndex = self.index
		actions = gameState.getLegalActions(agentIndex)
		from game import Directions
		returned_action = Directions.STOP
		for action in actions:
			successorGameState = gameState.generateSuccessor(
				agentIndex, action)
			value = self.value(gameState=successorGameState,
							   depth=0,
							   agentIndex=agentIndex)
			if value > maxValue:
				maxValue = value
				returned_action = action

		return returned_action


def betterEvaluationFunction(currentGameState):
	"""
	Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
	evaluation function (question 5).
	DESCRIPTION: <write something here so we know what you did>
	"""
	from sys import maxsize
	if currentGameState.isWin():
		return maxsize
		

	pacmanPos = currentGameState.getPacmanPosition()
	foodList = currentGameState.getFood().asList()
	ghostStates = currentGameState.getGhostStates()

	minimum_dist_from_ghosts = maxsize
	minimum_dist_from_scared_ghost = maxsize
	scared_ghost_found = False
	from util import manhattanDistance

	for ghost in ghostStates:
		ghost_pos = ghost.getPosition()
		dist = manhattanDistance(ghost_pos, pacmanPos)
		if ghost.scaredTimer == 0 and dist < minimum_dist_from_ghosts:
			minimum_dist_from_ghosts = dist

		if ghost.scaredTimer > 0 and dist < minimum_dist_from_scared_ghost:
			scared_ghost_found = True
			minimum_dist_from_scared_ghost = dist

	if minimum_dist_from_ghosts <= 2:
		return -maxsize
	if scared_ghost_found:
		return currentGameState.getScore()+5/minimum_dist_from_scared_ghost

	minimum_food_dist = maxsize
	for food_pos in foodList:
		dist_from_food = manhattanDistance(pacmanPos, food_pos)
		if dist_from_food < minimum_food_dist:
			minimum_food_dist = dist_from_food

	if minimum_food_dist == 0:
		return maxsize

	return currentGameState.getScore()-8/minimum_dist_from_ghosts+4/minimum_food_dist
	


# Abbreviation
better = betterEvaluationFunction