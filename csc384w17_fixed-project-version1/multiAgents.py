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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


def scoreEvaluationFunction(currentGameState):
   """
     This default evaluation function just returns the score of the state.
     The score is the same one displayed in the Pacman GUI.

     This evaluation function is meant for use with adversarial search agents
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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    def play_pacman(self, gameState, depth):
        agent = 0
        legActions = gameState.getLegalActions(agent)
        cost = [0]
        if gameState.isWin() or len(legActions) == 0 or self.depth < depth:
            return self.evaluationFunction(gameState), Directions.STOP
        for action in legActions:
            successor = gameState.generateSuccessor(agent, action)
            cost.append((self.play_ghosts(successor, depth, agent + 1),action))
        return max(cost) 

    def play_ghosts(self, gameState, depth, agent):
#        print("play ghost", depth, agent)
        legActions = gameState.getLegalActions(agent)
        if gameState.isLose() or len(legActions) == 0:
            return self.evaluationFunction(gameState), Directions.STOP
        successors = [gameState.generateSuccessor(agent, action) for action in legActions]
        #cost = []
        if gameState.getNumAgents() - 1 == agent:
            cost = []
            for succ in successors:
                cost.append(self.play_pacman(succ,depth+1))
        else:
           cost = []
           for succ in successors:
                cost.append(self.play_ghosts(succ,depth,agent+1))
        return min(cost)

           
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
        """
        "*** YOUR CODE HERE ***"
#        util.raiseNotDefined()
        return self.play_pacman(gameState, 1)[1]
        


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def play_pacman(self, gameState, depth, alpha, beta):
        curr_val = float("-inf")
        direction = Directions.STOP
        agent = 0
        legActions = gameState.getLegalActions(agent)
        cost = [0]
        if gameState.isWin() or len(legActions) == 0 or self.depth < depth:
            return self.evaluationFunction(gameState), Directions.STOP
        for action in legActions:
            succ = gameState.generateSuccessor(agent, action)
            cost = self.play_ghosts(succ, depth, agent+1,alpha, beta)[0]
            if cost > curr_val:
                direction = action
                curr_val = cost
            if curr_val > beta:
                return curr_val, direction 
            # Find largest alpha
            alpha = max(alpha, curr_val)
        return curr_val, direction


    def play_ghosts(self, gameState, depth, agent, alpha, beta):
        legActions = gameState.getLegalActions(agent)
        curr_val = float("inf")
        direction = Directions.STOP
        if gameState.isLose() or len(legActions) == 0:
            return self.evaluationFunction(gameState), Directions.STOP

        for action in legActions:
            succ = gameState.generateSuccessor(agent,action)
            if gameState.getNumAgents() - 1 == agent:
                cost = self.play_pacman(succ, depth+1,alpha,beta)[0]
            else:
                cost = self.play_ghosts(succ,depth,agent+1,alpha,beta)[0]
            if cost < curr_val:
                direction = action
                curr_val = cost
            if curr_val < alpha:
                return curr_val, direction
            beta = min(beta, curr_val)
        return curr_val, direction 

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
#        util.raiseNotDefined()
        alpha = float("-inf")
        beta = float("inf")
        return self.play_pacman(gameState, 1, alpha,beta)[1]


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

