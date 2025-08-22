# QvaRateUtils

Utilidades en Python para procesar y gestionar datos de tasas de cambio del peso cubano (CUP).

## Descripción del Proyecto

Este mini proyecto forma parte de un servicio que recopila diariamente los valores del peso cubano (CUP) en diferentes monedas (USD, EUR, MLC) y los almacena en una base de datos PostgreSQL para su posterior análisis.

## Estructura del Proyecto

```
.
├── .gitignore
├── README.md
├── get.excel.html          # Página HTML para descargar datos Excel desde QvaRate API
├── insert.py               # Script de inserción a base de datos
├── qvap.py                 # Procesador de datos JSON
├── requeriments.txt        # Dependencias de Python
├── jsonFiles/              # Archivos de datos JSON
│   ├── eur.json           # Datos de tasa EUR/CUP
│   ├── mlc.json           # Datos de tasa MLC/CUP
│   ├── new.json           # Datos procesados y consolidados
│   └── usd.json           # Datos de tasa USD/CUP
```

## Flujo de Trabajo

### 1. Recopilación de Datos
Un servicio externo recopila diariamente las tasas de cambio del CUP y las almacena en archivos JSON separados:
- `usd.json` - Tasas USD/CUP
- `eur.json` - Tasas EUR/CUP  
- `mlc.json` - Tasas MLC/CUP

### 2. Limpieza y Procesamiento
El script `qvap.py` se encarga de:
- Leer los archivos JSON crudos
- Limpiar y procesar los datos
- Extraer valores medianos para cada moneda
- Consolidar todo en un archivo limpio `new.json`

### 3. Inserción en Base de Datos
El script `insert.py` toma los datos limpios de `new.json` e inserta la información en PostgreSQL.

## Uso

### Procesar Datos de Tasas de Cambio
```bash
python qvap.py
```

Este script:
- Lee los archivos JSON desde el directorio `jsonFiles/`
- Procesa y limpia los datos de tasas de cambio
- Genera un archivo consolidado en `jsonFiles/new.json`

### Insertar Datos en PostgreSQL
```bash
python insert.py
```

Este script:
- Lee los datos procesados desde `jsonFiles/new.json`
- Realiza inserción masiva en la tabla `currencies`
- Utiliza el método COPY de PostgreSQL para máxima eficiencia

### Descargar Datos Excel (Opcional)
Abre `get.excel.html` en un navegador para descargar archivos Excel desde la API de QvaRate para rangos de fechas específicos.

## Configuración de Base de Datos

La conexión a PostgreSQL se configura en `insert.py`:

```python
DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres", 
    "password": "postgres.",
    "host": "localhost",
    "port": 5432
}
```

### Esquema de Tabla Requerido

```sql
CREATE TABLE currencies (
    date DATE NOT NULL,
    usd DECIMAL(10,2),
    eur DECIMAL(10,2), 
    mlc DECIMAL(10,2)
);
```

## Formato de Datos

### Datos Procesados (new.json)
```json
[
    {
        "date": "2025-07-22",
        "usd": 388.50,
        "eur": 435.25, 
        "mlc": 225.00
    }
]
```

Los valores representan las tasas de cambio medianas del CUP respecto a cada moneda extranjera.
