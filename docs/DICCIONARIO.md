# Diccionario y capas

Todas las geometrías utilizan longitud/latitud WGS 84 (EPSG:4326 / CRS84). Las capas no representan límites prediales ni una decisión normativa.

## UPZ

`upz_limites.geojson` conserva exclusivamente geometría, `upz_codigo` y `upz_nombre`. `upz_priorizacion.geojson` añade:

| Campo | Tipo | Significado |
| --- | --- | --- |
| upz_codigo | texto | Identificador de la UPZ; clave para unir capas y CSV |
| upz_nombre | texto | Nombre procedente de la capa oficial |
| prioridad_id | texto | very-high, high, medium, low o very-low |
| prioridad | texto | Muy alto, Alto, Medio, Bajo o Muy bajo |
| puntaje_publicado | texto o null | Decimal original de Tabla 3; null si no se publicó en esa tabla |
| posicion_publicada | entero o null | Posición en Tabla 3, entre 1 y 11 |
| fuente_categoria | texto | Identifica recuperación del Mapa 1 p. 34 |
| fuente_puntaje | texto o null | Tabla 3 p. 35, únicamente donde existe puntaje |

`puntajes_publicados.csv` utiliza `puntaje` para el mismo decimal. Se conserva como texto para no modificar la precisión transcrita; se puede convertir a numérico al analizarlo. No confundir null con prioridad baja ni con puntaje cero.

## Localidades

`localidades_contexto.geojson` tiene `code` y `name`, ambos de texto. Sus 20 geometrías son contexto: no se les asigna categoría. Incluye Sumapaz, fuera de la capa de 112 UPZ.

## Equipamientos ancla

`manzanas_existentes.geojson` contiene puntos con `id`, `nombre`, `consulta_directorio`, `vigencia_capa`, `fuente_directorio`, `fuente_coordenadas` y `nota_coordenadas`. Las fechas son ISO YYYY-MM-DD. `vigencia_capa` es null para El Dorado porque su ubicación proviene del destino Maps enlazado por la ficha oficial, distinto de la capa anterior. Los puntos no son cobertura, capacidad, número de personas ni territorio de una Manzana. No incluyen teléfonos, correos ni nombres de coordinadoras.

## Variables y pesos

`variables_pesos.csv`: `grupo_id`, `grupo`, `peso_grupo_pct`, `variable`, `peso_variable_pct` y `fuente`. El peso del grupo se repite en cada una de sus variables: para sumarlo, agrupar primero por `grupo_id`. Los pesos de variables y de los siete grupos distintos suman 99%. No contiene observaciones de las variables por UPZ.

## Leyenda

| ID | Categoría | Color | UPZ |
| --- | --- | --- | ---: |
| very-high | Muy alto | #754589 | 22 |
| high | Alto | #9101a8 | 22 |
| medium | Medio | #c79ed8 | 22 |
| low | Bajo | #9dafd7 | 23 |
| very-low | Muy bajo | #9ec3d7 | 23 |

La leyenda conserva también `not-prioritized`, gris #e1e1e1, presente en el mapa original: ninguna de las 112 UPZ recuperadas recibe esa categoría. Fuera de los polígonos no se infiere una categoría.
