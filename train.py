from utils import *


width = 200
height = 200

max_generations = 1000
population_size = 200
mutation_rate = 0.01
games_per_snake = 10




if __name__ == '__main__':
    # 1) Initialize models and snakegames
    models = np.array([])
    game = SnakeGame(render=False, player=False, width=width, height=height)
    for m in range(population_size):
        models = np.append(models, NeuralNetwork())

    for generation in range(max_generations):
        models, fitnessGeneration, scoreGeneration = train_step(game, models, mutation_rate, generation, population_size, max_generations, games_per_snake)
        
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