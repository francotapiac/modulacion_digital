import numpy as np
import scipy as sc
import lectura_arreglo as la
import modulacion as mod
import canal as ca
import simulacion as sim
import graficar as graf
from scipy import integrate

#Cada vez que aumenta la tasa de datos (tasa de bits), debe aumentar la frecuencia de la portadora

arregloBits = la.crearArregloBits()                 #Arreglo de bits
A = 0                                               #Amplitud con bit 0
B = 3                                               #Amplitud con bit 1
bps = 5                                             #tasa de bits: bits por segundo
tiempoArreglo = len(arregloBits)                    #Tiempo duración
frecuenciaPortadora = 5*bps
frecuenciaMuestreoPortadora = 5*frecuenciaPortadora
largoArregloAleatorio = 100000
arregloSNR = [0.5,1,-2]
snr = 2




#********************************************************************
#******************************* Main *******************************
#********************************************************************

#1. Obtención de la portadora
tiempoPortadora = la.obtenerTiempoPortadora(bps,frecuenciaMuestreoPortadora)
portadora = la.obtenerPortadora(frecuenciaPortadora,tiempoPortadora)

#2. Modulada de la señal original
modulada,tiempoModulador = mod.moduladorASK(A,B,arregloBits,tiempoArreglo,portadora,bps)
demodulada = mod.demodularASK(A,B,modulada, portadora, frecuenciaMuestreoPortadora,tiempoPortadora,tiempoModulador)

#3. Implementación de ruido de una señal
senalRuido = sim.simuladorRuido(modulada, snr)

resultadosBER = []
senal = sim.crearSenalDigital(largoArregloAleatorio)
moduladaSenalCreada,tiempoModuladorSenalCreada = mod.moduladorASK(A,B,senal,len(senal),portadora,bps)
#senal = senal[0:1000]
ber = 1
for snr in arregloSNR:
    ber = sim.simularTransmisionBits(senal,moduladaSenalCreada,snr)
    resultadosBER.append(ber)
print(resultadosBER)


graf.crearSubGrafico(arregloBits,np.linspace(0,tiempoArreglo/bps,tiempoArreglo),"Arreglo de bits","tiempo","amplitud","r",3,1,1)
graf.crearSubGrafico(portadora,tiempoPortadora,"Portadora en el tiempo","tiempo","amplitud","g",3,1,2)
graf.crearSubGrafico(modulada,tiempoModulador,"Modulada ASK","tiempo","amplitud","purple",3,1,3)
graf.mostrarGraficos()

graf.graficar(portadora,tiempoPortadora,"Señal Portadora")
graf.graficar(modulada,tiempoModulador,"Modulada ASK")
graf.graficar(demodulada,np.linspace(0,tiempoArreglo/bps,tiempoArreglo),"Demodulada ASK")
graf.graficar(senalRuido,tiempoModulador,"Señal modulada con ruido")




