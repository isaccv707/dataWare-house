# 🚀 Guía de Inicio Rápido

## Para Principiantes Absolutos - ¡Comienza en 3 Pasos!

### Paso 1: Instalar Requisitos Previos (Configuración única)

#### Usuarios de Windows:
1. **Instalar Python** (si no lo tienes):
   - Descargar de: https://www.python.org/downloads/
   - ⚠️ **IMPORTANTE**: Marca "Add Python to PATH" durante la instalación
   - Versión mínima: Python 3.8+

2. **Instalar Docker Desktop** (opcional pero recomendado):
   - Descargar de: https://www.docker.com/products/docker-desktop
   - Esto es necesario para la funcionalidad de base de datos
   - Puedes omitir esto si solo quieres probar la aplicación

### Paso 2: Configuración (Una sola vez)

#### Opción A: Forma Fácil (Windows)
Doble clic en: **`SETUP.bat`**

#### Opción B: Forma Manual
Abre PowerShell o Símbolo del sistema en la carpeta del proyecto y ejecuta:
```bash
pip install -r requirements.txt
docker-compose up -d
python src/etl_load_dw.py
```

### Paso 3: Ejecutar la Aplicación

#### Opción A: Forma Fácil (Windows)
Doble clic en: **`RUN.bat`**

Elige:
- **Opción 1**: Predictor de Éxito de Productos (para productos con reseñas)
- **Opción 2**: Asesor de Emprendedores (para productos nuevos)
- **Opción 3**: Ambas aplicaciones al mismo tiempo

#### Opción B: Usando PowerShell
```powershell
.\launch_apps.ps1
```

#### Opción C: Lanzamiento Manual
```bash
# Para Predictor de Éxito de Productos:
streamlit run app.py

# Para Asesor de Emprendedores:
streamlit run entrepreneur_advisor_app.py --server.port 8502
```

---

## 🎯 Qué Hace Cada Aplicación

### 1️⃣ Predictor de Éxito de Productos (`app.py`)
**Úsala cuando**: Ya tienes un producto con reseñas de clientes

**Características**:
- Predice si tu producto será exitoso
- Basado en: calificación, número de reseñas, precio, categoría
- Usa Machine Learning (Random Forest)
- Obtén predicciones instantáneas

**Cómo usar**:
1. Ingresa la calificación de tu producto (1-5 estrellas)
2. Ingresa el número de reseñas
3. Ingresa el precio
4. Selecciona la categoría
5. Haz clic en "Predecir"

### 2️⃣ Asesor de Emprendedores (`entrepreneur_advisor_app.py`)
**Úsala cuando**: Quieres vender un producto NUEVO (sin reseñas aún)

**Características**:
- Predice el éxito basándose solo en precio y categoría
- Obtén tasas de éxito por categoría
- Recomendaciones de precio óptimo
- Análisis de competencia
- Calculadora de ganancias
- Información del mercado

**Cómo usar**:
1. Ingresa el precio de tu producto
2. Selecciona la categoría
3. Obtén análisis de mercado instantáneo y recomendaciones

---

## 📱 Acceder a las Aplicaciones

Después de lanzar, abre tu navegador web y ve a:
- **Predictor de Productos**: http://localhost:8501
- **Asesor de Emprendedores**: http://localhost:8502

¡Las aplicaciones usualmente se abren automáticamente en tu navegador predeterminado!

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

---

## 🛑 Cómo Detener la Aplicación

- Presiona `Ctrl + C` en la ventana de terminal/comando
- O simplemente cierra la ventana de terminal
- Para detener Docker: `docker-compose down`

---

## 📞 ¿Necesitas Más Ayuda?

Consulta el [LEEME.md](LEEME.md) principal para:
- Documentación detallada
- Vista general de la arquitectura
- Información para desarrolladores
- Documentación de API

---

## 🎉 ¡Estás Listo!

Eso es todo. Ahora tienes una poderosa herramienta de predicción de éxito de productos de Amazon a tu alcance.

**¡Felices Ventas! 🚀📦**
