from board import Board
from ship import Ship
import sound
import random
import copy
import cPickle


def validation(username, password, new_user):
    '''(str, str, str)---> dict or bool
    Return dictionary users if available else,
    Return False and if the key(usename) of users does
    not match with value(password), Return False'''
    if new_user == "new":
        return creation(username, password)
    try:
        f = open('users.data')
        users = cPickle.load(f)
        f.close
        if users[username] != password:
            print "the username and password didn't match, try again"
            return False
    except Exception:
        return False

    return users


def creation(username, password):
    '''(str,str)--> dict
    Return a dict with the username as key and password as value'''
    try:

        f = open('users.data')
        users = cPickle.load(f)
        f.close

        while username in users:
            print "the username is already exist choose a different username"
            return False
        users[username] = password

    except IOError:
        users = {}
        users[username] = password
    return users


def ask_dimension():
    ''' (None) ---> tuple
    Return a tuple which made up of an int from user's input'''
    area = raw_input("Give your dimension of board, n such that\
n * n board is produced \t: ")
    try:
        area = int(area)
        tup = (area, area)
        if tup[0] * tup[1] < 4:
            print "Your dimension should be bigger than 1x1"
            raise Exception
        return tup
    except Exception:
        print "please provide valid input"
        return ask_dimension()


def manual_placing(board, num_ship, len_ship, name, i=0):
    '''(board, int, int, str, int) --> str
    Return "Done" if all the ship is successfully placed'''

    while i < num_ship:

            row = input("Please provide the row : ")
            coloumn = input("Please provide the coloumn  : ")
            orientation = raw_input("Please provide the orientation \
of the ship : ")
            ship_name = name + str(i)
            if board.fit_ship(len_ship, row, coloumn, orientation) == False:
                print "Please provide valid inputs for placing the ship"
                return manual_placing(board, num_ship, len_ship, name, i=0)

            board.placing_ship(len_ship, row, coloumn, orientation, ship_name)
            i += 1
            print board
    return "done"


def auto_placing(board, num_ship, len_ship, name):
    '''(board, int, int, str) --> None
    Automatically place the ships on the board'''

    i = 0
    while i < num_ship:
        name = name + str(i)
        random_placing(name, len_ship)


def ask_ship(board, k=0):
    '''(board, int) --> list
    Print the maximum of each kind of ships the player can have.
    Ask the player to input the amount of each kind of ship they
    want. If the input is invalid, the function will ask again.
    Return a list of ints which represent the amount of each ships.
    '''
    ships = ["aircraft", "submarine", "destroyer", "patrol"]

    e_list = []

    while k < 4:
        patrol = -1
        if board.max_ship(5 - k) == 0:
            patrol = 0
            e_list.append(0)

        print "maximum %s is %d" % (ships[k], board.max_ship(5 - k))
        if patrol == -1:
            while 1:
                try:
                    patrol = input("How many ships are you wishing\
to have? \t:")
                    break
                except Exception:
                    pass

            while patrol > board.max_ship(5 - k) or patrol == -1:
                print "maximum patrol ship is %d" % (board.max_ship(5 - k))
                patrol = input("How many patrol ships are you wishing\
to have? \t:")
            manual_placing(board, patrol, 5 - k, ships[k][0])

            e_list.append(patrol)
        k += 1

    return e_list


def second_ask(board, board2, l, method="manual"):
    '''(board, board, list, str) --> str
    If the player want the amount of ships is bigger than the maximum that
    the board can place, ask player for the amount again and automatically
    or manually placing on the board.'''

    ships = ["aircraft", "submarine", "destroyer", "patrol"]
    before = board.box.copy()
    if method == "auto":
        board2.box = before
        return auto_fill(board1, board2)

    for k in range(4):
        maxim = board.max_ship(5 - k)
        if maxim < l[k]:
            print "you will not have enough space to place all the ships, \
so please rearrange your order or you can choose computer to arrange for you"
            method = raw_input("To switch to auto pleae type 'auto' if not \
just press ENTER:")
            board.box = before
            return second_ask(board, l, method)
        print "\n now you can place your %s ships" % (ships[k])
        manual_placing(board, l[k], 5 - k, ships[k][0])

    return "DONE"


