# Comparativa de APIs de Mapas para Eco-Vecino

Este documento evalúa las tres opciones principales para integrar mapas interactivos en la plataforma de gestión de residuos y centros de acopio **Eco-Vecino**.

---

## Resumen de Opciones

| Criterio | Leaflet + OpenStreetMap (OSM) | Mapbox GL JS | Google Maps Platform |
| :--- | :--- | :--- | :--- |
| **Costo Inicial** | **100% Gratis** (Código Abierto) | Gratis hasta 50,000 cargas/mes | $200 USD de crédito gratis/mes (~28,000 cargas) |
| **Requisito de Facturación** | Ninguno | Tarjeta de crédito requerida para registro | Tarjeta de crédito y cuenta Google Cloud requerida |
| **API Key / Token** | No requerido | Requerido | Requerido |
| **Estilo Visual** | Básico/Raster (Personalizable con capas) | Vectorial/3D Premium (Muy personalizable) | Vectorial/2D Premium (Familiar para usuarios) |
| **Rendimiento** | Excelente (Librería muy liviana) | Excelente (Renderizado WebGL en GPU) | Bueno (Pesado por la cantidad de features) |
| **Búsqueda y Geocodificación**| Limitada (Requiere APIs externas gratis) | Excelente (Mapbox Search/Geocoding) | Líder del mercado (Google Places API) |

---

## 1. Leaflet + OpenStreetMap (OSM)
*La opción recomendada para el prototipo inicial y fases tempranas.*

### Pros
* **Sin Costos Ocultos:** Al ser open-source, no hay límites de uso ni facturación mensual por parte de la librería.
* **Sin Fricción de Configuración:** No se necesita registrar una tarjeta de crédito, crear cuentas en la nube ni generar API Keys para empezar a desarrollar o probar localmente.
* **Ligereza:** El core de Leaflet pesa menos de 40 KB, lo que garantiza tiempos de carga extremadamente rápidos.
* **Gran Ecosistema:** Miles de plugins gratuitos disponibles para clustering de marcadores, rutas, mapas de calor, etc.

### Contras
* **Estilos Estándar:** Las teselas (tiles) por defecto de OpenStreetMap tienen un aspecto simple y tradicional. (Se puede mitigar usando proveedores gratuitos alternativos como CartoDB Voyager/Positron o Stamen).
* **Renderizado Rasterizado:** Por defecto usa imágenes rasterizadas en 2D, a diferencia del renderizado vectorial fluido de Mapbox.

---

## 2. Mapbox GL JS
*La mejor opción para una experiencia interactiva y visual premium en 3D.*

### Pros
* **Diseño Premium:** Renderizado de mapas vectoriales ultra-fluidos con soporte para rotaciones, inclinación y visualización 3D de edificios.
* **Mapbox Studio:** Herramienta visual increíble para diseñar mapas que combinen perfectamente con la paleta de colores de la aplicación (modo oscuro, minimalista, etc.).
* **Free Tier Generoso:** 50,000 cargas de mapa para web gratuitas al mes es más que suficiente para producción en fases iniciales.

### Contras
* **Registro Obligatorio:** Requiere registrar una tarjeta de crédito para crear la cuenta y obtener la API Key.
* **Licencia Cerrada:** A partir de la versión 2.0, Mapbox GL JS pasó a ser una librería de código cerrado y de pago por uso (aunque existen forks libres como *MapLibre GL*).

---

## 3. Google Maps Platform (Maps JavaScript API)
*La opción ideal si la precisión de búsqueda de direcciones y Street View son críticos.*

### Pros
* **Datos Precisos:** La base de datos de ubicaciones, comercios y calles más actualizada y completa del mundo.
* **Google Places Autocomplete:** El buscador de direcciones y autocompletado es sumamente robusto y reduce errores de entrada de datos.
* **Street View:** Integración nativa para ver imágenes a nivel de calle de los centros de acopio.

### Contras
* **Esquema de Precios Alto:** Aunque da $200 USD de crédito gratuito al mes, el costo por cada 1000 peticiones adicionales es el más alto del mercado.
* **Complejidad de Consola:** La configuración en Google Cloud Platform (GCP) puede ser confusa y requiere gestionar restricciones de API Keys para evitar robos de cuota.

---

## Selección para la Fase Actual: Leaflet + OpenStreetMap

Para el hito actual de **Eco-Vecino**, se ha seleccionado **Leaflet** utilizando capas de **CartoDB (Voyager)**. 

### Justificación:
1. **Facilidad de revisión**: El evaluador o profesor en GitHub podrá clonar el repositorio y levantar el mapa inmediatamente sin tener que configurar variables de entorno o crear cuentas externas.
2. **Estética Mejorada**: Utilizando los estilos *Voyager* de CartoDB, logramos un diseño limpio, moderno e interactivo que compite visualmente con Mapbox sin requerir tokens.
3. **Migración Sencilla**: La lógica estructural de Leaflet es muy similar a la de Mapbox GL JS, facilitando una futura migración si los requerimientos de la aplicación lo exigen.
