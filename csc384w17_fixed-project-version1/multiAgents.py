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

        # Calculate the average
        cost_sum = 0
        for c in cost:
            if type(c[0]) != tuple:
                cost_sum += c[0] 
            else:
                cost_sum += c[0][0]
        avg = cost_sum/len(cost)
       # return min(cost)
        return avg, Directions.STOP


    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
#        util.raiseNotDefined()
        return self.play_pacman(gameState, 1)[1]

class MonteCarloAgent(MultiAgentSearchAgent):
    """
        Your monte-carlo agent (question 5)
        ***UCT = MCTS + UBC1***
        TODO:
        1) Complete getAction to return the best action based on UCT.
        2) Complete runSimulation to simulate moves using UCT.
        3) Complete final, which updates the value of each of the states visited during a play of the game.

        * If you want to add more functions to further modularize your implementation, feel free to.
        * Make sure that your dictionaries are implemented in the following way:
            -> Keys are game states.
            -> Value are integers. When performing division (i.e. wins/plays) don't forget to convert to float.
      """

    def __init__(self, evalFn='mctsEvalFunction', depth='-1', timeout='40', numTraining=100, C='2', Q=None):
        # This is where you set C, the depth, and the evaluation function for the section "Enhancements for MCTS agent".
        if Q:
            if Q == 'minimaxClassic':
                pass
            elif Q == 'testClassic':
                pass
            elif Q == 'smallClassic':
                pass
            else: # Q == 'contestClassic'
                assert( Q == 'contestClassic' )
                pass
        # Otherwise, your agent will default to these values.
        else:
            self.C = int(C)
            # If using depth-limited UCT, need to set a heuristic evaluation function.
            if int(depth) > 0:
                evalFn = 'scoreEvaluationFunction'
        self.states = []
        self.plays = dict()
        self.wins = dict()
        self.calculation_time = datetime.timedelta(milliseconds=int(timeout))

        self.numTraining = numTraining

        "*** YOUR CODE HERE ***"

        MultiAgentSearchAgent.__init__(self, evalFn, depth)

    def update(self, state):
        """
        You do not need to modify this function. This function is called every time an agent makes a move.
        """
        self.states.append(state)

    def getAction(self, gameState):
        """
        Returns the best action using UCT. Calls runSimulation to update nodes
        in its wins and plays dictionary, and returns best successor of gameState.
        """
        "*** YOUR CODE HERE ***"
        games = 0
        begin = datetime.datetime.utcnow()
        while datetime.datetime.utcnow() - begin < self.calculation_time:
            games += 1

        util.raiseNotDefined()

    def run_simulation(self, state):
        """
        Simulates moves based on MCTS.
        1) (Selection) While not at a leaf node, traverse tree using UCB1.
        2) (Expansion) When reach a leaf node, expand.
        4) (Simulation) Select random moves until terminal state is reached.
        3) (Backpropapgation) Update all nodes visited in search tree with appropriate values.
        * Remember to limit the depth of the search only in the expansion phase!
        Updates values of appropriate states in search with with evaluation function.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

    def final(self, state):
        """
        Called by Pacman game at the terminal state.
        Updates search tree values of states that were visited during an actual game of pacman.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def mctsEvalFunction(state):
    """
    Evaluates state reached at the end of the expansion phase.
    """
    return 1 if state.isWin() else 0

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION:  
          
    """
    "*** YOUR CODE HERE ***"
#    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

