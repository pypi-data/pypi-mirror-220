import matplotlib.pyplot as plt

def trasparente(color:str):
    """Para sacar los graficos en trasparente que puede ser util en cualquier caso. Solo funciona con matplotlib
    Args:
        color (str): Escoge el color que deseas, pero siempre utilizando las convenciones de python
    """
    #crea un figura con fondo trasparente
    fig=plt.figure(facecolor="none")
    
    #crear ejes dentro de la figura
    ax=fig.add_subplot(111, facecolor="none")
    
    ax=plt.gca()
    # Cambiar el color de los ejes, los números y el marco
    ax.spines['bottom'].set_color(color)   # Eje x
    ax.spines['left'].set_color(color)    # Eje y
    ax.spines['top'].set_color(color)     # Remover borde superior
    ax.spines['right'].set_color(color)   # Remover borde derecho
    
    ax.xaxis.label.set_color(color)   # color de la etiqueta del eje x
    ax.yaxis.label.set_color(color)   # color de la etiqueta del eje y
    
    ax.tick_params(axis='x', colors=color)   # Color de los ticks del eje x
    ax.tick_params(axis='y', colors=color)   # Color de los ticks del eje y