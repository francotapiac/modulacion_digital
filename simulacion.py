import numpy as np
import modulacion as mod
import graficar as graf
import scipy as sc
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

def calcularBER(senalOriginal,senalDemodulada):
    cantidadDiferentes = 0
    for elemento1,elemento2 in zip(senalOriginal,senalDemodulada):
        if(elemento1 != elemento2):
            cantidadDiferentes = cantidadDiferentes + 1
    ber = cantidadDiferentes/len(senalOriginal)
    return ber

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