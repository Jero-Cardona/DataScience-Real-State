import numpy as np
import pandas as pd

# Configuración inicial
np.random.seed(42)
n_registros = 54700

# ── DICCIONARIO MAESTRO BASADO EN EL PDF (CON VARIABLES NUMÉRICAS) ────────────
# Se definen los valores de metro cuadrado por estrato y las clasificaciones numéricas.
sectores_info = {
    'Comuna 1 (Centro Histórico)': {
        'estratos': [2, 3, 4],
        'precio_m2_estrato': {2: 3_500_000, 3: 4_100_000, 4: 4_800_000},
        'area_mean': 134.8, 'area_std': 25.0, 'dist': 1.5,
        'tipo_num': 1, 'conj_num': 0, 'topo_num': 0, 'parq_num': 0
    },
    'Comuna 2 (San Antonio)': {
        'estratos': [3, 4, 5],
        'precio_m2_estrato': {3: 4_500_000, 4: 4_900_000, 5: 5_500_000},
        'area_mean': 146.5, 'area_std': 28.0, 'dist': 3.5,
        'tipo_num': 1, 'conj_num': 0, 'topo_num': 0, 'parq_num': 1
    },
    'Comuna 3 (Uribe Jaramillo)': {
        'estratos': [2, 3],
        'precio_m2_estrato': {2: 5_000_000, 3: 6_000_000},
        'area_mean': 106.45, 'area_std': 20.0, 'dist': 12.0,
        'tipo_num': 1, 'conj_num': 0, 'topo_num': 1, 'parq_num': 1
    },
    'Comuna 4 (El Porvenir)': {
        'estratos': [3, 4],
        'precio_m2_estrato': {3: 4_600_000, 4: 5_200_000},
        'area_mean': 157.27, 'area_std': 30.0, 'dist': 2.5,
        'tipo_num': 1, 'conj_num': 1, 'topo_num': 0, 'parq_num': 1
    },
    'Corregimiento Occidente (Llanogrande)': {
        'estratos': [5, 6],
        'precio_m2_estrato': {5: 7_200_000, 6: 8_500_000},
        'area_mean': 546.86, 'area_std': 120.0, 'dist': 12.0,
        'tipo_num': 0, 'conj_num': 1, 'topo_num': 1, 'parq_num': 1
    },
    'Corregimiento Sur (Cabeceras)': {
        'estratos': [4, 5, 6],
        'precio_m2_estrato': {4: 10_000_000, 5: 12_000_000, 6: 14_000_000},
        'area_mean': 327.6, 'area_std': 80.0, 'dist': 14.0,
        'tipo_num': 0, 'conj_num': 1, 'topo_num': 2, 'parq_num': 1
    },
    'Corregimiento Norte (Galicia/La Mosca)': {
        'estratos': [2, 3, 4],
        'precio_m2_estrato': {2: 6_500_000, 3: 7_600_000, 4: 8_500_000},
        'area_mean': 213.0, 'area_std': 45.0, 'dist': 10.0,
        'tipo_num': 0, 'conj_num': 0, 'topo_num': 3, 'parq_num': 1
    },
    'Corregimiento Centro (Río Abajo)': {
        'estratos': [3, 4],
        'precio_m2_estrato': {3: 1_200_000, 4: 1_600_000},
        'area_mean': 1135.0, 'area_std': 250.0, 'dist': 6.0,
        'tipo_num': 0, 'conj_num': 0, 'topo_num': 2, 'parq_num': 1
    }
}

# ── GENERACIÓN DE DATOS ───────────────────────────────────────────────────────
sectores_list = list(sectores_info.keys())
sectores_seeds = np.random.choice(sectores_list, size=n_registros)

data_final = []

for sector_nombre in sectores_seeds:
    s = sectores_info[sector_nombre]
    
    # 1. Estrato
    estrato = int(np.random.choice(s['estratos']))
    
    # 2. Generación de Área
    area = np.random.normal(s['area_mean'], s['area_std'])
    area = max(area, 40.0) # Aseguramos que no haya propiedades irreales (menores a 40m2)
    
    # 3. Cálculo del Precio (Área * Valor m² según Estrato y Sector)
    valor_m2_base = s['precio_m2_estrato'][estrato]
    precio_estimado = area * valor_m2_base
    
    # Ruido aleatorio (+/- 5%) para simular dinámicas del mercado inmobiliario
    ruido_mercado = np.random.uniform(0.95, 1.05)
    precio_final = round((precio_estimado * ruido_mercado), -6) # Redondeado a millones
    
    # Agregar al array principal
    data_final.append({
        "Sector": sector_nombre,
        "Tiene_Parqueadero_Num": s['parq_num'],
        "Precio_Venta_COP": int(precio_final),
        "Estrato": estrato,
        "Area_Construida_m2": round(area, 2),
        "Distancia_CC_SanNicolas_km": s['dist'],
        "Conjunto_Cerrado_Num": s['conj_num'],
        "Urbana_Rural_Num": s['tipo_num'],
        "Topografia_Num": s['topo_num']
    })

