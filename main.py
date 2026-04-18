import numpy as np
import pandas as pd

# Configurar semilla para reproducibilidad
np.random.seed(42)
n_samples = 5000

# Perfiles base exactos de tu tabla
sectores_info = {
    'Comuna 1 (Centro Histórico)': {'parq_pred': 0, 'precio': 300000000, 'estrato_min': 2, 'estrato_max': 4, 'area': 70, 'dist': 1.5, 'tipo': 'Urbana', 'conj_pred': 0, 'topo': 'Mayormente Plana'},
    'Comuna 2 (San Antonio)': {'parq_pred': 1, 'precio': 450000000, 'estrato_min': 3, 'estrato_max': 5, 'area': 80, 'dist': 3.5, 'tipo': 'Urbana', 'conj_pred': 1, 'topo': 'Plana'},
    'Comuna 3 (Uribe Jaramillo)': {'parq_pred': 0, 'precio': 250000000, 'estrato_min': 2, 'estrato_max': 3, 'area': 60, 'dist': 2.0, 'tipo': 'Urbana', 'conj_pred': 0, 'topo': 'Plana y Ondulada'},
    'Comuna 4 (El Porvenir)': {'parq_pred': 1, 'precio': 350000000, 'estrato_min': 3, 'estrato_max': 4, 'area': 65, 'dist': 2.5, 'tipo': 'Urbana', 'conj_pred': 1, 'topo': 'Plana'},
    'Corregimiento Occidente (Llanogrande)': {'parq_pred': 1, 'precio': 3500000000, 'estrato_min': 5, 'estrato_max': 6, 'area': 350, 'dist': 12.0, 'tipo': 'Rural', 'conj_pred': 1, 'topo': 'Plana y levemente ondulada'},
    'Corregimiento Sur (Cabeceras)': {'parq_pred': 1, 'precio': 1500000000, 'estrato_min': 4, 'estrato_max': 6, 'area': 200, 'dist': 14.0, 'tipo': 'Rural', 'conj_pred': 1, 'topo': 'Ondulada'},
    'Corregimiento Norte (Galicia/La Mosca)': {'parq_pred': 1, 'precio': 600000000, 'estrato_min': 2, 'estrato_max': 4, 'area': 150, 'dist': 10.0, 'tipo': 'Rural', 'conj_pred': 0, 'topo': 'Montañosa y Quebrada'},
    'Corregimiento Centro (Río Abajo)': {'parq_pred': 1, 'precio': 800000000, 'estrato_min': 3, 'estrato_max': 4, 'area': 180, 'dist': 6.0, 'tipo': 'Rural', 'conj_pred': 0, 'topo': 'Ondulada'}
}

# 1. Seleccionar sectores aleatoriamente
sectores_list = list(sectores_info.keys())
sectores_generados = np.random.choice(sectores_list, size=n_samples)

# Diccionario para almacenar los datos
data = {
    'Sector': [], 
    'Tiene_parqueadero': [], 
    'Precio_venta_COP': [], 
    'Estrato': [], 
    'Area_construida_m2': [], 
    'Distancia_CC_San_Nicolas_km': [], 
    'Urbana_Rural': [], 
    'Tiene_conjunto_cerrado': [], 
    'Topografia': []
}

# 2. Generar datos usando distribuciones estadísticas
for sector in sectores_generados:
    info = sectores_info[sector]
    data['Sector'].append(sector)
    
    # Parqueadero (1 = Sí, 0 = No) con 85% de probabilidad de seguir la regla
    prob_parq = [0.15, 0.85] if info['parq_pred'] == 1 else [0.85, 0.15]
    data['Tiene_parqueadero'].append(np.random.choice([0, 1], p=prob_parq))
    
    # Precio (Distribución normal centrada en tu promedio)
    precio = np.random.normal(loc=info['precio'], scale=info['precio'] * 0.15)
    data['Precio_venta_COP'].append(int(round(max(175000000, precio)))) 
    
    # Estrato
    data['Estrato'].append(np.random.randint(info['estrato_min'], info['estrato_max'] + 1))
    
    # Área construida (m2)
    area = np.random.normal(loc=info['area'], scale=info['area'] * 0.15)
    data['Area_construida_m2'].append(round(max(20, area), 1))
    
    # Distancia a C.C. San Nicolás (km)
    dist = np.random.normal(loc=info['dist'], scale=info['dist'] * 0.15)
    data['Distancia_CC_San_Nicolas_km'].append(round(max(0.5, dist), 2))
    
    # Urbana / Rural
    data['Urbana_Rural'].append(info['tipo'])
    
    # Conjunto cerrado (1 = Sí, 0 = No)
    prob_conj = [0.15, 0.85] if info['conj_pred'] == 1 else [0.85, 0.15]
    data['Tiene_conjunto_cerrado'].append(np.random.choice([0, 1], p=prob_conj))
    
    # Topografía
    data['Topografia'].append(info['topo'])

# 3. Convertir a DataFrame y guardar
df = pd.DataFrame(data)
df.to_csv('dataset_rionegro_original.csv', index=False)

print("¡Dataset de 5000 datos generado exitosamente con tus variables exactas!")