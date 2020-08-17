import serial
from random import randint
import os

#declarando la conexion del jugador
#serialPort1 = serial.Serial(port = "COM1", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
#serialPort2 = serial.Serial(port = "COM4", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
#serialString = ""


#--------JUGADORES--------#

#funcion para crear el carton del bingo
def crearCartonBingo():
    carton = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    i = 0
    j= 0
    lista=[]
    while i < 5:
        randomNum = randint(1, 15)
        while randomNum in lista:
            randomNum = randint(1, 15)
        carton[i][j] = randomNum
        lista.append(randomNum)
        i+=1

    i = 0
    j= 1
    lista=[]
    while i < 5:
        randomNum = randint(16, 30)
        while randomNum in lista:
            randomNum = randint(16, 30)
        carton[i][j] = randomNum
        lista.append(randomNum)
        i+=1

    i = 0
    j= 2
    lista=[]
    while i < 5:

        if i == 2:
            carton[i][j] = 0
        else:
            randomNum = randint(31, 45)
            while randomNum in lista:
                randomNum = randint(31, 45)
            carton[i][j] = randomNum
            lista.append(randomNum)

        i+=1

    i = 0
    j= 3
    lista=[]
    while i < 5:
        randomNum = randint(46, 60)
        while randomNum in lista:
            randomNum = randint(46, 60)
        carton[i][j] = randomNum
        lista.append(randomNum)
        i+=1

    i = 0
    j= 4
    while i < 5:
        randomNum = randint(61, 75)
        while randomNum in lista:
            randomNum = randint(61, 75)
        carton[i][j] = randomNum
        lista.append(randomNum)
        i+=1


    return carton


#funcion para mostrar carton de bingo

def backspace(n):
    print('\r', end='')

def mostrarCarton():
    print('Carton del jugador ', end="", flush=True)
    print(letra)
    print(' ')
    print('||  | B | I | N | G | O |  ||')
    print(' ')

    i=0
    j=0

    while i < 5:
        j=0
        print('|| ', end="", flush=True)
        while j < 5:
            if carton[i][j] < 10:
                print(' | ', end="", flush=True)
            else:
                print(' |', end="", flush=True)
            if carton[i][j] == 0:
                print('X', end="", flush=True)
            else:
                print(carton[i][j], end="", flush=True)
            j+=1
        print(' | ', end="", flush=True)
        print(' ||\r\n')
        i+=1


#funcion para buscar si el numero recibido se encuentra en el carton
def buscarNumero(numero):
    i=0
    j=0

    while i < 5:
        j=0
        while j < 5:
            if (carton[i][j] == numero):
                carton[i][j] = 0
                flag=1
                return[i,j]
            j+=1
        i+=1
    return[None,None]

#funcion para buscar si ya se hizo bing0
def buscarBingo(x,y):

    #REVISAR

    #busca bingo esquinas
    flag = 0;
    i=x
    j=y

    if carton[0][0] != 0:
        flag = 1
    elif carton[0][4] != 0:
        flag = 1
    elif carton[4][0] != 0:
        flag = 1
    elif carton[4][4] != 0:
        flag = 1

    if flag == 0:
        return 1

    #busca bingo dada una posicion verticalmente
    flag = 0
    i=0
    while i < 5:
        if carton[x][i] != 0:
            flag = 1
        i+=1
    if flag == 0:
        return 1

    #busca bingo dada una posicion horizontalmente
    flag = 0
    i=0
    while i < 5:
        if carton[i][y] != 0:
            flag = 1
        i+=1
    if flag == 0:

        return 1

    #busca bingo diagonal principal superior
    if (x == 0 and y == 4) or (x == 4 and y == 0):
        print('')
    elif (x == y):

        flag = 0
        i=x
        j=y

        while (i >= 0 and j >= 0):

            if carton[i][j] != 0:
                flag = 1
            j-=1
            i-=1

        #busca bingo diagonal principal inferior
        i=x
        j=y
        while (i < 5 and j < 5):

            if carton[i][j] != 0:
                flag = 1
            i+=1
            j+=1

        if flag == 0:
            return 1



    if (x == 0 and y == 0) or (x == 4 and y == 4):
        print('')
    elif (x + y == 4):
        #busca bingo diagonal secundaria inferior
        flag = 0
        i=x
        j=y

        while (i >= 0 and j < 5):

            if carton[i][j] != 0:
                flag = 1
            i-=1
            j+=1


        #busca bingo diagonal secundaria superior
        i=x
        j=y
        while (i < 5 and j >= 0):

            if carton[i][j] != 0:
                flag = 1
            i+=1
            j-=1

        if flag == 0:

            return 1


    return 0


#funcion para tomar numero
def extraerNumero(input):
    numero = 0
    i=0
    while i < len(input):
        if input[i] != 'A' and input[i] != 'B' and input[i] != 'C':
            numero = numero * 10 + int(input[i])
        i += 1
    return numero


