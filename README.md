# RL-tictactoe-MCST
Assignment 3 model based reinforcement learning, learn best policy for tic tac toe using monte carlo search tree 

![Alt text](plotParamterC.png?raw=true "Title")

The plot shows the convergence of the model using different values for the c parameter. We find that a more greedy value (closer to 1) converges way faster and also 
(almost) finds the best policy. Intuitively this makes sense since its such a simple problem with many duplicate states (since order doesn't matter in tictactoe), therefore
extensively exploring is a waste of time.


# RL-shortestpath-Qlearning
Assignment 4, model-less (value based) reinforcement learning solution to the shortest path problem. I have implemented Q-learning with some optimizations to find the end point (40,0) in a 50x50 grid, where each state transition is a stochastic process (it may or may not be congested). It learns the fastest path by looking at the maximum Q value for a certain starting point and action pair.

![Alt text](qlearningShortestPath/final_i50000d099a06eps01.png?raw=true "Title")
