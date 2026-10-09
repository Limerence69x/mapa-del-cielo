#!/usr/bin/env python3
"""Genera el bloque de datos (estrellas + constelaciones) que va dentro de index.html.

Fuente: Yale Bright Star Catalogue 5ª ed. (posiciones J2000, magnitud V, temperatura).
Uso:  python3 tools/build_data.py   (reemplaza lo que hay entre los marcadores DATA en index.html)
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MAG_LIMIT = 5.3

SUP = {'1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'}


def parse_ra(s):
    h, m, sec = re.findall(r'[\d.]+', s)
    return (float(h) + float(m) / 60 + float(sec) / 3600) * 15


def parse_dec(s):
    d, m, sec = re.findall(r'[\d.]+', s)
    v = float(d) + float(m) / 60 + float(sec) / 3600
    return -v if s.strip().startswith('-') else v


raw = json.load(open(os.path.join(HERE, 'bsc5-short.json'), encoding='utf-8'))
cat = []
for x in raw:
    try:
        cat.append(dict(hr=int(x['HR']), ra=parse_ra(x['RA']), dec=parse_dec(x['Dec']), mag=float(x['V']),
                        k=int(x.get('K') or 6000), b=x.get('B', ''), c=x.get('C', ''), n=x.get('N', '')))
    except Exception:
        pass


def resolve(con, letter):
    """'Cru','α' -> estrella más brillante con esa letra de Bayer (α¹, α²...). 'π3' -> π³."""
    m = re.match(r'^(.)(\d)?$', letter)
    base, idx = m.group(1), m.group(2)
    if idx:
        cands = [s for s in cat if s['c'] == con and s['b'] == base + SUP[idx]]
    else:
        cands = [s for s in cat if s['c'] == con and (s['b'] == base or (s['b'][:1] == base and len(s['b']) == 2))]
    if not cands:
        raise SystemExit(f'No encuentro {letter} {con}')
    return min(cands, key=lambda s: s['mag'])


# Figuras: cada línea es una polilínea de letras de Bayer; "Tau:β" usa otra constelación.
CONST = {
    'Cru': ('Cruz del Sur', True, ['α γ', 'β δ']),
    'Cen': ('Centauro', True, ['α β ε ζ μ ν θ', 'ζ η κ', 'ε γ δ', 'ν ι']),
    'Sco': ('Escorpión', True, ['ν β δ π ρ', 'δ σ α τ ε μ ζ η θ ι κ λ υ']),
    'Ori': ('Orión', True, ['α λ γ', 'α ζ ε δ γ', 'ζ κ', 'δ β', 'γ π3', 'π1 π2 π3 π4 π5 π6', 'α μ ξ', 'μ ν']),
    'CMa': ('Can Mayor', True, ['β α ο2 δ η', 'δ ε ζ', 'α ι γ']),
    'Car': ('Carina', True, ['α χ ε ι υ θ ω β υ']),
    'Vel': ('Vela', False, ['γ δ κ φ μ λ γ', 'λ ψ']),
    'Pup': ('Popa', False, ['ξ ρ ζ π ν τ', 'π σ']),
    'Mus': ('Mosca', False, ['ε α β δ γ α']),
    'TrA': ('Triángulo Austral', False, ['α β γ α']),
    'Lup': ('Lobo', False, ['ζ α β δ γ ε α']),
    'Ara': ('Altar', False, ['θ α β ζ η', 'β γ δ']),
    'CrA': ('Corona Austral', False, ['ε γ α β δ ζ']),
    'Sgr': ('Sagitario', False, ['γ ε ζ τ σ φ λ δ γ', 'δ ε', 'φ ζ', 'δ φ', 'λ μ', 'σ ο π']),
    'Gru': ('Grulla', False, ['γ λ δ β ε ζ', 'α β']),
    'Pav': ('Pavo', False, ['α β δ', 'β γ']),
    'Tuc': ('Tucán', False, ['δ α γ ε ζ β']),
    'Hyi': ('Hidra Macho', False, ['α β γ α']),
    'Phe': ('Fénix', False, ['ε α β γ', 'β ζ']),
    'Eri': ('Erídano', False, ['β ν γ δ ε η', 'η τ1 τ3 τ4 τ5 τ6 υ2 θ φ χ α']),
    'Col': ('Paloma', False, ['ε α β γ δ', 'β η']),
    'Lep': ('Liebre', False, ['μ α β ε', 'α ζ η', 'β γ δ α']),
    'CMi': ('Can Menor', False, ['α β']),
    'Gem': ('Géminis', False, ['α τ ε μ η', 'β δ ζ γ', 'α β']),
    'Tau': ('Tauro', False, ['ζ α θ2 γ δ ε β', 'γ λ']),
    'Aur': ('Auriga', False, ['α β θ Tau:β ι α']),
    'Per': ('Perseo', False, ['γ α δ ε ζ', 'α β']),
    'Ari': ('Aries', False, ['α β γ']),
    'Leo': ('Leo', False, ['ε μ ζ γ η α θ β δ γ', 'δ θ']),
    'Hya': ('Hidra', False, ['σ δ ε ζ θ ι α υ1 λ μ ν ξ β γ π']),
    'Crv': ('Cuervo', False, ['α ε γ δ β ε']),
    'Vir': ('Virgo', False, ['β η γ δ ε', 'γ α', 'δ ζ α']),
    'Lib': ('Libra', False, ['σ α β γ α']),
    'Oph': ('Ofiuco', False, ['α κ δ ε ζ η β α']),
    'Aql': ('Águila', False, ['γ α β', 'α δ θ', 'δ λ', 'δ ζ']),
    'Lyr': ('Lira', False, ['α ε ζ α', 'ζ β γ δ ζ']),
    'Cyg': ('Cisne', False, ['α γ η β', 'ε γ δ']),
    'Peg': ('Pegaso', False, ['α β And:α γ α', 'α ζ θ ε', 'β η']),
    'And': ('Andrómeda', False, ['α δ β γ']),
    'Cas': ('Casiopea', False, ['ε δ γ α β']),
    'UMa': ('Osa Mayor', False, ['η ζ ε δ α β γ δ']),
    'Boo': ('Boyero', False, ['α ε δ β γ ρ α', 'α η', 'α ζ']),
    'CrB': ('Corona Boreal', False, ['θ β α γ δ ε']),
    'Her': ('Hércules', False, ['ε ζ η π ε', 'ζ β', 'π ρ']),
    'Cap': ('Capricornio', False, ['α β ψ ω ζ δ γ θ β']),
    'Aqr': ('Acuario', False, ['ε β α γ ζ η', 'α θ λ δ']),
    'PsA': ('Pez Austral', False, ['α ε', 'α δ γ β']),
    'Cet': ('Ballena', False, ['ι β η θ ζ τ β', 'ζ ο δ γ α']),
    'Dor': ('Dorado', False, ['γ α β δ']),
}

used = {}  # hr -> index
stars = []
for s in sorted([s for s in cat if s['mag'] <= MAG_LIMIT], key=lambda s: s['mag']):
    used[s['hr']] = len(stars)
    stars.append(s)


def idx_of(s):
    if s['hr'] not in used:
        used[s['hr']] = len(stars)
        stars.append(s)
    return used[s['hr']]


consts = []
for code, (name, hl, lines) in CONST.items():
    polys = []
    for line in lines:
        toks = [t for t in line.split() if t]
        if len(toks) < 2:
            continue
        poly = []
        for t in toks:
            c2, l2 = (t.split(':') if ':' in t else (code, t))
            poly.append(idx_of(resolve(c2, l2)))
        polys.append(poly)
    consts.append({'c': code, 'n': name, 'h': 1 if hl else 0, 'l': polys})

# Nombres propios: sólo el componente más brillante si se repite (Castor A/B).
seen = set()
out = []
for s in stars:
    n = s['n']
    if n in seen:
        n = ''
    seen.add(n)
    out.append([round(s['ra'], 3), round(s['dec'], 3), s['mag'], round(s['k'] / 100), s['b'], s['c'], n])

js = ('const STARS=' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';\n'
      + 'const CONSTS=' + json.dumps(consts, ensure_ascii=False, separators=(',', ':')) + ';')

path = os.path.join(ROOT, 'index.html')
html = open(path, encoding='utf-8').read()
new = re.sub(r'/\*DATA-START\*/.*?/\*DATA-END\*/', lambda m: '/*DATA-START*/\n' + js + '\n/*DATA-END*/', html, flags=re.S)
if new == html and '/*DATA-START*/' not in html:
    sys.exit('index.html no tiene marcadores DATA')
open(path, 'w', encoding='utf-8').write(new)
print(f'{len(out)} estrellas, {len(consts)} constelaciones, {len(js)//1024} KB')
