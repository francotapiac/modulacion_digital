import numpy as np
import scipy as sc
import graficar as graf
from scipy import integrate
#Entradas:      Amplitudes A y B, arreglo de bits de la señal original, 
#               tiempo de la señal original y la portadora obtenida
#               según el tiempio.
#Salidas:       Señal original modulada y el tiempo de la señal modulada    
#Descripcion:   para cada bit de la señal original se verifica su valor. 
#               En caso de que el bit sea 0, se multiplica la portadora
#               por la amplituda A, en caso contrario, se multiplica por B.
#               Finalmente, se obtiene la señal modulada y su tiempo.
def modularASK(senal, bps, freqPortadora, freqMuestreoPortadora, cond):
    #Generar Intervalo de tiempo para la portadora
    tiempoPortadora = np.linspace(0,1/bps,freqMuestreoPortadora)
    #Generar Portadora
    portadora = np.cos(2*np.pi*freqPortadora*tiempoPortadora)
    #Graficar Portadora en el tiempo
    if(cond):
        graf.graficar(portadora, tiempoPortadora, "Señal Portadora en el tiempo", "Tiempo (s)", "Amplitud")

    #Algoritmo para modular
    senalModulada = []
    for bit in senal:
        for dato in portadora:
            senalModulada.append(3*bit*dato)
        #modulador = np.concatenate([modulador,(bit*portadora)])   
    tiempoModulada = np.linspace(0,len(senal)/bps,len(senalModulada))
    return np.array(senalModulada),tiempoModulada
    #Generar intervalo de tiempo para la modulada

#Entradas:      Amplitudes A,B, señal original modulada, señal portadora, 
#               freucencua de muestreo de la portadora (tamanoSegmento),
#               tiempo de la portadora y tiempo de la señal modulada.
#Salida:        Señal demodulada
#Descripción:   
def demodularASK(modulada, bps,freqPortadora, freqMuestreoPortadora):
    #Generar Intervalo de tiempo para la portadora
    tiempoPortadora = np.linspace(0,1/bps,freqMuestreoPortadora)
    #Generar Portadora
    portadora = np.cos(2*np.pi*freqPortadora*tiempoPortadora)
    areaEstandar = integrate.trapz(2*portadora*portadora, tiempoPortadora)
    inicio = 0
    fin = len(tiempoPortadora)
    demodulada = []
    for i in range(0,len(modulada), len(tiempoPortadora)):
        area = integrate.trapz(portadora*modulada[inicio:fin], tiempoPortadora)
        if(area >= areaEstandar):
            demodulada.append(1)
        else:
            demodulada.append(0)
        inicio = fin
        fin = fin + len(tiempoPortadora)
    
    print("demodulada: ")
    print(np.array(demodulada))
    return demodulada