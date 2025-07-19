import time
import os

def effacer_console():
    time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')