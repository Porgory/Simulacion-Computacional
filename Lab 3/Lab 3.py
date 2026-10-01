import math
import matplotlib.pyplot as plt

class GeneradorCongruencial:
    def __init__(self, semilla=123456789):
        self.x = semilla
        self.a = 1664525
        self.c = 1013904223
        self.m = 2**32

    def uniforme(self):
        self.x = (self.a * self.x + self.c) % self.m
        return self.x / self.m


gen = GeneradorCongruencial(123456789)


def exponencial(u, tasa):
    return -math.log(1.0 - u) / tasa


print("\n" + "=" * 70)
print("LABORATORIO 4 - GENERACION DE VARIABLES ALEATORIAS CONTINUAS")
print("=" * 70)

print("\n2. CONSULTA PREVIA\n")

print("1. ¿Que es una variable aleatoria?")
print("Es una funcion que asigna un numero real a cada resultado posible de un experimento aleatorio.")

print("\n2. ¿Que es una distribucion de probabilidad?")
print("Es la forma de describir como se distribuyen las probabilidades de los posibles valores de una variable aleatoria.")

print("\n3. Diferencia entre distribucion discreta y continua:")
print("Una distribucion discreta trabaja con valores aislados y asigna una probabilidad a cada valor.")
print("Una distribucion continua trabaja con valores de un intervalo y se describe mediante una funcion de densidad.")
print("En una variable continua, la probabilidad de obtener exactamente un valor es cero.")

print("\n4. Distribucion exponencial:")
print("La distribucion exponencial modela tiempos entre eventos de un proceso de Poisson.")
print("Su funcion de densidad es f(x)=lambda*exp(-lambda*x), para x >= 0.")
print("Su parametro lambda es la tasa de ocurrencia de eventos.")

print("\n5. Distribucion Gamma:")
print("La Gamma es una distribucion continua definida para valores mayores o iguales que cero.")
print("Usaremos los parametros de forma alfa y tasa beta.")
print("Su densidad es f(x)=beta^alfa*x^(alfa-1)*exp(-beta*x)/Gamma(alfa).")

print("\n6. Normal estandar:")
print("La normal estandar es una distribucion normal con media 0 y desviacion estandar 1.")
print("Sus parametros son media mu=0 y desviacion estandar sigma=1.")

print("\n7. Proceso de Poisson y proceso de Poisson no homogeneo:")
print("Un proceso de Poisson homogeneo tiene una tasa constante lambda.")
print("Un proceso de Poisson no homogeneo tiene una tasa que cambia con el tiempo, lambda(t).")
print("La diferencia principal es que en el primero la intensidad es constante y en el segundo depende del tiempo.")


N = 1000


def generar_a(n):
    valores = []
    for _ in range(n):
        u = gen.uniforme()
        x = math.log(1.0 + u * (math.e - 1.0))
        valores.append(x)
    return valores


def densidad_a(x):
    return math.exp(x) / (math.e - 1.0)


def densidad_b(x):
    if 2.0 <= x <= 3.0:
        return (x - 2.0) / 2.0
    if 3.0 < x <= 6.0:
        return (2.0 - x / 3.0) / 2.0
    return 0.0


def generar_b(n):
    valores = []
    intentos = 0

    while len(valores) < n:
        x = 2.0 + 4.0 * gen.uniforme()
        y = 0.5 * gen.uniforme()
        intentos += 1

        if y <= densidad_b(x):
            valores.append(x)

    return valores, intentos


def generar_c(n):
    valores = []
    for _ in range(n):
        u = gen.uniforme()
        x = (-1.0 + math.sqrt(1.0 + 8.0 * u)) / 2.0
        valores.append(x)
    return valores


def densidad_c(x):
    return x + 0.5 if 0.0 <= x <= 1.0 else 0.0


def generar_d(n, alpha=2.0, beta=1.5):
    valores = []
    for _ in range(n):
        u = gen.uniforme()
        x = (-math.log(1.0 - u) / alpha) ** (1.0 / beta)
        valores.append(x)
    return valores


def densidad_d(x, alpha=2.0, beta=1.5):
    if x < 0:
        return 0.0
    return alpha * beta * (x ** (beta - 1.0)) * math.exp(-alpha * (x ** beta))


