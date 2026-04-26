# Análisis del Mercado Inmobiliario Residencial de Rionegro, Antioquia: Una Aproximación desde el Álgebra Lineal

---

## Introducción

El municipio de Rionegro, ubicado en el oriente antioqueño de Colombia, ha experimentado un crecimiento inmobiliario sostenido en los últimos años, impulsado por su cercanía al Aeropuerto Internacional José María Córdova, su conectividad con Medellín y la expansión de su infraestructura comercial. En este contexto, comprender la estructura de precios del mercado residencial representa un desafío analítico relevante tanto para inversionistas privados como para agentes del sector.

El presente análisis fue desarrollado en respuesta a una solicitud de una firma de inversión interesada en identificar qué variables influyen en el precio de una vivienda en Rionegro, cómo se relacionan entre sí, y cuáles concentran mayor variación. Para abordar esta pregunta, se aplicaron técnicas de álgebra lineal —específicamente escalamiento de matrices, cálculo de covarianza y descomposición espectral— sobre un dataset simulado, construido a partir de fuentes oficiales y portales inmobiliarios del municipio.

La justificación del enfoque matricial radica en su capacidad para revelar estructuras latentes en los datos: relaciones entre variables que no son evidentes en un análisis univariado y que permiten sintetizar la complejidad del mercado en componentes interpretables. Como señala Cohen (2022), las operaciones sobre matrices son herramientas fundamentales para describir y comprender la variabilidad en conjuntos de datos multidimensionales.

---

## Metodología

### Construcción del Dataset

Ante la ausencia de un dataset público consolidado de precios residenciales en Rionegro, se optó por el **Camino B** de la metodología propuesta: la simulación de datos con distribuciones estadísticas realistas. El dataset fue generado con NumPy (`np.random.seed(42)`) y comprende **54.700 registros**, cifra fundamentada en el registro catastral municipal, que reporta aproximadamente 47.000 inmuebles de vivienda; se adicionaron cerca de 7.000 registros para incorporar fincas y propiedades rurales.

La generación se estructuró alrededor de **ocho sectores geográficos** de Rionegro, cada uno con parámetros propios de precio por metro cuadrado, área construida media, distancia al Centro Comercial San Nicolás y características urbanísticas. Los sectores incluidos fueron:

- Comuna 1 (Centro Histórico)
- Comuna 2 (San Antonio)
- Comuna 3 (Uribe Jaramillo)
- Comuna 4 (El Porvenir)
- Corregimiento Occidente (Llanogrande)
- Corregimiento Sur (Cabeceras)
- Corregimiento Norte (Galicia / La Mosca)
- Corregimiento Centro (Río Abajo)

El precio de cada inmueble se calculó como el producto entre el área construida (generada con distribución normal) y el valor del metro cuadrado según estrato y sector, con un ruido de mercado aleatorio de ±5% para simular variabilidad real. Los valores de referencia (entre COP 1.200.000/m² en zonas rurales y COP 14.000.000/m² en Cabeceras estrato 6) fueron contrastados con listados del portal Metrocuadrado y con datos del Observatorio Inmobiliario de Antioquia.

Las **variables finales** del dataset son:

| Variable | Tipo | Descripción |
|---|---|---|
| `Sector` | Categórica | Zona geográfica del inmueble |
| `Precio_Venta_COP` | Numérica continua | Precio de venta en pesos colombianos |
| `Area_Construida_m2` | Numérica continua | Área construida en metros cuadrados |
| `Estrato` | Numérica discreta | Estrato socioeconómico (2–6) |
| `Distancia_CC_SanNicolas_km` | Numérica continua | Distancia al C.C. San Nicolás en km |
| `Conjunto_Cerrado_Num` | Binaria | 1 si tiene conjunto cerrado, 0 si no |
| `Urbana_Rural_Num` | Binaria | 1 si es urbano, 0 si es rural |
| `Topografia_Num` | Numérica discreta | Tipo de topografía (0 = plana, 1–3 = pendientes) |
| `Tiene_Parqueadero_Num` | Binaria | 1 si tiene parqueadero, 0 si no |

