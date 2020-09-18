import numpy as np
import scipy as sc
import lectura_arreglo as la
import modulacion as mod
import canal as ca
import simulacion as sim
import graficar as graf
from scipy import integrate
import matplotlib.pyplot as plt
#********************************************************************
#******************************* Main *******************************
#********************************************************************

#Cada vez que aumenta la tasa de datos (tasa de bits), debe aumentar la frecuencia de la portadora

senalCorta = la.crearArregloBits()                 #Arreglo de bits
A = 0                                               #Amplitud con bit 0
B = 3                                               #Amplitud con bit 1
bps = 5                                             #tasa de bits: bits por segundo
tiempoSenalCorta = np.linspace(0,len(senalCorta)/bps,len(senalCorta))                   #Tiempo duración
frecuenciaPortadora = 10*bps
frecuenciaMuestreoPortadora = 10*frecuenciaPortadora
largoSenalLarga = 100000
arregloSNR = [0.5,1,-2]
arregloBPS = [5,20,30]
snrDb = 2

#1. Obtención de la portadora
tiempoPortadora = la.obtenerTiempoPortadora(bps,frecuenciaMuestreoPortadora)
portadora = la.obtenerPortadora(frecuenciaPortadora,tiempoPortadora)

#2. Modulada de la señal original
modulada, tiempoModulador = mod.moduladorASK(A,B,senalCorta,len(senalCorta),portadora,bps)
demodulada = mod.demodularASK(A,B,modulada, portadora, frecuenciaMuestreoPortadora,tiempoPortadora,tiempoModulador)

#3. Implementación de ruido de una señal
senalRuido = sim.simuladorRuido(modulada, snrDb)

#Graficar Resultados
graf.graficarSenalEnTiempo(senalCorta, tiempoSenalCorta, "Señal Digital en el Tiempo")
graf.graficar(portadora, tiempoPortadora, "Portadora en el Tiempo")
graf.graficar(modulada,tiempoModulador, "Señal Modulada ASK en el Tiempo")
graf.graficar(senalRuido, tiempoModulador, "Señal Modulada con Ruido AWGN")
plt.show()

###########################################################################################################
#Simulacion canal de comunicacion

resultados = []
resultadosBER = []
senal = sim.crearSenalDigital(largoSenalLarga)
ber = 1
for bps in arregloBPS:
    modulada,tiempoModulada = mod.moduladorASK(A,B,senal,len(senal),portadora,bps)
    print("1")
    for snr in arregloSNR:
        print("2")
        ber = sim.simularTransmisionBits(A,B,senal,modulada,snr,portadora,
                                    frecuenciaMuestreoPortadora, tiempoPortadora, tiempoModulada)
        resultadosBER.append(ber)
    resultados.append(resultadosBER)
    resultadosBER = []

plt.figure()
plt.plot(arregloSNR,resultados[0],resultadosBER[1],resultados[2], "Curva BER normalizada a la razón SNR para diferentes BPS")




#graf.graficar(portadora,tiempoPortadora,"Señal Portadora")
#graf.graficar(modulada,tiempoModulador,"Modulada ASK")
#graf.graficar(demodulada,np.linspace(0,tiempoArreglo/bps,tiempoArreglo),"Demodulada ASK")
#graf.graficar(senalRuido,tiempoModulador,"Señal modulada con ruido")