# ── CREACIÓN Y GUARDADO DEL DATAFRAME ─────────────────────────────────────────
df = pd.DataFrame(data_final)

# Asegurar el mismo orden de la tabla original del PDF
columnas_orden = [
    "Sector", "Tiene_Parqueadero_Num", "Precio_Venta_COP", "Estrato", 
    "Area_Construida_m2", "Distancia_CC_SanNicolas_km", 
    "Conjunto_Cerrado_Num", "Urbana_Rural_Num", "Topografia_Num"
]
df = df[columnas_orden]

# Guardar a CSV
df.to_csv("dataset_inmobiliario_numerico_rionegro.csv", index=False)

print("Dataset numérico generado exitosamente con 5000 registros.")
print("\n--- Muestra del DataFrame resultante ---")
print(df.head(10))



# ── ANÁLISIS 2: TRANSFORMACIÓN POR ESCALAR (MIN-MAX) 
# Análisis 2 — Transformación por escalar
""" El precio en pesos colombianos y la distancia en kilómetros no viven en la misma
escala. Eso es un problema para las operaciones matriciales que vienen.
Transformen su matriz para que todas las columnas sean comparables. Elijan el
método, impleméntenlo y expliquen:
• ¿Qué operación de álgebra lineal realizaron? ¿Por qué se llama así? 
R/ La operación que realizamos es la normalziacion Min-Max, que tambien es conocida como escalamiento, simplemente es realizar la multiplicacion de vector (una columna entera) en este caso fue precio y distancia al CC San Nicolas restandole a ese valor de cada vector el minimo, por un escalar (un numero) que se obtiene de la formula 1 / (maximo - minimo) de cada vector, de esta manera obtenemos valores entre 0 y 1, donde los 0 se alejan se acrecan mas sea al dato que buscamos en este caso a una casa mas economica o mas cercana al CC San Nicolas, y los 1 se alejan mas de ese dato, es decir a una casa mas cara o mas lejana al CC San Nicolas.

Se llama de esta manera la operacion que realizamos porque el numero escalar encoge o estira el tamaño del vector. Estos nos ayuda para que los valores de nuestra 2 columnas (Vectores) sean comparables, es decir que vivan en el mismo vencidario numerico que seria entre 0 y 1, de esta manera evitamos que una de las 2 columnas domine a la otra por tener valores mas grandes, tambien para cuando apliquemos algoritmos de inteligencia artificial, estos no se vean sesgados por la escala de los datos, y puedan aprender patrones de manera mas eficiente y tener resultado mas coherentes."""


""" • Muestren los valores antes y después para al menos dos columnas. 
R/="""

print("\n" + "="*50)
print("ANÁLISIS 2: ANTES Y DESPUÉS DE LA TRANSFORMACIÓN")
print("="*50)

# 1. Definimos las columnas que vamos a transformar
col_precio = 'Precio_Venta_COP'
col_distancia = 'Distancia_CC_SanNicolas_km'

# 2. Calculamos los mínimos y máximos de toda la columna (nuestros vectores)
min_precio = df[col_precio].min()
max_precio = df[col_precio].max()

min_dist = df[col_distancia].min()
max_dist = df[col_distancia].max()

# 3. Aplicamos la operación de álgebra lineal: (vector - minimo) * escalar
# Recordando que el escalar es 1 / (maximo - minimo)
df['Precio_Escalado'] = (df[col_precio] - min_precio) / (max_precio - min_precio)
df['Distancia_Escalada'] = (df[col_distancia] - min_dist) / (max_dist - min_dist)

# 4. Mostramos el "Antes y Después" para cumplir con el taller
columnas_comparacion = [
    col_precio, 'Precio_Escalado', 
    col_distancia, 'Distancia_Escalada'
]

print("\n--- Muestra de los valores originales vs transformados ---")
# Imprimimos 10 registros para que se vea claramente el efecto
print(df[columnas_comparacion].head(10))
# ── GENERACIÓN DEL NUEVO CSV ESCALADO ────────────────────────────────────────
# Creamos un nombre de archivo diferente para no sobrescribir el anterior
nombre_archivo_escalado = "dataset_rionegro_analisis_escalado.csv"