Se excluyeron variables como número de pisos y cantidad de celdas de parqueadero por considerarse poco discriminatorias en el contexto global del mercado de Rionegro, dado que no aplican de manera uniforme a todos los tipos de inmuebles del municipio.

### Operaciones de Álgebra Lineal Aplicadas

#### Análisis 2: Escalamiento Min-Max (Transformación por Escalar)

Para hacer comparables variables con magnitudes muy distintas —como el precio en pesos (orden de miles de millones) y la distancia en kilómetros (orden de unidades)—, se aplicó la normalización Min-Max. Esta operación puede expresarse como:

$$x' = (x - x_{\min}) \cdot \frac{1}{x_{\max} - x_{\min}}$$

donde el factor $\frac{1}{x_{\max} - x_{\min}}$ es un **escalar** que contrae o estira el vector de datos para que todos sus valores queden en el intervalo $[0, 1]$. La operación se denomina "transformación por escalar" precisamente porque multiplica un vector por un número único que afecta a todos sus elementos de manera proporcional (Cohen, 2022, cap. 2).

#### Análisis 3: Matriz de Covarianza

La matriz de covarianza se calculó sobre las cuatro variables numéricas principales (`Precio_Venta_COP`, `Area_Construida_m2`, `Distancia_CC_SanNicolas_km`, `Estrato`), previamente normalizadas con Min-Max. La operación matricial empleada fue:

$$C = \frac{1}{n-1} \cdot X_{c}^{T} \cdot X_{c}$$

donde $X_{c}$ es la matriz de datos centrada (a cada columna se le resta su media). Esta multiplicación produce covarianza porque el producto punto entre dos columnas de $X_{c}$ acumula los productos de las desviaciones respecto a la media; al dividir por $n - 1$, se obtiene el promedio de esas desviaciones conjuntas, que es la definición formal de covarianza (Cohen, 2022, cap. 5). La implementación en Python utilizó el operador `@` para el producto matricial.

#### Análisis 4: Eigenvalores y Eigenvectores

Los eigenvalores y eigenvectores de la matriz de covarianza $C$ se calcularon con `np.linalg.eig()`. La relación fundamental verificada fue:

$$C \cdot v = \lambda \cdot v$$

donde $v$ es un eigenvector y $\lambda$ su eigenvalor asociado. Los resultados fueron ordenados de mayor a menor para facilitar la interpretación en términos de varianza explicada (Cohen, 2022, cap. 14).

---

## Resultados

### Análisis 1: Dataset y representación matricial

El dataset final fue convertido a una matriz NumPy de dimensiones **54.700 × 9**, que representa 54.700 inmuebles (filas) descritos por 9 variables (columnas). Los rangos de valores son coherentes con el mercado de Rionegro: áreas desde ~40 m² (apartamentos pequeños en zona urbana) hasta ~1.500 m² (propiedades rurales en Río Abajo), y precios desde aproximadamente COP 48.000.000 hasta más de COP 2.000.000.000 en sectores de alto valor como Cabeceras.

### Análisis 2: Transformación por escalar

Antes del escalamiento, la columna `Precio_Venta_COP` operaba en rangos de decenas de millones, mientras que `Distancia_CC_SanNicolas_km` operaba entre 1,5 y 14 km. Sin normalización, la distancia euclidiana entre dos inmuebles quedaría completamente dominada por las diferencias de precio, haciendo invisible la componente geográfica.

La demostración con tres casas del dataset confirmó el problema: sin escalar, la distancia matemática entre una casa cercana al C.C. (misma zona) y una lejana resultaba menor que entre dos casas con distancias geográficas similares pero precios distintos, es decir, el modelo clasificaba la similitud de manera incorrecta. Tras el escalamiento, ambas dimensiones contribuyeron con igual peso y la comparación fue coherente con la realidad del mercado.

