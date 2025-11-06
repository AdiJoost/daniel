import sys
import os

def initNotebook():
    root_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
    sys.path.append(root_dir)

