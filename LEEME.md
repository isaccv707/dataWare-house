# 📦 Predicción de Éxito de Productos en Amazon - Proyecto Data Warehouse

## 🎯 Para Usuarios Finales - Comienza en 30 Segundos

### ⚡ Inicio Rápido (Usuarios de Windows)
1. **Doble clic en: `SETUP.bat`** (Configuración única - instala todo)
2. **Doble clic en: `RUN.bat`** (Inicia la aplicación)
3. **Abre tu navegador** en http://localhost:8501 o http://localhost:8502

### 📚 ¿Nuevo en esto? Lee: [INICIO_RAPIDO.md](INICIO_RAPIDO.md)
**¡Guía completa para principiantes con capturas de pantalla y solución de problemas!**

---

## 📋 Descripción del Proyecto

Este proyecto implementa una solución completa de data warehouse para predecir el éxito de productos en Amazon utilizando machine learning. Incluye:

- **Pipeline ETL**: Extrae, Transforma y Carga datos desde CSV a un data warehouse PostgreSQL
- **Modelo de Machine Learning**: Clasificador Random Forest para predecir el éxito de productos
- **Dos Aplicaciones Web Streamlit**: Para productos con y sin reseñas
- **Data Warehouse**: Esquema estrella PostgreSQL con tablas de dimensiones y hechos
- **Herramientas para Emprendedores**: Análisis de mercado y predicción de éxito para nuevos vendedores

**Criterios de Éxito del Producto:**
- Calificación ≥ 4.0
- Número de reseñas ≥ 50

---

## 🚀 Para Emprendedores

### ¿Quieres vender en Amazon pero aún no tienes reseñas?

Proporcionamos dos aplicaciones Streamlit especializadas para ayudarte a tomar decisiones basadas en datos:

#### 🎨 Aplicaciones Web (Streamlit)

**1. 🚀 Asesor de Emprendedores** - Para productos NUEVOS SIN reseñas:
```bash
streamlit run entrepreneur_advisor_app.py --server.port 8502
```
Visita: http://localhost:8502

**Características:**
- Predice el éxito basándose solo en precio y categoría
- Análisis de tasa de éxito por categoría (83% para Computadoras y Accesorios)
- Recomendaciones de optimización de precios
- Análisis de competencia
- Calculadora de ganancias
- Basado en 1,465 productos reales de Amazon

**2. 📦 Predictor de Éxito de Productos** - Para productos CON reseñas existentes:
```bash
streamlit run app.py
```
Visita: http://localhost:8501

**Características:**
- Predice el éxito para productos con calificaciones y reseñas
- Predicciones potenciadas por ML usando Random Forest
- Puntuaciones de probabilidad en tiempo real

---

**💡 Lanzamiento Rápido (Ambas Aplicaciones):**
```powershell
.\launch_apps.ps1
```

**Hallazgos Clave del Mercado:**
- ✅ 83% de tasa de éxito en Computadoras y Accesorios
- ✅ 100% de tasa de éxito en Productos de Oficina
- ✅ Rango de precio óptimo: ₹299-999
- ✅ Descuento recomendado: 45-55%

---

## 🛠️ Stack Tecnológico

- **Python 3.8+**
- **PostgreSQL** (vía Docker)
- **Machine Learning**: scikit-learn, pandas, numpy
- **Framework Web**: Streamlit
- **Base de Datos**: psycopg2-binary
- **Visualización**: matplotlib, seaborn

---

## 📁 Estructura del Proyecto

```
dataWare-house/
├── app.py                          # Aplicación web Streamlit (con reseñas)
├── entrepreneur_advisor_app.py     # App de asesor (sin reseñas)
├── launch_apps.ps1                 # Lanzador PowerShell para apps
├── SETUP.bat                       # Instalador automático Windows
├── RUN.bat                         # Lanzador fácil Windows
├── STOP.bat                        # Detener todos los servicios
├── CHECK_SYSTEM.bat                # Verificar instalación
├── docker-compose.yml              # Configuración contenedor PostgreSQL
├── requirements.txt                # Dependencias Python
├── data/
│   └── amazon.csv                  # Dataset fuente (1,465 productos)
├── models/
│   ├── modelo_random_forest.pkl    # Modelo ML entrenado
│   └── encoder_category.pkl        # Codificador de categorías
└── src/
    ├── __init__.py
    ├── db_connection.py            # Utilidades conexión PostgreSQL
    ├── etl_load_dw.py              # Pipeline ETL para cargar DW
    ├── preprocessing.py            # Limpieza y preprocesamiento de datos
    ├── train_model.py              # Entrenar modelo desde CSV
    └── train_model_from_dw.py      # Entrenar modelo desde DW
```

