import random
import string

from math import floor

from beta.market import MARKET
from beta.portfolio import Portfolio

mutation_probability = 0.2
population_size = 25
breed_factor = 0.5
iteration_count = 100


def random_name():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))


def adjust_weight(new_portfolio_values):
    current_sum = sum(new_portfolio_values.values())
    for item in new_portfolio_values.items():
        new_portfolio_values[item[0]] = item[1] * (1 / current_sum)
    return new_portfolio_values


def remove_random_asset(portfolio):
    new_portfolio_values = portfolio.asset_and_weights.copy()
    if len(portfolio.asset_and_weights.items()) > 1:
        removed_item = random.choice(list(portfolio.asset_and_weights.items()))
        new_portfolio_values.pop(removed_item[0])
    return Portfolio(random_name(), adjust_weight(new_portfolio_values))


def add_random_asset(portfolio):
    new_portfolio_values = portfolio.asset_and_weights.copy()
    if len(new_portfolio_values) < len(MARKET.get_assets()):
        asset_to_add = random.choice(list(set(MARKET.get_assets()) - set(new_portfolio_values.keys())))
        weight = random.random()
        new_portfolio_values[asset_to_add] = weight
    return Portfolio(random_name(), adjust_weight(new_portfolio_values))


def change_random_asset(portfolio):
    new_portfolio_values = portfolio.asset_and_weights.copy()
    asset_to_adjust = random.choice(list(portfolio.asset_and_weights.keys()))
    value_to_add = random.random() - 0.5
    new_value = portfolio.weight(asset_to_adjust) + value_to_add
    if new_value <= 0:
        new_portfolio_values.pop(asset_to_adjust)
    else:
        new_portfolio_values[asset_to_adjust] = new_value
    return Portfolio(random_name(), adjust_weight(new_portfolio_values))


def crossover(first_portfolio, other_portfolio):
    new_portfolio_values = {}
    all_assets = set(first_portfolio.asset_and_weights.keys()).union(other_portfolio.asset_and_weights.keys())
    for asset in all_assets:
        pick_from = first_portfolio if random.random() > 0.5 else other_portfolio
        if pick_from.weight(asset) > 0:
            new_portfolio_values[asset] = pick_from.weight(asset)
    if sum(new_portfolio_values.values()) == 0:
        new_portfolio_values[list(all_assets)[0]] = 1
    return Portfolio(random_name(), adjust_weight(new_portfolio_values))


def generate_start_portfolios():
    population = []
    for p in range(0, population_size):
        portfolio = build_random_portfolio()
        population.append(MARKET.evaluate_portfolio_return(portfolio))
    return population


def build_random_portfolio():
    asset_count = random.randint(1, len(MARKET.assets))
    new_portfolio_values = {}
    for asset in random.sample(MARKET.assets, asset_count):
        new_portfolio_values[asset] = random.random()
    portfolio = Portfolio(random_name(), adjust_weight(new_portfolio_values))
    return portfolio


def mutate(portfolio):
    random_mutation = random.random()
    if random_mutation < 0.2:
        return add_random_asset(portfolio)
    else:
        if random_mutation < 0.4:
            return remove_random_asset(portfolio)
        else:
            return change_random_asset(portfolio)


def add_mutations(population):
    mutations = []
    for portfolio in population:
        if random.random() > mutation_probability:
            mutations.append(MARKET.evaluate_portfolio_return(mutate(portfolio.portfolio)))
    return mutations


def breed(population):
    offspring = []
    for i in range(1, floor(len(population) * breed_factor)):
        parents = random.sample(population, 2)
        child = MARKET.evaluate_portfolio_return(crossover(parents[0].portfolio, parents[1].portfolio))
        offspring.append(child)
    return offspring


def is_valid(p_return):
    return p_return.std_dev < 5


def extinct(population):
    survivors = []
    for portfolio in population:
        if is_valid(portfolio):
            survivors.append(portfolio)
    max_mean = max(p.mean for p in survivors)
    max_diverse = max(diversity(p, survivors) for p in survivors)
    survivors.sort(key=lambda p: p.mean / max_mean + diversity(p, survivors) / max_diverse + diversification(p), reverse=True)
    return survivors[:population_size]


def diversity(individual, population):
    return sum(distance(individual, other) for other in population)


def distance(first, other):
    return sum(abs(first.portfolio.weight(asset) - other.portfolio.weight(asset)) for asset in MARKET.assets)


def diversification(portfolio):
    return len(list(filter(lambda v: v > 0, portfolio.portfolio.asset_and_weights.values()))) / len(MARKET.assets)


def add_foreigners():
    foreigners = []
    for i in range(1, floor(population_size / 6)):
        foreigners.append(MARKET.evaluate_portfolio_return(build_random_portfolio()))
    return foreigners


def evolution():
    population = generate_start_portfolios()
    for i in range(1, iteration_count):
        population.extend(add_mutations(population))
        population.extend(add_foreigners())
        population.extend(breed(population))
        survivors = extinct(population)
        population = survivors
        print('### Finished Iteration {0} ###'.format(i))
        for portfolio in population:
            print(portfolio)
    return population


evolution()
