
import csv
import sys
sys.path.append('src')


from nn import *
from SnakeGame import *
tf.keras.backend.set_floatx('float64')


def write_csv(data):
    with open('__output/fitness.csv', 'a', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(data)


def model_selection_probability(models, fitness, n):
    pdistribution = fitness / np.sum(fitness)
    return(np.random.choice(models, size=n, replace=True, p=pdistribution))


def model_selection_top(models, fitness, n):
    return(models[fitness.argsort()[::-1][:n]])


def clone_model(model):
    model_copy = NeuralNetwork()
    model_copy.build((None, 4))
    model_copy.setWeights(model)
    return(model_copy)


def run_game(game, model, replay=False):
    """
        One game run is running one game and measure fitness of this model.
        For each time step get "vision" and supply to model to get prediction of direction.
    """
    
    while (game.running):
        x = game.vision()
        direction = np.argmax(model(np.array(x)))
        game.run(direction)
        if (game.minsteps < 0):
            if (replay is False):
                game.running = False
            else:
                game.win.close()
                game.reset()
            
    
    
    
def train_step(game, models, mutation_rate, generation, population_size, max_generations, games_per_snake, fitness_option='mean'):
    
    fitnessList = np.array([])
    scoreList = []
    models_new = np.array([])
    
    # Loop over games    
    for i in range(population_size):
        model = models[i]
        
        # Run same model multiple times
        optimal_fitness = []
        for j in range(games_per_snake):
            run_game(game, model)
            game.calculate_fitness()
            optimal_fitness.append((game.fitness, game.score, game.steps))
            game.reset()

        # Determine final model. Either pick worst model as baseline, or average between the games.
        optimal_fitness = np.array(optimal_fitness)
        
        
        if fitness_option == 'worst':
            # Worst game of each model
            ofitness, oscore, osteps = optimal_fitness[optimal_fitness[:,0].argsort()][0,:]
            game.set_fitness(ofitness)
            game.set_score(oscore)
            game.set_steps(osteps)
        elif fitness_option == 'best':
            # Best game of each model
            ofitness, oscore, osteps = optimal_fitness[optimal_fitness[:,0].argsort()[::-1]][0,:]
            game.set_fitness(ofitness)
            game.set_score(oscore)
            game.set_steps(osteps)
        else:
            # Mean performance of each model (fitness_option == 'mean')
            game.set_fitness(np.mean(optimal_fitness[:,0]))
            game.set_score(np.mean(optimal_fitness[:,1]))
            game.set_steps(np.mean(optimal_fitness[:,2]))
        


        fitnessList = np.append(fitnessList, game.fitness)
        scoreList.append(game.score)
        print(">>> Generation: %3d/%4d --- Game: %3d/%3d --- score/steps/fitness: %5.1f/%7.1f/%9.2E" %(generation, max_generations, i, len(models), game.score, game.steps, game.fitness))


    for j in range(int(population_size * 0.1)):
        models_new = np.append(models_new, model_selection_top(models, fitnessList, 2))
        
    # Pick two best parents to crossbreed. Then mutate.
    while len(models_new) < population_size:
        selected = model_selection_probability(models, fitnessList, 2)
        model_copy = clone_model(selected[0])
        model_copy.crossbreed(selected[1])
        model_copy.mutate(mutation_rate)
        models_new = np.append(models_new, model_copy)

    return(models_new, fitnessList, scoreList)
    
