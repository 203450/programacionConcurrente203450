import threading
import time
import queue
import random

PRODUCTORES = 5
CONSUMIDORES = 10
# CONTADOR = 10

queue = queue.Queue(maxsize = 10)
condicion = threading.Condition()

class Productor(threading.Thread):
    
    def __init__(self, id):
        threading.Thread.__init__(self)
        self.id = id
        
    def run(self):
        while True:
            if condicion.acquire():
                if queue.full():
                    condicion.wait()
                else:
                    item = random.randint(0, 100)
                    queue.put(item)
                    
                    print(f"El productor {self.id} produjo {item} item(s)")
                    
                    condicion.notify()
                    condicion.release()
                    
                    time.sleep(5)

class Consumidor(threading.Thread):
    
    def __init__(self, id):
        threading.Thread.__init__(self)
        self.id = id
        
    def run(self):
        while True:
            if condicion.acquire():
                
                if queue.empty():
                    condicion.wait()
                else:
                    item = queue.get()
                    
                    print(f"El consumidor {self.id} consumió: {item} item(s)")
                    
                    condicion.notify()
                    condicion.release()
                    time.sleep(5)
        
def main():
    
    productores = []
    consumidores = []
    
    for i in range(PRODUCTORES):
        productores.append(Productor(i))
        
    for i in range(CONSUMIDORES):
        consumidores.append(Consumidor(i))
        
    for c in productores:
        c.start()
        
    for p in consumidores:
        p.start()

if __name__ == '__main__':
    main()