import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as sc
import warnings
warnings.filterwarnings('ignore')

#Cada vez que aumenta la tasa de datos (tasa de bits), debe aumentar la frecuencia de la portadora

arregloBits = [1,1,0,1,0,0,1,1,0,1,0,1,0,0]         #Arreglo de bits
A = 1                                               #Amplitud con bit 0
B = 2                                               #Amplitud con bit 1
bps = 10                                            #tasa de bits: bits por segundo
tiempoArreglo = len(arregloBits)                    #Tiempo duración
frecuenciaMuestrePortadora = 15

############### Todo lo relacionado a la portadora (mover a otro archivo)
def obtenerTiempoPortadora(bps):
    tiempoPortadora = np.linspace(0,1 - 1/bps,bps)
    return tiempoPortadora

def obtenerPortadora(frecuenciaMuestrePortadora,tiempoPortadora):
    portadora = np.cos(2*np.pi*frecuenciaMuestrePortadora*tiempoPortadora)
    return portadora

############### Todo lo relacionado a modular ASK (mover a otro archivo)
def moduladorASK(A,B,arregloBits, tiempoArreglo, portadora):
    modulador = []
    for bit in arregloBits:
        if(bit == 0):
            modulador = np.concatenate([modulador,(A*portadora)])   
        else:
            modulador = np.concatenate([modulador,(B*portadora)])    
    tiempoModulador = np.linspace(0,tiempoArreglo,len(modulador))
    return modulador,tiempoModulador



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

############### Main ###############
tiempoPortadora = obtenerTiempoPortadora(bps)
portadora = obtenerPortadora(frecuenciaMuestrePortadora,tiempoPortadora)

modulador,tiempoModulador = moduladorASK(A,B,arregloBits,tiempoArreglo,portadora)


crearSubGrafico(arregloBits,np.linspace(0,tiempoArreglo,tiempoArreglo),"Arreglo de bits","tiempo","amplitud","r",3,1,1)
crearSubGrafico(portadora,tiempoPortadora,"Portadora en el tiempo","tiempo","amplitud","g",3,1,2)
crearSubGrafico(modulador,tiempoModulador,"Modulada ASK","tiempo","amplitud","purple",3,1,3)
plt.show()

graficar(portadora,tiempoPortadora,"Señal Portadora")
graficar(modulador,tiempoModulador,"Modulada ASK")




