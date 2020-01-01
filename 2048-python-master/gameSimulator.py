import random
from tkinter import Frame, Label, CENTER
import time

from logic import Logic
import constants as c
from AISearchesThread import AISearchGridThread
from numpy.random import shuffle
from AISearchesNoThread import AISearchGridNoThread


class GameGrid(Frame):
    """
        Simulates game UI
        Gets best move (from other classes) + adds it to simulation

        This class calculates the "best" next move.
        ->  we will iterates over each potential key (direction/ left, right, up or down) and pass them to the given
         search_function (search_function declaration is found in AISearchesThread.py or AISearchesNoThread.py).
        The return of this search_function obtains the "best" moves for each of those keys (directions).

        BEST PRACTISE: is to iterate multiple times over the keys (directions) this will eliminate
        lucky tile spawns in current matrix = make an average/total of all iterations per key (direction) and then
        choose best result as "best" move.
            -> "best" key moves are send to us from the used class (AISearchesNoThreads) via the given score_type

        score_type: in this class we have different ways that a child class
         (AISearchesThread.py or AISearchesNoThread.py) can give us potential "best" moves.
         score_type is the chosen method in this class that will be used to do so.
            -> methods: set_score(), set_score_lowest(), set_score_highest()
        search_function: the method of the child class we will ask to search the next "best" move in a given state
    """
    array_keys = ['\'a\'', '\'s\'', '\'d\'', '\'w\'']

    left_score = 0
    right_score = 0
    up_score = 0
    down_score = 0
    made_direction = None
    total_time_needed = 0
    average_time_per_move = 0

    def __init__(self, search_function, game_score_alg, score_type, depth, iterations):
        """

        :param search_function: search method that will be used
        :param game_score_alg: which Logic.[game score algorithm] you want to use
                    -> see Logic.py
        :param score_type: method through which child class will update best potential move (in this class)
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
        # Set up Frame (UI) to use
        Frame.__init__(self)

        self.grid()
        self.master.title('2048')

        # (NOT USED FOR THIS IMPLEMENTATION) used to bind keys for player input
        # self.master.bind("<Key>", self.key_down)

        # setting commands to change UI -> key press == left: logic.left
        self.commands = {c.KEY_UP:  Logic.up, c.KEY_DOWN:  Logic.down,
                         c.KEY_LEFT: Logic.left, c.KEY_RIGHT: Logic.right,
                         c.KEY_UP_ALT: Logic.up, c.KEY_DOWN_ALT: Logic.down,
                         c.KEY_LEFT_ALT: Logic.left, c.KEY_RIGHT_ALT: Logic.right,
                         c.KEY_H: Logic.left, c.KEY_L: Logic.right,
                         c.KEY_K: Logic.up, c.KEY_J: Logic.down}
        
        self.grid_cells = []
        self.init_grid()
        self.init_matrix()
        self.update_grid_cells()

        # Start of Search
        print("START")

        # Loop that iterates until game is over -> no more moves left
        while Logic.game_state_win_text(self.matrix) == 'not over':
            start_time = time.time()

            # Get best move -> see class documentation for more info of usage/best practise
            self.key_down_char(self.get_best_move(search_function, game_score_alg, score_type, depth, iterations))

            # Run time needed for a move
            run_time = time.time() - start_time
            # Adding al run_time values
            # -> Run time needed for all moves (until game_state != 'not over')
            self.total_time_needed += run_time
            self.average_time_per_move += 1

            # Printing extra info after each move of made direction, current score,
            # highest tile, run time needed
            print("\nMade direction: " + self.key_to_direction(self.made_direction))
            print("Current official score: " + str(Logic.game_score(self.matrix)))
            print("Current highest tile: " + str(Logic.highest_tile(self.matrix)))
            print("Time needed to find move: {} seconds".format(run_time))

            # Updates the UI state
            self.update()

        # End of search: game_state != 'not over'
        print("\nEND")

        # Printing extra info of game search results
        # -> total game score, Highest gotten tile, run time needed for all moves
        print("\nOfficial game score: " + str(Logic.game_score(self.matrix)))
        print("Highest tile: " + str(Logic.highest_tile(self.matrix)))
        print("Total time needed: {} seconds".format(self.total_time_needed))
        print("Time average per move: {} seconds".format(self.total_time_needed / self.average_time_per_move))
        print("Total moves made: {}".format(self.average_time_per_move))

        # set tile text of win
        if Logic.game_state_win_text(self.matrix) == 'win':
            self.grid_cells[1][1].configure(
                text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
            self.grid_cells[1][2].configure(
                text="Win!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)

        # Prevents UI from closing
        self.mainloop()

    def get_best_move(self, search_function, game_score_alg, score_type, depth, iterations):
        """
        This method (and class) calculate the "best" next move, meaning that we will iterates over
        each potential key (direction/ left, right, up or down) and pass them to the given search_function.
        The return of this search_function obtains the "best" moves for each of those keys (directions).

        BEST PRACTISE: is to iterate multiple times over the keys (directions) this will eliminate
        lucky tile spawns in current matrix = make an average/total of all iterations per key (direction) and then
        choose best result as "best" move.
            -> "best" key moves are send to us from the used class (AISearchesNoThreads) via the given score_type
        :param search_function: search method that will be used -> method of used class (AISearchesNoThreads)
        :param game_score_alg: which Logic.[game score algorithm] you want to use
                    -> see Logic.py
        :param score_type: method through which child class will update best potential move (in this class)
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
        :return key: "best" move
        """
        # Clear previous gotten best move scores
        self.clear()

        # See method documentation for detailed use description
        # Getting score of each key
        for key in range(4):
            # Iterations over search_function
            for i in range(iterations):
                _ = AISearchGridNoThread(self.matrix, self.history_matrixs, self.array_keys[key],
                              self, search_function, game_score_alg, score_type, depth)

        # Gets the key (left, up, down, right) with the highest obtained score
        # If highest key is actually multiple keys = coin flip
        highest_score_key = []

        if self.left_score == max(self.left_score, self.right_score, self.up_score, self.down_score):
            highest_score_key.append(self.array_keys[0])
        if self.down_score == max(self.left_score, self.right_score, self.up_score, self.down_score):
            highest_score_key.append(self.array_keys[1])
        if self.right_score == max(self.left_score, self.right_score, self.up_score, self.down_score):
            highest_score_key.append(self.array_keys[2])
        if self.up_score == max(self.left_score, self.right_score, self.up_score, self.down_score):
            highest_score_key.append(self.array_keys[3])

        # If highest key is actually multiple keys = coin flip
        if len(highest_score_key) > 1:
            return random.choice(highest_score_key)

        # Used in __init__ to print extra information
        self.made_direction = highest_score_key[0]

        # Return key that obtained highest score
        return highest_score_key[0]

    def get_best_move_thread(self, search_function, game_score_alg, score_type, depth, iterations):
        """
             This method (and class) calculate the "best" next move, meaning that we will iterates over
             each potential key (direction/ left, right, up or down) and pass them to the given search_function.
             The return of this search_function obtains the "best" moves for each of those keys (directions).

             BEST PRACTISE: is to iterate multiple times over the keys (directions) this will eliminate
             lucky tile spawns in current matrix = make an average/total of all iterations per key (direction) and then
             choose best result as "best" move.
                 -> "best" key moves are send to us from the used class (AISearchesNoThreads) via the given score_type
             :param search_function: search method that will be used -> method of used class (AISearchesThreads)
             :param game_score_alg: which Logic.[game score algorithm] you want to use
                         -> see Logic.py
             :param score_type: method through which child class will update best potential move (in this class)
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
             :return key: "best" move
             """
        # Keep track of amount of threads we use
        threads_used = 0

        # Clear previous gotten best move scores
        self.clear()

        # Holds instances of class AISearchGridThread
        gameGrid = []

        # See method documentation for detailed use description
        # Getting score of each key
        for key in range(4):
            # Iterations over search_function
            for i in range(iterations):
                gameGrid.append(AISearchGridThread(self.matrix, self.history_matrixs, self.array_keys[key],
                              self, search_function, game_score_alg, score_type, depth))
                threads_used += 1

        # Starting the threads
        for i in range(threads_used):
            gameGrid[i].start()
            gameGrid[i].setName("Thread " + str(threads_used))

        # Wait for all threads to finish
        for i in range(threads_used):
            gameGrid[i].join()

        # Gets the key (left, up, down, right) with the highest obtained score
        # If highest key is actually multiple keys = coin flip
        highest_score_key = []

        if self.left_score == max(self.left_score, self.right_score, self.up_score, self.down_score):
            highest_score_key.append(self.array_keys[0])
        if self.down_score == max(self.left_score, self.right_score, self.up_score, self.down_score):
            highest_score_key.append(self.array_keys[1])
        if self.right_score == max(self.left_score, self.right_score, self.up_score, self.down_score):
            highest_score_key.append(self.array_keys[2])
        if self.up_score == max(self.left_score, self.right_score, self.up_score, self.down_score):
            highest_score_key.append(self.array_keys[3])

        # If highest key is actually multiple keys = coin flip
        if len(highest_score_key) > 1:
            return random.choice(highest_score_key)

        # Used in __init__ to print extra information
        self.made_direction = highest_score_key[0]

        # Return key that obtained highest score
        return highest_score_key[0]

    def clear(self):
        """
        Clear previous gotten best move scores
        :return:
        """
        self.left_score = 0
        self.right_score = 0
        self.up_score = 0
        self.down_score = 0

    def set_score(self, key, total):
        """
        Method that is used in child class (AISearchesThread.py or AISearchesNoThread.py)
        to return us the potential "best" moves per key.
        :param key: move (direction) to allocate total with
        :param total: best/average score that the search made with given key
        :return:
        """
        # Need to check if tuple or not
        # Python sometimes sends key as tuple or char
        if isinstance(key, tuple):
            if key[0] == '\'a\'':
                self.left_score += total
            if key[0] == '\'s\'':
                self.down_score += total
            if key[0] == '\'d\'':
                self.right_score += total
            if key[0] == '\'w\'':
                self.up_score += total
        else:
            if key == '\'a\'':
                self.left_score += total
            if key == '\'s\'':
                self.down_score += total
            if key == '\'d\'':
                self.right_score += total
            if key == '\'w\'':
                self.up_score += total

    def set_score_lowest(self, key, total):
        """
        Method that is used in child class (AISearchesThread.py or AISearchesNoThread.py)
        to return us there scores per key (direction).
        Sets the lowest gotten total as score for given key (direction).
        :param key: move (direction) to allocate total with
        :param total: score that the search made with given key
        :return:
        """
        # Need to check if tuple or not
        # Python sometimes sends key as tuple or char
        if isinstance(key, tuple):
            if key[0] == '\'a\'':
                if self.left_score == 0:
                    self.left_score = total
                    return
                if self.left_score > total:
                    self.left_score = total
            if key[0] == '\'s\'':
                if self.down_score == 0:
                    self.down_score = total
                    return
                if self.down_score > total:
                    self.down_score = total
            if key[0] == '\'d\'':
                if self.right_score == 0:
                    self.right_score = total
                    return
                if self.right_score > total:
                    self.right_score = total
            if key[0] == '\'w\'':
                if self.up_score == 0:
                    self.up_score = total
                    return
                if self.up_score > total:
                    self.up_score = total
        else:
            if key == '\'a\'':
                if self.left_score == 0:
                    self.left_score = total
                    return
                if self.left_score > total:
                    self.left_score = total
            if key == '\'s\'':
                if self.down_score == 0:
                    self.down_score = total
                    return
                if self.down_score > total:
                    self.down_score = total
            if key == '\'d\'':
                if self.right_score == 0:
                    self.right_score = total
                    return
                if self.right_score > total:
                    self.right_score = total
            if key == '\'w\'':
                if self.up_score == 0:
                    self.up_score = total
                    return
                if self.up_score > total:
                    self.up_score = total

    def set_score_highest(self, key, total):
        """
        Method that is used in child class (AISearchesThread.py or AISearchesNoThread.py)
        to return us there scores per key (direction).
        Sets the highest gotten total as score for given key (direction).
        :param key: move (direction) to allocate total with
        :param total: score that the search made with given key
        :return:
        """
        if isinstance(key, tuple):
            if key[0] == '\'a\'':
                if self.left_score == 0:
                    self.left_score = total
                    return
                if self.left_score < total:
                    self.left_score = total
            if key[0] == '\'s\'':
                if self.down_score == 0:
                    self.down_score = total
                    return
                if self.down_score < total:
                    self.down_score = total
            if key[0] == '\'d\'':
                if self.right_score == 0:
                    self.right_score = total
                    return
                if self.right_score < total:
                    self.right_score = total
            if key[0] == '\'w\'':
                if self.up_score == 0:
                    self.up_score = total
                    return
                if self.up_score < total:
                    self.up_score = total
        else:
            if key == '\'a\'':
                if self.left_score == 0:
                    self.left_score = total
                    return
                if self.left_score < total:
                    self.left_score = total
            if key == '\'s\'':
                if self.down_score == 0:
                    self.down_score = total
                    return
                if self.down_score < total:
                    self.down_score = total
            if key == '\'d\'':
                if self.right_score == 0:
                    self.right_score = total
                    return
                if self.right_score < total:
                    self.right_score = total
            if key == '\'w\'':
                if self.up_score == 0:
                    self.up_score = total
                    return
                if self.up_score < total:
                    self.up_score = total

    def key_down_char(self, char):
        """
        Used to change self.matrix (game state) by moving the matrix (game) numbers to given direction (char)
        :param char: char = key = move (direction) to make
        :return:
        """
        key = char
        if key == c.KEY_BACK and len(self.history_matrixs) > 1:
            self.matrix = self.history_matrixs.pop()
            self.update_grid_cells()
            print('back on step total step:', len(self.history_matrixs))
        elif key in self.commands:
            self.matrix, done = self.commands[char](self.matrix)
            if done:
                self.matrix = Logic.add_tile(self.matrix)
                # record last move
                self.history_matrixs.append(self.matrix)
                self.update_grid_cells()
                done = False
                if Logic.game_state(self.matrix) == 'win':
                    self.grid_cells[1][1].configure(
                        text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(
                        text="Win!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                """if logic.game_state(self.matrix) == 'lose':
                    self.grid_cells[1][1].configure(
                        text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(
                        text="Lose!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)"""

    @staticmethod
    def key_to_direction(key):
        """
        Char key (direction) translation to direction in text
        :param key: move (direction) in char form
        :return: translation of char key (direction) to direction in text
        """
        if key == '\'a\'':
            return 'left'
        if key == '\'s\'':
            return 'down'
        if key == '\'d\'':
            return 'right'
        if key == '\'w\'':
            return 'up'

        return 'error'

    # NOT USED AT THE MOMENT -> made for user interaction = user plays game
    def key_down(self, event):

        key = repr(event.char)
        if key == c.KEY_BACK and len(self.history_matrixs) > 1:
            self.matrix = self.history_matrixs.pop()
            self.update_grid_cells()
            print('back on step total step:', len(self.history_matrixs))
        elif key in self.commands:
            self.matrix, done = self.commands[repr(event.char)](self.matrix)
            if done:
                self.matrix = Logic.add_tile(self.matrix)
                # record last move
                self.history_matrixs.append(self.matrix)
                self.update_grid_cells()
                done = False
                if Logic.game_state(self.matrix) == 'win':
                    self.grid_cells[1][1].configure(
                        text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(
                        text="Win!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                if Logic.game_state(self.matrix) == 'lose':
                    self.grid_cells[1][1].configure(
                        text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(
                        text="Lose!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)

    # NEXT METHODS ARE USED FOR MATRIX... NOT IN SCOPE OF ASSIGNMENT

    def generate_next(self):
        index = (self.gen(), self.gen())
        while self.matrix[index[0]][index[1]] != 0:
            index = (self.gen(), self.gen())
        self.matrix[index[0]][index[1]] = 2

    def init_grid(self):
        background = Frame(self, bg=c.BACKGROUND_COLOR_GAME,
                           width=c.SIZE, height=c.SIZE)
        background.grid()

        for i in range(c.GRID_LEN):
            grid_row = []
            for j in range(c.GRID_LEN):
                cell = Frame(background, bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                             width=c.SIZE / c.GRID_LEN,
                             height=c.SIZE / c.GRID_LEN)
                cell.grid(row=i, column=j, padx=c.GRID_PADDING,
                          pady=c.GRID_PADDING)
                t = Label(master=cell, text="",
                          bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                          justify=CENTER, font=c.FONT, width=5, height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    @staticmethod
    def gen(self):
        return random.randint(0, c.GRID_LEN - 1)

    def init_matrix(self):
        self.matrix = Logic.new_game(4)
        self.history_matrixs = list()
        self.matrix = Logic.add_tile(self.matrix)
        self.matrix = Logic.add_tile(self.matrix)

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
        self.update_idletasks()