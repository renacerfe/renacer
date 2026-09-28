#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
motor_mapas.py — Dibuja mapas bíblicos en SVG a partir de datos reales.

Cada mapa se compone con estas capas, en este orden:
  1. Mar (fondo) y retícula de coordenadas.
  2. Tierra, lagos y ríos (Natural Earth, dominio público).
  3. Fronteras modernas (línea discontinua tenue).
  4. Regiones bíblicas con relleno translúcido (Bible-Geocoding-Data).
  5. Rutas y viajes (líneas con flechas y paradas numeradas).
  6. Lugares bíblicos con sus nombres en español.
  7. Rótulo con título, referencia bíblica, escala, rosa de los vientos y
     pie con las fuentes y licencias.

La proyección es equirectangular con corrección por la latitud media, de modo
que las distancias son razonablemente fieles en mapas regionales. El texto va
siempre en español y evita solaparse: cuando dos etiquetas chocan se colocan
sobre otro punto libre y, si aun así no hay sitio, se usa una leyenda
numerada.
"""

import json
import math
from pathlib import Path

AQUI = Path(__file__).resolve().parent
DATOS = AQUI.parent / "app" / "datos"

# ---------------------------------------------------------------------------
# Paleta y estilos
# ---------------------------------------------------------------------------
COL = {
    "mar": "#cfe3f0",
    "mar_borde": "#a8c8dd",
    "tierra": "#f4ecd8",
    "tierra_borde": "#c9bb97",
    "lago": "#bcdcee",
    "rio": "#7fb2d4",
    "frontera": "#b9b2a0",
    "region_relleno": "rgba(196,150,45,0.16)",
    "region_borde": "#b98a2b",
    "etiqueta": "#2b2013",
    "halo": "rgba(255,255,255,0.82)",
    "titulo": "#4a3410",
    "nota": "#6b5b45",
}

FUENTES_HTML = ('Datos: openbible.info (Bible-Geocoding-Data, CC BY 4.0) · '
                'Natural Earth (dominio público) · Renacer · Atlas Bíblico')

# Tipos de lugar: forma del símbolo y tamaño
SIMBOLOS = {
    "ciudad o poblado": ("circulo", 3.4),
    "ciudad": ("circulo", 3.4),
    "aldea": ("circulo", 2.8),
    "puerto": ("circulo", 3.2),
    "fortaleza": ("cuadrado", 3.0),
    "torre": ("cuadrado", 2.6),
    "monte": ("triangulo", 3.6),
    "colina": ("triangulo", 3.0),
    "cordillera": ("triangulo", 3.4),
    "río": ("onda", 3.0),
    "mar o lago": ("onda", 3.0),
    "desierto": ("punto", 2.6),
    "valle": ("punto", 2.8),
    "región": ("punto", 2.6),
    "isla": ("circulo", 3.0),
    "manantial": ("circulo", 2.4),
    "pozo": ("circulo", 2.4),
}


def _cargar_json(ruta):
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Proyección y utilidades geométricas
# ---------------------------------------------------------------------------
class Proyeccion:
    def __init__(self, bbox, ancho, alto, margen=(64, 64, 64, 96)):
        self.lon0, self.lat0, self.lon1, self.lat1 = bbox
        self.ancho, self.alto = ancho, alto
        self.mizq, self.mder, self.marriba, self.mabajo = margen
        self.lat_media = (self.lat0 + self.lat1) / 2.0
        self.k = math.cos(math.radians(self.lat_media))
        ancho_geo = max(1e-6, (self.lon1 - self.lon0) * self.k)
        alto_geo = max(1e-6, (self.lat1 - self.lat0))
        self.escala = min((ancho - self.mizq - self.mder) / ancho_geo,
                          (alto - self.marriba - self.mabajo) / alto_geo)
        # centrado dentro del marco
        self.ox = self.mizq + ((ancho - self.mizq - self.mder) - ancho_geo * self.escala) / 2.0
        self.oy = self.marriba + ((alto - self.marriba - self.mabajo) - alto_geo * self.escala) / 2.0

    def punto(self, lon, lat):
        x = self.ox + (lon - self.lon0) * self.k * self.escala
        y = self.oy + (self.lat1 - lat) * self.escala
        return round(x, 1), round(y, 1)

    def ruta(self, puntos, cerrar=False):
        if not puntos:
            return ""
        partes = []
        for i, (lon, lat) in enumerate(puntos):
            x, y = self.punto(lon, lat)
            partes.append(("M" if i == 0 else "L") + f"{x},{y}")
        if cerrar:
            partes.append("Z")
        return " ".join(partes)

    def ancho_grados(self):
        return self.lon1 - self.lon0

    def km_por_grado_lon(self):
        return 111.32 * self.k

    def km_por_grado_lat(self):
        return 110.57


def _esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def ancho_texto(texto, tam):
    """Estimación del ancho de un texto en píxeles (fuente serif)."""
    anchos = {"i": 0.28, "l": 0.28, "j": 0.3, "f": 0.33, "t": 0.33, "r": 0.36,
              "m": 0.86, "w": 0.76, "M": 0.9, "W": 1.0, "I": 0.3}
    total = 0.0
    for c in texto:
        total += anchos.get(c, 0.53)
    return total * tam


class Colisiones:
    """Evita que las etiquetas se solapen entre sí."""

    def __init__(self):
        self.cajas = []

    def libre(self, x, y, ancho, alto):
        for (bx, by, ba, bb) in self.cajas:
            if x < bx + ba and bx < x + ancho and y < by + bb and by < y + alto:
                return False
        return True

    def reservar(self, x, y, ancho, alto):
        self.cajas.append((x, y, ancho, alto))


# ---------------------------------------------------------------------------
# Dibujo del mapa
# ---------------------------------------------------------------------------
class Mapa:
    def __init__(self, base, regiones, lugares, def_mapa, extras=None):
        self.base = base
        self.regiones = {r["id"]: r for r in regiones}
        self.por_id = {l["id"]: l for l in lugares}
        self.extras = extras or {}
        for clave, valor in self.extras.items():
            completo = dict(valor)
            completo.setdefault("nombre", valor.get("n", clave))
            completo.setdefault("original", valor.get("n", clave))
            completo.update({"id": clave, "adaptado": False, "refs": valor.get("refs", [])})
            self.por_id.setdefault(clave, completo)
        self.avisos = []
        self.por_nombre = {}
        for l in lugares:
            self.por_nombre.setdefault(l["nombre"].lower(), l)
            self.por_nombre.setdefault(l["original"].lower(), l)
        self.def_mapa = def_mapa
        self.ancho = int(def_mapa.get("ancho", 1200))
        self.alto = int(def_mapa.get("alto", 820))
        self.proy = Proyeccion(def_mapa["bbox"], self.ancho, self.alto,
                               margen=(62, 62, 108, 184))
        self.capas = []          # capas del mapa (se recortan al área de dibujo)
        self.capas_marco = []    # rótulo, leyenda y pie
        self.leyenda = []
        self.colisiones = Colisiones()

    # -- resolución de lugares ------------------------------------------
    def resolver_lugar(self, ref):
        """Acepta un identificador, un nombre o un diccionario."""
        if isinstance(ref, dict):
            nombre = ref.get("n") or ref.get("nombre")
            lon, lat = ref.get("lon"), ref.get("lat")
            tipo = ref.get("tipo", "ciudad o poblado")
            refs = ref.get("refs", [])
            lugar = {"nombre": nombre, "lon": lon, "lat": lat, "tipo": tipo,
                     "refs": refs, "id": ref.get("id"), "adaptado": False,
                     "original": nombre}
            return lugar
        lugar = self.por_id.get(ref) or self.por_nombre.get(str(ref).lower())
        if lugar is None and isinstance(ref, str):
            base = ref.rsplit("-", 1)[0]
            lugar = self.por_id.get(base) or self.por_nombre.get(base.lower())
            if lugar is None:
                import difflib
                cerca = difflib.get_close_matches(ref, list(self.por_id.keys()), n=1, cutoff=0.86)
                if cerca:
                    lugar = self.por_id[cerca[0]]
                    self.avisos.append(f"{ref} -> {cerca[0]}")
        if lugar is None:
            self.avisos.append(f"NO ENCONTRADO: {ref}")
        return lugar

    # -- capas -----------------------------------------------------------
    def area_dibujo(self):
        """Rectángulo donde se dibuja el mapa (deja sitio al rótulo y al pie)."""
        return (self.proy.mizq * 0.4, self.proy.marriba,
                self.ancho - self.proy.mder * 0.4, self.alto - self.proy.mabajo)

    def dentro(self, x, y, ancho=0, alto=0):
        x0, y0, x1, y1 = self.area_dibujo()
        return x >= x0 and y >= y0 and x + ancho <= x1 and y + alto <= y1

    def dibujar_base(self, con_fronteras=True, con_rios=True, con_graticula=True):
        s = []
        s.append(f'<rect x="0" y="0" width="{self.ancho}" height="{self.alto}" fill="{COL["mar"]}"/>')
        if con_graticula:
            paso_lon = self._paso(self.def_mapa["bbox"][0], self.def_mapa["bbox"][2], 10)
            paso_lat = self._paso(self.def_mapa["bbox"][1], self.def_mapa["bbox"][3], 10)
            lon = math.ceil(self.def_mapa["bbox"][0] / paso_lon) * paso_lon
            while lon <= self.def_mapa["bbox"][2]:
                x1, y1 = self.proy.punto(lon, self.def_mapa["bbox"][1])
                x2, y2 = self.proy.punto(lon, self.def_mapa["bbox"][3])
                s.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#ffffff" '
                         f'stroke-opacity="0.35" stroke-width="0.7" stroke-dasharray="3,5"/>')
                lon += paso_lon
            lat = math.ceil(self.def_mapa["bbox"][1] / paso_lat) * paso_lat
            while lat <= self.def_mapa["bbox"][3]:
                x1, y1 = self.proy.punto(self.def_mapa["bbox"][0], lat)
                x2, y2 = self.proy.punto(self.def_mapa["bbox"][2], lat)
                s.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#ffffff" '
                         f'stroke-opacity="0.35" stroke-width="0.7" stroke-dasharray="3,5"/>')
                lat += paso_lat
        # tierra
        caminos = []
        for anillo in self.base["tierra"]:
            if not self._en_ventana(anillo):
                continue
            caminos.append(self.proy.ruta(anillo, cerrar=True))
        if caminos:
            s.append(f'<path d="{" ".join(caminos)}" fill="{COL["tierra"]}" stroke="{COL["tierra_borde"]}" '
                     f'stroke-width="0.9" fill-rule="evenodd"/>')
        # lagos
        lagos = [self.proy.ruta(a, cerrar=True) for a in self.base["lagos"] if self._en_ventana(a)]
        if lagos:
            s.append(f'<path d="{" ".join(lagos)}" fill="{COL["lago"]}" stroke="{COL["rio"]}" stroke-width="0.7"/>')
        # ríos
        if con_rios:
            rios = []
            for linea in self.base["rios"]:
                if self._en_ventana(linea):
                    rios.append(self.proy.ruta(linea))
            if rios:
                s.append(f'<path d="{" ".join(rios)}" fill="none" stroke="{COL["rio"]}" '
                         f'stroke-width="1.1" stroke-linecap="round" stroke-opacity="0.9"/>')
        # fronteras modernas
        if con_fronteras:
            fr = []
            for linea in self.base["fronteras"]:
                if self._en_ventana(linea):
                    fr.append(self.proy.ruta(linea))
            if fr:
                s.append(f'<path d="{" ".join(fr)}" fill="none" stroke="{COL["frontera"]}" '
                         f'stroke-width="0.8" stroke-dasharray="5,4" stroke-opacity="0.75"/>')
        self.capas.append("\n".join(s))

    def _paso(self, a, b, objetivo):
        rango = max(1e-6, b - a)
        bruto = rango / max(1, objetivo)
        for paso in (0.05, 0.1, 0.25, 0.5, 1, 2, 5, 10, 15, 20, 30):
            if paso >= bruto:
                return paso
        return 30

    def _en_ventana(self, puntos):
        lon0, lat0, lon1, lat1 = self.def_mapa["bbox"]
        d = 0.6
        for p in puntos:
            if lon0 - d <= p[0] <= lon1 + d and lat0 - d <= p[1] <= lat1 + d:
                return True
        return False

    def dibujar_regiones(self, ids=None):
        s = []
        nombres = []
        for region in self.regiones.values():
            if ids and region["id"] not in ids and region["nombre"] not in ids:
                continue
            for anillo in region["anillos"]:
                if not self._en_ventana(anillo):
                    continue
                s.append(f'<path d="{self.proy.ruta(anillo, cerrar=True)}" fill="{COL["region_relleno"]}" '
                         f'stroke="{COL["region_borde"]}" stroke-width="1" stroke-dasharray="7,3"/>')
            cx, cy = region["centro"]
            lon0, lat0, lon1, lat1 = self.def_mapa["bbox"]
            if lon0 <= cx <= lon1 and lat0 <= cy <= lat1:
                bx0, by0, bx1, by1 = region["bbox"]
                ancho_px = abs(bx1 - bx0) * self.proy.k * self.proy.escala
                alto_px = abs(by1 - by0) * self.proy.escala
                nombres.append((region["nombre"], cx, cy, ancho_px * alto_px))
        self.capas.append("\n".join(s))
        if nombres:
            etiquetas = []
            for nombre, cx, cy, tam_region in nombres:
                # solo se rotula la región si en pantalla hay sitio suficiente
                if tam_region < 2600:
                    continue
                x, y = self.proy.punto(cx, cy)
                ancho_e = ancho_texto(nombre, 13.5) + 30
                candidatos = [(x, y)]
                for radio in (16, 30, 46, 64):
                    for dx, dy in ((0, -radio), (0, radio), (-radio, 0), (radio, 0),
                                   (-radio * 0.7, -radio * 0.7), (radio * 0.7, -radio * 0.7),
                                   (-radio * 0.7, radio * 0.7), (radio * 0.7, radio * 0.7)):
                        candidatos.append((x + dx, y + dy))
                for (cx2, cy2) in candidatos:
                    if not self.dentro(cx2 - ancho_e / 2, cy2 - 13, ancho_e, 19):
                        continue
                    if self.colisiones.libre(cx2 - ancho_e / 2, cy2 - 13, ancho_e, 19):
                        self.colisiones.reservar(cx2 - ancho_e / 2, cy2 - 13, ancho_e, 19)
                        etiquetas.append(
                            f'<text x="{round(cx2, 1)}" y="{round(cy2, 1)}" class="region">{_esc(nombre)}</text>')
                        break
            self.capas.append(f'<g class="etiqueta-region">{"".join(etiquetas)}</g>')

    def dibujar_rutas(self, rutas):
        s = []
        for ruta in rutas:
            puntos = []
            for p in ruta.get("puntos", []):
                if isinstance(p, (list, tuple)) and len(p) == 2 and all(isinstance(v, (int, float)) for v in p):
                    puntos.append((p[0], p[1]))
                else:
                    lugar = self.resolver_lugar(p)
                    if lugar:
                        puntos.append((lugar["lon"], lugar["lat"]))
            if len(puntos) < 2:
                continue
            color = ruta.get("color", "#b45309")
            grosor = ruta.get("grosor", 2.6)
            estilo = ruta.get("estilo", "solida")
            dash = ' stroke-dasharray="9,5"' if estilo == "punteada" else ""
            s.append(f'<path d="{self.proy.ruta(puntos)}" fill="none" stroke="#ffffff" '
                     f'stroke-width="{grosor + 2.4}" stroke-opacity="0.55" stroke-linecap="round" '
                     f'stroke-linejoin="round"{dash}/>')
            s.append(f'<path d="{self.proy.ruta(puntos)}" fill="none" stroke="{color}" '
                     f'stroke-width="{grosor}" stroke-linecap="round" stroke-linejoin="round"'
                     f' marker-end="url(#flecha-{self._id_color(color)})"{dash}/>')
        self.capas.append("\n".join(s))

    def _id_color(self, color):
        return color.replace("#", "c")

    def dibujar_lugares(self, lugares, numerar=None):
        """
        Dibuja símbolos y etiquetas. Los lugares más citados de la Biblia se
        etiquetan directamente; los secundarios se dibujan como puntos menores.
        Si dos etiquetas chocan, el lugar pasa a la leyenda numerada inferior.
        """
        puntos = []
        for ref in lugares:
            lugar = self.resolver_lugar(ref)
            if not lugar or lugar.get("lon") is None:
                continue
            lon0, lat0, lon1, lat1 = self.def_mapa["bbox"]
            if not (lon0 - 0.4 <= lugar["lon"] <= lon1 + 0.4 and lat0 - 0.4 <= lugar["lat"] <= lat1 + 0.4):
                continue
            if lugar not in puntos:
                puntos.append(lugar)
        if not puntos:
            return

        def importancia(lugar):
            if isinstance(lugar, dict) and "total_refs" in lugar:
                return lugar["total_refs"]
            return 25

        puntos.sort(key=lambda l: -importancia(l))
        max_etiquetas = int(self.def_mapa.get("max_etiquetas", 24))
        principales = puntos[:max_etiquetas]
        secundarios = puntos[max_etiquetas:]
        if numerar:
            principales, secundarios = puntos, []

        simbolos, etiquetas, leyenda = [], [], []
        for lugar in secundarios:
            x, y = self.proy.punto(lugar["lon"], lugar["lat"])
            forma, tam = SIMBOLOS.get(lugar.get("tipo", ""), ("circulo", 3.2))
            if forma == "triangulo":
                simbolos.append(f'<path d="M{x},{y - 3} L{x + 3},{y + 2.4} L{x - 3},{y + 2.4} Z" '
                                f'fill="#6b5b45" fill-opacity="0.75"/>')
            elif forma == "onda":
                simbolos.append(f'<circle cx="{x}" cy="{y}" r="2.2" fill="none" stroke="#2f6b8f" stroke-width="1.2"/>')
            else:
                simbolos.append(f'<circle cx="{x}" cy="{y}" r="2.1" fill="#6b5b45" fill-opacity="0.8"/>')

        for i, lugar in enumerate(principales, 1):
            x, y = self.proy.punto(lugar["lon"], lugar["lat"])
            forma, tam = SIMBOLOS.get(lugar.get("tipo", ""), ("circulo", 3.2))
            tam += 0.6
            estilo = lugar.get("estilo", "")
            relleno = "#8b2f1f" if estilo == "destacado" else "#33261a"
            if forma == "circulo":
                simbolos.append(f'<circle cx="{x}" cy="{y}" r="{tam}" fill="{relleno}" stroke="#fdf9ef" stroke-width="1.2"/>')
            elif forma == "triangulo":
                d = tam + 1
                simbolos.append(f'<path d="M{x},{y - d} L{x + d},{y + d * 0.85} L{x - d},{y + d * 0.85} Z" '
                                f'fill="{relleno}" stroke="#fdf9ef" stroke-width="1.1"/>')
            elif forma == "cuadrado":
                simbolos.append(f'<rect x="{x - tam}" y="{y - tam}" width="{tam * 2}" height="{tam * 2}" '
                                f'fill="{relleno}" stroke="#fdf9ef" stroke-width="1.1"/>')
            elif forma == "onda":
                simbolos.append(f'<circle cx="{x}" cy="{y}" r="{tam - 0.4}" fill="none" stroke="#2f6b8f" stroke-width="1.5"/>')
            else:
                simbolos.append(f'<circle cx="{x}" cy="{y}" r="{tam - 0.8}" fill="{relleno}" stroke="#fdf9ef" stroke-width="1"/>')

            nombre = lugar["nombre"]
            tam_texto = 13.5 if lugar.get("importante") or len(principales) <= 16 else 12.5
            ancho_e = ancho_texto(nombre, tam_texto) + 5
            alto_e = tam_texto + 4
            candidatos = [
                (x + tam + 4, y + tam_texto * 0.34),
                (x - tam - 4 - ancho_e, y + tam_texto * 0.34),
                (x + tam + 4, y - tam_texto * 0.9),
                (x - tam - 4 - ancho_e, y - tam_texto * 0.9),
                (x - ancho_e / 2, y - tam - alto_e - 1),
                (x - ancho_e / 2, y + tam + alto_e),
                (x + tam + 8, y - tam - alto_e + 2),
                (x - tam - 8 - ancho_e, y - tam - alto_e + 2),
                (x + tam + 8, y + tam + alto_e + 2),
                (x - tam - 8 - ancho_e, y + tam + alto_e + 2),
            ]
            colocado = None
            for (cx, cy) in candidatos:
                if not self.dentro(cx, cy, ancho_e, alto_e):
                    continue
                if self.colisiones.libre(cx, cy, ancho_e, alto_e):
                    colocado = (cx, cy)
                    break
            if colocado is None:
                etiquetas.append(f'<text x="{x}" y="{y - tam - 4}" class="numero">{len(leyenda) + 1}</text>')
                leyenda.append((len(leyenda) + 1, nombre, lugar.get("refs") or []))
                continue
            cx, cy = colocado
            self.colisiones.reservar(cx, cy, ancho_e, alto_e)
            etiquetas.append(
                f'<text x="{round(cx, 1)}" y="{round(cy + tam_texto * 0.74, 1)}" class="lugar" '
                f'font-size="{tam_texto}">{_esc(nombre)}</text>')
        self.capas.append(f'<g class="simbolos">{"".join(simbolos)}</g>')
        self.capas.append(f'<g class="etiquetas">{"".join(etiquetas)}</g>')
        self.leyenda = leyenda

    def dibujar_etiquetas_extra(self, etiquetas):
        """Nombres de tribus, montes o comarcas que se colocan sin símbolo."""
        partes = []
        for et in etiquetas:
            x, y = self.proy.punto(et["lon"], et["lat"])
            lon0, lat0, lon1, lat1 = self.def_mapa["bbox"]
            if not (lon0 <= et["lon"] <= lon1 and lat0 <= et["lat"] <= lat1):
                continue
            tam = et.get("tam", 12.5)
            partes.append(f'<text x="{x}" y="{y}" class="etiqueta-extra" '
                          f'font-size="{tam}">{_esc(et.get("n", ""))}</text>')
        self.capas.append(f'<g class="etiquetas-extra">{"".join(partes)}</g>')

    # -- rótulos y adornos ------------------------------------------------
    def dibujar_rotulo(self):
        d = self.def_mapa
        titulo = _esc(d.get("titulo", "Mapa bíblico"))
        subtitulo = _esc(d.get("subtitulo", ""))
        partes = [
            f'<rect x="0" y="0" width="{self.ancho}" height="{self.alto}" fill="none" '
            f'stroke="{COL["tierra_borde"]}" stroke-width="6"/>',
            f'<rect x="0" y="0" width="{self.ancho}" height="88" fill="rgba(250,246,236,0.94)"/>',
            f'<line x1="0" y1="88" x2="{self.ancho}" y2="88" stroke="{COL["region_borde"]}" stroke-width="2"/>',
            f'<text x="{self.ancho / 2}" y="42" class="titulo">{titulo}</text>',
            f'<text x="{self.ancho / 2}" y="70" class="subtitulo">{subtitulo}</text>',
            f'<rect x="0" y="{self.alto - 74}" width="{self.ancho}" height="74" fill="rgba(250,246,236,0.94)"/>',
            f'<line x1="0" y1="{self.alto - 74}" x2="{self.ancho}" y2="{self.alto - 74}" stroke="{COL["region_borde"]}" stroke-width="1.4"/>',
            f'<text x="{self.ancho / 2}" y="{self.alto - 13}" class="pie">{FUENTES_HTML}</text>',
        ]
        # escala gráfica
        km = self._km_barra()
        x0, y0 = 92, self.alto - 52
        px = km / self.proy.km_por_grado_lon() * self.proy.k * self.proy.escala
        partes.append(
            f'<g class="escala"><rect x="{x0}" y="{y0}" width="{px / 2:.0f}" height="7" fill="#3b2f1e"/>'
            f'<rect x="{x0 + px / 2:.0f}" y="{y0}" width="{px / 2:.0f}" height="7" fill="#fdf9ef" '
            f'stroke="#3b2f1e" stroke-width="1"/>'
            f'<text x="{x0}" y="{y0 - 5}" class="escala-txt">0</text>'
            f'<text x="{x0 + px:.0f}" y="{y0 - 5}" class="escala-txt">{km} km</text></g>')
        # rosa de los vientos
        nx, ny = self.ancho - 78, self.alto - 56
        partes.append(
            f'<g class="norte"><path d="M{nx},{ny - 22} L{nx + 7},{ny + 6} L{nx},{ny} L{nx - 7},{ny + 6} Z" '
            f'fill="#4a3410"/><text x="{nx}" y="{ny + 22}" class="norte-txt">N</text></g>')
        self.capas_marco.append("\n".join(partes))

    def _km_barra(self):
        lon0, lat0, lon1, lat1 = self.def_mapa["bbox"]
        ancho_km = (lon1 - lon0) * self.proy.km_por_grado_lon()
        objetivo = ancho_km / 4.5
        for paso in (5, 10, 20, 25, 50, 100, 150, 200, 250, 500, 750, 1000, 1500, 2000):
            if paso >= objetivo:
                return paso
        return 2000

    def dibujar_leyenda(self):
        """Leyenda de los lugares que no pudieron etiquetarse en el mapa."""
        if not self.leyenda:
            return
        columnas = 1 if len(self.leyenda) <= 13 else 2
        filas = math.ceil(len(self.leyenda) / columnas)
        base_y = self.alto - 158
        alto_caja = filas * 16 + 34
        x0 = 66
        ancho_caja = self.ancho - 2 * x0
        partes = ['<g class="leyenda-marco">',
                  f'<rect x="{x0 - 14}" y="{base_y - 22}" width="{ancho_caja}" height="{alto_caja}" '
                  f'rx="7" fill="rgba(253,249,239,0.93)" stroke="{COL["region_borde"]}" stroke-width="1"/>',
                  f'<text x="{x0 - 4}" y="{base_y - 7}" class="leyenda-titulo">'
                  f'Índice de lugares (los números del mapa)</text>']
        ancho_col = ancho_caja / columnas
        for i, (num, nombre, refs) in enumerate(self.leyenda):
            col = i // filas
            fila = i % filas
            x = x0 + 4 + col * ancho_col
            y = base_y + 8 + fila * 16
            ref = (" · " + refs[0]) if refs else ""
            texto = nombre + ref
            limite = 46 if columnas == 2 else 90
            if len(texto) > limite:
                texto = texto[:limite - 1] + "…"
            partes.append(f'<text x="{x}" y="{y}" class="leyenda-item">'
                          f'<tspan class="leyenda-num">{num}.</tspan> {_esc(texto)}</text>')
        partes.append("</g>")
        self.capas_marco.append("".join(partes))

    # -- salida -----------------------------------------------------------
    def svg(self):
        cuerpo = "\n".join(c for c in self.capas if c)
        marco = "\n".join(c for c in self.capas_marco if c)
        x0, y0, x1, y1 = self.area_dibujo()
        recorte = (f'<clipPath id="recorte"><rect x="{x0}" y="{y0}" width="{x1 - x0}" '
                   f'height="{y1 - y0}"/></clipPath>')
        defs = [recorte]
        for ruta in self.def_mapa.get("rutas", []):
            color = ruta.get("color", "#b45309")
            defs.append(
                f'<marker id="flecha-{self._id_color(color)}" viewBox="0 0 10 10" refX="8" refY="5" '
                f'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
                f'<path d="M0,1 L9,5 L0,9 z" fill="{color}"/></marker>')
        estilos = f"""
    text {{ font-family: "Noto Serif", "DejaVu Serif", Georgia, serif; }}
    .titulo {{ font-size: 27px; font-weight: 700; fill: {COL['titulo']}; text-anchor: middle; letter-spacing: 0.4px; }}
    .subtitulo {{ font-size: 14.5px; fill: {COL['nota']}; text-anchor: middle; font-style: italic; }}
    .pie {{ font-size: 11px; fill: {COL['nota']}; text-anchor: middle; }}
    .etiqueta-extra {{ fill: #6b4c11; text-anchor: middle; letter-spacing: 1.4px; font-weight: 600; paint-order: stroke; stroke: {COL['halo']}; stroke-width: 3px; }}
    .lugar {{ fill: {COL['etiqueta']}; paint-order: stroke; stroke: {COL['halo']}; stroke-width: 2.8px; stroke-linejoin: round; }}
    .numero {{ fill: #7a2e12; font-size: 11px; font-weight: 700; text-anchor: middle; paint-order: stroke; stroke: {COL['halo']}; stroke-width: 2.6px; }}
    .region {{ fill: #8a6413; font-size: 13.5px; font-weight: 700; text-anchor: middle; letter-spacing: 2.2px; opacity: 0.85; paint-order: stroke; stroke: #fdf9ef; stroke-width: 3.4px; stroke-opacity: 0.95; }}
    .escala-txt, .norte-txt {{ font-size: 10.5px; fill: #3b2f1e; text-anchor: middle; }}
    .leyenda-titulo {{ font-size: 12px; font-weight: 700; fill: {COL['titulo']}; }}
    .leyenda-item {{ font-size: 11.5px; fill: {COL['etiqueta']}; }}
    .leyenda-num {{ font-weight: 700; fill: #7a2e12; }}
"""
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.ancho} {self.alto}" '
                f'width="{self.ancho}" height="{self.alto}" role="img" '
                f'aria-label="{_esc(self.def_mapa.get("titulo", "Mapa bíblico"))}">'
                f'<defs><style>{estilos}</style>{"".join(defs)}</defs>'
                f'<g clip-path="url(#recorte)">{cuerpo}</g>{marco}</svg>')

    def construir(self):
        d = self.def_mapa
        self.dibujar_base(con_fronteras=d.get("fronteras", True),
                          con_rios=d.get("rios", True),
                          con_graticula=d.get("graticula", True))
        if d.get("regiones"):
            self.dibujar_regiones(d["regiones"])
        if d.get("rutas"):
            self.dibujar_rutas(d["rutas"])
        if d.get("etiquetas_extra"):
            self.dibujar_etiquetas_extra(d["etiquetas_extra"])
        if d.get("lugares"):
            self.dibujar_lugares(d["lugares"], numerar=d.get("numerar"))
        self.dibujar_leyenda()
        self.dibujar_rotulo()
        return self.svg()


def bbox_de_lugares(lista, extras, aspecto, margen=0.14):
    """
    Calcula la ventana geográfica que abarca los lugares indicados, con un
    margen, y la ensancha para que su proporción coincida con la del lienzo
    (así no queda espacio vacío en los bordes).
    """
    lon_min = lat_min = float("inf")
    lon_max = lat_max = float("-inf")
    def coords(ref):
        if isinstance(ref, dict):
            return ref.get("lon"), ref.get("lat")
        valor = extras.get(ref)
        if valor:
            return valor.get("lon"), valor.get("lat")
        return None, None
    for ref in lista:
        lon, lat = coords(ref)
        if lon is None or lat is None:
            continue
        lon_min, lon_max = min(lon_min, lon), max(lon_max, lon)
        lat_min, lat_max = min(lat_min, lat), max(lat_max, lat)
    if lon_min == float("inf"):
        return None
    ancho = max(0.6, lon_max - lon_min)
    alto = max(0.6, lat_max - lat_min)
    lon_min -= ancho * margen
    lon_max += ancho * margen
    lat_min -= alto * margen
    lat_max += alto * margen
    lat_media = (lat_min + lat_max) / 2
    k = math.cos(math.radians(lat_media))
    ancho_actual = (lon_max - lon_min) * k
    alto_actual = lat_max - lat_min
    if ancho_actual / alto_actual < aspecto:
        objetivo = alto_actual * aspecto
        extra = (objetivo - ancho_actual) / k / 2
        lon_min -= extra
        lon_max += extra
    else:
        objetivo = ancho_actual / aspecto
        extra = (objetivo - alto_actual) / 2
        lat_min -= extra
        lat_max += extra
    return [round(lon_min, 4), round(lat_min, 4), round(lon_max, 4), round(lat_max, 4)]


def cargar_entorno():
    base = _cargar_json(DATOS / "base.json")
    regiones = _cargar_json(DATOS / "regiones.json")
    lugares = _cargar_json(DATOS / "lugares.json")
    return base, regiones, lugares


def generar(def_mapa, entorno=None, extras=None):
    base, regiones, lugares = entorno or cargar_entorno()
    mapa = Mapa(base, regiones, lugares, def_mapa, extras=extras)
    svg = mapa.construir()
    return svg, mapa.avisos
