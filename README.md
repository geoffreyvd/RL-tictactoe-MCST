# RL-tictactoe-MCST
Assignment 3 model based reinforcement learning, learn best policy for tic tac toe using monte carlo search tree 

![Alt text](plotParamterC.png?raw=true "Title")
The plot shows the convergence of the model using different values for the c parameter. On short we find that a more greedy value (closer to 1) converges way faster and also 
approximately finds the best policy. Intuitively this makes sense since its such a simple problem with many duplicate states (since order doesn't matter in tictactoe), therefore
is extensively exploring a waste of time.
