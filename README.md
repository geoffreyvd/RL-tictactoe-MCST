# RL-tictactoe-MCST
Assignment 3 model based reinforcement learning, learn best policy for tic tac toe using monte carlo search tree 

![Alt text](plotParamterC.png?raw=true "Title")

The plot shows the convergence of the model using different values for the c parameter. We find that a more greedy value (closer to 1) converges way faster and also 
(almost) finds the best policy. Intuitively this makes sense since its such a simple problem with many duplicate states (since order doesn't matter in tictactoe), therefore
extensively exploring is a waste of time.
