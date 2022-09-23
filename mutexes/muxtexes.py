import threading

mutex=threading.Lock()
def crito(id):
    global x;
    x= x + id
    print("Hilo =" +str(id) + " => " +str(x))
    x=1

class Hilo(threading.Thread):
    def __init__(self,id):
        threading.Thread.__init__(self)
        self.id=id

    def run(self):
        mutex.acquire() #inicializa semáforo, lo adquiere
        crito(self.id)
        mutex.release() #
threads_semaphore = [Hilo(1),Hilo(2),Hilo(3)]
x=1;
for t in threads_semaphore:
    t.start