# import matplotlib
# import matplotlib.pyplot as plt
# from matplotlib.colors import BoundaryNorm
# from matplotlib.ticker import MaxNLocator
import numpy as np
import random
import seaborn
import matplotlib.pyplot as plt

LENGTH_X = 50
LENGTH_Y = 50
MAXIMUM_EPISODE_STEPS = 1000

def QlLearning(env, iterations =15000, discount_factor=0.99, alpha = 0.6, epsilon = 0.2):
    #initialize q value array:
    Q = np.array([[[0 for l in range(4)] for i in range(50)] for j in range(50)], dtype='f')

    #loop iterations
    for i in range(0, iterations):
        #choose random beginning state 
        # env.restart()
        state = random.randrange(0, LENGTH_X, 1), random.randrange(0, LENGTH_Y, 1)
        if state == (40,0): #edge case, u cant start from the end point (this causes the reward to be bigger than 1 )
            continue
        # state = 39,0
        print("ITERATION: " + str(i))

        #loop maximum x amount of times, or untill reward(terminal state)
        for step in range(0, MAXIMUM_EPISODE_STEPS):
            x,y = state
            # print("state: " + str(x) + "," + str(y))
            #choose next action (based on epsilon-greedy and maximum reward)
            actions = env.getActionsForState((x,y))

            if random.random() < epsilon:
                action = random.choice(actions)
            else:
                if np.all(Q[x][y] == Q[x][y][0]):
                    action = random.choice(actions)
                else:
                    bestAction = actions[0]
                    bestValue = -1
                    for a in actions:
                        if Q[x][y][a] > bestValue:
                            bestValue = Q[x][y][a]
                            bestAction = a
                    action = bestAction
                    # actionIndex = np.argmax(Q[x][y])
            # print("action: " + str(action))

            #take action and observe new state and reward
            #optimization for faster learning
            congested = True
            amountOfTrials =0
            next_state, reward, done = 0,0,0
            while congested: 
                amountOfTrials+=1
                next_state, reward, done = env.takeStep((x,y),action) 
                if (x,y) != next_state:
                    congested=False 
                if amountOfTrials == 100:#100% congested                    
                    next_state = (x,y)
                    reward = -1
                    done = True #otherwise could get stuck if all 4 roads are congested
                    break
            
            #calculate Q value from this episode and store it

            #first determine best value from next state
            newX, newY = next_state        
            # max_value = max(Q[newX][newY])
            # max_index = Q[newX][newY].index(max_value) 
            # best_next_action = max_index
            best_next_action = np.argmax(Q[newX][newY])

            #then calculate difference between current q value and new q value, multiply this difference times the learning rate   
            td_target = reward + (discount_factor**amountOfTrials) * Q[newX][newY][best_next_action] 
            td_delta = td_target - Q[x][y][action] 
            # print("value before: ", Q[x][y][action])
            Q[x][y][action] = Q[x][y][action]+alpha*td_delta
            if done:
                # print("reward was: " + str(reward))
                # print("new Q value for state", state, ": ", Q[x][y][action])
                break
            # print("end of step")

            state = next_state
    return Q   

class Environment:
    def __init__(self):
        self.generateTransitionProbabilities()
        self.rewardcheckpoint1 = 1
        self.rewardcheckpoint2 = 1
    
    def restart(self):
        self.rewardcheckpoint1 = 1
        self.rewardcheckpoint2 = 1

    def reachedCheckpoint1(self):
        reward = self.rewardcheckpoint1
        self.rewardcheckpoint1 = 0
        return reward

    def reachedCheckpoint2(self):
        reward = self.rewardcheckpoint2
        self.rewardcheckpoint2 = 0
        return reward

    def generateTransitionProbabilities(self):
        # POINT 1: realization of congestion
        # Transition probability matrix, 50x50 -> for each state there are several probabilities.
        # [LEFT, UP,RIGHT, DOWN] [0.  0.6 0.2 1. ]
        # corners: 2, 1st & last of all rows and columns have 3, rest has 4

        random.seed(1)
        probs = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]

        Tpm = []
        for i in range(50):            
            if i == 0:
                tpm1 = []
                for j in range(50):
                    s = random.choices(probs, k=4)
                    s[1]=0
                    if j == 0:
                        s[0]=0
                    if j == 49:
                        s[2]=0
                    tpm1.append(s)
                Tpm.append(tpm1)
            
            
            elif i == 49:
                tpm2 = []
                for j in range(50):
                    s = random.choices(probs, k=4)
                    s[3] =0
                    if j == 0:
                        s[0]=0
                    if j == 49:
                        s[2]=0
                    tpm2.append(s)
                Tpm.append(tpm2)
            
            else:
                tpm3 = []
                for j in range(50):
                    s = random.choices(probs, k=4)
                    if j==0:
                        s[0]=0
                    if j==49:
                        s[2]=0
                    tpm3.append(s)
                Tpm.append(tpm3)
                        
        Tpm = np.array(Tpm)
        self.grid = Tpm

    def takeStep(self, state, action):
        x, y = state
        congestionProbability = self.grid[x][y][action]
        congested = random.random() < congestionProbability
        if congested:
            return state, 0, False
        newstate = self.getNewState(state,action)
        if newstate == (40,0):
            return (40,0), 1, True 

        reward = 0
        if newstate == (25,15):
            reward = self.reachedCheckpoint1()     
        if newstate == (10,30):
            reward = self.reachedCheckpoint2()     
        return newstate, reward, False

    def getNewState(self, state, action):
        x, y = state
        #apparently x and y should be swapped
        #fyi the grid goes from 0 downwards to 50 (y), and 
        # if action == 0: #left?
        #     x=x-1
        # if action == 1: #up?
        #     y=y-1
        # if action == 2: #right?
        #     x=x+1
        # if action == 3: #down?
        #     y=y+1
        if action == 0: #left?
            y-=1
        if action == 1: #up?
            x=x-1
        if action == 2: #right?
            y+=1
        if action == 3: #down?
            x=x+1
        return (x,y)

    def getActionsForState(self, state):
        x, y = state
        congestionProbsPerActions = self.grid[x][y]
        possibleActions = []
        for i in range(0, len(congestionProbsPerActions)):
            if congestionProbsPerActions[i] != 0:
                possibleActions.append(i)
        # print("state: ",state, "congestionprobs: ",congestionProbsPerActions, "possibleActions: ", possibleActions)
        return possibleActions
        
if __name__ == "__main__":
    print("initializing env")
    #initalize environment: convergence probabilities
    env = Environment()
    print("done.")

    #initialize state action pairs to 0, 2500 states, 4 actions  

    #start Qlearning 
    print("start of qlearning")
    Q = QlLearning(env)
    x = np.arange(0,50, 1)  
    y = np.arange(0, 50, 1) 
    Z = np.array([[max(Q[i][j])*1000 for i in range(50)] for j in range(50)])
    
    # print(Z)
    # for x in Z:
    #     for y in x:
    #         if y!=0:
    #             print(y)
    # Z[1][1]=0.99*1000
    # Z[2][2]=-0.99*1000
    # Z[3][4]=-0.5*1000
    # Z[5][5]=0.5*1000
    # print("highest Q value for state 9,1:",max(Q[39][0]))
    # fig, ax = plt.subplots()
    # im = ax.pcolormesh(x, y, Z)
    # plt.colorbar(im, ax=ax)
    # plt.show()
    
    policy = np.array([[np.argmax(Q[i][j]) for i in range(50)] for j in range(50)])
    seaborn.heatmap(policy)
    
    plt.show()