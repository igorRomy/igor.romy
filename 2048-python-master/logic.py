#
# CS1010FC --- Programming Methodology
#
import random
import copy
from numpy.ma import absolute

import constants


class Logic:
    """
    Has the "logic" of the grid
    It can move/merge the grid (when user/AI wants to go in a sertain direction this class will perform
        the movement of the data/matrix/grid)
    It reads the values on the grid = get: score, game state

    Extra: (NOT USED in this implementation) can reverse previous movements
        to do so you need to use history matrix in your parent class...
    """

    @staticmethod
    def new_game(n):
        """
        Initiates new game = matrix set up
        :param n:
        :return matrix:
        """
        matrix = []

        for i in range(n):
            matrix.append([0] * n)
        return matrix

    @staticmethod
    def add_tile(matrix):
        """
        Official way -> Adds new tile, value 2 (80% chance) or 4 (20% chance), to the given matrix
            Game rules: after a move in the game you have to add a new tile
        :param matrix:
        :return matrix:
        """
        a = random.randint(0, len(matrix)-1)
        b = random.randint(0, len(matrix)-1)
        while matrix[a][b] != 0:
            a = random.randint(0, len(matrix)-1)
            b = random.randint(0, len(matrix)-1)

        # setting chance of getting tile : value 2 (80% chance) or 4 (20% chance), to the given matrix
        population = [2, 4]
        weights = [0.8, 0.2]
        matrix[a][b] = random.choices(population, weights)[0]

        return matrix

    @staticmethod
    def add_two(matrix):
        """
        Adds new tile, value 2
            Game rules: after a move in the game you have to add a new tile
        :param matrix:
        :return matrix:
        """
        a = random.randint(0, len(matrix) - 1)
        b = random.randint(0, len(matrix) - 1)
        while matrix[a][b] != 0:
            a = random.randint(0, len(matrix) - 1)
            b = random.randint(0, len(matrix) - 1)

        matrix[a][b] = 2

        return matrix

    @staticmethod
    def game_score_count_tile_values(matrix):
        """
        Counts the total score of a matrix/game: sum of the tile values
        :param matrix:
        :return total_score:
        """
        total_score = 0
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                total_score += matrix[i][j]

        return total_score

    @staticmethod
    def game_score(matrix):
        """
        Official way to score points -> higher tiles get more points than just their shown value
        Counts the total score of a matrix/game: please see implementation, example: tile value 8 = (2+2) + (2+2) + (4+4),
        Rule: tile of value 2 = score 0
        :param matrix:
        :return total_score:
        """
        total_score = 0

        for i in range(len(matrix)):
            for j in range(len(matrix[0])):

                value_to_multiply_tile = 0
                tile_copy = copy.deepcopy(matrix[i][j])

                # a tile of worth 0 = an empty tile in game
                if tile_copy != 0 or tile_copy != 2:
                    while tile_copy > 2:
                        value_to_multiply_tile += 1
                        tile_copy /= 2
                    total_score += matrix[i][j] * value_to_multiply_tile

        return total_score

    # using weight matrix
    @staticmethod
    def game_score_with_weight_matrix(matrix):
        """
        Counts the total score of a matrix/game: using formula of game_score() + multiplying it by the positional weight
            of the tile (WEIGHT_MATRIX in constants.py)
        :param matrix:
        :return total_score:
        """
        total_score = 0

        # formula of game_score()
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):

                value_to_multiply_tile = 0
                tile_copy = copy.deepcopy(matrix[i][j])

                # a tile of worth 0 = an empty tile in game
                if tile_copy != 0 or tile_copy != 2:
                    while tile_copy > 2:
                        value_to_multiply_tile += 1
                        tile_copy /= 2

                    # multiplying by positional weight
                    total_score += (matrix[i][j] * value_to_multiply_tile) * constants.WEIGHT_MATRIX[i][j]

                # multiplying the positional weight to a tile with value 2
                if matrix[i][j] == 2:
                    total_score += matrix[i][j] * constants.WEIGHT_MATRIX[i][j]

        return total_score

    # using weight matrix zigzag
    @staticmethod
    def game_score_with_weight_matrix_zig_zag(matrix):
        """
        Counts the total score of a matrix/game: using formula of game_score() + multiplying it by the positional weight
            of the tile (WEIGHT_MATRIX2 in constants.py)
        :param matrix:
        :return total_score:
        """
        total_score = 0

        # formula of game_score()
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):

                value_to_multiply_tile = 0
                tile_copy = copy.deepcopy(matrix[i][j])

                # a tile of worth 0 = an empty tile in game
                if tile_copy != 0 or tile_copy != 2:
                    while tile_copy > 2:
                        value_to_multiply_tile += 1
                        tile_copy /= 2

                    # multiplying by positional weight
                    total_score += (matrix[i][j] * value_to_multiply_tile) * constants.WEIGHT_MATRIX2[i][j]

                # multiplying the positional weight to a tile with value 2
                if matrix[i][j] == 2:
                    total_score += matrix[i][j] * constants.WEIGHT_MATRIX2[i][j]

        return total_score

    # using weight matrix and penalty score
    @staticmethod
    def game_score_with_weight_matrix_and_penalty(matrix):
        """
         Counts the total score of a matrix/game: using formula of game_score_with_weight_matrix() + penalty score
            penalty score =
        :param matrix:
        :return total_score:
        """
        total_score = 0
        penalty = 0
        neighbourScore = 0

        # formula of game_score()
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):

                value_to_multiply_tile = 0
                tile_copy = copy.deepcopy(matrix[i][j])

                # a tile of worth 0 = an empty tile in game
                if tile_copy != 0 or tile_copy != 2:
                    while tile_copy > 2:
                        value_to_multiply_tile += 1
                        tile_copy /= 2

                    # multiplying by positional weight
                    total_score += (matrix[i][j] * value_to_multiply_tile) * constants.WEIGHT_MATRIX[i][j]

                # multiplying the positional weight to a tile with value 2
                if matrix[i][j] == 2:
                    total_score += matrix[i][j] * constants.WEIGHT_MATRIX[i][j]

                if matrix[i][j] == 0:
                    # freeSpaceScore += 50
                    pass

                # Getting the neighbours tile values of current tile
                # If tile at position [i][j] doesn't exist... just skip to the next
                try:
                    neighbourScore += matrix[i][j+1]
                except IndexError:
                    pass
                try:
                    neighbourScore += matrix[i+1][j]
                except IndexError:
                    pass
                try:
                    neighbourScore += matrix[i][j - 1]
                except IndexError:
                    pass
                try:
                    neighbourScore += matrix[i-1][j]
                except IndexError:
                    pass

                penalty += absolute(matrix[i][j] - neighbourScore)

        return total_score + penalty

    @staticmethod
    def game_state(matrix):
        """
        Gives the current game state:
            'win' = gotten a tile of 2048 (NOT USED)
            'lose' = no empty tiles + no merges possible (no moves)
            'not over" =  no 'lose' or 'win', keep on playing
        :param matrix:
        :return game_state:  'win' | 'lose' | 'not over'
        """

        """
        # To set winning tile
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == 2048:
                    # return 'win'
                    # return 'not over'
            """
        for i in range(len(matrix)-1):
            # intentionally reduced to check the row on the right and below
            # more elegant to use exceptions but most likely this will be their solution
            for j in range(len(matrix[0])-1):
                if matrix[i][j] == matrix[i+1][j] or matrix[i][j+1] == matrix[i][j]:
                    return 'not over'
        for i in range(len(matrix)):  # check for any zero entries
            for j in range(len(matrix[0])):
                if matrix[i][j] == 0:
                    return 'not over'
        for k in range(len(matrix)-1):  # to check the left/right entries on the last row
            if matrix[len(matrix)-1][k] == matrix[len(matrix)-1][k+1]:
                return 'not over'
        for j in range(len(matrix)-1):  # check up/down entries on last column
            if matrix[j][len(matrix)-1] == matrix[j+1][len(matrix)-1]:
                return 'not over'
        return 'lose'

    @staticmethod
    def highest_tile(matrix):
        tile = 0
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] > tile:
                    tile = matrix[i][j]

        return tile

    @staticmethod
    def reverse(matrix):
        """
        (NOT USED in this implementation) can reverse previous movements
            to do so you need to use history matrix in your parent class...
        :param matrix:
        :return new:
        """
        new = []
        for i in range(len(matrix)):
            new.append([])
            for j in range(len(matrix[0])):
                new[i].append(matrix[i][len(matrix[0])-j-1])
        return new

    # NEXT METHODS ARE USED FOR MATRIX CHANGES... NOT IN SCOPE OF ASSIGNMENT

    @staticmethod
    def transpose(matrix):
        new = []
        for i in range(len(matrix[0])):
            new.append([])
            for j in range(len(matrix)):
                new[i].append(matrix[j][i])
        return new

    @staticmethod
    def cover_up(matrix):
        new = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        done = False
        for i in range(4):
            count = 0
            for j in range(4):
                if matrix[i][j] != 0:
                    new[i][count] = matrix[i][j]
                    if j != count:
                        done = True
                    count += 1
        return new, done

    @staticmethod
    def merge(matrix):
        done = False
        for i in range(4):
            for j in range(3):
                if matrix[i][j] == matrix[i][j+1] and matrix[i][j] != 0:
                    matrix[i][j] *= 2
                    score = matrix[i][j] *2
                    matrix[i][j+1] = 0
                    done = True
        return matrix, done

    @staticmethod
    def up(game):
        # print("up")
        # return matrix after shifting up
        game = Logic.transpose(game)
        game, done = Logic.cover_up(game)
        temp = Logic.merge(game)
        game = temp[0]
        done = done or temp[1]
        game = Logic.cover_up(game)[0]
        game = Logic.transpose(game)
        return game, done

    @staticmethod
    def down(game):
        # print("down")
        game = Logic.reverse(Logic.transpose(game))
        game, done = Logic.cover_up(game)
        temp = Logic.merge(game)
        game = temp[0]
        done = done or temp[1]
        game = Logic.cover_up(game)[0]
        game = Logic.transpose( Logic.reverse(game))
        return game, done

    @staticmethod
    def left(game):
        # print("left")
        # return matrix after shifting left
        game, done = Logic.cover_up(game)
        temp = Logic.merge(game)
        game = temp[0]
        done = done or temp[1]
        game = Logic.cover_up(game)[0]
        return game, done

    @staticmethod
    def right(game):
        # print("right")
        # return matrix after shifting right
        game = Logic.reverse(game)
        game, done = Logic.cover_up(game)
        temp = Logic.merge(game)
        game = temp[0]
        done = done or temp[1]
        game = Logic.cover_up(game)[0]
        game = Logic.reverse(game)
        return game, done