def auto_fill(board1, board2=0):
    '''(board, board) --> list
    Ask for the input of the value of each ship.Random placing the ship
    and return a list with the int of the ships which havnt filled on
    the board.'''
    ships = ["aircraft", "submarine", "destroyer", "patrol"]
    new_ship_list = []
    t = 0

    for k in range(4):
        patrol = -1
        i = 0

        if board2 != 0:
            minimum_value = min(board1.max_ship(5 - k), board2.max_ship(5 - k))
        else:
            minimum_value = board1.max_ship(5 - k)

        if minimum_value == 0:
            patrol = 0

        if patrol == -1:
            print "maximum %s is %d" % (ships[k], minimum_value)
            while 1:
                try:
                    patrol = input("How many ship are you wishing\
                    to have? \t:")
                    break
                except:
                    pass

        while minimum_value < patrol:
            print "maximum %s ship is %d" % (ships[k], minimum_value)
            patrol = input("How many patrol ships are you wishing\
to have? \t:")
            while 1:
                try:
                    patrol = input("How many ship are you wishing\
to have? \t:")
                    break
                except:
                    pass

        while i < patrol:
            arranged = 0
            if patrol == minimum_value:
                arranged = 5

            elif  (float(patrol) / float(minimum_value + (i / 10))) > 0.85:
                arranged = 5

            board1.random_placing(ships[k][0] + str(i), 5 - k, arranged)
            if board2 != 0:
                board2.random_placing(ships[k][0] + str(i), 5 - k, arranged)
            i += 1

        new_ship_list.append(patrol)
    return new_ship_list


def ask_computer(board, board2, k=0):
    '''(board, board, int) --> list
    Print the maximum of each kind of ships the computer player can have.
    Ask for the input the amount of each kind of ship. If the input is
    invalid, the function will ask again. Return a list of ints which
    represent the amount of each ships.
    '''
    ships = ["aircraft", "submarine", "destroyer", "patrol"]
    i = 0

    e_list = []

    while k < 4:
        patrol = -1
        minimum = min(board.max_ship(5 - k), board2.max_ship(5 - k))
        if minimum == 0:
            patrol = 0
            e_list.append(0)

        print "maximum %s are %d" % (ships[k], minimum)
        if patrol == -1:
            patrol = input("How many ships are you wishing to have? \t:")

            while minimum < patrol:
                print "maximum %s are %d" % (ships[k], minimum)
                while 1:
                    try:
                        patrol = input("How many ships are you wishing to \
have (You can't choose more than maximum number)? \t:")
                        break
                    except Exception:
                        pass
            manual_placing(board, patrol, 5 - k, ships[k][0])

            e_list.append(patrol)

        while i < patrol:
            arranged = 0
            if  (float(patrol) / (minimum)) > 0.85:
                arranged = 5

            board2.random_placing(ships[k][0] + str(i), 5 - k, arranged)
            i += 1

        k += 1
    return e_list