def graficar_resultado(valores, densidad, xmin, xmax, titulo, bins=30):
    plt.figure(figsize=(9, 5))
    plt.hist(
        valores,
        bins=bins,
        density=True,
        alpha=0.65,
        edgecolor="black",
        label="Valores generados"
    )

    paso = (xmax - xmin) / 500.0
    xs = [xmin + i * paso for i in range(501)]
    ys = [densidad(x) for x in xs]

    plt.plot(xs, ys, linewidth=2, label="Distribucion teorica")
    plt.title(titulo)
    plt.xlabel("x")
    plt.ylabel("Densidad")
    plt.legend()
    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.show()


print("\n" + "=" * 70)
print("5.1 GENERACION DE VARIABLES ALEATORIAS CONTINUAS")
print("=" * 70)

a = generar_a(N)

print("\na) Funcion de densidad f(x)=e^x/(e-1), 0<=x<=1")
print("Primeros 10 valores:", [round(x, 5) for x in a[:10]])
print("Promedio generado:", round(sum(a) / N, 5))
print("Promedio teorico:", round(1 / (math.e - 1), 5))

graficar_resultado(
    a,
    densidad_a,
    0,
    1,
    "a) Distribucion generada vs teorica"
)


b, intentos_b = generar_b(N)

print("\nb) Funcion de densidad por tramos - metodo del rechazo")
print("Primeros 10 valores:", [round(x, 5) for x in b[:10]])
print("Promedio generado:", round(sum(b) / N, 5))
print("Intentos realizados:", intentos_b)
print("Tasa de aceptacion:", round(N / intentos_b, 4))

graficar_resultado(
    b,
    densidad_b,
    2,
    6,
    "b) Metodo del rechazo",
    bins=30
)


c = generar_c(N)

print("\nc) F(x)=(x^2+x)/2 - transformada inversa")
print("Primeros 10 valores:", [round(x, 5) for x in c[:10]])
print("Promedio generado:", round(sum(c) / N, 5))
print("Promedio teorico:", round(7 / 12, 5))

graficar_resultado(
    c,
    densidad_c,
    0,
    1,
    "c) Transformada inversa"
)


ALPHA = 2.0
BETA = 1.5

d = generar_d(N, ALPHA, BETA)

print("\nd) Distribucion Weibull")
print("Parametros usados: alpha =", ALPHA, "beta =", BETA)
print("Primeros 10 valores:", [round(x, 5) for x in d[:10]])
print("Promedio generado:", round(sum(d) / N, 5))

media_weibull = (
    (1 / ALPHA) ** (1 / BETA)
    * math.gamma(1 + 1 / BETA)
)

print("Promedio teorico aproximado:", round(media_weibull, 5))

graficar_resultado(
    d,
    lambda x: densidad_d(x, ALPHA, BETA),
    0,
    max(d),
    "d) Distribucion Weibull",
    bins=30
)


print("\nCONCLUSIONES 5.1")
print("- En los cuatro casos se generaron 1000 valores usando un generador congruencial mixto.")
print("- La transformada inversa permite obtener directamente los casos a y c.")
print("- Para la densidad por tramos del punto b se utilizo el metodo del rechazo.")
print("- Para Weibull se aplico la transformada inversa a partir de su funcion de distribucion.")
print("- Los histogramas permiten comparar visualmente los valores generados con la distribucion teorica.")


def proceso_poisson(T, tasa):
    tiempos = []
    tiempo = 0.0

    while True:
        u = gen.uniforme()
        interarribo = exponencial(u, tasa)
        tiempo += interarribo

        if tiempo > T:
            break

        tiempos.append(tiempo)

    return tiempos


print("\n" + "=" * 70)
print("5.2 GENERANDO PROCESOS DE POISSON")
print("=" * 70)

T = 20.0
LAMBDA = 2.0

poisson = proceso_poisson(T, LAMBDA)

print("\na) Proceso de Poisson")
print("Valores usados: T =", T, "lambda =", LAMBDA)
print("Numero de eventos:", len(poisson))
print("Tiempos de los eventos:")
print([round(x, 5) for x in poisson])

esperado = LAMBDA * T

print("Numero esperado de eventos lambda*T:", esperado)

plt.figure(figsize=(10, 4))
plt.step(
    [0] + poisson,
    range(len(poisson) + 1),
    where="post"
)

plt.title("Proceso de Poisson")
plt.xlabel("Tiempo")
plt.ylabel("Numero acumulado de eventos")
plt.grid(alpha=0.25)
plt.tight_layout()
plt.show()


