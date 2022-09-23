from threading import Thread, Semaphore
import pytube

semaforo = Semaphore(1) #Crea la variable semáforo

def critico(id):
    # print(id)
    links = ['https://youtu.be/xU8m9X-1fgE', 'https://youtu.be/OZ_3ZzhYuC0', 'https://youtu.be/LctX9TRXSFI']
    global x;
    print("Hilo = "+str(id)+" => "+ links[id])
    SAVE_PATH = "D:/Archivos/Tareas/Programación Concurrente/semaforovideos"
    yt = pytube.YouTube(links[id])
    stream = yt.streams.first()
    stream.download(SAVE_PATH)
    print("Video descargado")
    x=0

class Hilo(Thread):
    def __init__(self,id):
        Thread.__init__(self)
        self.id=id

    def run(self):
        semaforo.acquire() #inicializa semáforo, lo adquiere
        critico(self.id)
        semaforo.release() #Libera un semaforo e incrementa la variable
        
threads_semaphore = [Hilo(0),Hilo(1),Hilo(2)]

x=1;

for t in threads_semaphore:
    t.start()
  