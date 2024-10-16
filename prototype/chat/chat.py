# hello.py
import time

def print_hello():
    while True:
        print("Hello, World!")
        time.sleep(1)  # Pause d'une seconde pour éviter un trop grand nombre d'affichages

if __name__ == '__main__':
    print_hello()
