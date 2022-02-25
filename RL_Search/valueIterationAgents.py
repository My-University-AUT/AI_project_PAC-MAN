# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp
import util

from learningAgents import ValueEstimationAgent
import collections


class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """

    def __init__(self, mdp, discount=0.9, iterations=100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter()  # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        from sys import maxsize
        for iteration in range(self.iterations):
            iteration_values = util.Counter()  # A Counter is a dict with default 0

            for state in self.mdp.getStates():
                max_q_val =  self.maxQvalue(state)
                if max_q_val:
                    iteration_values[state] = max_q_val

            self.values = iteration_values

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        value = 0
        transitions = self.mdp.getTransitionStatesAndProbs(
            state, action)
        for (s_prime, transition_value) in transitions:
            s_prime_value = self.getValue(s_prime)
            transition_reward = self.mdp.getReward(state, action, s_prime)
            # print(transition_value)
            value += transition_value * \
                (transition_reward + self.discount * s_prime_value)

        return value

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        actions = self.mdp.getPossibleActions(state)

        # print("===============")
        # print(state)
        # print("---------------")
        # print(self.values)
        # print("================")
        from sys import maxsize
        max_q_val = -maxsize
        max_state = None
        for action in actions:
            value = self.computeQValueFromValues(state, action)
            # print(value)
            if value > max_q_val:
                max_q_val = value
                max_state = action

        return max_state

    def maxQvalue(self, state):
        from sys import maxsize

        max_value = -maxsize
        actions = self.mdp.getPossibleActions(state)

        for action in actions:
            q_val = self.computeQValueFromValues(state, action)
            if q_val > max_value:
                max_value = q_val
        if max_value != -maxsize:
            return max_value
        else:
            return None

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)


class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """

    def __init__(self, mdp, discount=0.9, iterations=1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

        # self.runValueIteration()

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
    
        size_of_states = len(self.mdp.getStates())
        for iteration in range(self.iterations):
            iteration_state = iteration % size_of_states
            # print("iteration state:  ",iteration_state)
            state = self.mdp.getStates()[iteration_state]

            # check if the state is terminal then no need to compute action. In fact there's no action from terminal state!
            if not self.mdp.isTerminal(state):
                action = self.computeActionFromValues(state)
                if action:
                    q_val = self.computeQValueFromValues(state, action)
                    self.values[state] = q_val


class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """

    def __init__(self, mdp, discount=0.9, iterations=100, theta=1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):

        states_predecessors = util.Counter()
        for state in self.mdp.getStates():
            states_predecessors[state] = set()

        for state in self.mdp.getStates():
            actions = self.mdp.getPossibleActions(state)
            for action in actions:
                transitions = self.mdp.getTransitionStatesAndProbs(
                    state, action)
                for (s_prime, _) in transitions:
                    states_predecessors[s_prime].add(state)

        queue = util.PriorityQueue()
        for state in self.mdp.getStates():
            if not self.mdp.isTerminal(state):
                max_q_val = self.maxQvalue(state)
                diff = abs(self.getValue(state) - max_q_val)
                queue.push(state, -diff)

        for iteration in range(self.iterations):

            if queue.isEmpty():
                return

            state = queue.pop()
            if not self.mdp.isTerminal(state):
                self.values[state] = self.maxQvalue(state)

            for state_predecessor in states_predecessors[state]:
                max_predecessor_q_val = self.maxQvalue(state_predecessor)

                diff = abs(self.getValue(state_predecessor) -
                           max_predecessor_q_val)

                if diff > self.theta:
                    queue.update(state_predecessor, -diff)
