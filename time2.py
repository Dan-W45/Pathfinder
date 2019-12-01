import threading
 
def run_check():
    threading.Timer(0.5, run_check).start()
    print("Hilkjahds fkjlha sdl kjhflkjasdh ")


run_check()

while True:
    print('Hello')
