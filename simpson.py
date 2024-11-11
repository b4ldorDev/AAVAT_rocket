import numpy as np

def integrar(x):
    return 0.0098*x**4 - 0.1465*x**3 + 0.6*x**2 + 0.5277*x - 4.6


def simpson(func, a, b, tramos):
    if tramos % 2 != 0:
        raise ValueError("Error")

    h = (b - a) / tramos  
    xi = np.linspace(a, b, tramos + 1)
    deltaAreas = (h / 3) * np.sum([func(xi[i]) + 4 * func(xi[i + 1]) + func(xi[i + 2]) for i in range(0, tramos, 2)])
    return deltaAreas
a = 3
b = 9 
tramos = 100

area =simpson(integrar, a, b, tramos)

print(f'Número de tramos: {tramos}')
print(f'Resusltado con simpson {area}' ) 