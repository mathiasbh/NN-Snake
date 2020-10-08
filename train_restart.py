
from utils import *


width = 200
height = 200

max_generations = 1001
population_size = 200
mutation_rate = 0.01
games_per_snake = 10
distance_option = "simple" 
fitness_option = "mean"

# Load model as starting model. This model will be duplicated (population_size) and mutated as new starting generation.
model_number = 999
latest_model_name = '__models/checkpoint_generation' + str(model_number)


if __name__ == '__main__':
    # Initialize selected model and initialize game.
    models = np.array([])
    game = SnakeGame(render=False, player=False, width=width, height=height)
    
    model = NeuralNetwork()
    model.build((None, 4))
    model(np.array([[0,0,0,0]]))
    model.load_weights(latest_model_name)
    
    # Add all models and mutate
    models = np.append(models, model)
    while len(models) < population_size:
        model_copy = clone_model(model)
        model_copy.mutate(mutation_rate)
        models = np.append(models, model_copy)


    # Run additional generations and save to models/
    for generation in range(max_generations):
        new_generation_value = generation + model_number + 1
        models, fitnessGeneration, scoreGeneration = train_step(game, models, mutation_rate, new_generation_value, population_size, max_generations+new_generation_value, games_per_snake, fitness_option=fitness_option)
        
        fitnessAvg = np.mean(fitnessGeneration)
        fitnessMax = np.max(fitnessGeneration)
        fitnessMed = np.median(fitnessGeneration)
        
        scoreAvg = np.mean(scoreGeneration)
        scoreMax = np.max(scoreGeneration)
        scoreMed = np.median(scoreGeneration)
        
        print("Average fitness: ", fitnessAvg, "Max fitness: ", fitnessMax)
        
        # Save generation
        models[0].save_weights('__models/checkpoint_restart_generation' + str(new_generation_value), overwrite=True)
        write_csv([new_generation_value, fitnessAvg, fitnessMed, fitnessMax, scoreAvg, scoreMed, scoreMax])
        
        game.reset()
