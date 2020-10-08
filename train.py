from utils import *


width = 200
height = 200

max_generations = 1000
population_size = 200
mutation_rate = 0.01
games_per_snake = 20
distance_option = "simple" 
# setting this to anything other than "simple" changes distance option to measuring actual distance to nearest wall rather than boolean value if there is a wall
# or snake segment on the square right next the the snake head.


if __name__ == '__main__':
    # Initialize models and snakegames
    models = np.array([])
    game = SnakeGame(render=False, player=False, width=width, height=height, distance_option=distance_option)
    for m in range(population_size):
        models = np.append(models, NeuralNetwork())

    for generation in range(max_generations):
        models, fitnessGeneration, scoreGeneration = train_step(game, models, mutation_rate, generation, population_size, max_generations, games_per_snake, fitness_option='best')
        
        fitnessAvg = np.mean(fitnessGeneration)
        fitnessMax = np.max(fitnessGeneration)
        fitnessMed = np.median(fitnessGeneration)
        
        scoreAvg = np.mean(scoreGeneration)
        scoreMax = np.max(scoreGeneration)
        scoreMed = np.median(scoreGeneration)
        
        print("Average fitness: ", fitnessAvg, "Max fitness: ", fitnessMax)
        
        # Save generation
        models[0].save_weights('__models/checkpoint_generation' + str(generation), overwrite=True)
        write_csv([generation, fitnessAvg, fitnessMed, fitnessMax, scoreAvg, scoreMed, scoreMax])
        
        game.reset()
