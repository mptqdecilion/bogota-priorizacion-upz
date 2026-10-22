# Verificación del paquete

22 de octubre de 2026.

- Comparación con las fuentes canónicas: 112 geometrías, nombres y categorías exactos; 20 localidades exactas; 27 IDs, nombres y coordenadas exactos; 11 puntajes y posiciones conservados y 101 valores null.
- `python scripts/validar.py`: unión de capas y tablas idéntica a la capa temática, recuentos, coordenadas, pesos y ausencia de campos de contacto comprobados.
- `node --check app.js`: sintaxis aprobada.
- Navegador: 112 polígonos y 27 puntos; al ocultar puntos quedan cero; resaltado de muy alto con 22 polígonos y otros 90 atenuados. La Sabana (102): puntaje 0.48323 y posición 9; Las Nieves (93): bajo y sin puntaje publicado. Cambio a fondo vacío comprobado. Selección vacía cierra la ficha.
- Vista a 1280 px y 390 px sin desborde horizontal. No se realizó una prueba exhaustiva con lectores de pantalla o QGIS.
- Revisión suplementaria nativa Codex de solo lectura: cotejó las cuatro fuentes, scripts, controles y documentación; se añadió «Sin mapa base» para permitir ocultar las calles. Sin defectos materiales pendientes en el alcance revisado. No fue una revisión entre familias, ni una nueva revisión del PDF/raster original o de todas las condiciones externas. La revisión humana y entre familias permanece separada.

Los archivos SHA-256 de `data/SHA256SUMS.txt` identifican las capas y tablas de esta entrega; no prueban por sí solos exactitud científica. Los hashes de los insumos históricos están en `data/procedencia.json`.
