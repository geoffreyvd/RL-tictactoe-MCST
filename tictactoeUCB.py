import random
import time
import math

def simulateGameUCB(state, turn, model):
    reward = 1
    while turn < 10:
        if turn % 2 == 1:
            #RL turn
            stateCopy = state.copy() #needed bcz its pass by reference
            action = root.bestAction(stateCopy)
            if action == None:
                action = selectAction(state)
        else:
            #enemy turn
            action = selectActionEnemy(state)
        state.append(action)
        turn+=1    

        if(turn > 4):
            #check if theres a winner
            reward = checkWinner(state)
            if reward != None:
                break
    if reward == None:
        reward = 0
    return state,reward #-1 lost, 0 tie, 1 won

def selectAction(state):
    remainingActions = getRemainingActions(state)
    action = random.choice(remainingActions)
    return action

def selectActionEnemy(state):
    remainingActions = getRemainingActions(state)
    action = random.choice(remainingActions)
    return action

def getRemainingActions(state):
    possibleActions = range(1,10)
    remainingActions = list(filter(lambda x: (x not in state), possibleActions)) 
    return remainingActions

def checkWinner(state):
    #return none when no winner, 1 if player 1 wins and, -1 if enemy wins
    win_condition = [[1, 2, 3], [4, 5, 6], [7,8,9], [1, 4, 7], [2, 5, 8], [3,6,9], [1, 5, 9], [3, 5, 9]]
    player_moves = state[0::2]
    opponent_moves = state[1::2]
    for i in win_condition:
        if set(i).issubset(player_moves): 
            return 1
        elif set(i).issubset(opponent_moves):
            return -1
    return None #TODO

def saveGame(state, reward):
    # player1actions = list(filter(lambda x: (x % 2 == 1), state)) 
    root.updateTree(state, reward)

class Tree(object):
    def __init__(self, position, remainingActions):
        # print("position:" + str(position) + " remaining actions:")
        # print(remainingActions)
        self.position = position
        self.childs = []
        self.childPositions = remainingActions
        for i in remainingActions:
            templist = remainingActions.copy()
            templist.remove(i)
            self.childs.append(Tree(i, templist))
        self.totaltries = 0
        self.successes = 0
        self.cParameter = math.sqrt(2)
        #accuracy = totaltries/succeses
    
    def updateTree(self, state, reward):
        #in the root node this is just the overall accuracy
        #if len(state) % 2 ==0 you can skip these 2:
        self.totaltries+=1
        self.successes+=reward
        # print("updating Tree with state: ", state)
        if state:
            childPosition = state.pop(0)
            childIndex = self.childPositions.index(childPosition)
            self.childs[childIndex].updateTree(state, reward)

    def bestAction(self, state):
        # print("checking best action for state", state)
        if len(state) !=0:
            childPosition = state.pop(0)
            childIndex = self.childPositions.index(childPosition)
            return self.childs[childIndex].bestAction(state)
        else:
            # print("my position: ", self.position, "with childs, accuracy: ")
            bestTotalScoreUCB = 0
            bestAction = None
            #UCT action selection by using UCB            
            for child in self.childs:
                if child.totaltries == 0:
                    break
                exploitation = child.successes / child.totaltries
                exploration = self.cParameter * math.sqrt(math.log(self.totaltries)/child.totaltries)
                totalScoreUCB = exploitation + exploration
                # print(child.position, totalScoreUCB)
                if totalScoreUCB > bestTotalScoreUCB:
                    bestTotalScoreUCB = totalScoreUCB
                    bestAction = child.position
            # if bestAction == None:
            #     print("learned model incomplete")
            # print("we found best accuracy for child position: ", bestAction)
            return bestAction


if __name__ == "__main__":
    print("building tree")
    root = Tree(0, list(range(1,10)))
    print("finished building tree")
    converged = False
    print("training")
    n = 300000 #number of training rounds
    accuracies = [0]*(n+1)
    while not converged:
        # print("totaltries: ", str(root.totaltries), "total successes: ", str(root.successes))
        # print("tries startign with position 1, should be ~1/9 fo total: " , str(root.childs[1].totaltries))
        actionsPlayed = [] #positions of placed game pieces, where the first entry is the first action of player1, second entry first action of enemy, etc,...
        turn = 1
        state, reward = simulateGameUCB(actionsPlayed, turn, root)
        saveGame(state, reward)
        #plot data
        accuracies[root.totaltries]=root.successes/root.totaltries
        if root.totaltries == n:
            break
        #if lastAccuracy == root.accuracy then converged

    print(root.bestAction([]))
    print(root.successes/root.totaltries)

    for child in root.childs:
        print("position: ", child.position)
        print("success: ", child.successes)
        print("totaltries: ", child.totaltries)
    