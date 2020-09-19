import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
from scipy import integrate

def generarSenal(largo):
    senal = np.random.randint(2,size = largo)
    return senal

def graficar(senal, tiempo, titulo, xLabel, yLabel):
    plt.figure()
    plt.plot(tiempo, senal)
    plt.title(titulo)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.grid()

def graficarSenalDigital(senal, tiempo, titulo, xLabel, yLabel):
    plt.figure()
    plt.plot(tiempo,senal, drawstyle='steps-pre')
    plt.title(titulo)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.grid()

def modularASK(senal, bps, freqPortadora, freqMuestreoPortadora):
    #Generar Intervalo de tiempo para la portadora
    tiempoPortadora = np.linspace(0,1/bps,freqMuestreoPortadora)
    #Generar Portadora
    portadora = np.cos(2*np.pi*freqPortadora*tiempoPortadora)
    #Graficar Portadora en el tiempo
    graficar(portadora, tiempoPortadora, "Señal Portadora en el tiempo", "Tiempo (s)", "Amplitud")

    #Algoritmo para modular
    senalModulada = []
    for bit in senal:
        for dato in portadora:
            senalModulada.append(3*bit*dato)
        #modulador = np.concatenate([modulador,(bit*portadora)])   
    tiempoModulada = np.linspace(0,len(senal)/bps,len(senalModulada))
    return np.array(senalModulada),tiempoModulada
    #Generar intervalo de tiempo para la modulada

def simuladorRuido(senal, tiempoModulada, snrDb):
    ruido = np.random.normal(0.0, snrDb, len(senal))
    senalRuido = modulada + ruido
    return senalRuido

def demodularASK(modulada):
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

########################################################################################################
#Datos Iniciales
bps = 5
freqPortadora = 3*bps
freqMuestreoPortadora = 5*freqPortadora
arregloSNR = [-2,-1,0.5,1]
arregloBPS = [5,10,15]
snrDb = 0.1

#Prueba para un caso pequeño
#Generar Señal
senalDigital = generarSenal(100)
print("senal original")
print(senalDigital)
tiempo = np.linspace(0,len(senalDigital)/bps,len(senalDigital))
graficarSenalDigital(senalDigital, tiempo, "Señal Digital en el Tiempo", "Tiempo (s)", "Amplitud")
#Modular la Señal
modulada, tiempoModulada = modularASK(senalDigital, bps, freqPortadora, freqMuestreoPortadora)
graficar(modulada, tiempoModulada, "Señal Modulada en ASK", "Tiempo (s)", "Amplitud")
#Agregar Ruido
moduladaRuido = simuladorRuido(modulada, tiempoModulada, snrDb)
graficar(moduladaRuido, tiempoModulada, "Señal Modulada con Ruido AWGN", "Tiempo (s)", "Amplitud")
#Demodular la Señal
demodulada = demodularASK(moduladaRuido)

#Simulacion Caso grande

plt.show()