# Guardamos el DataFrame que ya tiene las columnas 'Precio_Escalado' y 'Distancia_Escalada'
df.to_csv(nombre_archivo_escalado, index=False)

print(f"\n¡Listo! Se ha generado el archivo: {nombre_archivo_escalado}")
print("Ábrelo para comparar las columnas originales con las escaladas lado a lado.")

""" • ¿Qué le pasaría al análisis si no hicieran esta transformación? Demuestren con
un ejemplo concreto usando sus datos. 

R/ Si no hicieramos esa transformacion tendriamos un problema de escala, al tener 2 vectores con valores tan grandes como lo son los precios de las casas en pesos colombianos, y las distancias en kilometros, si mas adelante aplicaramos algoritmos de inteligencia artificial se verian afectados por la diferencia de escala, porque es mucha la diferencia que hay en el precio que son millones a la distancia que solo son numeros, entonces el algortimos ignoraria eso por completo y le daria mas importancia al precio que a la distancia. Un ejemplo seria, como si tuvieramos de 3 casas en llanogrande:

 - Casa A con un precio de 1200000000 con una distancia del CC San Nicolas de 2km
 - Casa B con un precio de 1200000000 con una distancia del CC San Nicolas de 10km
 - Casa C con un precio de 1200100000 con una distancia del CC San Nicolas de 2km
 
 Si nos ponemos a ver la logica, la casa A y la casa C son similares, 100000 pesos seria la diferencia entre las 2 porque la distancia al CC San Nicolas es la misma, pero si no hubieramos hecho la transformacion, el agoritmo de inteligencia artificial podria ver a la casa C como una casa totalmente diferente a la casa A solo por una diferencia de 100000 pesos porque ese valor es mucho más grande que la distancia por lo que el modelo podria aprender patrones erroneos, por lo que la normalizacion nos ayuda a evitar esto haciendo que ambas variables hablen el mismo idioma numerico (0 y 1)."""

# ── Ejemplo de codigo de como seria sin la transformacion ────────────────────────────────────────

# ---------------------------------------------------------
# DEMOSTRACIÓN DEL SESGO CON DATOS REALES DEL DATASET
# ---------------------------------------------------------
print("\n" + "="*50)
print("DEMOSTRACIÓN: QUÉ PASA SI NO ESCALAMOS (DATOS REALES)")
print("="*50)

# 1. Buscar Casa A (Tomamos la primera casa de nuestro dataset)
casa_A = df.iloc[0]
precio_A = casa_A['Precio_Venta_COP']
dist_A = casa_A['Distancia_CC_SanNicolas_km']

# 2. Buscar Casa B (Precio muy similar a A, pero muy lejos en distancia)
# Filtro: Precio con menos del 2% de diferencia, pero a más de 5km de distancia
filtro_B = (abs(df['Precio_Venta_COP'] - precio_A) < (precio_A * 0.15)) & (abs(df['Distancia_CC_SanNicolas_km'] - dist_A) > 5)
casa_B = df[filtro_B].iloc[0] # Tomamos la primera que cumpla la condición
precio_B = casa_B['Precio_Venta_COP']
dist_B = casa_B['Distancia_CC_SanNicolas_km']

# 3. Buscar Casa C (Misma zona/distancia que A, pero con diferente precio)
# Filtro: Exactamente la misma distancia, pero con una diferencia de precio notable (ej. > 20 millones)
filtro_C = (df['Distancia_CC_SanNicolas_km'] == dist_A) & (abs(df['Precio_Venta_COP'] - precio_A) > 50000000)
casa_C = df[filtro_C].iloc[0]
precio_C = casa_C['Precio_Venta_COP']
dist_C = casa_C['Distancia_CC_SanNicolas_km']

print("\n--- CASAS SELECCIONADAS DEL DATASET ---")
print(f"Casa A ({casa_A['Sector']}): Precio {precio_A:,.0f} | Distancia {dist_A} km")
print(f"Casa B ({casa_B['Sector']}): Precio {precio_B:,.0f} | Distancia {dist_B} km")
print(f"Casa C ({casa_C['Sector']}): Precio {precio_C:,.0f} | Distancia {dist_C} km")

print("\n--- 1. CÁLCULO SIN ESCALAR (El error del modelo) ---")
# Calculamos la distancia euclidiana con los datos crudos
dist_A_B_bruta = np.sqrt((precio_A - precio_B)**2 + (dist_A - dist_B)**2)
dist_A_C_bruta = np.sqrt((precio_A - precio_C)**2 + (dist_A - dist_C)**2)

