import os
import threading
import time

mutex = threading.Lock()

personas = [1,2,3,4,5,6,7,8]
estado = [0,0,0,0,0,0,0,0]

# Estados: 0 = esperando, 1 = comiendo, 2 = sataisfecho

def crito(id):
    print("La persona: "+str(personas[id]) + " estado: " + str(estado[id]))
    print('\n')
    
    for j in range(0,8):
        print("Persona: " + str(personas[j]) + " estado: " + str(estado[j]))
        
    time.sleep(2)
    os.system('cls')
    
    estado[id] = 1
    
    print("La persona: "+str(personas[id]) + " estado: " + str(estado[id]))
    print('\n')
    
    for j in range(0,8):
        print("La persona: " + str(personas[j]) + " estado: " + str(estado[j]))
    
    estado[id] = 2

class Hilo(threading.Thread):
    def __init__(self, id):
        threading.Thread.__init__(self)
        self.id = id
        
    def run(self):
        mutex.acquire()
        crito(self.id)
        time.sleep(3)
        os.system("cls")
        mutex.release()

for i in range(0,8):
    hilo = Hilo(i)
    hilo.start()