### Análisis 3: Matriz de covarianza

La matriz de covarianza resultante fue de dimensiones **4 × 4** (una fila y una columna por cada variable analizada). Se verificó su simetría mediante `np.allclose(C, C.T)`, que retornó `True`, confirmando la propiedad matemática esperada de toda matriz de la forma $X^{T}X$.

Los hallazgos más relevantes fueron:

- **Par con mayor covarianza** (fuera de la diagonal): `Distancia_CC_SanNicolas_km` y `Precio_Venta_COP`, con un valor de **0.0422**. Este resultado es consistente con la dinámica del mercado rionegrero: las zonas más alejadas del C.C. San Nicolás (como Llanogrande y Cabeceras) corresponden a sectores de alto valor por metro cuadrado, lo que establece una covariación positiva entre distancia y precio. Paradójicamente, la ubicación captura más variabilidad de precios que el tamaño del inmueble.

- **Par con covarianza más cercana a cero**: `Distancia_CC_SanNicolas_km` y `Area_Construida_m2` (**0.0061**). Esto indica que el tamaño de los inmuebles es prácticamente independiente de su ubicación geográfica: existen propiedades grandes y pequeñas tanto cerca como lejos del C.C. San Nicolás.

### Análisis 4: Eigenvalores y eigenvectores

Se obtuvieron **4 eigenvalores**, uno por cada variable incluida en la matriz de covarianza. Los resultados, ordenados de mayor a menor, fueron:

| Eigenvalor | Valor | Varianza explicada | Acumulado |
|---|---|---|---|
| λ₁ | 0.1747 | 62.47% | 62.47% |
| λ₂ | 0.0730 | 26.10% | 88.57% |
| λ₃ | 0.0265 | 9.46% | 98.03% |
| λ₄ | 0.0055 | 1.97% | 100.00% |

Con solo **dos eigenvalores** se explica el **88.57%** de la variación total del mercado inmobiliario. Este resultado implica que la complejidad del dataset puede ser sintetizada eficientemente en dos componentes principales sin pérdida significativa de información.

El eigenvector asociado al eigenvalor dominante (λ₁ = 0.1747) tuvo los siguientes pesos por variable:

| Variable | Peso absoluto |
|---|---|
| Distancia_CC_SanNicolas_km | **0.7916** |
| Estrato | 0.4775 |
| Precio_Venta_COP | 0.3691 |
| Area_Construida_m2 | 0.0954 |

La variable `Distancia_CC_SanNicolas_km` domina con un peso de 0.7916, señalando que la **ubicación respecto al C.C. San Nicolás es el factor con mayor poder explicativo** sobre la variación del mercado inmobiliario en Rionegro.

La verificación de la identidad $C \cdot v = \lambda \cdot v$ produjo una norma de diferencia de **2.11 × 10⁻¹⁶**, un valor numéricamente equivalente a cero, lo que confirma matemáticamente la validez del eigenvector calculado.

### Análisis 5: Visualizaciones para la firma de inversión

Se generaron tres gráficas orientadas a un público no especializado en álgebra lineal:

**Gráfica 1 — Scree Plot (Varianza explicada por eigenvalor):** Muestra la contribución de cada componente principal a la variación total del mercado. La caída pronunciada después del primer eigenvalor confirma que el mercado de Rionegro, pese a su diversidad sectorial, está estructurado fundamentalmente alrededor de una sola dimensión de variación: la ubicación estratégica. Para un inversionista, esto significa que no es necesario analizar decenas de variables; con entender bien la geografía del mercado, se captura la mayor parte de la información relevante.

**Gráfica 2 — Mapa de calor de la matriz de correlación:** Visualiza las relaciones entre todas las variables numéricas. Las celdas más intensas revelan dónde hay mayor dependencia entre factores. La alta correlación entre estrato, distancia y precio confirma que el mercado de Rionegro está estratificado geográficamente: invertir en zonas de estrato alto alejadas del centro (como Llanogrande o Cabeceras) implica precios elevados pero también mayor variabilidad, lo que representa tanto mayor riesgo como mayor potencial de valorización.

