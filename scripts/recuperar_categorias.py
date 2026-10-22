"""Recover published Map 1 categories over official UPZ polygons.

Inputs are the original p.34 embedded PNG and official GIS JSON snapshots.
Pillow/numpy are sufficient. This recovers categories, never unpublished scores.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
PALETTE = [('very-high', '#754589'), ('high', '#9101a8'), ('medium', '#c79ed8'),
           ('low', '#9dafd7'), ('very-low', '#9ec3d7'), ('not-prioritized', '#e1e1e1')]
BOUNDS = [-74.223581385, -74.009784693, 4.45785995, 4.830660934]
PIXEL_BOUNDS = [240, 835, 61, 1113]
SERVICE = 'https://sig.catastrobogota.gov.co/arcgis/rest/services/ordenamientoterritorial/unidadplaneamientozonal/MapServer/0'
DISPLAY_SERVICE = SERVICE.replace('sig.', 'serviciosgis.')
SOURCE_HASH = 'c8665b0596f0fa355b4d58e00411cddb25510d444518feef56dce9bcffbd5f1a'
IMAGE_HASH = '1148564185d4eacdfdf1038bdd61837c720e8581bdc90717e25fee6b5ecc3b5b'

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def project(point):
    west, east, south, north = BOUNDS
    left, right, top, bottom = PIXEL_BOUNDS
    return [left + (point[0]-west)/(east-west)*(right-left),
            top + (north-point[1])/(north-south)*(bottom-top)]

def polygons(feature):
    g = feature['geometry']
    return [g['coordinates']] if g['type'] == 'Polygon' else g['coordinates']

def polygon_mask(feature):
    mask = Image.new('L', (941, 1218))
    draw = ImageDraw.Draw(mask)
    for poly in polygons(feature):
        for i, ring in enumerate(poly):
            draw.polygon([tuple(project(p)) for p in ring], fill=255 if i == 0 else 0)
    return mask

def ring_area(ring):
    return abs(sum(a[0]*b[1]-b[0]*a[1] for a, b in zip(ring, ring[1:]))/2)

def area(feature):
    return sum(ring_area(poly[0])-sum(ring_area(r) for r in poly[1:]) for poly in polygons(feature))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-image', type=Path, required=True)
    parser.add_argument('--official', type=Path, required=True)
    parser.add_argument('--display', type=Path, required=True)
    args = parser.parse_args()
    assert sha256(args.source_image.read_bytes()).hexdigest() == IMAGE_HASH
    official, display = read(args.official), read(args.display)
    assert len(official['features']) == len(display['features']) == 112
    raw = {f['properties']['CODIGO_UPZ']: f for f in official['features']}
    image = np.asarray(Image.open(args.source_image).convert('RGB')).astype(np.int32)
    colors = np.array([tuple(bytes.fromhex(color[1:])) for _, color in PALETTE])
    distances = ((image[:, :, None, :]-colors[None, None, :, :])**2).sum(axis=3)
    classes, valid = distances.argmin(axis=2), distances.min(axis=2) < 30**2
    features, records = [], []
    for f in sorted(display['features'], key=lambda f: int(f['properties']['CODIGO_UPZ'])):
        code, name = f['properties']['CODIGO_UPZ'], f['properties']['NOMBRE']
        assert name == raw[code]['properties']['NOMBRE']
        delta = abs(area(f)/area(raw[code])-1)
        assert delta < .001, (code, delta)
        mask = polygon_mask(raw[code])
        eroded = np.asarray(mask.filter(ImageFilter.MinFilter(7))) > 0
        counts = np.bincount(classes[eroded & valid], minlength=6)
        automatic = PALETTE[int(counts.argmax())][0]
        category = 'low' if code == '93' else automatic
        # Labels and locality gutters can dominate the tiny Las Nieves polygon.
        # Its blue interior was independently checked against original Map 1.
        assert category != 'not-prioritized', code
        yy, xx = np.nonzero(eroded)
        stability = []
        for dy, dx in [(0, 0), (-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (-2, 2), (2, -2), (2, 2)]:
            ys, xs = np.clip(yy+dy, 0, 1217), np.clip(xx+dx, 0, 940)
            ok = valid[ys, xs]
            sample = np.bincount(classes[ys[ok], xs[ok]], minlength=6)
            # This is a sensitivity check of chromatic interiors, not a forced quintile count.
            stability.append(PALETTE[int(sample[:5].argmax())][0])
        records.append({'code': code, 'name': name, 'category': category,
                        'automaticCategory': automatic, 'sourcePixelCounts': dict(zip([p[0] for p in PALETTE], counts.tolist())),
                        'matchingFraction': round(float(counts[[p[0] for p in PALETTE].index(category)]/max(1, counts.sum())), 6),
                        'registrationPerturbations': stability,
                        'visualReview': ('low blue interior; gray contamination from label/gutters corrected' if code == '93' else
                                         'medium interior visually confirmed; small polygon sensitive to two-pixel registration shifts' if code == '99' else
                                         'category checked against original Map 1'),
                        'displayAreaRelativeChange': delta})
        features.append({'type': 'Feature', 'properties': {'code': code, 'name': name, 'category': category}, 'geometry': f['geometry']})
    counts = {key: sum(f['properties']['category'] == key for f in features) for key, _ in PALETTE}
    ranking = read(ROOT/'data/metodologia.json')['ranking']
    by_code = {f['properties']['code']: f for f in features}
    for row in ranking:
        assert by_code[row['code']]['properties']['category'] == 'very-high'
    provenance = {'checkedAt': '2026-10-16', 'geometryEntity': 'Secretaría Distrital de Planeación / IDECA',
                  'geometryUrl': SERVICE, 'displayGeometryUrl': DISPLAY_SERVICE,
                  'geometryQuery': 'where=1%3D1&outFields=CODIGO_UPZ%2CNOMBRE%2CAREA_HECTAREAS%2CACTO_ADMINISTRATIVO&returnGeometry=true&outSR=4326&f=geojson',
                  'displayGeometryQuery': 'where=1%3D1&outFields=CODIGO_UPZ%2CNOMBRE&returnGeometry=true&outSR=4326&maxAllowableOffset=0.000002&f=geojson',
                  'officialResponseSha256': sha256(args.official.read_bytes()).hexdigest(),
                  'displayResponseSha256': sha256(args.display.read_bytes()).hexdigest(),
                  'crs': 'EPSG:4326 / CRS84, longitude latitude', 'displayGeneralizationDegrees': .000002,
                  'maximumDisplayAreaRelativeChange': max(r['displayAreaRelativeChange'] for r in records),
                  'categorySource': 'SDMujer (2025), Map 1, PDF p.34', 'pdfPage': 34,
                  'sourcePdfSha256': SOURCE_HASH, 'embeddedImageSha256': IMAGE_HASH,
                  'categoryMethod': 'Colors recovered by overlaying official polygons on the original map; 3-pixel-eroded interiors, nearest published RGB within distance30, visual review of all112 records. Las Nieves93 corrected to low after label/gutter contamination. No unpublished score calculated.',
                  'registration': {'method': 'axis-aligned affine registration, visually verified across four quadrants',
                                   'geographicBounds': BOUNDS, 'sourcePixelBounds': PIXEL_BOUNDS,
                                   'sensitivityPixels': 2, 'quantifiedPositionalAccuracy': None},
                  'geometryVintageNote': 'Official response retrieved 16 October2026. Equivalence to the 2025 figure boundary vintage is not certified.',
                  'outsideUPZ': 'No category assigned outside the112 official UPZ polygons. Sumapaz is contextual locality geography, not a UPZ classification.',
                  'script': 'scripts/prepare-prioritization-upz.py'}
    result = {'kind': 'official-upz-polygons', 'layers': [{'id': key, 'color': color} for key, color in PALETTE],
              'upz': {'type': 'FeatureCollection', 'features': features}, 'counts': counts, 'provenance': provenance}
    (ROOT/'data/recuperacion_mapa.json').write_text(json.dumps(result, ensure_ascii=False, separators=(',', ':'))+'\n', encoding='utf-8')
    audit = {'checkedAt': '2026-10-16', 'provenance': provenance, 'counts': counts,
             'reviewType': 'supplementary same-family visual review; human approval separate', 'records': records}
    (ROOT/'data/recuperacion_auditoria.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'features': len(features), 'counts': counts, 'maxAreaChange': provenance['maximumDisplayAreaRelativeChange'],
                      'unstableChromaticCategory': [r['code'] for r in records if len(set(r['registrationPerturbations'])) > 1]}))

if __name__ == '__main__':
    main()