def generar_coxian(lambdas, alphas):
    tiempo_total = 0.0
    etapas_realizadas = 0

    for i in range(len(lambdas)):
        u = gen.uniforme()
        tiempo_total += exponencial(u, lambdas[i])
        etapas_realizadas += 1

        u = gen.uniforme()

        if u > alphas[i]:
            break

    return tiempo_total, etapas_realizadas


print("\nb) Variable aleatoria Coxian")

lambdas = [1.0, 1.5, 2.0, 1.2, 0.8]
alphas = [0.90, 0.80, 0.70, 0.60, 0.50]

print("Tasas lambda_i:", lambdas)
print("Probabilidades alpha_i:", alphas)

muestras_coxian = []
etapas_coxian = []

for _ in range(1000):
    tiempo, etapas = generar_coxian(
        lambdas,
        alphas
    )

    muestras_coxian.append(tiempo)
    etapas_coxian.append(etapas)

print(
    "Primeros 10 tiempos Coxian:",
    [round(x, 5) for x in muestras_coxian[:10]]
)

print(
    "Promedio del tiempo de trabajo:",
    round(sum(muestras_coxian) / len(muestras_coxian), 5)
)

print(
    "Promedio de etapas realizadas:",
    round(sum(etapas_coxian) / len(etapas_coxian), 5)
)

plt.figure(figsize=(9, 5))

plt.hist(
    muestras_coxian,
    bins=30,
    density=True,
    edgecolor="black"
)

plt.title("Variable aleatoria Coxian")
plt.xlabel("Tiempo total de trabajo")
plt.ylabel("Densidad")
plt.grid(alpha=0.25)
plt.tight_layout()
plt.show()


print("\nCONCLUSIONES 5.2")
print("- El proceso de Poisson se genero acumulando tiempos entre eventos con distribucion exponencial.")
print("- Con lambda=2 y T=20, el numero esperado de eventos es 40.")
print("- La variable Coxian se genero sumando tiempos exponenciales mientras el trabajador continua a la siguiente etapa.")
print("- Las probabilidades alpha_i controlan si el trabajador continua o termina el trabajo.")


def intensidad(t):
    if 0.0 < t < 5.0:
        return t / 5.0

    if 5.0 <= t < 10.0:
        return 1.0 + 5.0 * (t - 5.0)

    return 0.0


def proceso_poisson_no_homogeneo(T):
    lambda_max = 26.0
    eventos = []
    tiempo = 0.0

    while True:
        u = gen.uniforme()

        tiempo += exponencial(
            u,
            lambda_max
        )

        if tiempo > T:
            break

        u_aceptacion = gen.uniforme()

        if u_aceptacion <= intensidad(tiempo) / lambda_max:
            eventos.append(tiempo)

    return eventos


print("\n" + "=" * 70)
print("5.3 PROCESO DE POISSON NO HOMOGENEO")
print("=" * 70)

eventos_nh = proceso_poisson_no_homogeneo(10.0)

print("Intervalo: 0 < t < 10")
print("Intensidad maxima usada:", 26.0)
print("Eventos generados:", len(eventos_nh))
print("Tiempos:")
print([round(x, 5) for x in eventos_nh])

valor_esperado_nh = 2.5 + 67.5

print(
    "Numero esperado de eventos:",
    valor_esperado_nh
)

plt.figure(figsize=(10, 4))

plt.step(
    [0] + eventos_nh,
    range(len(eventos_nh) + 1),
    where="post"
)

plt.title("Proceso de Poisson no homogeneo")
plt.xlabel("Tiempo")
plt.ylabel("Numero acumulado de eventos")
plt.grid(alpha=0.25)
plt.tight_layout()
plt.show()


print("\nCONCLUSIONES 5.3")
print("- Se utilizo el metodo de adelgazamiento para generar el proceso no homogeneo.")
print("- La intensidad cambia con el tiempo y alcanza un maximo de 26 en el intervalo estudiado.")
print("- Primero se genero un proceso homogeneo con tasa 26 y luego se aceptaron eventos segun lambda(t)/26.")
print("- La cantidad esperada de eventos entre 0 y 10 es 70.")


print("\n" + "=" * 70)
print("CONCLUSION GENERAL")
print("=" * 70)

print("Los metodos de transformada inversa y rechazo permiten generar variables")
print("aleatorias continuas a partir de funciones de distribucion o densidad.")

print("Los procesos de Poisson se pueden construir usando tiempos entre llegadas")
print("exponenciales, mientras que para una tasa variable se puede utilizar")
print("el metodo de adelgazamiento.")

print("=" * 70)