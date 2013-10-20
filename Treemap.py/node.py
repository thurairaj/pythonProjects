class Tree(object):
    '''A tree that stores information of a directory, each node in the tree
    contains the name and size of a file in the directory.'''

    class Node(object):
        '''A node in tree stores the size and name of a file.'''

        def __init__(self, k):
            '''(Node, tuple) -> Nonetype
            Create a Node with key k, k is in the form of (filename, filesize).
            and _range None, _range is the range that one file occupied
            in the pygame screen.'''

            self.key = k
            self._range = None

        def total(self):
            '''Node -> int
            Return the size of a file in the directory stored in Node.'''

            return self.key[1]

        def getting_range(self, x, y):
            '''(Node, int, int) -> tuple
            Getting the range that a file occupied in the pygame window,
            using a helper function.'''

            return _getting_range(self, x, y)

    def __init__(self):
        '''Tree -> NoneType
        Create a Tree with root None, child as an empty list
        and _range as None.'''

        self.root = None
        self.child = []
        self._range = None

    def __str__(self):
        '''Tree -> str
        Return the string representation of the root of a tree.'''

        return self.root.key

    def insert_directory(self, k):
        '''(Tree, tuple) -> Nonetype
        Insert a new directory  at the end of Tree.
        Tuple k is in the form of (directory, size)'''

        if self.root:
            new_tree = Tree()
            new_tree.insert_directory(k)
            self.child.append(new_tree)
        else:
            self.root = Tree.Node(k)

    def insert_files(self, k):
        '''(Tree, tuple) -> Nonetype
        Insert a new file to a directory Tree.
        Tuple k is in the form of (filename, size)'''

        self.child.append(Tree.Node(k))

    def search_tree(self, d):
        '''(Tree, unicode) -> object
        Search if the directory d is in the tree by a helper function.'''

        return _search_tree(self, d)

    def total(self):
        '''Tree -> Nonetype
        Return the total size of a directory Tree by a helper function.'''

        return _total(self)

    def getting_range(self, x, y):
        '''(Tree, int, int) -> onject
        Return the range of a Tree.'''

        return _getting_range(self, x, y)


def _total(tree):
    '''Tree -> tuple
    Return the total size of a directory stored in Tree.
    tuple is in the form of (x coordinate, y coordinate).'''

    if tree.child:
        _sum = tree.root.key[1]
        for child in tree.child:
            if type(child) == Tree:
                _sum += child.total()
            else:
                _sum += child.total()
    else:
        return tree.root.key[1]

    return _sum


def _getting_range(tree, x, y):
    '''(Object, int, int) -> object
    Return the file name and file size that (x, y) indicates in 
    pygame window.'''

    if type(tree) == Tree:
        if tree.child and tree._range:
            if x in tree._range[0] and y in tree._range[1]:

                for child in tree.child:
                    filename = _getting_range(child, x, y)
                    if filename:
                        return filename

                return tree.root.key

            else:
                return None
        elif tree._range and x in tree._range[0] and y in tree._range[1]:
                return tree.root.key[0]

    elif type(tree) == Tree.Node:
        if tree._range and x in tree._range[0] and y in tree._range[1]:
            return tree.key

    return None


def _search_tree(tree, name):
    '''(Tree, unicode) -> object
    If name is in the tree, return the subtree start from where name is 
    located in the tree. Return True or False if name is leaf or not in 
    the tree.'''

    if type(tree) == Tree:
        if tree.root.key[0] == name:
            return tree
        else:
            for child in tree.child:
                contain_tree = _search_tree(child, name)
                if type(contain_tree) == Tree:
                    return contain_tree
                elif contain_tree == True:
                    return tree
            return None

    else:
        if tree.key[0] == name:
            return True
        else:
            return False