if __name__ == "__main__":
    save = "no"
    sink = sound.load_sound("sink.wav")
    ship_dict = {"p": "patrol", "d": "destroyer", "s": "submarine", \
                 "a": "aircraft"}
    print "\n***********WELCOME TO BATTLESHIP******************************"
    new_user = raw_input("Are you a new user? (if yes please type new) : ")
    print "Please type your username and password "
    username = raw_input("Username : ")
    password = raw_input("Password : ")
    users = validation(username, password, new_user)

    while users == False:
        new_user = raw_input("if you want to create new account please type\
'new' : ")
        username = raw_input("Username : ")
        password = raw_input("Password : ")
        users = validation(username, password, new_user)

    print "\n*************GAME SETTING*********************************"

    against = raw_input("Play against computer / multiplayer : ")
    while against != "computer" and against != "multiplayer":
        against = raw_input("With whom you want to play? \
(computer / multiplayer)")

    if against == "multiplayer":
        print "\n*************GAME SETTING*********************************"
        board1 = ask_dimension()
        player1_board = Board(board1[0], board1[1])
        player2_board = Board(board1[0], board1[1])

        print "\n^^^^^^^^^^^^^^^^^^^^^^^^^^^ The Board\
^^^^^^^^^^^^^^^^^^^^^^^"
        print player1_board
        print "\n"
        auto_manual = raw_input("player 1 choose your method of choosing the\
ship a/m : ")

        while auto_manual != "a" and auto_manual != "m":
            print "provide a proper method"
            auto_manual = raw_input(" a/m : ")
        auto_manual1 = raw_input("player 2 choose your method \
of choosing the ship a/m : ")

        while auto_manual1 != "a" and auto_manual1 != "m":
            print "provide a proper method"
            auto_manual1 = raw_input(" a/m : ")

        if auto_manual == 'a' and auto_manual1 == 'a':
            list_ships = auto_fill(player1_board, player2_board)
        elif auto_manual == 'a' and auto_manual1 == 'm':
            print "\n*****************PLAYER 1******************************\n"
            list_ships = auto_fill(player1_board)
            print "\n*****************PLAYER 2******************************\n"
            second_ask(player2_board, player1_board, list_ships)

        elif auto_manual == 'm' and auto_manual1 == 'a':
            print "\n*****************PLAYER 2********************\n"
            list_ships = auto_fill(player2_board)
            print "\n*****************PLAYER 1********************\n"
            second_ask(player1_board, player2_board, list_ships)

        else:
            print "\n*****************PLAYER 1********************\n"
            list_ships = ask_ship(player1_board)
            print "\n*****************PLAYER 2********************\n"
            second_ask(player2_board, player1_board, list_ships)

        player1_ships = Ship(player1_board.create_ship())
        player2_ships = Ship(player2_board.create_ship())
        player_shot2 = None

        while (not player1_ships.is_empty()) and \
              (not player2_ships.is_empty()):
            print "\n*****************PLAYER 1******************************\n"
            print 'Your board :'
            print player1_board
            print '\nOpponent board :'
            print player2_board.opponent_view()
            print '\n'
            if type(player_shot2) == list:
                sink.play()
                print "your opponent sinked your %s" % \
                      (ship_dict[player_shot2[0][1]])

            target1 = input("Player1, your target in tuple form please : ")
            while type(target1) != tuple and (target1 not in \
                                              player1_board.box):
                target1 = input("Player1, your target in tuple form please : ")

            player_shot1 = player2_board.shot(target1, player2_ships)
            while player_shot1 == False:
                print "You already hit that spot, so choose another spot"
                target1 = input("Player1, your target in tuple form please : ")
                player_shot1 = player2_board.shot(target1, player2_ships)

            if type(player_shot1) == list:
                sink.play()
                print "you sinked your opponent's %s" % \
                      (ship_dict[player_shot1[0][1]])

            if player2_ships.is_empty():
                print "Winner is Player1"
                break

            print "\n*****************PLAYER 2******************************\n"
            print 'Your board :'
            print player2_board
            print '\nOpponent board :'
            print player1_board.opponent_view()
            print '\n'
            if type(player_shot1) == list:
                sink.play()
                print "your opponent sinked your %s" % \
                      (ship_dict[player_shot1[0][1]])

            target2 = input("Player2, your target in tuple form please : ")
            while type(target2) != tuple and \
                  (target2 not in player1_board.box):
                target2 = input("Player2, your target in tuple form please : ")

            player_shot2 = player1_board.shot(target2, player1_ships)
            while player_shot2 == False:
                print "You already hit that spot, so choose another spot"
                target2 = input("Player2, your target in tuple form please : ")
                player_shot2 = player1_board.shot(target2, player1_ships)

            if type(player_shot2) == list:
                sink.play()
                print "you sinked your opponent's %s" % \
                      (ship_dict[player_shot2[0][1]])

            if player1_ships.is_empty():
                print "Player 2 is the winner"
                break

    else:
        continue_game = False
        try:
            f = open('game.data')
            game = cPickle.load(f)
            f.close

        except IOError:
            game = {}

        if username in game:
            continue_game = raw_input("Do you want to \
continue the game? type(yes/no)")
            continue_game = continue_game.lower()
        if continue_game == "yes":
            player1_board = game[username][0]
            computer = game[username][1]
            random_computer = game[username][2]
            challenge = game[username][3]
            comp_shot = game[username][4]
            comp_ship = game[username][5]

        else:
            board1 = ask_dimension()
            player1_board = Board(board1[0], board1[1])
            computer = Board(board1[0], board1[1])
            random_computer = computer.box.keys()
            challenge = input("Choose your difficulty level (1 or 2) : ")
            print "\n^^^^^^^^^^^^^^^^^^^^^^^The Board\
^^^^^^^^^^^^^^^^^^^^^^^"
            print player1_board
            print "\n"
            auto_manual = raw_input("Player, do you want to place ships\
manually (type 'm') or automatically (type 'a') : ")
            while auto_manual != "a" and auto_manual != "m":
                print "Sorry your method is not defined"
                auto_manual = raw_input(" a/m : ")
            if auto_manual == "a":
                list_ships = auto_fill(player1_board, computer)
                print player1_board
            elif auto_manual == 'm':
                print "\n*****************PLAYER 1**************************\n"
                ask_computer(player1_board, computer)
                print player1_board
            comp_shot = None
            comp_ship = []

        player1_ships = Ship(player1_board.create_ship())
        computer_ships = Ship(computer.create_ship())

        while (not player1_ships.is_empty()) \
              and (not computer_ships.is_empty()):
            print "\n*****************PLAYER 1***********\
********************\n"
            try:
                if type(comp_shot) == list:
                    print "Too bad, your %s ship has been sunk" % \
                          (ship_dict[comp_shot[0][1]])
                print 'Your board :'
                print player1_board
                print '\nOpponent board :'
                print computer.opponent_view()
                print '\n'
                target1 = input("Player1, choose your aim \
                (give in (row,coloum) form: ")
                if type(target1) != tuple and target1 != -1:
                    target1 = input("Player1, \
                    choose your aim (give in (row,coloum) form: ")

                if target1 == -1:
                    save = raw_input("Do you want to save the game ?  :")
                    save = save.lower()
                    break

                player_shot = computer.shot(target1, computer_ships)
                while player_shot == False:
                    print "You already hit that spot, so choose another spot"
                    target1 = input("Player, your target \
in tuple form please : ")
                    player_shot = computer.shot(target1, player1_ships)

                if type(player_shot) == list:
                    print "you sinked your opponent's %s" % \
                          (ship_dict[player_shot[0][1]])

                if computer_ships.is_empty():
                    print "Player is the WINNER"
                    break

                print "n*****************computer\
1**********************************\n"
                if type(player_shot) == list:
                    sink.play()
                    print "Too bad, your %s has been sunk" % \
                          (ship_dict[player_shot[0][1]])

                if challenge == 1:
                    index = random.randint(0, len(random_computer) - 1)
                    target2 = random_computer.pop(index)
                    comp_shot = player1_board.shot(target2, player1_ships)

                elif challenge == 2:
                    if len(comp_ship) > 1:
                        for items in comp_ship:
                            if items in random_computer:
                                comp_ship.remove(items)
                                random_computer.remove(items)
                                target2 = items
                                comp_shot = player1_board.shot(target2, \
                                                               player1_ships)
                                break
                    else:
                        index = random.randint(0, len(random_computer) - 1)
                        target2 = random_computer.pop(index)
                        comp_shot = player1_board.shot(target2, player1_ships)
                        if type(comp_shot) == str:
                            comp_ship = player1_ships.ship[comp_shot]

                if type(comp_shot) == list:
                    sink.play()
                    print "You sinked your opponent's %s ship" % \
                          (ship_dict[comp_shot[0][1]])

                if player1_ships.is_empty():
                    print "computer WON"
                    break
            except KeyError:
                print "your spot is out of range"
                pass

    if save == "yes":
        game[username] = [player1_board, computer, random_computer, \
                          challenge, comp_shot, comp_ship]
        f = open("game.data", "w")
        cPickle.dump(game, f)
        f.close()

    if save == 'no':
        if username in game:
            del(game[username])
        f = open("game.data", "w")
        cPickle.dump(game, f)
        f.close()

    f = open("users.data", "w")
    cPickle.dump(users, f)
    f.close()
