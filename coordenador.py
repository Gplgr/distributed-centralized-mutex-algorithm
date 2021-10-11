import threading as thr
import socket as sk
import sys 
import subprocess
import time
import datetime as dt

#mutex para acesso à fila de execução
filamutex = thr.Lock()
        
#mutex para controlar a escrita no log do coordenador, para evitar escritas fora de ordem
logmutex = thr.Lock()

#classe da thread responsável por identificar novas conexões e criar threads 
# conectadas por TCP aos processos para a execução da recgião crítica
class Listener (thr.Thread):
    def __init__ (self, r, n):
        thr.Thread.__init__(self)
        self.r = r
        self.n = n
        self.csocket = None

        #mutex para controlar o acesso à região crítica
        self.mutex = thr.Lock()

        #fila de acesso para ordenar a entrada no mutex
        self.fifo = []

        #lista de threads do tipo runner
        self.runnerlist = []

    def run(self):

        #IPv4 + TCP local na porta 4267
        self.csocket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        self.csocket.bind(("127.0.0.1",4267))
        self.csocket.listen(5)

        #Conexões criadas, estabelecidas e iniciadas para cada processo
        for i in range(self.n):
            p,addr = self.csocket.accept()
            self.runnerlist.append(Runner(self.r, self.n, p, addr, self.mutex, self.fifo))
            self.runnerlist[i].start()
        self.csocket.close()

#Classe de thread responsável por executar a região crítica para cada socket recebido
class Runner(thr.Thread):
    def __init__ (self, r, n, p, addr, mutex, fifo):
        thr.Thread.__init__(self)
        self.r = r
        self.n = n
        self.p = p
        self.addr = addr
        self.mutex = mutex
        self.fifo = fifo

        #atributo que recebe a identificação do processo no sistema
        self.id = None

        #contador para ser retornado pela interface e limitar o número
        #de execuções para r
        self.contador = 0

        #variável para interrupção suave da execução
        self.stop = False

    #método principal relativo à região crítica distribuída
    def run(self):
        while self.contador < int(self.r) and not self.stop:

            #recebimento de requests
            msg = self.p.recv(10).decode()

            #escrita do request no log
            logmutex.acquire()
            logger = open("coordLog.txt","a+")
            logger.write(str("request "+msg+" "+str(dt.datetime.now())+"\n"))
            logger.close()
            logmutex.release()

            msgcode = msg.split("|")
            self.id = msgcode[1]

            #controle para impedir a quebra da sequência de estados request --> grant --> release
            if msgcode[0] != "0":
                print("identificação de mensagem inválida; era para receber request")
                continue

            #escrita na fifo
            filamutex.acquire()
            self.fifo.insert(0,self.id)
            filamutex.release()

            #verificação se é o primeiro da fila
            while self.fifo[-1] != self.id:
                time.sleep(float(k))
            
            #início da região crítica para essa thread relativa a um processo
            #remove da fila, envia o grant, escreve no log e espera a mensagem release
            # para enfim escrever a última mensagem no log e liberar a rc
            self.mutex.acquire()
            self.fifo.pop()
            self.p.send(("1"+msg[1:]).encode())

            logmutex.acquire()
            logger = open("coordLog.txt","a+")
            logger.write(str("grant "+"1"+msg[1:]+" "+str(dt.datetime.now())+"\n"))
            logger.close()
            logmutex.release()
        
            msg = self.p.recv(10).decode()

            logmutex.acquire()
            logger = open("coordLog.txt","a+")
            logger.write(str("release "+msg+" "+str(dt.datetime.now())+"\n"))
            logger.close()
            logmutex.release()
    
            msgcode = msg.split("|")
            if msgcode[0] != "2":
                print("identificação de mensagem inválida; era para receber release")
                continue

            self.mutex.release()
            self.contador += 1
        self.p.close()

if __name__ == "__main__":
    #pegando os argumentos de entrada
    n,k,r = int(sys.argv[1]),sys.argv[2],sys.argv[3]

    #Limpando os arquivos .txt para otimizar os testes caso eles contenham
    #alguma execução anterior
    open("resultado.txt","w").close()
    open("coordLog.txt","w").close()

    #Entrando na thread que estabelece e controla o socket do servidor
    receiver = Listener(r,n)
    receiver.start()

    #Criando os processos em forma de subprocessos independentes do coordenador
    #de forma que a única comunicação possível é pelos sockets.
    for i in range(n):
        subprocess.Popen([sys.executable,"processo.py",k,r], stdin=None, stdout=None, stderr=None, close_fds=True)
    
    #Trecho da interface
    print("1: Imprime a fila de pedidos atual")
    print("2: Imprime quantas vezes cada processo foi atendido")
    print("3: Encerra a execução")

    while True:
        cod = input("Insira o codigo: ")
        if cod == "1":
            #imprimindo a fila com restrição de acesso
            filamutex.acquire()
            print(receiver.fifo)
            filamutex.release()

        elif cod == "2":
            #Retorna um texto com o id do processo no sistema e quantas vezes ele
            #executou até o presente momento
            for i in receiver.runnerlist:
                print("O processo",i.id,"executou",i.contador,"vezes.")
    
        elif cod == "3":
            #interrompe o processo da interface após enviar um sinal de encerramento
            #para cada thread do tipo runner
            for i in receiver.runnerlist:
                i.stop = 1
            break

        else:
            print("Código inválido. Tente novamente.")
    
    print("Finalizando interface")