print(f"Diferencia matemática Casa A y Casa B: {dist_A_B_bruta:,.2f}")
print(f"Diferencia matemática Casa A y Casa C: {dist_A_C_bruta:,.2f}")
print("-> ERROR FATAL: El modelo se ciega por los millones de pesos y clasifica mal la similitud geográfica.")

print("\n--- 2. CÁLCULO CON DATOS ESCALADOS (La solución) ---")
# Como nuestro DataFrame ya tiene las columnas escaladas, las usamos directamente
precio_A_esc, dist_A_esc = casa_A['Precio_Escalado'], casa_A['Distancia_Escalada']
precio_B_esc, dist_B_esc = casa_B['Precio_Escalado'], casa_B['Distancia_Escalada']
precio_C_esc, dist_C_esc = casa_C['Precio_Escalado'], casa_C['Distancia_Escalada']

# Nueva distancia matemática con los valores entre 0 y 1
dist_A_B_escalada = np.sqrt((precio_A_esc - precio_B_esc)**2 + (dist_A_esc - dist_B_esc)**2)
dist_A_C_escalada = np.sqrt((precio_A_esc - precio_C_esc)**2 + (dist_A_esc - dist_C_esc)**2)

print(f"Diferencia matemática Casa A y Casa B: {dist_A_B_escalada:.5f}")
print(f"Diferencia matemática Casa A y Casa C: {dist_A_C_escalada:.5f}")
print("-> ÉXITO: El modelo ahora compara de forma equilibrada, dando el peso correcto a la ubicación.")

# =====================================================================
# PREPARACIÓN Y ANÁLISIS 3: MATRIZ DE COVARIANZA (El insumo necesario)
# =====================================================================
print("\n" + "="*50)
print("PREPARACIÓN Y ANÁLISIS 3: MATRIZ DE COVARIANZA")
print("="*50)

# 1. Seleccionamos las 4 variables numéricas principales para analizar
cols_analisis = ['Precio_Venta_COP', 'Area_Construida_m2', 'Distancia_CC_SanNicolas_km', 'Estrato']

# 2. Normalizamos (Min-Max) todas para que la covarianza no se sesgue
df_norm = pd.DataFrame()
for col in cols_analisis:
    min_val = df[col].min()
    max_val = df[col].max()
    df_norm[col] = (df[col] - min_val) / (max_val - min_val)

# 3. Operación Matricial de Covarianza: (X_centrado^T * X_centrado) / (n - 1)
X_centrado = df_norm - df_norm.mean()
# En Python, el símbolo '@' hace la multiplicación de matrices (producto punto)
matriz_covarianza = (X_centrado.T @ X_centrado) / (len(df_norm) - 1)

print("Matriz de Covarianza calculada exitosamente. Dimensiones:", matriz_covarianza.shape)

# =====================================================================
# ANÁLISIS 4: EIGENVALORES Y EIGENVECTORES
# =====================================================================
print("\n" + "="*50)
print("ANÁLISIS 4: EIGENVALORES Y EIGENVECTORES")
print("="*50)

# 1. Calculamos los eigenvalores y eigenvectores de la matriz de covarianza
eigenvalores, eigenvectores = np.linalg.eig(matriz_covarianza)

# 2. Ordenamos de mayor a menor (Paso obligatorio en ciencia de datos)
pares_eigen = [(np.abs(eigenvalores[i]), eigenvectores[:, i]) for i in range(len(eigenvalores))]
pares_eigen.sort(key=lambda x: x[0], reverse=True)

eigenvalores_ord = np.array([par[0] for par in pares_eigen])
eigenvectores_ord = np.array([par[1] for par in pares_eigen]).T

print(f"\n--- RESPUESTAS PARA EL TALLER ---")

# SOLUCION DE PREGUNTAS DE ANÁLISIS 4:
"""• ¿Cuántos eigenvalores obtuvieron? ¿Podría haber más o menos? ¿Por qué? 
R/ Obtuvimos 4 eigenvalores, uno por cada variable numerica que analizamos en la matriz de covarianza. Como es una matriz de 4x4, el numero maximo que eigenvalores que podemos obtener es 4. Si podrian haber mas si agregamos una nueva variable como el numero de parqueaderos, o podria haber menos si quitamos la variable de estrato de la matriz de covarianza. Es decir el numerom de eigenvalores siempre es igual al numero de columnas de nuestra matriz.
"""

"""•Calculen qué porcentaje de la variación total representa cada eigenvalor.
R/ """

