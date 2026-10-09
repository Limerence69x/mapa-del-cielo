# Mapa del Cielo 🌌

Mapa del cielo en vivo para el celular, todo en un solo archivo (`index.html`) y en español.

**Ábrelo aquí:** https://limerence69x.github.io/mapa-del-cielo/

- Usa el GPS y la hora para calcular estrellas, constelaciones, Luna (con su fase), Sol y planetas.
- Apunta el celular al cielo: la brújula y el giroscopio mueven el mapa en tiempo real.
- Sin sensores (computador): arrastra con el dedo o el mouse; zoom con dos dedos o la rueda.
- Si no das la ubicación, usa Villa Alemana, Chile.
- Buscador con flecha guía, control de tiempo, modo noche rojo y fichas con curiosidades.

## Datos y precisión
- 2.319 estrellas del *Yale Bright Star Catalogue* (todas hasta magnitud 5,3), con precesión a la fecha actual.
- Luna: teoría ELP-2000 truncada (Meeus) con corrección de paralaje; Sol: Meeus; planetas: elementos keplerianos de JPL.
- Verificado contra astropy (`tools/test_astro.mjs` + `tools/check_astropy.py`): error máximo ~5 minutos de arco
  (Saturno), menos de 0,5′ para estrellas, Sol y Luna.

## Desarrollo
`python3 tools/build_data.py` regenera el bloque de datos de estrellas y constelaciones dentro de `index.html`.
