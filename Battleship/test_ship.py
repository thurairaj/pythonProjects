import unittest
from ship import Ship


class TestKillShip(unittest.TestCase):

    def setUp(self):
        """Set up a ship."""
        self.ship = Ship({'p0': [(0, 0), (0, 1)], 'p1': [(1, 0), (1, 1)]})

    def tearDown(self):
        """Clean up."""
        self.ship = None

    def testKillShip(self):
        """Test the kill ship function."""
        self.ship.kill_ship('p0')
        self.assertEqual(self.ship.ship, {'p1': [(1, 0), (1, 1)]})


class TestIsEmpty(unittest.TestCase):

    def setUp(self):
        """Set up a ship."""
        self.ship0 = Ship({'p0': [(0, 0), (0, 1)]})
        self.ship1 = Ship({})

    def tearDown(self):
        """Clean up."""
        self.ship = None

    def testIsEmpty(self):
        """Test if the ship is empty."""

        result = self.ship1.is_empty()
        self.assertTrue(result)

    def testIsNotEmpty(self):
        """Test if the ship is not empty."""

        result = self.ship0.is_empty()
        self.assertFalse(result)


def killship_suite():
    """Return a test suite for killship function."""

    return unittest.TestLoader().loadTestsFromTestCase(TestKillShip)


def isempty_suite():
    """Return a test suite for isempty function."""

    return unittest.TestLoader().loadTestsFromTestCase(TestIsEmpty)


if __name__ == '__main__':

    runner = unittest.TextTestRunner()
    runner.run(killship_suite())
    runner.run(isempty_suite())
