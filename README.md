# Neural Network Snake using Genetic Algorithm
In this project I will go through my implementation of a Genetic Algorithm  for the game Snake.


## Introduction and idea
A Genetic Algorithm is based on Charles Darwin's theory of evolution and the concept natural selection. The idea is to intialize with a population of randomly generated models and let them play the game a snake that determines how well they have performed. The models are then ranked and the best performing models crossbred and mutated which make up the next generation of snakes.


## Snake
The game snake is coded from scratch and can be played by running SnakeGame.py. The controls is left and right arrow to steer and escape to close down the app.
Training can be started by running train.py which outputs the best model for each generation to the folder models as well as appending performance to output/fitness.csv.
You can run a model and see how to performs using test.py.

### Fitness score
Each model is ranked based on the fitness which is defined as
fitness = <img src="https://render.githubusercontent.com/render/math?math=s^2 \cdot 2^p"> for <img src="https://render.githubusercontent.com/render/math?math=p < 10"> and
fitness = <img src="https://render.githubusercontent.com/render/math?math=s^2 \cdot 2^{10} \cdot (p - 9)"> for <img src="https://render.githubusercontent.com/render/math?math=p \ge 10">
where s denotes the number of steps and p denotes number of points.

This is inspired from other similar projects, however, I've tried adjusting the values and formulas without much improvement.

## Neural network
I'm using a fairly small neural network with a single hidden layer with six neurons. The input layer has four neurons where the first three indicates if there is a wall or segment of the snake in front or besides the head of the snake (boolean). The fourth neuron measures the angle to point in relation to the snake direction. The output layer has three neurons with a softmax activation function that determines if the snake should turn left, right og keep going straight.

The model seems more stable using this configuration in comparison to measuring the distance to nearest wall/snake segment in any line of sight.

Because of the random nature of initial spawn direction of the snake and randomly placed points, for each model I determine the fitness of the model based on the results of ten games.

### Mutation and crossbreeding


## Results
The following results are based on training for 1099 generations where each generation consists of 200 snakes, each run 10 times. The mutation rate is set at 1%, and the game board size of 10 by 10.

![](Figure/Fitness_generation.png)
Fitness as a function of generations trained.


![](Figure/Score_generation.png)
Number of "apples" eating (score) as a function of generations trained.

Initially there is a quick improvement of the models in the first few generations with a max score around 8. Next, around generation 70 there is an drastic improvement in fitness and score followed by a more linear improvement in fitness. Unfortunately, the random nature of the game, mutations and crossbreeding does not guarantee a stable converging towards better models between generations, something I hoped running each model multiple times and calculating the average score, number of steps and fitness.

As you can see I only reach about a maximum score just above 20 which obviously does not mean I have solved the game. Maybe I need to run for much longer and hope for a random mutation that drastically improves the model, or figure out a more fitting fitness function.


## Future
If I wish to run for more generations I need to look into optimization of the game as it is rather slow. Each generation runs 200 snakes, 10 times each giving 2 million games run over the course of 1000 generations. I could not get multiprocessing to work with tensorflow and making predictions on the same model in parallel which would greatly reduce runtime, and probably make each model more robust with the ability to increase games run per model.