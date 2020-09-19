import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
from scipy import integrate
from numpy.random import rand, randn

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

def modularASK(senal, bps, freqPortadora, freqMuestreoPortadora, cond):
    #Generar Intervalo de tiempo para la portadora
    tiempoPortadora = np.linspace(0,1/bps,freqMuestreoPortadora)
    #Generar Portadora
    portadora = np.cos(2*np.pi*freqPortadora*tiempoPortadora)
    #Graficar Portadora en el tiempo
    if(cond):
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
    w = 1
    T = 2*np.pi/w
    energia = sc.integrate.simps(modulada**2,tiempoModulada)
    potenciaSenal = (1/T)*energia
    print(potenciaSenal)
    snr = 10.0**(snrDb/10.0)
    print(snr)
    desviacionEstandar = np.sqrt(potenciaSenal/snr)
    print(desviacionEstandar)
    ruido = np.random.normal(0,desviacionEstandar,len(senal))
    senalRuido = senal + ruido
    return senalRuido

def demodularASK(modulada, bps,freqPortadora, freqMuestreoPortadora):
    #Generar Intervalo de tiempo para la portadora
    tiempoPortadora = np.linspace(0,1/bps,freqMuestreoPortadora)
    #Generar Portadora
    portadora = np.cos(2*np.pi*freqPortadora*tiempoPortadora)
    areaEstandar = integrate.trapz(3*portadora*portadora, tiempoPortadora)
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

def calcularBER(senalOriginal,senalDemodulada):
    cantidadDiferentes = 0
    for elemento1,elemento2 in zip(senalOriginal,senalDemodulada):
        if(elemento1 != elemento2):
            cantidadDiferentes = cantidadDiferentes + 1
    ber = cantidadDiferentes/len(senalOriginal)
    return ber

def simulacion(modulada, tiempoModulada, arraySNRinDb, freqPortadora, freqMuestreoPortadora):
    #array para guardar los ber calculados para cada señal con diferentes snr
    moduladaRuido = []
    demodulada = []
    BER = [None]*len(arraySNRinDb)
    i = 0
    for snrDb in arraySNRinDb:
        ber = 0
        #Agregar Ruido
        moduladaRuido = simuladorRuido(modulada, tiempoModulada, snrDb)
        #graficar(moduladaRuido, tiempoModulada, "Señal Modulada con Ruido AWGN - SNR="+str(snrDb) + " BPS="+str(bps), "Tiempo (s)", "Amplitud")
        #Demodular la Señal
        demodulada = demodularASK(moduladaRuido, bps, freqPortadora, freqMuestreoPortadora)
        #Calcular BER
        ber = calcularBER(senalDigital, demodulada)
        print("ber: "+ str(ber))
        #Guardar ber
        BER[i] = ber
        i +=1
    return BER

########################################################################################################
#Datos Iniciales
largoSenal = 10
bps = 5
freqPortadora = 3*bps
freqMuestreoPortadora = 5*freqPortadora
snrDb = 0.1

#Prueba para un caso pequeño
#Generar Señal
senalDigital = generarSenal(10)
print("senal corta")
print(senalDigital)
tiempo = np.linspace(0,len(senalDigital)/bps,len(senalDigital))
graficarSenalDigital(senalDigital, tiempo, "Señal Digital en el Tiempo", "Tiempo (s)", "Amplitud")
#Modular la Señal
modulada, tiempoModulada = modularASK(senalDigital, bps, freqPortadora, freqMuestreoPortadora, True)
graficar(modulada, tiempoModulada, "Señal Modulada en ASK", "Tiempo (s)", "Amplitud")
#Agregar Ruido
moduladaRuido = simuladorRuido(modulada, tiempoModulada, snrDb)
graficar(moduladaRuido, tiempoModulada, "Señal Modulada con Ruido AWGN", "Tiempo (s)", "Amplitud")
#Demodular la Señal
demodulada = demodularASK(moduladaRuido, bps, freqPortadora, freqMuestreoPortadora)

#Simulacion Caso grande
largoSenal = 10000
arraySNRinDb = range(0,5)
arrayBPS = [5,10,20]
plt.figure()
for bps in arrayBPS:
    freqPortadora = 3*bps
    freqMuestreoPortadora = 5*freqPortadora
    senalDigital = generarSenal(largoSenal)
    modulada, tiempoModulada = modularASK(senalDigital, bps, freqPortadora, freqMuestreoPortadora, False)
    BER = simulacion(modulada, tiempoModulada, arraySNRinDb, freqPortadora, freqMuestreoPortadora)

    plt.plot(arraySNRinDb, BER, 'bo', arraySNRinDb, BER, 'k')
    #plt.axis([0, 10, 1e-6, 0.1])
    plt.xscale('linear')
    plt.yscale('log')
    plt.xlabel('SNR(dB)')
    plt.ylabel('BER')
    plt.grid(True)
    plt.title('BER vs SNR')

"""
for n in range (0, lenSNR): 
    snrDb = arraySNRinDb[n]   
    snr=10.0**(snrDb/10.0)
    ruido = 1/np.sqrt(2*snr)
    SenalRuido = modulada + ruido * randn(len(modulada))
    demodulada = demodularASK(SenalRuido, bps, freqPortadora, freqMuestreoPortadora)
    BER[n] = calcularBER(senalDigital, demodulada)
"""


plt.show()

"""
print(resultadoSimulacion[0])
print(resultadoSimulacion[1])
print(resultadoSimulacion[2])
plt.figure()
plt.plot(SNR,resultadoSimulacion[0])
plt.plot(SNR,resultadoSimulacion[1])
plt.plot(SNR,resultadoSimulacion[2])
plt.show()
"""
