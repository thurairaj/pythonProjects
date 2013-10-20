class Ship(object):

    def __init__(self, ship_dict):
        self.ship = ship_dict

    def kill_ship(self, name):
        '''(self, name) --> None
        Delete the name from self.ship'''
        del(self.ship[name])

    def is_empty(self):
        '''(self) --> bool
        Return True if the self.ship is empty'''
        if self.ship == {}:
            return True
        else:
            return False


def helper(num_ship, name, dic):
    for i in range(num_ship):
        j = "%s%d" % (name, i)
        dic[j] = []
    return dic
