
from utils import run_game
from nn import *
from SnakeGame import *

height = 400
width = 400


# Load model
model = NeuralNetwork()
model.build((None, 4))
model(np.array([[0,0,0,0]]))
model.load_weights('__models/checkpoint_restart_generation1073')

game = SnakeGame(render=True, player=False, FPS=60, height=height, width=width)
run_game(game, model, replay=True)

