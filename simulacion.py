import numpy as np
import modulacion as mod
import graficar as graf
import scipy as sc

# Entradas: senal -> array con los datos de la señal
#           tiempoModulada -> array que representa el tiempo
#           snrdB -> entero que representa el snr en decibeles
#           cond -> booleano que se utiliza para saber si se debe graficar o no
# Salidas:   senalRuido -> array con los datos de la señal con ruido
#------------------------------------------
# Esta funcion agrega ruido blanco gaussiano a la señal ingresada como 
# parametro segun el snr ingresado
def simuladorRuido(senal, tiempoModulada, snrDb, cond):
    w = 1
    T = 2*np.pi/w
    energia = sc.integrate.simps(senal**2,tiempoModulada)
    potenciaSenal = (1/T)*energia
    print(potenciaSenal)
    snr = 10.0**(snrDb/10.0)
    print(snr)
    desviacionEstandar = np.sqrt(potenciaSenal/snr)
    print(desviacionEstandar)
    ruido = np.random.normal(0,desviacionEstandar,len(senal))
    if(cond):
        graf.graficarRuido(ruido,'Ruido AWGN con SNR = '+str(snrDb)+ '(dB)', 'Tiempo (s)', 'Amplitud', 'SNR = '+str(snrDb)+ '(dB)')
    senalRuido = senal + ruido
    return senalRuido

# Entradas: senalOriginal -> array con los datos de la señal
#           senalDemodulada -> array con los datos de la señal demodulada
# Salidas:   ber -> float que representa la tasa de error de bits
#------------------------------------------
# Esta funcion cuenta los bits diferentes entre la señal original 
# y la señal demodulada y calcula la tasa de error de bits
def calcularBER(senalOriginal,senalDemodulada):
    cantidadDiferentes = 0
    for elemento1,elemento2 in zip(senalOriginal,senalDemodulada):
        if(elemento1 != elemento2):
            cantidadDiferentes = cantidadDiferentes + 1
    ber = cantidadDiferentes/len(senalOriginal)
    return ber

# Entradas: senalOriginal -> array con los datos de la señal
#           modulada -> array con los datos de la señal modulada
#           tiempoModulada -> array que representa el tiempo
#           arraySNRinDb -> array que contiene los snr a utilizar
#           freqPortadora -> frecuencia de la señal portadora utilizada
#           freqMuestreoPortadora -> frecuencia de muestreo de la señal portadora utilizada
#           bps -> Tasa de bits por segundo utilizada
# Salidas:   BER -> array con los ber calculados
#------------------------------------------
# Esta funcion agrega diferentes niveles de ruido blanco gaussiano a la señal 
# ingresada como parametro luego demodula y va calculando las tasas de error de bits
# los ber calculados se guardan y se retornan en un array
def simulacion(senalOriginal, modulada, tiempoModulada, arraySNRinDb, freqPortadora, freqMuestreoPortadora, bps):
    #array para guardar los ber calculados para cada señal con diferentes snr
    moduladaRuido = []
    demodulada = []
    BER = [None]*len(arraySNRinDb)
    i = 0
    for snrDb in arraySNRinDb:
        ber = 0
        #Agregar Ruido
        moduladaRuido = simuladorRuido(modulada, tiempoModulada, snrDb, False)
        #Demodular la Señal
        demodulada = mod.demodularASK(moduladaRuido, bps, freqPortadora, freqMuestreoPortadora)
        #Calcular BER
        ber = calcularBER(senalOriginal, demodulada)
        print("ber: "+ str(ber))
        #Guardar ber
        BER[i] = ber
        i +=1
    return BER