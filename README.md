# Bogotá: priorización de Manzanas del Cuidado por UPZ

Mapa interactivo y capas separadas para reutilizar el **Mapa 1 · Priorización por UPZ**, publicado en la metodología de la Secretaría Distrital de la Mujer de 2025. Paquete preparado el 22 de octubre de 2026.

## Qué contiene

| Archivo | Contenido |
| --- | --- |
| `data/upz_limites.geojson` | 112 polígonos de UPZ con código y nombre, sin clasificación |
| `data/upz_priorizacion.geojson` | Los mismos polígonos con cinco categorías y los 11 puntajes publicados |
| `data/localidades_contexto.geojson` | 20 localidades, incluido Sumapaz, sin categoría de prioridad |
| `data/manzanas_existentes.geojson` | 27 equipamientos ancla; corte del directorio: 2 de octubre de 2026 |
| `data/categorias_upz.csv` | Categoría recuperada para cada una de las 112 UPZ |
| `data/puntajes_publicados.csv` | Las 11 filas de la Tabla 3, con los decimales originales |
| `data/variables_pesos.csv` | Desglose de siete grupos, 20 variables y pesos publicados |
| `data/leyenda.json` | Colores y recuentos por categoría |
| `data/metodologia.json` | Etapas, descripción de construcción, pesos y ranking transcritos |
| `data/auditoria_categorias.json` | Muestreo de colores, sensibilidad y revisión de las asignaciones |
| `data/procedencia.json` | Fuentes, fechas, consultas y hashes de los insumos originales |

Las capas se pueden abrir directamente en QGIS. El formato GeoJSON usa WGS 84, coordenadas **longitud, latitud**, EPSG:4326 / CRS84. Los códigos UPZ son texto.

## Abrir el mapa

**[Ver el mapa interactivo en línea](https://mptqdecilion.github.io/bogota-priorizacion-upz/)**, sin descargar el repositorio. GitHub Pages publica los archivos de la raíz de `main` y se actualiza después de cada cambio en esa rama. Las capas y las tablas también se pueden descargar desde el mapa.

La interfaz utiliza **JavaScript y Leaflet**, HTML y CSS. No necesita compilación, npm, claves API ni paquetes instalados.

Con Node.js ya instalado, desde esta carpeta:

```sh
node scripts/servir.mjs
```

Abra <http://127.0.0.1:4174/>. Alternativamente, con Python ya instalado:

```sh
python -m http.server 4174 --bind 127.0.0.1
```

Use un servidor HTTP: abrir `index.html` con doble clic puede bloquear la carga de datos. Leaflet está incluido con su licencia; las calles OpenStreetMap requieren internet. Los polígonos, puntos y tablas se cargan desde este repositorio. El selector de capas permite ocultar calles, localidades, priorización o puntos. Los puntos se muestran sin ficha ni nombre emergente.

## Reconstruir y comprobar

Los scripts de unión y validación utilizan Python y su biblioteca estándar:

```sh
python scripts/reconstruir_capa.py
python scripts/validar.py
```

La unión reproduce la capa temática a partir de límites y CSV. **No calcula de nuevo el índice ICNC.** El procedimiento para volver a recuperar colores desde el raster original se documenta en [METODOLOGIA.md](docs/METODOLOGIA.md); requiere insumos externos y, únicamente para ese paso opcional, Pillow y NumPy.

## Alcance

Las categorías fueron recuperadas de los colores del Mapa 1, no descargadas como una base oficial de clasificación. La Tabla 3 publica puntajes solo para 11 UPZ: los demás valores son `null`, no cero. La base con los valores de las 20 variables para todas las UPZ no está disponible en este paquete; por tanto, no permite recalcular el índice completo.

Los pesos de la Tabla 2 suman **99%**, aunque el documento imprime un total de 100%. Se preservan los porcentajes publicados. Las UPZ corresponden a la unidad usada por esa metodología, no a una sustitución por Unidades de Planeamiento Local (UPL). La cartografía fue consultada en octubre de 2026 y su equivalencia exacta con los límites de la figura de 2025 no está certificada. Un puntaje alto no mide impacto en salud, calidad ni efectividad.

## Fuentes y atribución

- Secretaría Distrital de la Mujer (2025). [Metodología de priorización de los modelos de operación del Sistema Distrital de Cuidado](https://sistemadecuidado.gov.co/wp-content/uploads/2026/02/Metodologia-Priorizacion-SIDICU-VF.pdf), Mapa 1 p. 34, Tabla 3 p. 35 y Tablas 1–2 pp. 29–31.
- Secretaría Distrital de Planeación / IDECA. [Capa UPZ](https://sig.catastrobogota.gov.co/arcgis/rest/services/ordenamientoterritorial/unidadplaneamientozonal/MapServer/0), consultada el 16 de octubre de 2026.
- Secretaría Distrital de Planeación / IDECA. [Localidades](https://datosabiertos.bogota.gov.co/dataset/localidad-bogota-d-c), consulta y procesamiento del 14 de octubre de 2026.
- Secretaría Distrital de la Mujer. [Directorio de Manzanas](https://sistemadecuidado.gov.co/directorio-manzanas/), consultado el 2 de octubre de 2026. Coordenadas de la capa oficial, con la excepción documentada de El Dorado.

Preparación del recurso: María Paula Tamayo, Care for Health / Decilion. No es una publicación oficial del Distrito. Consulte [el diccionario](docs/DICCIONARIO.md), [el método](docs/METODOLOGIA.md) y [las condiciones de terceros](THIRD_PARTY.md). El código original de esta interfaz se publica bajo MIT; esa licencia no reemplaza los derechos de terceros sobre datos, documentos o bibliotecas.
