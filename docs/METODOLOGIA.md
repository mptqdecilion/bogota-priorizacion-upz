# Método y reproducción

## Geometría y clasificación son insumos diferentes

Se consultaron 112 polígonos de la Secretaría Distrital de Planeación / IDECA el 16 de octubre de 2026. La respuesta de visualización usa `outSR=4326` y `maxAllowableOffset=0.000002` grados, conservando código, nombre y coordenadas. Frente a la respuesta completa, el mayor cambio relativo de área fue 0,00549%. Se trata de una generalización para visualización. Las localidades fueron generalizadas a 0,000025 grados y redondeadas a seis decimales.

Las categorías se recuperaron del raster incrustado del Mapa 1, página PDF 34 de la metodología de 2025, mediante correspondencia afín sin rotación. Se redujo el interior de los polígonos tres píxeles para evitar bordes y rótulos. Se contó el color publicado más cercano dentro de una distancia RGB de 30. La sensibilidad se comprobó desplazando la muestra hasta dos píxeles en nueve combinaciones. Todas las asignaciones se cotejaron visualmente con la figura. No se recalcularon puntajes ni quintiles desde datos primarios.

La auditoría registra los conteos de color y la estabilidad por UPZ. Las Nieves (93) se corrigió a bajo por contaminación gris de rótulos y bordes. Chapinero (99), de prioridad media, es sensible al desplazamiento por su tamaño. Las 11 filas de Tabla 3 corresponden a muy alto. La transformación facilita recuperar colores; no certifica precisión posicional ni igualdad de la versión de límites de 2025 y 2026. La revisión visual documentada es suplementaria y no sustituye una validación humana independiente.

## Reproducir la unión de datos publicados

```sh
python scripts/reconstruir_capa.py
python scripts/validar.py
```

Entradas: `upz_limites.geojson`, `categorias_upz.csv` y `puntajes_publicados.csv`. Salida: `upz_priorizacion.geojson`. El código mantiene los decimales originales y null para puntajes no publicados.

## Volver a recuperar las categorías del raster

El script opcional `scripts/recuperar_categorias.py` requiere Pillow y NumPy ya disponibles, el PNG original de la página 34 y las respuestas GeoJSON completas y de visualización del servicio oficial. Los enlaces, consultas y hashes exactos están en `data/procedencia.json`. El documento original se enlaza en README; no se redistribuye el PDF ni su raster en el repositorio.

```sh
python scripts/recuperar_categorias.py --source-image inputs/mapa1.png --official inputs/upz_oficial.geojson --display inputs/upz_visualizacion.geojson
```

Salidas: `data/recuperacion_mapa.json` y `data/recuperacion_auditoria.json`. La imagen debe tener el hash y dimensiones registrados por el script. Consultar hoy un servicio mutable puede devolver una versión distinta: los hashes identifican la versión utilizada, pero no garantizan que siga descargable. El paso opcional no se ejecuta al abrir el mapa.

## Manzanas y límites

Se conservan 27 puntos del directorio consultado el 2 de octubre de 2026. Veintiséis coordenadas proceden de la capa oficial con vigencia 16 de diciembre de 2025. Para El Dorado se utilizó el destino Maps enlazado desde su ficha oficial tras el traslado, no el centro de la vista de Google Maps ni la antigua sede. Las propiedades incluyen la excepción y sus fuentes. No hay fichas emergentes de puntos en la interfaz.

La base completa de las 20 variables por UPZ no está incluida ni se infiere de los colores. Pesos transcritos: 99%, sin normalización a 100%. La visualización corresponde al modelo fijo y al documento de 2025; no es una actualización del índice ni una evaluación del servicio.
