import sys

def temporalidade(linhas):
    temporalidade = True
    for i in range(len(linhas)-1):
        if linhas[i][2]+linhas[i][3] > linhas[i+1][2]+linhas[i+1][3]:
            temporalidade = False
            print(i,i+1)

    if temporalidade:
        print("Todas as escritas estão em ordem")
    else:
        print("Tem escrita fora de ordem")

def seqGeral(linhas):
    correto = True
    for i in range(len(linhas)):
        if linhas[i][0] == "request":
            check = 0
            for j in range(i+1,len(linhas)):
                if linhas[j][1].split("|")[1] == linhas[i][1].split("|")[1]:
                    if linhas[j][0] == "grant" and check == 0:
                        check = 1
                    elif linhas[j][0] == "release" and check == 1:
                        break
                    else:
                        correto = False
                        break
            if not correto:
                break

    if correto:
        print("A sequencialidade request --> grant --> release foi respeitada para cada pedido")
    else:
        print("A sequencialidade request --> grant --> release não foi respeitada em todos os pedidos")


if __name__ == "__main__":
    n,k,r = int(sys.argv[1]),float(sys.argv[2]),int(sys.argv[3])    
    log = open("coordLog.txt",'r')
    linhas = log.read().split("\n")

    #removendo a linha em branco ao final do arquivo
    linhas.pop()

    #transformando a lista em uma matriz n*r x 4
    for i in range(len(linhas)):
        linhas[i] = linhas[i].split(" ")

    #verificando se as escritas foram feitas em ordem temporal
    temporalidade(linhas)

    #verificando se, para cada processo, a sequência
    # request --> grant --> release
    # é respeitada
    #teste com complexidade de pior caso O(n²) (na prática um pouco menor)
    seqGeral(linhas)