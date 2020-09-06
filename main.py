import numpy as np
import matplotlib.pyplot as plt
import scipy as sc
from scipy import integrate

#Cada vez que aumenta la tasa de datos (tasa de bits), debe aumentar la frecuencia de la portadora

arregloBits = [1,1,0,1,0,0,1,1,0,1,0,1,0,0]         #Arreglo de bits
A = 1                                               #Amplitud con bit 0
B = 2                                               #Amplitud con bit 1
bps = 10                                            #tasa de bits: bits por segundo
tiempoArreglo = len(arregloBits)                    #Tiempo duración
frecuenciaPortadora = 10*bps
frecuenciaMuestreoPortadora = 10*frecuenciaPortadora

############### Todo lo relacionado a la portadora (mover a otro archivo)
def obtenerTiempoPortadora(bps,frecuenciaMuestreoPortadora):
    tiempoPortadora = np.linspace(0,1/bps,frecuenciaMuestreoPortadora)    #Se multiplica
    return tiempoPortadora

def obtenerPortadora(frecuenciaPortadora,tiempoPortadora):
    portadora = np.cos(2*np.pi*frecuenciaPortadora*tiempoPortadora)
    return portadora

############### Todo lo relacionado a modular ASK (mover a otro archivo)
def moduladorASK(A,B,arregloBits, tiempoArreglo, portadora):
    modulador = []
    for bit in arregloBits:
        if(bit == 0):
            modulador = np.concatenate([modulador,(A*portadora)])   
        else:
            modulador = np.concatenate([modulador,(B*portadora)])    
    tiempoModulador = np.linspace(0,tiempoArreglo/bps,len(modulador))
    return modulador,tiempoModulador


########### Demodular
def calcularArea(y,x):
    integral = integrate.trapz(y,x)
    return integral

def demodularASK(modulada, portadora, tamanoSegmento, tiempoPortadora,tiempoModulada):
    areaA1 = calcularArea(portadora,tiempoPortadora)
    print("areaA1:" + str(areaA1))
    demodulada = []
    segmento = []
    segmentoTiempo = []
    contador = 0
    areaSegmento = 0

    for elemento1, elemento2 in zip(modulada,tiempoModulada):
        if( contador == tamanoSegmento - 1):
            areaSegmento = calcularArea(segmento,segmentoTiempo)
            print("area segmento:" + str(areaSegmento))
            if( areaSegmento >= areaA1):
                demodulada.append(1)
            else:
                demodulada.append(0)
            segmentoTiempo = []
            segmento = []
            contador = 0
        else:
            segmento.append(elemento1)
            segmentoTiempo.append(elemento2)
            contador = contador + 1
    print(demodulada)
    return demodulada




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
tiempoPortadora = obtenerTiempoPortadora(bps,frecuenciaMuestreoPortadora)
portadora = obtenerPortadora(frecuenciaPortadora,tiempoPortadora)

modulada,tiempoModulador = moduladorASK(A,B,arregloBits,tiempoArreglo,portadora)
demodulada = demodularASK(modulada, portadora, frecuenciaMuestreoPortadora,tiempoPortadora,tiempoModulador)

crearSubGrafico(arregloBits,np.linspace(0,tiempoArreglo/bps,tiempoArreglo),"Arreglo de bits","tiempo","amplitud","r",3,1,1)
crearSubGrafico(portadora,tiempoPortadora,"Portadora en el tiempo","tiempo","amplitud","g",3,1,2)
crearSubGrafico(modulada,tiempoModulador,"Modulada ASK","tiempo","amplitud","purple",3,1,3)
plt.show()

graficar(portadora,tiempoPortadora,"Señal Portadora")
graficar(modulada,tiempoModulador,"Modulada ASK")
#graficar(demodulada,tiempoArreglo,"Demodulada ASK")