print("\n• Porcentaje de variación que representa cada eigenvalor:")
var_total = sum(eigenvalores_ord)
var_acumulada = 0
for i, val in enumerate(eigenvalores_ord):
    pct = (val / var_total) * 100
    var_acumulada += pct
    print(f"  Eigenvalor {i+1} ({val:.4f}): Explica el {pct:.2f}% de la variación (Acumulado: {var_acumulada:.2f}%)")

"""¿Cuántos eigenvalores necesitan para explicar más del 80% de la variación?
R/ Se necesitan solamente 2 eigenvalores para explicar mas del 80% de la variacion, el primer eigenvalor explica el 62.47% de la variacion y el segundo explica el 26.10% de la variacion, sumandolos nos da un resultado del 88.57% de la variacion por lo cual con solo 2 podemos explicar casi toda la complejidad del mercado inmobiliario de Rionegro usando solo 2 componentes principales, descartando a los otros."""

print("\n• Eigenvector del eigenvalor más grande (Pesos de las variables):")
# El primer eigenvector corresponde al eigenvalor más grande (el que más explica los datos)
eigenvector_principal = eigenvectores_ord[:, 0]
cols_analisis = ['Precio_Venta_COP', 'Area_Construida_m2', 'Distancia_CC_SanNicolas_km', 'Estrato']

"""• Miren el eigenvector del eigenvalor más grande. ¿Qué variable de Rionegro tiene más peso? ¿Qué le están diciéndole a la firma de inversión con ese resultado? 
R/ La variable de Rionegro que tiene más peso es la distancia al CC San Nicolas, con un peso de 0.7916. Lo que le estamos diciendo a la firma de inversion con este resultado es que el factor que influye mas y diferencia a una propiedad de la otra es su ubicacion con el CC San Nicolas, es decir, que las propiedades mas cercanas al mall son las que mas se valoran en el mercado inmobiliario de Rionegro, por lo tanto si van a invertir elijan propiedades que esten mas cercas al CC, porque incluso impacta mas que el tamaño fisico de la casa."""

for i, col in enumerate(cols_analisis):
    # Mostramos el valor absoluto para ver el peso (fuerza) real de la variable
    print(f"  Peso de {col}: {abs(eigenvector_principal[i]):.4f}")

"""• Verifiquen la definición C·v = λ·v para el eigenvalor más grande. Calculen la norma de la diferencia entre ambos lados. ¿Qué obtienen y qué confirma ese número
R/ """

print("\n• Verificación C * v = lambda * v para el eigenvalor más grande:")
# C es la matriz, v es el vector principal, lam es el eigenvalor principal
C = matriz_covarianza.values
v = eigenvector_principal
lam = eigenvalores_ord[0]

# Multiplicación matriz-vector (Lado izquierdo)
lado_izquierdo = C @ v
# Multiplicación escalar-vector (Lado derecho)
lado_derecho = lam * v

# Calculamos la norma de la diferencia (distancia entre los dos resultados)
norma_dif = np.linalg.norm(lado_izquierdo - lado_derecho)

print(f"  Norma de la diferencia: {norma_dif}")
print("  (Al ser un número tan cercano a cero, se confirma matemáticamente que ambos lados son iguales).")

""" • Si tuvieran que reducir su análisis a una sola variable para predecir el precio de una vivienda en Rionegro, ¿cuál sería según sus eigenvalores? ¿Están de acuerdo con ese resultado como personas que conocen el contexto? 
R/ Si tuvieramos que reducir el analisis a una sola variable para predecir el precio de una vivienda en Rionegro, esa variable segun los eigenvalores seria la distancia al CC San Nicolas, porque es la variable con mayor peso (0.7916), domina casi el 80% del peso. Como conocedores del contexto de Rionegro, si estamos de acuerdo con este resultado, porque hoy en dia lo que es el CC San Nicolas es un centro que ha venido desarollandose mucho, donde las personas ya tienen este sitio como un punto para salir a realizar vueltas, como comer, comprar algo ya que cuenta con casi todos los tipos de almacenes, hay locales de sura, sucursales de bancos de importantes de bancolombia, ya es un sitio que es mas que solo un centro comercial, ya es un lugar que hace parte de Rionegro, ya es un punto que donde se menciona van a saber que estan hablando de Rionegro, por algo es el centro comercial del oriente antioqueño, su ubicacion es central, tiene cerca de todo, como el centro de Rionegro, clinicas como la somer, por eso la distancia a este centro comercial es muy importante para el valor de las propiedades y lugar central para vivir cerca de él."""