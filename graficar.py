import matplotlib.pyplot as plt

def graficar(modulador, tiempoModulador, titulo):
    plt.figure()
    plt.plot(tiempoModulador,modulador)
    plt.title(titulo)
    plt.grid()

def graficarSenalEnTiempo(senal, tiempo, titulo):
    plt.figure()
    plt.plot(tiempo,senal, drawstyle='steps-pre')
    plt.title(titulo)
    plt.grid()

def crearSubGrafico(dato,valorEjeX,titulo,xLabel,yLabel,color,filas,columnas,posicion):
    plt.subplot(filas,columnas,posicion)
    plt.title(titulo)
    plt.plot(valorEjeX,dato,color=color, drawstyle='steps-pre')
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)

def mostrarGraficos():
    plt.show()