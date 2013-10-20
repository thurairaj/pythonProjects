import ship
import copy
import random


class OrientationError(Exception):

    def __init__(self):
        pass


class Board(object):

    def __init__(self, row, coloumn):
        self.box = {}
        self.row = row
        name_len = len(str((row * coloumn) / 2)) + 1
        self.name = "|" + name_len * "_" + "|"
        self.coloumn = coloumn
        for i in range(row):
            for j in range(coloumn):
                self.box[(i, j)] = self.name

    def opponent_view(self):
        '''('self') --> str
        Return the board in a str form without showing ships'''
        test = ''
        shot_box = "|" + (len(self.name) - 2) * "#" + "|"
        shot_ship = "|" + (len(self.name) - 2) * "$" + "|"
        n = 0
        for items in range(self.coloumn):
            if len(str(items)) < len(self.name):
                test += "(" + str(items) + (len(self.name) - \
                                            len(str(items)) - 2) * " " + ")"
        for i in range(self.row):
            test += "\n"
            for j in range(self.coloumn):
                if (self.box[(i, j)]).strip() == self.name or\
                   (self.box[(i, j)]).strip() == shot_box or\
                   (self.box[(i, j)]).strip() == shot_ship:
                    test += ((self.box[(i, j)]).strip())
                else:
                    test += self.name
            test += '( %d)' % (n)

            n += 1
        return test

    def __str__(self):
        '''('self') --> str
        Return the board in a str form'''
        test = ''
        for items in range(self.coloumn):
            if len(str(items)) < len(self.name):
                test += "(" + str(items) + (len(self.name) - \
                                            len(str(items)) - 2) * " " + ")"

        for i in range(self.row):
            test += '\n'
            for j in range(self.coloumn):
                test += ((self.box[(i, j)]).strip())
            test += "(" + str(i) + ")"
        return test

    def fit_ship(self, len_ship, row, coloumn, orientation):
        '''(self, int, int, int, str) --> bool
        Return True if the ship fits into the board, Return False if not'''
        try:
            if orientation == "v":
                for x in range(row, len_ship + row):
                    if self.box[x, coloumn] != self.name:
                        return False

            elif orientation == "h":
                for y in range(coloumn, len_ship + coloumn):
                    if self.box[row, y] != self.name:
                        return False

            else:
                return False
        except KeyError:
            return False

        return True

    def placing_ship(self, len_ship, row, coloumn, orientation, name):
        '''(self, int, int, str, str) ---> None
        Replace key of self.box to name'''
        if orientation == "v":
            for x in range(row, len_ship + row):
                self.box[x, coloumn] = "|%s|" % (name)

        elif orientation == "h":
            for y in range(coloumn, len_ship + coloumn):
                self.box[row, y] = "|%s|" % (name)

        else:
            raise OrientationError

    def shot(self, position, ship):
        ''' (self, tuple, ship(class)) --> list or str or bool
        Replace the value of self.box[position] to |##| if the box is empty
        else return false and if the board does not contain particular ship,
        then return that ship in list form'''
        try:
            before = self.box.values()

            specific_ship = self.box[position]
            if self.box[position] == "|" + (len(self.name) - 2) * "#" + "|" \
               or self.box[position] == "|" + (len(self.name) - 2) * "$" + "|":
                return False

            if self.box[position] != self.name:
                self.box[position] = "|" + (len(self.name) - 2) * "$" + "|"
            else:
                self.box[position] = "|" + (len(self.name) - 2) * "#" + "|"

            after = self.box.values()

            for items in before:
                if items not in after and items != self.name:
                    ship.kill_ship(items)
                    return [items]

            if specific_ship != self.name:
                return specific_ship

        except KeyError:
            return False

    def max_ship(self, len_ship):
        '''(self, int) --> int
        Return the maximum ship that can be placed on the board'''
        box_copy = self.box.copy()
        number_ship1 = self.help2_max(len_ship, "h", "v")
        self.box = box_copy.copy()
        number_ship2 = self.help2_max(len_ship, "v", "h")
        self.box = box_copy.copy()
        number_ship3 = self.help_max(len_ship, "h", "v")
        self.box = box_copy.copy()
        number_ship4 = self.help_max(len_ship, "v", "h")
        self.box = box_copy.copy()
        number_ship5 = self.help3_max(len_ship, "v")
        self.box = box_copy.copy()
        number_ship6 = self.help3_max(len_ship, "h")
        self.box = box_copy.copy()
        number_ship7 = self.help4_max(len_ship, "h")
        self.box = box_copy.copy()
        number_ship8 = self.help4_max(len_ship, "v")
        self.box = box_copy.copy()

        return max(number_ship1, number_ship2, number_ship3, number_ship4,\
                   number_ship5, number_ship6, number_ship7, number_ship8)

    def random_placing(self, name, len_ship, k=0):
        '''(self, str, int, int) --> None
        Replace the self.box's value to name, the key is selected randomly'''
        while len(name) < len(self.name) - 2:
            name = name + '-'
        while k < 4:
            row = random.randint(0, self.row - 1)
            coloumn = random.randint(0, self.row - 1)

            if self.fit_ship(len_ship, row, coloumn, 'h'):
                self.placing_ship(len_ship, row, coloumn, 'h', name)
                return "Done"
            else:
                if self.fit_ship(len_ship, row, coloumn, 'v'):
                    self.placing_ship(len_ship, row, coloumn, 'v', name)
                    return "Done"
                else:
                    k += 1

        if k >= 4:
            for i in range(0, self.row):
                for j in range(0, self.coloumn):
                    orientation = "h"
                    if self.fit_ship(len_ship, i, j, orientation):
                        self.placing_ship(len_ship, i, j, orientation, name)
                        return "Done"

                    else:
                        orientation = "v"
                        if self.fit_ship(len_ship, i, j, orientation):
                            self.placing_ship(len_ship, i, j, \
                                              orientation, name)
                            return "Done"

                        else:
                            orientation = "h"

    def help_max(self, len_ship, first_orientation, second_orientation):
        row = self.row
        coloumn = self.coloumn
        x = 0
        y = 0
        number_ship = 0

        for i in range(0, row):
            for j in range(0, coloumn):

                orientation = first_orientation
                if self.fit_ship(len_ship, i, j, orientation):
                    self.placing_ship(len_ship, i, j, orientation, "po")
                    number_ship += 1

                else:
                    orientation = second_orientation
                    if self.fit_ship(len_ship, i, j, orientation):
                        self.placing_ship(len_ship, i, j, orientation, "po")
                        number_ship += 1

                    else:
                        orientation = first_orientation

        return number_ship

    def help2_max(self, len_ship, first_orientation, second_orientation):
        row = self.row
        coloumn = self.coloumn
        x = 0
        y = 0
        number_ship = 0

        for i in range(0, coloumn):
            for j in range(0, row):

                orientation = first_orientation

                if self.fit_ship(len_ship, j, i, orientation):
                    self.placing_ship(len_ship, j, i, orientation, "po")
                    number_ship += 1

                else:
                    orientation = second_orientation
                    if self.fit_ship(len_ship, j, i, orientation):
                        self.placing_ship(len_ship, j, i, orientation, "po")
                        number_ship += 1

                    else:
                        orientation = first_orientation
        return number_ship

    def help3_max(self, len_ship, first_orientation):
        row = self.row
        coloumn = self.coloumn
        x = 0
        y = 0
        number_ship = 0

        for i in range(0, coloumn):
            for j in range(0, row):
                orientation = first_orientation
                if self.fit_ship(len_ship, j, i, orientation):
                    self.placing_ship(len_ship, j, i, orientation, "po")
                    number_ship += 1
                else:
                    orientation = first_orientation
        return number_ship

    def help4_max(self, len_ship, first_orientation):
        row = self.row
        coloumn = self.coloumn
        x = 0
        y = 0
        number_ship = 0

        for i in range(0, row):
            for j in range(0, coloumn):
                orientation = first_orientation
                if self.fit_ship(len_ship, i, j, orientation):
                    self.placing_ship(len_ship, i, j, orientation, "po")
                    number_ship += 1
                else:
                    orientation = first_orientation

    def create_ship(self):
        '''(self)---> dict
        Return dictionary whih is inverted dictionary of self.box'''
        boats = {}
        for point in self.box:

            if self.box[point] not in boats and self.box[point] != self.name:
                boats[self.box[point]] = [point]
            elif self.box[point] in boats and self.box[point] != self.name:
                boats[self.box[point]].append(point)

            shot_box = "|" + (len(self.name) - 2) * "#" + "|"
            if shot_box in boats:
                del(boats[shot_box])

        return boats
