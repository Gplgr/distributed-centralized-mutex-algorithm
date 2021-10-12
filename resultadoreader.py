import sys

def temporalidade(linhas):
    temporalidade = True
    for i in range(len(linhas)-1):
        if linhas[i][1] > linhas[i+1][1]:
            temporalidade = False

    if temporalidade:
        print("Todas as escritas estão em ordem")
    else:
        print("Tem escrita fora de ordem")

def execucaoPorProcesso(linhas):
    contador = {}
    for i in range(len(linhas)):
        if linhas[i][0] not in contador.keys():
            contador[linhas[i][0]] = 1
        else:
            contador[linhas[i][0]] += 1
    print (contador)

if __name__ == "__main__":
    n,k,r = int(sys.argv[1]),float(sys.argv[2]),int(sys.argv[3])    
    resultado = open("resultado.txt",'r')
    linhas = resultado.read().split("\n")

    #removendo a linha em branco ao final do arquivo
    linhas.pop()

    #transformando as linhas em uma matriz n*r x 2
    for i in range(len(linhas)):
        linhas[i] = linhas[i].split("   ")

    #Verificando se tem o número de linhas certo
    if len(linhas) == n*r:
        print("Numero de linhas (",n*r, ") correto")
    else:
        print("Numero de linhas (",len(linhas),") incorreto. Deveria ser",n*r)

    #Verificando quantas vezes cada processo registrou na saída
    execucaoPorProcesso(linhas)
    #Verificando se as linhas estão em ordem
    temporalidade(linhas)