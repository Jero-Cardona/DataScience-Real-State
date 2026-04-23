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