---

## 🚀 Comenzar (Detallado)

### Prerrequisitos

- **Python 3.8+** ([Descargar aquí](https://python.org/downloads)) - Asegúrate de marcar "Add Python to PATH"
- **Docker Desktop** (opcional pero recomendado) ([Descargar aquí](https://docker.com/products/docker-desktop))
- **Git** (opcional) ([Descargar aquí](https://git-scm.com/downloads))

### Métodos de Instalación

#### Método 1: Configuración de Un Clic ⭐ (Recomendado para Principiantes)

**Windows:**
```
1. Doble clic en: SETUP.bat
2. Espera la instalación (2-5 minutos)
3. Doble clic en: RUN.bat
4. ¡Elige tu aplicación y disfruta!
```

**Linux/Mac:**
```bash
chmod +x setup.sh run.sh
./setup.sh
./run.sh
```

**Para verificar que todo funciona:**
- Windows: Doble clic en `CHECK_SYSTEM.bat`
- Linux/Mac: `python3 check_system.py`

---

#### Método 2: Configuración Manual (Para Desarrolladores)

### 1. Clonar el Repositorio

```bash
git clone https://github.com/isaccv707/dataWare-house.git
cd dataWare-house
```

### 2. Instalar Dependencias Python

```bash
pip install -r requirements.txt
```

### 3. Iniciar el Data Warehouse PostgreSQL

```bash
docker-compose up -d
```

Esto iniciará un contenedor PostgreSQL con:
- **Host**: localhost
- **Puerto**: 5432
- **Base de Datos**: dw_amazon
- **Usuario**: postgres
- **Contraseña**: postgres123

Verificar que el contenedor está corriendo:

```bash
docker ps
```

### 4. Ejecutar Pipeline ETL (Cargar Data Warehouse)

Cargar los datos desde CSV al data warehouse PostgreSQL:

```bash
python src/etl_load_dw.py
```

Este script:
- Crea tablas de dimensiones y hechos
- Limpia y transforma los datos
- Carga datos en el data warehouse
- Muestra estadísticas sobre registros cargados

### 5. Entrenar el Modelo de Machine Learning

**Opción A: Entrenar desde CSV (Rápido)**
```bash
python src/train_model.py
```

**Opción B: Entrenar desde Data Warehouse (Recomendado)**
```bash
python src/train_model_from_dw.py
```

Esto genera:
- `models/modelo_random_forest.pkl` (modelo entrenado)
- `models/encoder_category.pkl` (codificador de categorías)

### 6. Ejecutar las Aplicaciones Web

**Opción A: Usar el Lanzador** (Recomendado)
```powershell
.\launch_apps.ps1
```

**Opción B: Lanzar Manualmente**

Predictor de Productos (con reseñas):
```bash
streamlit run app.py
```
Visita: http://localhost:8501

Asesor de Emprendedores (sin reseñas):
```bash
streamlit run entrepreneur_advisor_app.py --server.port 8502
```
Visita: http://localhost:8502

**Opción C: Ambas Aplicaciones Simultáneamente**
```bash
# Terminal 1
streamlit run app.py

# Terminal 2
streamlit run entrepreneur_advisor_app.py --server.port 8502
```

---

## 💡 Cómo Usar las Aplicaciones

### 📦 Predictor de Éxito de Productos (app.py)

**Úsalo cuando:** Ya tienes un producto con reseñas de clientes

**Cómo usar:**
1. Ingresa la calificación de tu producto (1-5 estrellas)
2. Ingresa el número de reseñas
3. Ingresa el precio
4. Selecciona la categoría
5. Haz clic en "Predecir"
6. Obtén tu predicción instantánea

### 🚀 Asesor de Emprendedores (entrepreneur_advisor_app.py)

**Úsalo cuando:** Quieres vender un producto NUEVO (sin reseñas aún)

**Cómo usar:**
1. Ingresa el precio de tu producto
2. Selecciona la categoría
3. Obtén análisis de mercado instantáneo y recomendaciones

**Características:**
- Predicción de éxito basada solo en precio y categoría
- Tasas de éxito por categoría
- Recomendaciones de precio óptimo
- Análisis de competencia
- Calculadora de ganancias
- Información del mercado

---

## 🗄️ Arquitectura del Data Warehouse

### Esquema Estrella

El data warehouse usa un esquema estrella con:

**Tabla de Hechos:**
- `fact_products`: Métricas centrales del producto (precio, descuento, calificación, reseñas, éxito)

**Tablas de Dimensión:**
- `dim_categories`: Información de categorías de productos
- `dim_ratings`: Información de calificaciones

### Conexión a la Base de Datos

```python
from src.db_connection import get_db_connection

conn = get_db_connection()
cursor = conn.cursor()

# Tu consulta aquí
cursor.execute("SELECT * FROM fact_products LIMIT 10")
results = cursor.fetchall()

cursor.close()
conn.close()
```

---

## 🤖 Machine Learning

### Modelo: Random Forest Classifier

**Características de Entrada:**
- `rating` (calificación del producto)
- `rating_count` (número de reseñas)
- `actual_price` (precio en ₹)
- `category` (codificado)

**Variable Objetivo:**
- `is_successful`: 1 si (rating ≥ 4.0 AND rating_count ≥ 50), sino 0

**Métricas del Modelo:**
- Precisión general: ~85%
- Mejor rendimiento en categoría "Computadoras y Accesorios": 83% de éxito

### Entrenar un Nuevo Modelo

```bash
# Desde CSV
python src/train_model.py

# Desde Data Warehouse
python src/train_model_from_dw.py
```

---

## ⚠️ Solución de Problemas

### "Python no se reconoce"
- Asegúrate de que Python esté instalado
- Reinstala Python y marca "Add Python to PATH"
- Reinicia tu computadora después de la instalación

### "Docker no está corriendo"
- Instala Docker Desktop
- Asegúrate de que Docker Desktop esté ejecutándose
- Busca el ícono de Docker en tu bandeja del sistema

### "Puerto ya en uso"
- Cierra cualquier otra aplicación en los puertos 8501 o 8502
- O ejecuta cada aplicación en un puerto diferente:
  ```bash
  streamlit run app.py --server.port 8503
  ```

### "Módulo no encontrado"
- Ejecuta la configuración nuevamente: doble clic en `SETUP.bat`
- O manualmente: `pip install -r requirements.txt`

### La aplicación no carga en el navegador
- Intenta abrir manualmente:
  - http://localhost:8501
  - http://127.0.0.1:8501
- Verifica si tu firewall está bloqueando la conexión

### Problemas con la Base de Datos
- Verifica que Docker esté ejecutándose: `docker ps`
- Reinicia los contenedores: `docker-compose restart`
- Revisa los logs: `docker-compose logs`

---

## 🛑 Cómo Detener la Aplicación

- Presiona `Ctrl + C` en la ventana de terminal/comando
- O simplemente cierra la ventana de terminal
- Para detener Docker: `docker-compose down`
- O usa: Doble clic en `STOP.bat`

---

## 📚 Documentación Adicional

| Archivo | Propósito | Audiencia |
|---------|-----------|-----------|
| **INICIO_RAPIDO.md** | Guía ultra-simple de 3 pasos | Principiantes absolutos |
| **GUIA_COMPLETA.md** | Guía completa para principiantes | Nuevos usuarios |
| **CREAR_ACCESOS_DIRECTOS.md** | Cómo crear atajos de escritorio | Usuarios avanzados |
| **GUIA_VIDEO.md** | Cómo crear tutoriales en video | Creadores de contenido |
| **INDICE_DOCS.md** | Navegación maestra de documentación | Todos |
| **📍 EMPIEZA AQUI.txt** | Archivo de bienvenida visual | Visitantes primerizos |

---

## 🎓 Ruta de Aprendizaje

### Nivel 1: Usuario Final (5 minutos)
1. Lee INICIO_RAPIDO.md
2. Ejecuta SETUP.bat
3. Ejecuta RUN.bat
4. Juega con la interfaz

### Nivel 2: Usuario Avanzado (1.5 horas)
1. Completa Nivel 1
2. Lee GUIA_COMPLETA.md
3. Explora ambas aplicaciones
4. Prueba todas las características
5. Crea atajos de escritorio

### Nivel 3: Usuario Experto (3 horas)
1. Completa Niveles 1-2
2. Lee este README completo
3. Explora el código fuente en src/
4. Entiende la estructura de datos
5. Conéctate a la base de datos

### Nivel 4: Desarrollador (5+ horas)
1. Completa Niveles 1-3
2. Estudia el entrenamiento del modelo ML
3. Revisa el pipeline ETL
4. Entiende el esquema estrella
5. Modifica y experimenta

---

## 🔍 Preguntas Frecuentes (FAQ)

### ¿Necesito conocimientos de programación?
No. Las aplicaciones tienen interfaz gráfica web. Solo usa SETUP.bat y RUN.bat.

### ¿Es gratis?
Sí, es 100% gratuito y de código abierto.

### ¿Funciona sin internet?
Después de la configuración inicial, sí. Solo necesitas internet para instalar dependencias.

### ¿Puedo usarlo para mi negocio?
¡Sí! Está diseñado específicamente para ayudar a emprendedores de Amazon.

### ¿Qué tan preciso es el modelo?
Aproximadamente 85% de precisión general, con 83% de tasa de éxito en Computadoras y Accesorios.

### ¿Puedo agregar mis propios datos?
Sí. Agrega tus datos al archivo `data/amazon.csv` y vuelve a entrenar el modelo.

### ¿Funciona en Mac/Linux?
Sí. Usa `setup.sh` y `run.sh` en lugar de los archivos .bat.

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Por favor:
1. Haz fork del repositorio
2. Crea una rama para tu característica
3. Haz commit de tus cambios
4. Push a la rama
5. Abre un Pull Request

---

## 📞 Obtener Ayuda

### Autoayuda (Recomendado)
1. Ejecuta `CHECK_SYSTEM.bat` para diagnosticar
2. Lee la sección de Solución de Problemas
3. Consulta GUIA_COMPLETA.md

### Ayuda de la Comunidad
1. Busca en GitHub Issues
2. Crea un nuevo GitHub Issue
3. Pregunta en Stack Overflow con etiquetas: `streamlit`, `python`, `machine-learning`

---

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso educativo y comercial.

---

## 🌟 Características Destacadas

✨ **Instalación de un clic** - Sin línea de comandos
✨ **Interfaz web hermosa** - Fácil de usar
✨ **IA potente** - Predicciones de Machine Learning
✨ **Análisis en tiempo real** - Resultados instantáneos
✨ **Sin reseñas necesarias** - Asesor de emprendedores
✨ **Basado en datos reales** - 1,465 productos de Amazon
✨ **Multiplataforma** - Windows, Mac, Linux
✨ **Completamente gratuito** - Código abierto

---

## 🎉 ¡Listo para Comenzar!

**Elige tu camino:**

- 🏃 **¿Solo quieres que funcione?**  
  → Doble clic: SETUP.bat, luego RUN.bat

- 📖 **¿Quieres aprender primero?**  
  → Abre: INICIO_RAPIDO.md o GUIA_COMPLETA.md

- 🔍 **¿Quieres explorar?**  
  → Abre: INDICE_DOCS.md

- ⚙️ **¿Quieres configurar?**  
  → Sigue este README

---

**Hecho con ❤️ para vendedores de Amazon**  
**¡Predice el éxito! 🚀**

---

Última Actualización: Noviembre 2025  
Repositorio: https://github.com/isaccv707/dataWare-house  
¿Preguntas? Consulta INDICE_DOCS.md o crea un issue en GitHub

---
