import matplotlib.pyplot as plt

def graficar(modulador, tiempoModulador, titulo):
    plt.plot(tiempoModulador,modulador)
    plt.title(titulo)
    plt.grid()
    plt.show()

def crearSubGrafico(dato,valorEjeX,titulo,xLabel,yLabel,color,filas,columnas,posicion):
    plt.subplot(filas,columnas,posicion, drawstyle='steps-pre')
    plt.title(titulo)
    plt.plot(valorEjeX,dato,color=color, drawstyle='steps-pre')
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)

def mostrarGraficos():
    plt.show()