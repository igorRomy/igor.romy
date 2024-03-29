import gameSimulator
import gameWithoutUI
from logic import Logic

"""
This is where we run an instance of the gameSimulator:GameGrid (parent class) -> child classes: 
                                                                                AISearchesThread, AISearchesNoThread

    :param search_function: search method that will be used
    :param game_score_alg: which Logic.[game score algorithm] you want to use
                -> see Logic.py
    :param score_type: method through which we will update best potential move
    :param depth: the depth you want the search tree's to have
    :param iterations: the amount of iterations you want to make over the chosen search_function.
        -> When we make an instance of the class that has the declaration of the chosen search_function
            we iterate over it with every key (direction)
             -> the child class will then return per key a total/average best score via score_type to us
             -> USING param: iterations to iterate above the key iterations will give us a chance to make a
                better prediction
                    -> Make an average/total of all iterations per key (direction) and then choose best result as
                       "best" move
                    -> (of course) this will also give best result in general

"""

# which function will you use
search_functions = ['pure_monte_carlo_tree_search', 'expectimax', 'variation_monte_carlo_tree_search']

# which score algorithm will you use
game_score_algs = ['game_score_count_tile_values', 'game_score',
                   'game_score_with_weight_matrix',
                   'game_score_with_weight_matrix_and_penalty', 'game_score_with_weight_matrix_zig_zag']

# which score type you will use
score_types = ['set_score', 'set_score_lowest', 'set_score_highest']

# BEST SEARCHES with acceptable time per move


def pure_monte_carlo_tree_search_without_ui():
    _ = gameWithoutUI.GameGrid(search_functions[0], game_score_algs[1], score_types[2], depth=0, iterations=50)


def pure_monte_carlo_tree_search_with_ui():
    _ = gameSimulator.GameGrid(search_functions[0], game_score_algs[1], score_types[0], depth=0, iterations=50)


def epectimax_without_ui():
    _ = gameWithoutUI.GameGrid(search_functions[1], game_score_algs[2], score_types[1], depth=3, iterations=30)


def epectimax_with_ui():
    _ = gameSimulator.GameGrid(search_functions[1], game_score_algs[2], score_types[1], depth=3, iterations=30)


def variation_monte_carlo_tree_search_without_ui():
    _ = gameWithoutUI.GameGrid(search_functions[2], game_score_algs[1], score_types[0], depth=8, iterations=40)


def variation_monte_carlo_tree_search_with_ui():
    _ = gameSimulator.GameGrid(search_functions[2], game_score_algs[1], score_types[0], depth=8, iterations=40)


def create_tests_without_ui(search_function, game_score_alg, score_type, iteration, depth=None):
    _ = gameWithoutUI.GameGrid(search_functions[search_function], game_score_algs[game_score_alg],
                               score_types[score_type], depth=depth, iterations=iteration)


def create_tests_with_ui(search_function, game_score_alg, score_type, iteration, depth=None):
    _ = gameSimulator.GameGrid(search_functions[search_function], game_score_algs[game_score_alg],
                               score_types[score_type], depth=depth, iterations=iteration)

# UNCOMMENT TO USE

#pure_monte_carlo_tree_search_without_ui()
#pure_monte_carlo_tree_search_with_ui()
#epectimax_without_ui()
#epectimax_with_ui()
#variation_monte_carlo_tree_search_without_ui()
variation_monte_carlo_tree_search_with_ui()

# create test... don't don't use depth when testing Pure Monte Carlo tree search!
#create_tests_without_ui(1, 1, 1, 10, 3)
#create_tests_with_ui(1, 1, 1, 10, 3)
