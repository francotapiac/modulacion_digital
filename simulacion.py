import numpy as np
import modulacion as mod
import scipy as sc
#Entradas:      señal modulada y la señal a ruido.
#Salida:        señal modulada con ruido
#Descripción:   
def simuladorRuido(modulada, tiempoModulada, snrDb):
    Nsamples = 100000
    sampling_rate = 42000
    potenciaSenal = np.sum(np.abs(np.fft.fft(modulada,sampling_rate//2)/Nsamples)**2)
    w = 1
    T = 2*np.pi/w
    energia = sc.integrate.simps(modulada**2,tiempoModulada)
    potenciaSenal = (1/T)*energia
    potenciaSenal = modulada.var()
    snr = 10.0**(snrDb/10.0)
    desviacionEstandar = np.sqrt(potenciaSenal/snr)
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
def simularTransmisionBits(A,B,senalOriginal,modulada,snr,portadora,frecuenciaMuestreoPortadora, tiempoPortadora, tiempoModulador):
    senalRuido = simuladorRuido(modulada, tiempoModulador, snr)
    demodulada = mod.demodularASK(A,B,senalRuido, portadora, frecuenciaMuestreoPortadora,tiempoPortadora,tiempoModulador)
    ber = calcularBER(senalOriginal,demodulada)
    return ber

def calcularBER(senalOriginal,senalDemodulada):
    cantidadDiferentes = 0
    for elemento1,elemento2 in zip(senalOriginal,senalDemodulada):
        if(elemento1 != elemento2):
            cantidadDiferentes = cantidadDiferentes + 1
    ber = cantidadDiferentes/len(senalOriginal)
    return ber