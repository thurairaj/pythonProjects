import unittest
from board import Board
from board import OrientationError
from ship import Ship


class TestOpponentView(unittest.TestCase):
    '''Test the behaviour of opponent_view function.'''

    def setUp(self):
        """Set up a board."""
        self.board = Board(2, 2)

    def tearDown(self):
        """Clean up."""
        self.board = None

    def testEmpty(self):
        """Test when the board is empty."""

        result = self.board.opponent_view()
        self.assertEqual(result, '(0 )(1 )\n|__||__|( 0)\n|__||__|( 1)')

    def testWithShipOnTheBoard(self):
        """Test when there is ship on board."""

        self.board.box[0, 0] = 'p0'
        result = self.board.opponent_view()
        self.assertEqual(result, '(0 )(1 )\n|__||__|( 0)\n|__||__|( 1)')


class TestStr(unittest.TestCase):
    """Test behaviour of __str__ function."""

    def setUp(self):
        """Set up a board."""
        self.board = Board(2, 2)

    def tearDown(self):
        """Clean up."""
        self.board = None

    def testStr(self):

        result = self.board.__str__()
        self.assertEqual(result, '(0 )(1 )\n|__||__|(0)\n|__||__|(1)')


class TestFitShip(unittest.TestCase):
    """Test behaviour of fit_ship function."""

    def setUp(self):
        """Set up a board."""
        self.board = Board(5, 5)

    def tearDown(self):
        """Clean up."""
        self.board = None

    def testBoardFitHorizonShips(self):
        """Test if the board can fit horizontal ships, when the length
        of the ship is less than the length of the board."""

        result = self.board.fit_ship(3, 0, 0, 'h')
        self.assertTrue(result)

    def testShipsIsLongerThanBoardHorizonally(self):
        """Test if the board can fit horizontal ships, when the length
        of the ship is more than the length of the board."""

        result = self.board.fit_ship(7, 0, 0, 'h')
        self.assertFalse(result)

    def testBoardCannotFitHorizonShips(self):
        """Test if the board can fit horizontal ships, when the length
        of the ship is less than the length of the board, but the
        position of start point of the ship does not fit."""

        result = self.board.fit_ship(5, 3, 3, 'h')
        self.assertFalse(result)

    def testBoardFitVerticalShips(self):
        """Test if the board can fit vertical ships, when the length
        of the ship is less than the length of the board."""

        result = self.board.fit_ship(3, 0, 0, 'v')
        self.assertTrue(result)

    def testShipsIsLongerThanBoardVertically(self):
        """Test if the board can fit vertical ships, when the length
        of the ship is more than the length of the board."""

        result = self.board.fit_ship(7, 0, 0, 'v')
        self.assertFalse(result)

    def testBoardCannotFitVerticalShips(self):
        """Test if the board can fit vertical ships, when the length
        of the ship is less than the length of the board, but the
        position of start point of the ship does not fit."""

        result = self.board.fit_ship(5, 3, 3, 'v')
        self.assertFalse(result)

    def testInvalidInput(self):
        """Test when the input is incalid."""

        result = self.board.fit_ship(5, 3, 3, 'g')
        self.assertFalse(result)

    def testKeyError(self):
        """Test the invalid input of the orientation."""

        result = self.board.fit_ship(5, -1, 19, 'g')
        self.assertFalse(result)


class TestPlacingShip(unittest.TestCase):
    """Test behaviour of PlacingShip function."""

    def setUp(self):
        """Set up a board."""
        self.board = Board(2, 2)

    def tearDown(self):
        """Clean up."""
        self.board = None

    def testVerticalPlacing(self):
        """Test placing vertical ships."""

        self.board.placing_ship(2, 0, 0, 'v', 'p0')
        result = self.board.__str__()
        self.assertEqual(result, '(0 )(1 )\n|p0||__|(0)\n|p0||__|(1)')

    def testHorizontalPlacing(self):
        """Test placing horizontal ships."""

        self.board.placing_ship(2, 0, 0, 'h', 'p0')
        result = self.board.__str__()
        self.assertEqual(result, '(0 )(1 )\n|p0||p0|(0)\n|__||__|(1)')

    def testInvalidInput(self):
        """Test the wrong position of the start point of the ship."""

        try:
            result = self.board.fit_ship(5, 3, 3, 'g')
        except OrientationError:
            pass


