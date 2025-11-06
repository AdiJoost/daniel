import unittest

class TestLogger(unittest.TestCase):

    def test_testing(self):
        #ARRANGE
        expectedValue = 2

        #ACT
        actualValue = 1+1

        #ASSERT
        self.assertEqual(expectedValue, actualValue)