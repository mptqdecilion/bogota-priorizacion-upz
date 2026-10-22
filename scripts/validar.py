"""Validaciones de integridad y reconstrucción del paquete público."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from reconstruir_capa import build

ROOT = Path(__file__).resolve().parents[1]
def read(name):
    return json.loads((ROOT / 'data' / name).read_text(encoding='utf-8'))
def rows(name):
    with (ROOT / 'data' / name).open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))
def positions(value):
    if isinstance(value[0], (int, float)):
        yield value
    else:
        for item in value:
            yield from positions(item)

data = read('upz_priorizacion.geojson')
assert len(data['features']) == 112
assert data == build(), 'La unión de límites y CSV difiere de la capa temática'
assert len({f['properties']['upz_codigo'] for f in data['features']}) == 112
expected = {'very-high': 22, 'high': 22, 'medium': 22, 'low': 23, 'very-low': 23}
assert Counter(f['properties']['prioridad_id'] for f in data['features']) == expected
assert sum(f['properties']['puntaje_publicado'] is not None for f in data['features']) == 11
audit = {r['code']: r['category'] for r in read('auditoria_categorias.json')['registros']}
for f in data['features']:
    assert f['properties']['prioridad_id'] == audit[f['properties']['upz_codigo']]
assert len(rows('puntajes_publicados.csv')) == 11
variables = rows('variables_pesos.csv')
assert len(variables) == 20
assert sum(int(v['peso_variable_pct']) for v in variables) == 99
assert sum({v['grupo_id']: int(v['peso_grupo_pct']) for v in variables}.values()) == 99
for filename, count in [('upz_limites.geojson',112),('localidades_contexto.geojson',20),('manzanas_existentes.geojson',27)]:
    layer = read(filename)
    assert layer['type'] == 'FeatureCollection' and len(layer['features']) == count
    for f in layer['features']:
        for lon, lat in positions(f['geometry']['coordinates']):
            assert -75 < lon < -73 and 3 < lat < 5.5
        assert not any(key in json.dumps(f['properties']).lower() for key in ['email','phone','contact','correo','teléfono'])
points=read('manzanas_existentes.geojson')['features']
assert all(f['geometry']['type']=='Point' for f in points)
assert len({f['properties']['id'] for f in points})==27
for f in data['features']:
    for lon, lat in positions(f['geometry']['coordinates']):
        assert -75 < lon < -73 and 3 < lat < 5.5
assert not any(ROOT.rglob('*.pdf')), 'El paquete no redistribuye los documentos completos'
assert (ROOT/'vendor/leaflet/LICENSE.txt').exists()
for line in (ROOT/'data/SHA256SUMS.txt').read_text(encoding='utf-8').splitlines():
    expected_hash, filename = line.split('  ', 1)
    assert hashlib.sha256((ROOT/'data'/filename).read_bytes()).hexdigest()==expected_hash, filename
print(json.dumps({'upz':112,'localidades':20,'manzanas':27,'puntajes_publicados':11,
                  'variables':20,'suma_pesos_publicados':99,'categorias':expected,
                  'reconstruccion_geojson':'coincide'},ensure_ascii=False))