**Gráfica 3 — Boxplot de precio por sector:** Muestra la dispersión de precios en cada zona de Rionegro. Los sectores urbanos (Centro Histórico, San Antonio, El Porvenir) presentan cajas estrechas, indicando precios homogéneos y alta liquidez; son aptos para estrategias de alta rotación. Los sectores como Llanogrande y Cabeceras presentan cajas anchas, señalando mercados de alto riesgo pero con potencial de ganancias extraordinarias por operación. La firma de inversión puede elegir su estrategia —volumen o exclusividad— con base en esta distribución.

---

## Conclusiones

El análisis reveló que el mercado inmobiliario residencial de Rionegro tiene una estructura más simple de lo que su diversidad aparente sugiere. Dos componentes principales explican cerca del 89% de su variación, y la variable con mayor poder explicativo no es el tamaño del inmueble ni su estrato, sino la **distancia al Centro Comercial San Nicolás**.

Este resultado es coherente con el rol que el C.C. San Nicolás ha adquirido en el municipio: ya no es solo un espacio comercial, sino un punto de referencia territorial que organiza la percepción de valor en Rionegro. Su cercanía a clínicas de referencia, sucursales bancarias, el centro histórico y vías principales lo convierte en el ancla de la valoración inmobiliaria del oriente antioqueño.

Para la **firma de inversión**, las recomendaciones derivadas del análisis son:

1. **Priorizar la ubicación sobre el tamaño.** La distancia al C.C. San Nicolás explica casi el 80% del peso en el componente principal dominante. Una propiedad bien ubicada —incluso con área moderada— captura más valor que una propiedad grande en zona periférica de bajo estrato.

2. **Distinguir estrategia según el sector.** Los sectores urbanos ofrecen menor variabilidad de precios (menor riesgo, mayor liquidez), mientras que Llanogrande y Cabeceras ofrecen alta variabilidad (mayor riesgo, mayor potencial de retorno). La elección depende del apetito de riesgo del inversionista.

3. **Vigilar la variable estrato.** Con un peso de 0.4775 en el eigenvector principal, el estrato es el segundo factor más influyente. Las propiedades en zonas de estrato 5 y 6 no solo valen más; tienen también mayor covariación con la distancia al C.C., lo que sugiere que la valorización futura estará concentrada en sectores de alta categoría bien ubicados.

4. **Considerar el potencial de zonas rurales estratégicas.** Corregimientos como Galicia/La Mosca presentan precios por metro cuadrado relativamente altos (COP 6.500.000–8.500.000/m²) a pesar de su distancia al centro, posiblemente impulsados por la demanda de fincas de descanso. Este segmento podría representar una oportunidad de nicho con valorización sostenida.

En síntesis, invertir en Rionegro con base en datos no requiere modelos complejos: entender la geografía del valor —con el C.C. San Nicolás como epicentro— es suficiente para orientar decisiones de alto impacto.

---

## Referencias

Cohen, M. X. (2022). *Practical linear algebra for data science: From core concepts to applications using Python*. O'Reilly Media.

Metrocuadrado. (2024). *Listados de inmuebles en Rionegro, Antioquia*. https://www.metrocuadrado.com

Municipio de Rionegro. (2023). *Registro catastral de inmuebles – Rionegro, Antioquia*. Secretaría de Planeación Municipal.

Observatorio Inmobiliario de Antioquia. (2023). *Informe de precios del suelo y vivienda en el oriente antioqueño*. Lonja de Propiedad Raíz de Medellín y Antioquia.

---

*Documento generado en cumplimiento de los requisitos del Proyecto Final de Álgebra Lineal Aplicada al Mercado Inmobiliario – 2024.*
