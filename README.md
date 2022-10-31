# 2048_MDP
Solving a 2048 game with Markov Decision Process

## Main workflow:

1) Create environment - instance of Game class (Game2048).<br />
2) Create agent - instance of agent class.<br />
3) Train agent with "train" method of Agent class:<br />
  3.1) Pass the environment for explore.<br />
  3.2) Pass the count of needed states to know (bound_of_states).<br />
  3.3) Pass the needed tile number that will be the winning indicator for state.<br />
4) Setting the state values of policy by calling the "create_policy" and pass the environment there.<br />
5) Set the environment to starting state by calling the "init" method of Game class with "start_state" attribute equal to True.<br />
6) Create game loop like:

```python
while True:
  if environment.max_tile_value != needed and not environment.game_over:
      state = environment.get_state()
      action = agent.forward(state)
      environment.forward(action)
  else:
      break
```
