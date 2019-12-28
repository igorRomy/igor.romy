import random

from logic import Logic
import constants as c
import copy
from collections import defaultdict


class AISearchGridNoThread:
    """
    Used to run AI searches
    Every search method in this class will first move the given matrix to a given direction(key)
    then they will run there "Formula" that returns best average/total score that they got.
    This score is used in parent class to calculate "best" next move

    Don't forget: parent class has to calculate "best" next move, meaning that parent class iterates over
    each potential key (direction/ left, right, up or down) and through the return of this class obtains best moves
    for each of those keys(directions).

    Best practise is to let parent class iterate multiple times over the keys (directions) this will eliminate
    lucky tile spawns in current matrix = make an average/total of all iterations per key (direction) and then choose
    best result as "best" move
        -> (of course) this will also give best result in general
    """
    left_score = 0
    right_score = 0
    up_score = 0
    down_score = 0
    array_keys = ['\'a\'', '\'s\'', '\'d\'', '\'w\'']
    array_keys_to_shuffle = ['\'a\'', '\'s\'', '\'d\'', '\'w\'']
    history_matrix = None
    matrix = None
    grid_cells = None
    parent_game_grid = None
    key = None
    allScores = []

    def __init__(self, matrix, list, key, parent_game_grid, search_function, game_score_alg, score_type, depth):
        """
        Initiates instance of class
        :param matrix: matrix (game state) to be used
        :param list: NOT USED BUT STILL NEEDS TO BE PRESENT, history_matrix: records last move for potential back track
        :param key: first move (direction) the given method (search_function) has to make
        :param parent_game_grid: parent class that is used, to update best potential moves via score_type
        :param search_function: search method that will be used
        :param game_score_alg: which Logic.[game score algorithm] you want to use
                    -> see Logic.py
        :param score_type: is a parent class method through which this class will update best potential move
        :param depth: the depth you want the search tree's to have
        """
        self.matrix = matrix
        self.list = list
        self.key = key,
        self.parent_game_grid = parent_game_grid
        self.grid_cells = []
        self.init_matrix(self.list, self.matrix)

        # Runs your chosen search_function and then updates best potential move in parent (via score_type)
        getattr(self.parent_game_grid, score_type)(self.key, getattr(self, search_function)(self.key,
                                                                                            game_score_alg, depth))

    def pure_monte_carlo_tree_search(self, key, game_score_alg, depth=None):
        """
        After making a move in a given direction(key), the method will iterate over
        the game (self.matrix) until there are no more moves to be made.
            -> return score
        :param key: first move (direction) the method has to make
        :param game_score_alg: the algorithm to be used
                to calculate the end score -> found in logic.py
        :param depth: depth value is not used...
                only when Logic.game_state != 'not over'
                the iteration will be stopped
        :return score: calculated by given game_score_alg
        """

        test_stuck_move_p1 = copy.deepcopy(self.matrix)

        # First movement in given direction
        self.key_down_char(key)

        # Tests if board has changed after first move
        #  -> THE GIVEN DIRECTION CAN'T MOVE BOARD = RETURN LOWEST SCORE (0)
        if test_stuck_move_p1 == self.matrix:
            return 0

        # Random moves until no moves can be made
        while Logic.game_state(self.matrix) == 'not over':
            self.key_down_char(random.choice(self.array_keys_to_shuffle))

        # Returning gotten score
        return getattr(Logic, game_score_alg)(self.matrix)

    def expectimax(self, key, game_score_alg, depth):
        """
         After making a move in given direction(key), the method will copy
         the current game state (depth 0/ node 1) -> create 4 new nodes in depth 1
         (4 new game states created by moving left,right,up or down from previous game state).
         This is repeated until given depth is achieved
            EXTRA: Each depth has 4 times more nodes than the previous depth
        :param key: first move (direction) the method has to make
        :param game_score_alg: the algorithm to be used
                to calculate the end score -> found in logic.py
        :param depth: depth value is not used...
                only when Logic.game_state != 'not over'
                the iteration will be stopped
        :return score: max gotten score
        """
        test_stuck_move_p1 = copy.deepcopy(self.matrix)

        # First movement in given direction
        self.key_down_char(key[0])

        # Tests if board has changed after first move
        #  -> THE GIVEN DIRECTION CAN'T MOVE BOARD = RETURN LOWEST SCORE (0)
        if test_stuck_move_p1 == self.matrix:
            return 0

        # All scores achieved at max depth are appended to list
        all_scores = []
        # See count as amount of nodes...
        # The more the depth is expanded the more nodes each depth will have
        # EXTRA: each deeper depth has 4 times more nodes than the previous depth
        count = 4
        # When we first iterate we start with a single node (first node)
        # To achieve depth scalability 'first_enter' notifies us that we only have one node
        first_enter = True
        # first_enter stays True until we have iterated over the fist node 4 times
        # -> number 4 = the possible directions (left,right,up,down)
        first_enter_counter = 0
        # Dictionary we use to keep track/save all nodes at each depth
        # -> used as: test_matrix[depth][node][key]
        test_matrix = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

        # This is the actual "formula" we use
        # We iterate until wanted depth is achieved
        # With every iteration the tree is expanded -> how higher depth how more nodes (game states)
        # When iteration is finished we return the best score (gotten from a node).
        t = True
        for depth_iteration in range(depth):
            key_rotation = 0
            past_node = 0
            counter = 0
            for node in range(count):
                counter += 1
                if first_enter:
                    first_enter_counter += 1
                    matrix_copy = copy.deepcopy(self.matrix)
                    test_matrix[depth_iteration][node] = self.key_down_char_with_matrix(self.array_keys[node], matrix_copy)

                    if first_enter_counter == 4:
                        count *= 4
                        first_enter = False
                else:
                    test_matrix[depth_iteration][node] = self.key_down_char_with_matrix(
                        self.array_keys[key_rotation], test_matrix[depth_iteration-1][past_node])
                    if key_rotation == 3:
                        key_rotation = 0
                    else:
                        key_rotation += 1
                if counter % 4 == 0:
                    past_node += 1
            # Next iteration will have 4 times more nodes... count = quantity of nodes
            if not t:
                count *= 4
            t = False
        # Iterating every node in max depth and adding there game score to all_scores
        for node in range(int(count/4)):
            all_scores.append(getattr(Logic, game_score_alg)(test_matrix[depth-1][node]))

        # Return highest gotten score of all nodes
        return max(all_scores)

    def variation_monte_carlo_tree_search(self, key, game_score_alg, depth):
        """
        After making a move in a given direction(key), the method will iterate over 4 copies of
        the current game state (self.matrix) performing random moves for each copy,
        starting with a defined key (first direction isn't random) until no more moves can be made.

        From this iteration we will get the copy that scored best with his starting key.
        This key is then used to perform a move in self.matrix (updating current game state).
        From this new current game state (self.matrix) we will redo the iteration until given depth is reached.
            -> return average best score
        :param key: first move (direction) the method has to make
        :param game_score_alg: the algorithm to be used
                to calculate the end score -> found in logic.py
        :param depth: depth value is not used...
                only when Logic.game_state != 'not over'
                the iteration will be stopped
        :return score: average of best gotten scores
        """
        test_stuck_move_p1 = copy.deepcopy(self.matrix)

        # First movement in given direction
        self.key_down_char(key[0])

        # Tests if board has changed after first move
        #  -> THE GIVEN DIRECTION CAN'T MOVE BOARD = RETURN LOWEST SCORE (0)
        if test_stuck_move_p1 == self.matrix:
            return 0

        # Total of all highest gotten scores for each depth iteration
        total = 0
        # All scores achieved at max depth are appended to list
        all_scores = []
        # Array to keep track/save matrix (game state)
        test_matrix = [1, 2, 3, 4]

        # past_best_score and next_key are used together...
        # When iterating: if the past_best_score is updated to a higher score...
        # the key (direction) accountable for giving this higher score is kept in next_key

        # Keeps highest gotten score until... now
        past_best_score = 0
        # Keeps next key(direction) to be used
        next_key = ""

        # This is the actual "formula" we use
        # We iterate until wanted depth is achieved
        # Each key iteration will give the best next_key (next move) for current depth
        # Each depth_iteration iteration will use next_key to perform next move
        # and append best achieved score (until then) to all_scores
        for depth_iteration in range(depth):
            for key in range(4):
                test_matrix[key] = self.key_down_char_with_matrix(self.array_keys[key], copy.deepcopy(self.matrix))
                # Random moves until no moves can be made
                while Logic.game_state(test_matrix[key]) == 'not over':
                    test_matrix[key] = self.key_down_char_with_matrix(random.choice(self.array_keys_to_shuffle),
                                                                      test_matrix[key])
                if past_best_score < getattr(Logic, game_score_alg)(test_matrix[key]):
                    past_best_score = getattr(Logic, game_score_alg)(test_matrix[key])
                    next_key = self.array_keys[key]

            # Append best achieved score (until now) to all_scores
            all_scores.append(past_best_score)
            # Use next_key to perform next move
            self.key_down_char(next_key)

        for i in range(len(all_scores)):
            total += all_scores[i]

        # Monte Carlo Tree Search normally returns average gotten score
        return total/len(all_scores)

    def key_down_char(self, key):
        """
        Used to change self.matrix (game state) by moving the matrix (game) numbers to given direction (key)
        :param key: move (direction) to make
        :return:
        """
        # Used to check if Logic.[direction] worked
        done = None
        # Need to check if tuple or not
        # Python sometimes sends key as tuple or char
        if isinstance(key, tuple):
            if key[0] == '\'a\'':
                self.matrix, done = Logic.left(self.matrix)
            if key[0] == '\'s\'':
                self.matrix, done = Logic.down(self.matrix)
            if key[0] == '\'d\'':
                self.matrix, done = Logic.right(self.matrix)
            if key[0] == '\'w\'':
                self.matrix, done = Logic.up(self.matrix)
        else:
            if key == '\'a\'':
                self.matrix, done = Logic.left(self.matrix)
            if key == '\'s\'':
                self.matrix, done = Logic.down(self.matrix)
            if key == '\'d\'':
                self.matrix, done = Logic.right(self.matrix)
            if key == '\'w\'':
                self.matrix, done = Logic.up(self.matrix)

        if done:
            # Logic.[direction] worked = add new tile (game rules)
            self.matrix = Logic.add_tile(self.matrix)
            # NOT USED, record last move for potential back track
            # self.history_matrix.append(self.matrix)
            # ONLY used in UI
            # self.update_grid_cells()
            # done = False

    def key_down_char_with_matrix(self, key, given_matrix):
        """
        Used to change given_matrix (game state) by moving the matrix (game) numbers to given direction (key)
            -> returns updated given_matrix
        :param key: move (direction) to make
        :param given_matrix: matrix (game state) to update
        :return: updated given_matrix
        """
        # Used to check if Logic.[direction] worked
        done = None
        # Need to check if tuple or not
        # Python sometimes sends key as tuple or char
        if isinstance(key, tuple):
            if key[0] == '\'a\'':
                given_matrix, done = Logic.left(given_matrix)
            if key[0] == '\'s\'':
                given_matrix, done = Logic.down(given_matrix)
            if key[0] == '\'d\'':
                given_matrix, done = Logic.right(given_matrix)
            if key[0] == '\'w\'':
                given_matrix, done = Logic.up(given_matrix)
        else:
            if key == '\'a\'':
                given_matrix, done = Logic.left(given_matrix)
            if key == '\'s\'':
                given_matrix, done = Logic.down(given_matrix)
            if key == '\'d\'':
                given_matrix, done = Logic.right(given_matrix)
            if key == '\'w\'':
                given_matrix, done = Logic.up(given_matrix)

        if done:
            # Logic.[direction] worked = add new tile (game rules)
            self.matrix = Logic.add_tile(given_matrix)
            # NOT USED, record last move for potential back track
            # self.history_matrix.append(self.matrix)
            # ONLY used in UI
            # self.update_grid_cells()
            # done = False

        return given_matrix

    # NEXT METHODS ARE USED FOR MATRIX... NOT IN SCOPE OF ASSIGNMENT

    @staticmethod
    def gen(self):
        return random.randint(0, c.GRID_LEN - 1)

    def init_matrix(self, list, matrix):
        self.matrix = Logic.new_game(4)
        # self.history_matrix = list
        self.matrix = matrix

    # NEXT METHODS ARE NOT USED AT THE MOMENT

    def get_matrix(self):
        return self.matrix

    def update_grid_cells(self):
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(
                        text="", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(
                        new_number), bg=c.BACKGROUND_COLOR_DICT[new_number],
                        fg=c.CELL_COLOR_DICT[new_number])

        # NOT USED AT THE MOMENT
        #self.update_idletasks()

    def generate_next(self):
        index = (self.gen(), self.gen())
        while self.matrix[index[0]][index[1]] != 0:
            index = (self.gen(), self.gen())
        self.matrix[index[0]][index[1]] = 2
