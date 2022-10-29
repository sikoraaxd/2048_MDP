# 2048_MDP
Solving a 2048 game with Markov Decision Process

## Main workflow:

1) Create environment - instance of Game class (Game2048).<br />
2) Create actor - instance of player class.<br />
3) Train actor with "train" method of Player class:<br />
  3.1) Pass the environment for explore.<br />
  3.2) Pass the count of needed states to know (boundOfStates).<br />
  3.3) Pass the needed tile number that will be the winning indicator for state.<br />
4) Setting the state values of policy by calling the "createPolicy" and pass the environment there.<br />
5) Set the environment to starting state by calling the "init" method of Game class with "startState" attribute equal to True.<br />
6) Create game loop like:

```python
while True:
  if environment.maxTileValue != needed and not environment.game_over:
      state = environment.getState()
      action = player.forward(state)
      environment.forward(action)
  else:
      break
```
