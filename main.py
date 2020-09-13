import numpy as np
import matplotlib.pyplot as plt
import scipy as sc
import lectura_arreglo as la
import modulacion as mod
import canal as ca
import simulacion as sim
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


############### Todo lo relacionado a graficar (mover a otro archivo)
def graficar(modulador, tiempoModulador, titulo):
    plt.plot(tiempoModulador,modulador)
    plt.title(titulo)
    plt.grid()
    plt.show()

def crearSubGrafico(dato,valorEjeX,titulo,xLabel,yLabel,color,filas,columnas,posicion):
    plt.subplot(filas,columnas,posicion)
    plt.title(titulo)
    plt.plot(valorEjeX,dato,color=color)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)

#********************************************************************
#******************************* Main *******************************
#********************************************************************

#1. Obtención de la portadora
tiempoPortadora = la.obtenerTiempoPortadora(bps,frecuenciaMuestreoPortadora)
portadora = la.obtenerPortadora(frecuenciaPortadora,tiempoPortadora)

#2. Modulada de la señal original
modulada,tiempoModulador = mod.moduladorASK(A,B,arregloBits,tiempoArreglo,portadora)
demodulada = mod.demodularASK(A,B,modulada, portadora, frecuenciaMuestreoPortadora,tiempoPortadora,tiempoModulador)

#3. Implementación de ruido de una señal
senalRuido = sim.simuladorRuido(modulada, snr)

resultadosBER = []
senal = sim.crearSenalDigital(largoArregloAleatorio)
moduladaSenalCreada,tiempoModuladorSenalCreada = moduladorASK(A,B,senal,len(senal),portadora)
#senal = senal[0:1000]
ber = 1
for snr in arregloSNR:
    ber = simularTransmisionBits(senal,moduladaSenalCreada,snr)
    resultadosBER.append(ber)
print(resultadosBER)


crearSubGrafico(arregloBits,np.linspace(0,tiempoArreglo/bps,tiempoArreglo),"Arreglo de bits","tiempo","amplitud","r",3,1,1)
crearSubGrafico(portadora,tiempoPortadora,"Portadora en el tiempo","tiempo","amplitud","g",3,1,2)
crearSubGrafico(modulada,tiempoModulador,"Modulada ASK","tiempo","amplitud","purple",3,1,3)
plt.show()

graficar(portadora,tiempoPortadora,"Señal Portadora")
graficar(modulada,tiempoModulador,"Modulada ASK")
graficar(demodulada,np.linspace(0,tiempoArreglo/bps,tiempoArreglo),"Demodulada ASK")
graficar(senalRuido,tiempoModulador,"Señal modulada con ruido")




