"""Compara los resultados de tools/test_astro.mjs con astropy (referencia)."""
import json, sys, warnings
warnings.filterwarnings('ignore')
from astropy.utils import iers
iers.conf.auto_download = False
from astropy.time import Time
from astropy.coordinates import EarthLocation, AltAz, SkyCoord, get_body, solar_system_ephemeris
import astropy.units as u
data = json.load(open(sys.argv[1]))
loc = EarthLocation(lat=-33.0422 * u.deg, lon=-71.3733 * u.deg, height=100 * u.m)
names = {'sun': 'sun', 'moon': 'moon', 'mercurio': 'mercury', 'venus': 'venus', 'marte': 'mars', 'jupiter': 'jupiter', 'saturno': 'saturn'}
worst = {}
def sep(a, b):
    c1 = SkyCoord(az=a[1] * u.deg, alt=a[0] * u.deg, frame='altaz'); c2 = SkyCoord(az=b[1] * u.deg, alt=b[0] * u.deg, frame='altaz')
    return c1.separation(c2).deg
for r in data:
    t = Time(r['date']); fr = AltAz(obstime=t, location=loc, pressure=0)
    print('==', r['date'])
    with solar_system_ephemeris.set('builtin'):
        for k, n in names.items():
            c = get_body(n, t, loc).transform_to(fr)
            ref = (c.alt.deg, c.az.deg); d = sep(r['bodies'][k], ref)
            worst[k] = max(worst.get(k, 0), d)
            print(f"  {k:9s} app alt {r['bodies'][k][0]:7.2f} az {r['bodies'][k][1]:7.2f} | astropy alt {ref[0]:7.2f} az {ref[1]:7.2f} | error {d*60:6.2f}'")
    for n, s in r['stars'].items():
        c = SkyCoord(ra=s['ra'] * u.deg, dec=s['dec'] * u.deg).transform_to(fr)
        d = sep(s['aa'], (c.alt.deg, c.az.deg)); worst['estrellas'] = max(worst.get('estrellas', 0), d)
        print(f"  {n:9s} app alt {s['aa'][0]:7.2f} az {s['aa'][1]:7.2f} | astropy alt {c.alt.deg:7.2f} az {c.az.deg:7.2f} | error {d*60:6.2f}'")
print('\nError máximo (minutos de arco):', {k: round(v * 60, 2) for k, v in worst.items()})
