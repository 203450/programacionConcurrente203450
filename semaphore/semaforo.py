from threading import Thread, Semaphore
from pytube import YouTube

semaforo=Semaphore(1) #Crea la variable semáforo

def critico(id):
    global x;
    x= x + id
    print("Hilo =" +str(id) + " => " +str(x))
    x=1

class Hilo(Thread):
    def __init__(self,id):
        Thread.__init__(self)
        self.id=id

    def run(self):
        semaforo.acquire() #inicializa semáforo, lo adquiere
        critico(self.id)
        semaforo.release() #Libera un semaforo e incrementa la variable
        
threads_semaphore = [Hilo(1),Hilo(2),Hilo(3),Hilo(4),Hilo(5)]
x=1;
for t in threads_semaphore:
    t.start()
    
#def signal(s):
#   if s == "bloqueado":
#        s.desbloquear()