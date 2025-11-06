import unittest
import os

def run_tests():
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir="./", pattern="test_*.py")
    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == "__main__":
    run_tests()