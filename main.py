import sys
import numpy as np
import config
from game import Game2048
from player import Player
from app import App

if __name__ == '__main__':
    sys.setrecursionlimit(10000)
    np.random.seed(config.SEED)

    environment = Game2048(2)
    player = Player()

    player.train(environment=environment,
                 bound_of_states=400,
                 needed=config.NEEDED)
    player.createPolicy(environment)

    environment.init(start_state=True)
    app = App(environment)

    while app.run:
        app.update(environment)
        value = 0
        actStr = 'x'
        if environment.maxTileValue != config.NEEDED and not environment.game_over:
            state = environment.getState()
            action = player.forward(state)
            environment.forward(action)
            value = round(player.getStateValue(state), 2)
            actStr = config.ACTION_ARROWS[action]

        
        app.draw(value = value, action = actStr)

    
