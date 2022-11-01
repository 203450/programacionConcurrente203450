# ACTIVIDAD 5 CORTE 2 ELABORADO POR:
 # - 203432 Camacho Toledo Jorge Alberto
 # - 203413 Orozco Reyes Marcos Iván
 # - 203450 Rios Mena Gustavo Vladimir

from threading import Thread, Condition, Lock
import random, queue
import time

mutex = Lock()
conditionReserva = Condition(mutex)
conditionFila = Condition(mutex)
conditionCliente = Condition(mutex)
conditionMesero = Condition(mutex)
conditionCocinero = Condition(mutex)

 # Creación de la clase recepcionista
class Recepcionista():
    def validar_reserva(self, id):
        if cantidad_Reservas.qsize() <= RESERVAS:
            # La recepcionista solo puede atender a una persona o grupo de personas que llegan juntos a la vez.
            conditionReserva.acquire()    
            time.sleep(2)
            print("Estado de recepción: Se realizó reserva")
            restaurante_NoAtendidos.append(id)
            conditionReserva.release()
            return 1
        else:
            # La recepcionista no puede atender a más personas por la cantidad máxima alcanzada
            conditionReserva.acquire()   
            time.sleep(1)
            print("Estado de recepción: Limite de reservas alcanzado, el cliente No."+id+" tendra que formarse en la cola")
            conditionReserva.release()
            return 0 

    def atender(self, id):
        if len(restaurante_NoAtendidos) <= 50:
            conditionFila.acquire()
            time.sleep(2)
            restaurante_NoAtendidos.append(id)
            print("Estado de atención: Acceso al cliente No." + id + " al restaurante")
            conditionFila.release()
            return 1
        else:
            conditionCliente.acquire()
            print('Estado de atención: Capacidad del restaurante llena ')
            return 0            
            
            


CAPACIDAD_RESTAURANTE = 50  #Definir la capacidad de clientes que se pueden atender de manera simultánea (capacidad del restaurante).
RESERVAS = (((CAPACIDAD_RESTAURANTE*20)/100)) # La capacidad máxima de reservas será equivalente al 20 % de la capacidad de comensales del restaurante.
MESEROS = int(((CAPACIDAD_RESTAURANTE*10)/100)) # La cantidad de meseros es igual al 10 % de la capacidad del restaurante.
COCINEROS = int((CAPACIDAD_RESTAURANTE*10)/100) # La cantidad de cocineros es igual al 10 % de la capacidad del restaurante.
restaurante_NoAtendidos = [] # "Comensales sin atender (cantidad de clientes esperando)".
restaurante_Atendidos = [] # "Comensales atendidos (cantidad de clientes atendidos)".
cola_Restaurante = queue.Queue(100) # Fila para acceso al restaurante.
cantidad_Reservas = queue.Queue(RESERVAS) # Cantidad de reservas actuales
recepcionista = Recepcionista() # Retorna valor booleano, el cual indica la realización de una reserva y en caso contrario, que se llenó.
ordenes = [] # Lista de ordenes de los clientes
comidasListas = [] # Lista de comidas listas para ser servidas

class Cliente(Thread):
    def __init__(self,id,valorReserva):
        super(Cliente,self).__init__()
        self.id = id
        self.valorReserva = valorReserva

    def hacer_reserva(self):
        reserva = recepcionista.validar_reserva(self.id)
        if reserva == 1:
            cantidad_Reservas.put(self.id)
            time.sleep(10)
            print("Estado de comensales: El cliente No." + self.id + " con reserva, llega al restaurante") 
            self.ordenar()
            self.comer()
        else:
            self.hacer_fila()

    def hacer_fila(self):
        cola_Restaurante.put(self.id)
        print("Estado de comensales: El cliente No." + self.id + " hace fila")
        entrada = recepcionista.atender(self.id)
        if entrada == 1:
            self.ordenar()
            self.comer()
        else:
            pass

    def comer(self):
        print("Estado de comensales: Cliente No." + self.id + " está comiendo")
        time.sleep(4)
        print("Estado de comensales: Cliente No." + self.id + " terminó de comer")
        restaurante_NoAtendidos.pop()
        if len(restaurante_NoAtendidos) >= CAPACIDAD_RESTAURANTE:
            conditionCliente.release()

    def ordenar(self):
        ordenLista = False
        print("Cliente num."+self.id+" Esperando comida")
        while ordenLista == False:
            while len(comidasListas) <=0:
                time.sleep(2)
            for comidas in comidasListas:
                if comidas == self.id:
                    print("El cliente"+self.id +" ha recibido su plato: La orden "+comidas)
                    ordenLista = True
                else:
                    time.sleep(2)

    def run(self):
        if self.valorReserva == 0:
            self.hacer_fila()
        else:
            self.hacer_reserva()
    

class Cocinero(Thread):
    def __init__(self,id):
        super(Cocinero,self).__init__()
        self.id = id

    def cocinar(self):
        print("El cocinero "+ self.id+" cocinara la  orden "+ordenes[0])
        time.sleep(10)
        print("Cocinero cocino orden num."+ordenes[0])
        comidasListas.append(ordenes.pop(0))
        
    def run(self):
        if len(ordenes) <= 0:
            print("Cocinero a la espera")
            time.sleep(10)
            self.run()
        else:
            while len(ordenes) > 0:
                self.cocinar()

class Mesero(Thread):
    def __init__(self,id):
        super(Mesero,self).__init__()
        self.id = id

    def tomar_orden(self):
        if len(restaurante_NoAtendidos) == 0:
            print("Meseros en espera")
        else:
         ordenLista = False
         print("El mesero"+self.id+" le esta tomando la orden al cliente no."+restaurante_NoAtendidos[0])
         time.sleep(3)
         print("la orden del cliente no."+restaurante_NoAtendidos[0]+" ha sido agregada")
         ordenes.append(restaurante_NoAtendidos[0])
         restaurante_Atendidos.append(restaurante_NoAtendidos.pop(0))
        if len(ordenes) <= 0:
            conditionCocinero.release()


    def run(self):
        if len(restaurante_NoAtendidos) <= 0:
            print("Mesero a la espera")
            time.sleep(10)
            self.run()
        else:
            time.sleep(int(self.id)*3)
            while len(restaurante_NoAtendidos) > 0:
                self.tomar_orden()
            
if __name__ == '__main__':
    clientes = queue.Queue()
    meseros =  []
    cocineros = []

    # Cuando se creen los hilos, algunos de éstos deberán pasar en un procedimiento de reservación y 
    # luego bloquearse, un determinado tiempo (definido por el alumno). Y luego que haya transcurrido 
    # el tiempo, deberán llegar al restaurante.
    for i in range(COCINEROS):
        cocineros.append(Cocinero(str(i+1)))


    for i in range(100):
        vl = random.randint(1,10)
        if vl < 6:
             clientes.put(Cliente(str(i+1),0))
        else:
             clientes.put(Cliente(str(i+1),1))
    
    for i in range(MESEROS):
        meseros.append(Mesero(str(i+1)))
        
    for i in range(100):
        cl = clientes.get()
        cl.start()

    for ms in meseros:
        ms.start()
    
    for cc in cocineros:
        cc.start()