#funcion principal para jugadores
def jugar():
    carton = crearCartonBingo()
    mostrarCarton()

    while(1):
        global serialPort1
        global serialPort2

        # Wait until there is data waiting in the serial buffer
        if(serialPort1.in_waiting > 0):
            os.system('cls')

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort1.readline()

            numeroRecibido = serialString.decode()
            pos=[None, None]
            print('Numero recibido:')
            numero = extraerNumero(numeroRecibido)
            print(numero)
            print(' ')


            if numero == 0:
                #avisando que el juego ha terminado
                serialPort2.write(numeroRecibido.encode())
                serialPort1.close()
                serialPort2.close()

                return 0
            else:
                pos = buscarNumero(numero)

            mostrarCarton()
            print('Esperando número...')

            #si no hubo coincidencias pasar al siguiente jugador
            if pos != [None,None]:

                #si  hubo coincidencias verificar si hubo bingo
                if buscarBingo(pos[0],pos[1]) == 1:
                    encontrado = letra
                    print('BINGO!!')
                    serialPort2.write(encontrado.encode())





            #else:

            #    serialPort2.write(numeroRecibido.encode())

            serialPort2.write(numeroRecibido.encode())





#--------JUGADOR QUE CANTA----------#

numeroRecibido = ''

#funcion principal para el que canta los números
def bingo():
    numMostrados = []
    while(1):
        #cantar un nuevo numero y pasarlo al primer jugador
        #os.system('cls')
        input('Presione enter para anunciar un número')


        randomNum = randint(1, 75)
        while randomNum in numMostrados:
            randomNum = randint(1, 75)
        numMostrados.append(randomNum)

        print(randomNum)
        serialPort1.write(str(randomNum).encode())
        if recibirRespuestaDeJugadores() == 1:
            serialPort1.write('0'.encode())
            serialPort1.close()
            serialPort2.close()
            return 1

        global numeroRecibido
        print(numeroRecibido)
        if (numeroRecibido == 'A' or numeroRecibido == 'B' or numeroRecibido == 'C') :
            return 1


#se ejecuta al final de cada ronda
def recibirRespuestaDeJugadores():

    #esperar a recibir una respuesta del ultimo jugador
    while (1):
        # Wait until there is data waiting in the serial buffer
        if(serialPort2.in_waiting > 0):
            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort2.readline()
            numeroRecibido = ''
            # Print the contents of the serial data
            numeroRecibido = serialString.decode()

            #al recibir el numero se acaba la ronda, si se recibe una letra se canta bingo
            print('ronda terminada')
            numero = extraerNumero(numeroRecibido)
            if len(numeroRecibido) - len(str(numero)) != 0:
                i = 0
                print('Partida terminada')
                print(len(numeroRecibido) - len(str(numero)))
                while(i < (len(numeroRecibido) - len(str(numero)))):
                    print('BINGO DE ', end="", flush=True)
                    print(numeroRecibido[i])
                    i+=1
                input('Presione una tecla para terminar el juego')
                return 1





            #if (numeroRecibido == 'A' or numeroRecibido == 'B' or numeroRecibido == 'C'):
            #    print('BINGO DE ', end="", flush=True)
            #    print(numeroRecibido)
            #    input('Presione una tecla para terminar el juego')
            #    numero = 0
            #    return 1

            return 0






#---------AMBOS------------#

serialString = ""

#eleccion de rol
def menu():

    os.system('cls') # NOTA para windows tienes que cambiar clear por cls
    print ("Selecciona un jugador")
    print ("\t1 - Principal")
    print ("\t2 - Jugador A")
    print ("\t3 - Jugador B")
    print ("\t4 - Jugador C")
    print ("\t9 - salir")


#asignar configuracion de puerto
def asignarPuerto(letra):
    global serialPort1
    global serialPort2

    if letra == "A":
        serialPort1 = serial.Serial(port = "COM1", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
        serialPort2 = serial.Serial(port = "COM2", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    elif letra == "B":
        serialPort1 = serial.Serial(port = "COM2", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
        serialPort2 = serial.Serial(port = "COM3", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    elif letra == "C":
        serialPort1 = serial.Serial(port = "COM3", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
        serialPort2 = serial.Serial(port = "COM4", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    elif letra == "P":
        serialPort1 = serial.Serial(port = "COM1", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
        serialPort2 = serial.Serial(port = "COM4", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)







#-----JUEGO------#

carton = crearCartonBingo()
letra = None
serialPort1 = None
serialPort2 = None

while (1):

    menu()

    #1. Seleccionar jugador

    opcionMenu = input("inserta un numero valor >> ")
    if opcionMenu == "1":
        letra = 'P'
    elif opcionMenu == "2":
        letra = 'A'
    elif opcionMenu == "3":
        letra = 'B'
    elif opcionMenu == "4":
        letra = 'C'
    else:
        print ("")
        input("No has pulsado ninguna opción correcta...\npulsa una tecla para continuar")

    asignarPuerto(letra)
    if (letra == 'A' or letra == 'B' or letra == 'C'):
        jugar()
    else:
        if bingo() == 1:
            print('Juego finalizado')









        # Tell the device connected over the serial port that we recevied the data!
        # The b at the beginning is used to indicate bytes!
        #serialPort.write(b"Thank you for sending data \r\n")
