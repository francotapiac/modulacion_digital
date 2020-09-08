import numpy as np
import matplotlib.pyplot as plt
import scipy as sc
from scipy import integrate

#Cada vez que aumenta la tasa de datos (tasa de bits), debe aumentar la frecuencia de la portadora

arregloBits = [1,1,0,1,0,0,1,1,0,1,0,1,0,0]         #Arreglo de bits
A = 2                                               #Amplitud con bit 0
B = 3                                               #Amplitud con bit 1
bps = 5                                             #tasa de bits: bits por segundo
tiempoArreglo = len(arregloBits)                    #Tiempo duración
frecuenciaPortadora = 5*bps
frecuenciaMuestreoPortadora = 5*frecuenciaPortadora

############### Todo lo relacionado a la portadora (mover a otro archivo)
def obtenerTiempoPortadora(bps,frecuenciaMuestreoPortadora):
    tiempoPortadora = np.linspace(0,1/bps,frecuenciaMuestreoPortadora)   
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

def demodularASK(A,B,modulada, portadora, tamanoSegmento, tiempoPortadora,tiempoModulada):
    areaA1 = 0
    if(A < B):
        areaA1 = calcularArea(A*portadora*portadora,tiempoPortadora)
    else:
        areaA1 = calcularArea(B*portadora*portadora,tiempoPortadora)
    portadora = portadora[0:len(portadora) - 1]
    demodulada = []
    segmento = []
    segmentoTiempo = []
    contador = 0
    areaSegmento = 0
    for elemento1, elemento2 in zip(modulada,tiempoModulada):
        if( contador == tamanoSegmento - 1):
            areaSegmento = calcularArea(portadora*segmento,segmentoTiempo)
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
    return demodulada

###### Agregar ruido

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

##### Sistema de comunicación
def crearSenalDigital():
    senal = np.random.randint(2,size = 100000)
    return senal

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
demodulada = demodularASK(A,B,modulada, portadora, frecuenciaMuestreoPortadora,tiempoPortadora,tiempoModulador)

snr = 2
senalRuido = simuladorRuido(modulada, snr)

arregloSNR = [0.5,1,-2]
resultadosBER = []
senal = crearSenalDigital()
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




