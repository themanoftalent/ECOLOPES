import random
import csv
import os
from deap import base, creator, tools, algorithms
import sys, getopt

def execute():
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register("attr_int", random.randint, 0, 1)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_int, n=270)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    def evaluate(individual):
        selected_species = [index for index, value in enumerate(individual) if value == 1]
        total_pfg = sum(data[index][2] for index in selected_species)
        return total_pfg,

    #print(f'{os.getcwd()}/data/PFG.csv')
    data_path = f'{os.getcwd()}/data/movies.csv'
    data_path = os.path.expanduser(data_path)

    try:
        with open(data_path, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)
            data = [tuple(map(int, row)) for row in csvreader]
    except FileNotFoundError:
        print(f"Error: File '{data_path}' not found.")

    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("evaluate", evaluate)

    population = toolbox.population(n=100)

    NGEN = 50
    for gen in range(NGEN):
        offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.1)
        fits = toolbox.map(toolbox.evaluate, offspring)
        for fit, ind in zip(fits, offspring):
            ind.fitness.values = fit
        population = toolbox.select(offspring, k=len(population))

    best_ind = tools.selBest(population, k=1)[0]
    selected_species_indices = [index for index, value in enumerate(best_ind) if value == 1]
    selected_species_data = [data[index] for index in selected_species_indices]

    #print("Selected species indices:", selected_species_indices)
    #print("Selected species data:", selected_species_data)

    # Save the selected species data as a CSV file
    output_directory = f'{os.getcwd()}/output'
    output_directory = os.path.expanduser(output_directory)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)


    output_path = os.path.join(output_directory, 'selected_species_data.csv') #emir burada Override yapiyor yapmasin

    with open(output_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Index', 'Species', 'PFG'])
        csvwriter.writerows(selected_species_data)

    #print(f"Selected species data saved to '{output_path}'")
