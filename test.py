
from utils import run_game
from nn import *
from SnakeGame import *

height = 200
width = 200

# Load model
model = NeuralNetwork()
model.build((None, 4))
model(np.array([[0,0,0,0]]))
model.load_weights('__models/04102020_10snakes_simplevision/checkpoint_generation989')

game = SnakeGame(render=True, player=False, FPS=60, height=height, width=width)
run_game(game, model, replay=True)