class TestShot(unittest.TestCase):
    """Test behaviour of shot function."""

    def setUp(self):
        """Set up a board."""
        self.board = Board(2, 2)
        self.board.box[0, 0] = '|p0|'
        self.board.box[0, 1] = '|p0|'
        self.ship = Ship({'|p0|': [(0, 0), (0, 1)]})

    def tearDown(self):
        """Clean up."""
        self.board = None
        self.ship = None

    def testShotOnWater(self):
        """Test the case when player shot on the water."""

        result = self.board.shot((1, 1), self.ship)
        self.assertEqual(result, None)

    def testShotOnShip(self):
        """Test the case when player shot on the ship."""

        result = self.board.shot((0, 1), self.ship)
        self.assertEqual(result, '|p0|')
        self.assertEqual(self.board.box[0, 1], '|$$|')

    def testShotOnAlreadyShot(self):
        """Test the case when player shot on the point
        whichalready been shot."""

        self.board.box[1, 1] = '|##|'
        self.board.box[1, 0] = '|$$|'
        result = self.board.shot((1, 1), self.ship)
        result2 = self.board.shot((1, 0), self.ship)
        self.assertFalse(result)
        self.assertFalse(result2)

    def testShotOnInvalidPoint(self):
        """Test the case when player shot on an invalid point."""

        try:
            self.board.shot((-1, 100), self.ship)
            self.fail('The position of shot point does not exist.')
        except Exception:
            pass


class TestMaxShip(unittest.TestCase):
    """Test behaviour of max_ship function."""

    def setUp(self):
        """Set up a board."""
        self.board = Board(5, 5)

    def tearDown(self):
        """Clean up."""
        self.board = None

    def testMaxPatrol(self):
        """Test the maximum of patrol a player can have."""

        result = self.board.max_ship(2)
        self.assertEqual(result, 12)

    def testMaxDestroyer(self):
        """Test the maximum of destroyer a player can have."""

        result = self.board.max_ship(3)
        self.assertEqual(result, 7)

    def testMaxSubmarine(self):
        """Test the maximum of submarine a player can have."""
        result = self.board.max_ship(4)
        self.assertEqual(result, 6)

    def testMaxAircraft(self):
        """Test the maximum of aircraft a player can have."""

        result = self.board.max_ship(5)
        self.assertEqual(result, 5)


class TestRandomPlacing(unittest.TestCase):
    """Test behaviour of random function."""

    def setUp(self):
        """Set up a board."""
        self.board = Board(5, 5)

    def tearDown(self):
        """Clean up."""
        self.board = None

    def testRandomPlacingPatrol(self):
        """Test the case when random placing patrol."""

        result = self.board.random_placing('p0', 2, k=0)
        self.assertEqual(result, "Done")

    def testRandomDestroyer(self):
        """Test the case when random placing destroyer."""

        result = self.board.random_placing('d0', 3, k=0)
        self.assertEqual(result, "Done")

    def testRandomPlacingSubmarine(self):
        """Test the case when random placing submarine."""

        result = self.board.random_placing('s0', 4, k=0)
        self.assertEqual(result, "Done")

    def testRandomPlacingAircraft(self):
        """Test the case when random placing aircraft."""

        result = self.board.random_placing('a0', 5, k=0)
        self.assertEqual(result, "Done")


def opponentview_suite():
    """Return a test suite for opponentview function."""

    return unittest.TestLoader().loadTestsFromTestCase(TestOpponentView)


def strsuite():
    """Return a test suite for __str__ function."""

    return unittest.TestLoader().loadTestsFromTestCase(TestStr)


def placingship_suite():
    """Return a test suite for placingship function."""

    return unittest.TestLoader().loadTestsFromTestCase(TestPlacingShip)


def fitship_suite():
    """Return a test suite for fit ship function."""

    return unittest.TestLoader().loadTestsFromTestCase(TestFitShip)


def shot_suite():
    """Return a test suite for shot function."""

    return unittest.TestLoader().loadTestsFromTestCase(TestShot)


def maxship_suite():
    """Return a test suite for maxshipfunction."""

    return unittest.TestLoader().loadTestsFromTestCase(TestMaxShip)


def randomplacing_suite():
    """Return a test suite for random placing function."""

    return unittest.TestLoader().loadTestsFromTestCase(TestRandomPlacing)


if __name__ == '__main__':

    runner = unittest.TextTestRunner()
    runner.run(opponentview_suite())
    runner.run(strsuite())
    runner.run(placingship_suite())
    runner.run(fitship_suite())
    runner.run(shot_suite())
    runner.run(maxship_suite())
    runner.run(randomplacing_suite())
