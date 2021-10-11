import socket as sk
import os
import sys
import time
import datetime as dt

def processo(k,r):
    #Estabelece o formato da conexão, os argumentos e o endereço desse processo 
    psocket = sk.socket(sk.AF_INET,sk.SOCK_STREAM)
    k,r = float(k),int(r)
    addr = str(os.getpid())

    #formato da mensagem de request
    request = "0|"+addr+"|"
    for i in range(10-len(request)):
        request+="0"

    #Formato da mensagem de release
    release = "2" + request[1:]
    try:
        psocket.connect(("127.0.0.1",4267))
        for j in range(r):

            #pedindo acesso
            psocket.send(request.encode())

            #acesso liberado
            grant = psocket.recv(10).decode()
            if grant.split("|")[0] != "1":
                print("identificação de mensagem inválida; era para receber grant")
                continue

            #regiao critica
            critico = open("resultado.txt","a+")
            escrita = addr +"   "+ str(dt.datetime.now()) +"\n"
            critico.write(escrita)
            critico.close()
            time.sleep(k)

            #saindo da rc
            psocket.send(release.encode())

    #Caso a thread relacionada a esse processo no coordenador encerre,
    # finaliza a execução
    except (ConnectionResetError, ConnectionAbortedError):
        return 0
    return 1

if __name__ == "__main__":
    #puxando os argumentos e executando
    k,r = sys.argv[1],sys.argv[2]
    processo(k,r)