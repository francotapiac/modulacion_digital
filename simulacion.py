import numpy as np
#Entradas:      señal modulada y la señal a ruido.
#Salida:        señal modulada con ruido
#Descripción:   
def simuladorRuido(modulada, snr):
    Nsamples = 100000
    sampling_rate = 42000
    potenciaSenal = np.sum(np.abs(np.fft.fft(modulada,sampling_rate//2)/Nsamples)**2)
    print("Potencial:" + str(potenciaSenal))
    desviacionEstandar = np.sqrt(potenciaSenal/snr)
    print("Desviacion:" + str(desviacionEstandar))
    ruido = np.random.normal(0,desviacionEstandar,len(modulada))
    senalRuido = modulada + ruido
    return senalRuido

#Entrada:       largo del arreglo aleatorio
#Salida:        señal digital con valores aleatorios
#Descripción:   se obtiene una señal con 0 y 1 de forma aleatoria, con
#               un largo definido.
def crearSenalDigital(largoArregloAleatorio):
    senal = np.random.randint(2,size = largoArregloAleatorio)
    return senal

#Entrada:
def simularTransmisionBits(senalOriginal,modulada,snr):
    senalRuido = simuladorRuido(modulada, snr)
    demodulada = demodularASK(A,B,senalRuido, portadora, frecuenciaMuestreoPortadora,tiempoPortadora,tiempoModulador)
    ber = calcularBER(senalOriginal,demodulada)
    return ber

def calcularBER(senalOriginal,senalDemodulada):
    cantidadDiferentes = 0
    for elemento1,elemento2 in zip(senalOriginal,senalDemodulada):
        if(elemento1 != elemento2):
            cantidadDiferentes = cantidadDiferentes + 1
    ber = cantidadDiferentes/len(senalOriginal)
    return ber