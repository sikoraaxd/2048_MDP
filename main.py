import sys
import numpy as np
import config
from game import Game2048
from agent import Agent
from app import App

if __name__ == '__main__':
    sys.setrecursionlimit(10000)
    np.random.seed(config.SEED)

    environment = Game2048(2)
    agent = Agent()

    agent.train(environment=environment,
                 bound_of_states=400,
                 needed=config.NEEDED)
    agent.create_policy(environment)

    environment.init(start_state=True)
    app = App(environment)

    while app.run:
        app.update(environment)
        value = 0
        actStr = 'x'
        if environment.max_tile_value != config.NEEDED and not environment.game_over:
            state = environment.get_state()
            action = agent.forward(state)
            environment.forward(action)
            value = round(agent.get_state_value(state), 2)
            actStr = config.ACTION_ARROWS[action]

        app.draw(value=value, action=actStr)
        

    
