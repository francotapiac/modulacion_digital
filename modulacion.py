import numpy as np
import scipy as sc
#Entradas:      Amplitudes A y B, arreglo de bits de la señal original, 
#               tiempo de la señal original y la portadora obtenida
#               según el tiempio.
#Salidas:       Señal original modulada y el tiempo de la señal modulada    
#Descripcion:   para cada bit de la señal original se verifica su valor. 
#               En caso de que el bit sea 0, se multiplica la portadora
#               por la amplituda A, en caso contrario, se multiplica por B.
#               Finalmente, se obtiene la señal modulada y su tiempo.
def moduladorASK(arregloBits, tiempoArreglo, portadora, bps):
    modulador = []
    for bit in arregloBits:
        for e in portadora:
            modulador.append(bit*e)
        #modulador = np.concatenate([modulador,(bit*portadora)])   
    tiempoModulador = np.linspace(0,tiempoArreglo/bps,len(modulador))
    return np.array(modulador),tiempoModulador

#Entradas:      Función y, eje x de la función
#Salida:        Integral de la función y respecto a x 
#Descipción:    Se obtiene el area de la función y, mediante integrate.trapz.
def calcularArea(y,x):
    integral = sc.integrate.trapz(y,x)
    return integral

#Entradas:      Amplitudes A,B, señal original modulada, señal portadora, 
#               freucencua de muestreo de la portadora (tamanoSegmento),
#               tiempo de la portadora y tiempo de la señal modulada.
#Salida:        Señal demodulada
#Descripción:   
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
            if( areaSegmento > areaA1):
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