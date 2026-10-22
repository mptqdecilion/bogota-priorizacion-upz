"""Reproduce la capa temática a partir de límites y tablas, sin recalcular el ICNC."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'

def rows(name):
    with (DATA / name).open(encoding='utf-8', newline='') as stream:
        return list(csv.DictReader(stream))

def build():
    limits = json.loads((DATA / 'upz_limites.geojson').read_text(encoding='utf-8'))
    categories = {r['upz_codigo']: r for r in rows('categorias_upz.csv')}
    ranking = {r['upz_codigo']: r for r in rows('puntajes_publicados.csv')}
    for feature in limits['features']:
        p = feature['properties']
        code = p['upz_codigo']
        assert p['upz_nombre'] == categories[code]['upz_nombre']
        p.update({k: categories[code][k] for k in ['prioridad_id', 'prioridad']})
        score = ranking.get(code)
        p.update(puntaje_publicado=score['puntaje'] if score else None,
                 posicion_publicada=int(score['posicion']) if score else None,
                 fuente_categoria='SDMujer (2025), Mapa 1, p. 34; recuperación de colores',
                 fuente_puntaje='SDMujer (2025), Tabla 3, p. 35' if score else None)
    return limits

if __name__ == '__main__':
    (DATA / 'upz_priorizacion.geojson').write_text(
        json.dumps(build(), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Capa reconstruida: data/upz_priorizacion.geojson')
