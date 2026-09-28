#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
construir_datos.py — Convierte las fuentes públicas (dominio público y
Creative Commons) en los archivos JSON que usa la aplicación de escritorio.

Fuentes utilizadas
------------------
1. Bible-Geocoding-Data (openbible.info, CC BY 4.0): 1.342 lugares bíblicos con
   coordenadas, tipos, referencias y geometrías; catálogo de fotografías de
   Wikimedia Commons con autoría y licencia.
2. bible-dictionary-dataset (NEUU, CC BY 4.0): 20.900 voces de los diccionarios
   de Easton (1897), Smith (1863), Hastings (1898), Hitchcock (1869) y Schaff,
   todos de dominio público.
3. bible-topics-dataset (NEUU, CC BY 4.0): 5.745 temas del índice temático de
   Nave (1896) y Torrey (1897) con 65.485 referencias, todos de dominio público.
4. Biblia Reina-Valera 1960 en JSON (los archivos que ya estaban en el
   repositorio del usuario).

Todo el texto de referencia que ve el usuario se convierte al español con
libros_es.py (nombres de libros, formato de citas) y con los diccionarios de
contenido/palabras_es.json y contenido/nombres_biblicos_es.json.
"""

import argparse
import gzip
import json
import os
import re
import shutil
import sys
import unicodedata
from datetime import date
from pathlib import Path

AQUI = Path(__file__).resolve().parent
APP = AQUI.parent
REPO = APP.parent

sys.path.insert(0, str(AQUI))
import libros_es as LE  # noqa: E402

FUENTES_POR_DEFECTO = Path(os.environ.get("RENACER_FUENTES", "/home/user/_fuentes"))
SALIDA = APP / "app" / "datos"
CONTENIDO = APP / "contenido"

# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------


def leer_json(ruta, defecto=None):
    try:
        with open(ruta, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return defecto


def escribir_json(ruta, datos, compacto=True, gzip_tambien=False):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        if compacto:
            json.dump(datos, f, ensure_ascii=False, separators=(",", ":"))
        else:
            json.dump(datos, f, ensure_ascii=False, indent=1)
    if gzip_tambien:
        with gzip.open(str(ruta) + ".gz", "wt", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, separators=(",", ":"))
    tam = ruta.stat().st_size
    print(f"  · {ruta.relative_to(APP)}  ({tam / 1024:.0f} KB)")
    return tam


def sin_acentos(t):
    return "".join(c for c in unicodedata.normalize("NFKD", t) if not unicodedata.combining(c))


def limpiar_texto(t):
    """Quita restos de marcado de las fuentes ThML/HTML y normaliza espacios."""
    if not t:
        return ""
    t = re.sub(r"<[^>]+>", " ", t)
    t = (t.replace("&nbsp;", " ").replace("&amp;", "&").replace("&quot;", '"')
          .replace("&#39;", "'").replace("&lt;", "<").replace("&gt;", ">"))
    t = re.sub(r"\[[a-zA-Z]{1,3}\]", "", t)          # marcas de notas [a], [b]
    t = re.sub(r"\s+", " ", t)
    return t.strip()


# ---------------------------------------------------------------------------
# Nombres en español
# ---------------------------------------------------------------------------

NOMBRES_LUGAR = {k: v for k, v in leer_json(CONTENIDO / "nombres_lugares_es.json", {}).items()
                 if not k.startswith("_")}
PALABRAS_ES = {k.lower(): v for k, v in leer_json(CONTENIDO / "palabras_es.json", {}).items()
               if not k.startswith("_")}
NOMBRES_PERSONA = {k.lower(): v for k, v in leer_json(CONTENIDO / "nombres_biblicos_es.json", {}).items()
                   if not k.startswith("_")}

TIPOS_EXCLUIDOS = {
    "altar", "room", "structure", "fortification", "stone heap", "people group",
    "building", "throne", "chamber", "object", "gate of the temple", "city gate",
    "temple", "ritual object", "watercourse", "artificial",
}

NOMBRES_EXCLUIDOS = {"east", "north", "south", "west", "angle", "east 1", "west 1"}

TIPOS_ES = {
    "settlement": "ciudad o poblado", "region": "región", "river": "río",
    "mountain": "monte", "mountain range": "cordillera", "hill": "colina",
    "island": "isla", "body of water": "mar o lago", "valley": "valle",
    "plain": "llanura", "well": "pozo", "spring": "manantial",
    "wilderness": "desierto", "sea": "mar", "lake": "lago", "cave": "cueva",
    "fortress": "fortaleza", "tower": "torre", "gate": "puerta", "pool": "estanque",
    "road": "camino", "garden": "huerto", "ruins": "ruinas", "port": "puerto",
    "province": "provincia", "kingdom": "reino", "altar": "altar", "room": "sala",
    "temple": "templo", "palace": "palacio", "building": "edificio", "wall": "muro",
    "city": "ciudad", "village": "aldea", "camp": "campamento", "island group": "archipiélago",
    "peninsula": "península", "strait": "estrecho", "canal": "canal", "spring": "manantial",
    "mountain pass": "paso de montaña", "oasis": "oasis", "harbor": "puerto",
    "unknown": "lugar", "natural": "lugar natural", "human": "lugar humano",
    "other": "otro", "bridge": "puente", "quarry": "cantera", "field": "campo",
    "threshing floor": "era", "cave": "cueva", "tomb": "sepulcro",
}

# Reglas de adaptación automática para los nombres sin traducción curada
# Prefijos geográficos que sí se traducen siempre
PREFIJOS_GEO = {
    "mount": "Monte", "sea": "Mar", "lake": "Lago", "city": "Ciudad",
    "valley": "Valle", "wilderness": "Desierto", "plain": "Llanura",
    "brook": "Torrente", "river": "Río", "tower": "Torre", "house": "Casa",
    "land": "Tierra", "waters": "Aguas", "field": "Campo", "pool": "Estanque",
    "gate": "Puerta", "well": "Pozo", "spring": "Manantial", "cave": "Cueva",
    "hill": "Collado", "rock": "Peña", "island": "Isla", "upper": None, "lower": None,
}

_REGLAS_ADAPTACION = [
    ("sh", "s"), ("ph", "f"), ("th", "t"), ("ch", "c"), ("dh", "d"),
    ("tz", "z"), ("ck", "c"), ("oo", "u"), ("ee", "i"), ("qu", "c"),
    ("ss", "s"), ("ll", "l"),
]

_ACENTOS_FINALES = [
    ("on", "ón"), ("el", "el"), ("er", "er"), ("im", "im"), ("ah", "á"),
    ("eh", "é"), ("ih", "í"), ("oh", "ó"), ("uh", "ú"), ("a", "á"), ("i", "í"),
]


def adaptar_palabra(palabra):
    """Adapta una palabra suelta (aproximación ortográfica al castellano)."""
    p = palabra.lower()
    for a, b in _REGLAS_ADAPTACION:
        p = p.replace(a, b)
    p = re.sub(r"(.)\1+", r"\1", p)
    for fin, nuevo in _ACENTOS_FINALES:
        if p.endswith(fin) and len(p) > len(fin) + 1:
            if fin not in ("a", "i") or len(p) > 4:
                if not p.endswith(("ia", "ea", "oa", "ua")):
                    p = p[: -len(fin)] + nuevo
            break
    return p.capitalize()


def adaptar_a_es(nombre):
    """
    Adapta automáticamente un nombre inglés a una forma castellana legible:
    traduce los prefijos geográficos conocidos (Valley of Elah -> Valle de Ela)
    y adapta el resto con reglas ortográficas sencillas. La aplicación avisa de
    que el nombre es adaptado y muestra siempre el original.
    """
    if not nombre:
        return nombre
    # Estructuras con "of": "Valley of Elah", "Wilderness of Ziph"
    m = re.match(r"^([A-Za-z]+)\s+of(?:\s+the)?\s+(.+)$", nombre)
    if m and m.group(1).lower() in PREFIJOS_GEO and PREFIJOS_GEO[m.group(1).lower()]:
        return f"{PREFIJOS_GEO[m.group(1).lower()]} de {adaptar_a_es(m.group(2))}"
    # "Upper Beth-horon" / "Lower Beth-horon"
    m = re.match(r"^(Upper|Lower)\s+(.+)$", nombre)
    if m:
        sufijo = "de arriba" if m.group(1) == "Upper" else "de abajo"
        return f"{adaptar_a_es(m.group(2))} {sufijo}"
    # "Mount X", "Sea X"
    m = re.match(r"^([A-Za-z]+)\s+(.+)$", nombre)
    if m and m.group(1).lower() in PREFIJOS_GEO and PREFIJOS_GEO[m.group(1).lower()]:
        return f"{PREFIJOS_GEO[m.group(1).lower()]} {adaptar_a_es(m.group(2))}"
    partes = re.split(r"([\-\s])", nombre)
    salida = []
    for parte in partes:
        if parte in ("-", " ", "") or parte[0].isdigit():
            salida.append(parte)
            continue
        palabra = parte.lower()
        # No tocar partículas sueltas
        if palabra in ("of", "the", "de", "el", "la", "al", "ar", "ur", "ai", "ir", "in", "on"):
            salida.append("" if palabra in ("of", "the") else palabra)
            continue
        salida.append(adaptar_palabra(palabra))
    texto = "".join(salida)
    texto = re.sub(r"\s+", " ", texto).strip().strip("-")
    texto = re.sub(r"-+", "-", texto)
    return texto


def nombre_es(original, con_adaptacion=True):
    """Devuelve (nombre_español, adaptado)."""
    if not original:
        return original, False
    clave = original.strip()
    if clave in NOMBRES_LUGAR:
        return NOMBRES_LUGAR[clave], False
    # "Babylon 1" -> "Babylon";  "Ramah 4" -> "Ramah"
    base = re.sub(r"\s+\d+$", "", clave)
    if base in NOMBRES_LUGAR:
        return NOMBRES_LUGAR[base], False
    if not con_adaptacion:
        return base, False
    return adaptar_a_es(base), True


def tipo_es(tipo):
    if not tipo:
        return "lugar"
    return TIPOS_ES.get(tipo, tipo)


# ---------------------------------------------------------------------------
# Traducción asistida de los títulos y etiquetas del índice temático
# ---------------------------------------------------------------------------

FRASES_ES = {
    "general references": "Referencias generales",
    "general scriptures concerning": "Escrituras generales acerca de",
    "general scriptures": "Escrituras generales",
    "general": "General",
    "instances of": "Casos de",
    "figurative": "Figurado",
    "symbolical": "Simbólico",
    "unclassified scriptures relating to": "Escrituras diversas relacionadas con",
    "exemplified": "Ejemplificado en",
    "illustrative": "Ilustrativo",
    "of christ": "de Cristo",
    "of jesus": "de Jesús",
    "of david": "de David",
    "of moses": "de Moisés",
    "of paul": "de Pablo",
    "of abraham": "de Abraham",
    "of jacob": "de Jacob",
    "of joseph": "de José",
    "of saul": "de Saúl",
    "of israel": "de Israel",
    "of solomon": "de Salomón",
    "of samuel": "de Samuel",
    "punishment of": "Castigo de",
    "punishment for": "Castigo por",
    "blessedness of": "Bienaventuranza de",
    "antiquity of": "Antigüedad de",
    "families of": "Familias de",
    "prophecies concerning": "Profecías acerca de",
    "prophecy concerning": "Profecía acerca de",
    "predictions respecting": "Predicciones acerca de",
    "exhortation to": "Exhortación a",
    "created by god": "Creado por Dios",
    "an ancestor of jesus": "Un antepasado de Jesús",
    "a benjamite": "Un benjaminita",
    "a levite": "Un levita",
    "a priest": "Un sacerdote",
    "a prophet": "Un profeta",
    "a city of": "Una ciudad de",
    "a precious stone": "Una piedra preciosa",
    "a characteristic of saints": "Una característica de los santos",
    "a characteristic of the wicked": "Una característica de los impíos",
    "one of the nethinim": "Uno de los netineos",
    "a city of the tribe of": "Una ciudad de la tribu de",
    "fulfilled": "Cumplido",
    "fulfilled in": "Cumplido en",
    "forbidden": "Prohibido",
    "forbid": "Prohibido",
    "commanded": "Mandado",
    "sent as a": "Enviado como",
    "free-will": "Voluntarias",
    "see also": "Véase también",
    "persons selected from": "Personas escogidas de",
    "to number the people": "para contar al pueblo",
    "to spy out the land": "para reconocer la tierra",
    "to divide the land": "para repartir la tierra",
    "strength of, on leaving egypt": "Fuerza de, al salir de Egipto",
}


TYPOS = {
    # erratas de digitalización del índice temático
    "0f": "of", "0F": "OF", "ofgod": "of God", "seechildren": "See children",
    "enjoine": "enjoined", "leviti": "Leviticus", "comman": "command",
    "melchize": "Melchizedek", "inva": "invasion", "chal": "Chaldeans",
    "zebu": "Zebulun", "ahaziah": "Ahaziah", "benhadad": "Ben-hadad",
    "gi": "Gibeon", "ma": "Maran-atha", "sam": "Samuel", "pas": "Passover",
    "mor": "Moreh", "ze": "Zebulun", "ha": "Haran", "mi": "Micah",
}


def traducir_texto_corto(texto, titulo=False):
    """
    Traduce un título o etiqueta del índice temático con el vocabulario de
    contenido/palabras_es.json. Devuelve (traducción, palabras_sin_traducir).
    """
    texto = limpiar_texto(texto or "")
    if not texto:
        return "", []
    # la fuente pegó palabras y trajo erratas de digitalización
    for mal, bien in TYPOS.items():
        texto = re.sub(rf"\b{re.escape(mal)}\b", bien, texto, flags=re.IGNORECASE if mal.islower() else 0)
    # "A. ..." / "1. ..." / ".Of ..." (se quita antes de mirar los «véase»)
    prefijo = ""
    m = re.match(r"^([0-9]+\.|[A-Z]\.|\(\d+\)|\.)\s*(.*)$", texto)
    if m:
        # el punto suelto no aporta nada; los códigos («A.», «1.») se conservan
        prefijo = "" if m.group(1) == "." else m.group(1) + " "
        texto = m.group(2)
    clave = texto.strip().rstrip(".").lower()
    if clave in FRASES_ES:
        return FRASES_ES[clave], []
    texto = re.sub(r"^\s*See\s*([A-Z]{3,})", r"Véase \1", texto)
    # "SeeARMIES", "SeeMUSIC": la fuente pegó el "véase"
    m = re.match(r"^See([A-Z]{3,}.*)$", texto)
    if m:
        return "Véase " + traducir_texto_corto(m.group(1))[0], []
    sin_traducir = []
    # se separa respetando las letras acentuadas (para no partir «Véase»)
    palabras = re.findall(r"[\w'\-]+|[^\w\s]+|\s+", texto, re.UNICODE)
    salida = []
    for palabra in palabras:
        if not palabra.strip():
            salida.append(" ")
            continue
        if not re.match(r"[^\W\d_]", palabra, re.UNICODE):
            salida.append(palabra)
            continue
        baja = palabra.lower().strip("'")
        if baja in NOMBRES_PERSONA:
            salida.append(NOMBRES_PERSONA[baja])
        elif baja in NOMBRES_LUGAR:
            salida.append(NOMBRES_LUGAR[baja])
        elif baja in PALABRAS_ES:
            salida.append(PALABRAS_ES[baja])
        elif baja.endswith("s") and baja[:-1] in PALABRAS_ES:
            salida.append(PALABRAS_ES[baja[:-1]])
        elif baja.endswith("es") and baja[:-2] in PALABRAS_ES:
            salida.append(PALABRAS_ES[baja[:-2]])
        elif baja.rstrip("s") in NOMBRES_PERSONA:
            salida.append(NOMBRES_PERSONA[baja.rstrip("s")])
        elif baja.rstrip("s") in NOMBRES_LUGAR:
            salida.append(NOMBRES_LUGAR[baja.rstrip("s")])
        else:
            sin_traducir.append(palabra)
            salida.append(palabra.capitalize())
    texto_es = "".join(salida)
    texto_es = re.sub(r"\s+", " ", prefijo + texto_es).strip()
    # Artículos sueltos y preposiciones mal colocadas al final
    texto_es = re.sub(r"\s+(de|a|en|por|con|acerca)$", "", texto_es)
    texto_es = (texto_es[:1].upper() + texto_es[1:]) if texto_es else texto_es
    if titulo:
        texto_es = texto_es.upper() if texto.isupper() else texto_es
    return texto_es, sin_traducir


# ---------------------------------------------------------------------------
# 1. Lugares
# ---------------------------------------------------------------------------

def cargar_imagenes(fuentes):
    """image.jsonl -> índice por image_id con URL, autor y licencia."""
    indice = {}
    ruta = fuentes / "Bible-Geocoding-Data-main" / "data" / "image.jsonl"
    if not ruta.exists():
        return indice
    for linea in open(ruta, encoding="utf-8"):
        try:
            d = json.loads(linea)
        except json.JSONDecodeError:
            continue
        indice[d.get("id")] = {
            "url": d.get("file_url") or d.get("url"),
            "pagina": d.get("url") or d.get("credit_url"),
            "autor": limpiar_texto(d.get("author") or d.get("credit") or ""),
            "licencia": d.get("license") or "",
            "descripcion": limpiar_texto(next(iter((d.get("descriptions") or {}).values()), "")),
            "credito_url": d.get("credit_url"),
            "ancho": d.get("width"), "alto": d.get("height"),
            "miniatura": (d.get("thumbnail_url_pattern") or "").replace("####", "800"),
        }
    return indice


def construir_lugares(fuentes):
    print("· Lugares bíblicos ...")
    imagenes = cargar_imagenes(fuentes)
    ruta = fuentes / "Bible-Geocoding-Data-main" / "data" / "ancient.jsonl"
    lugares = []
    imagenes_usadas = 0
    for linea in open(ruta, encoding="utf-8"):
        d = json.loads(linea)
        coords = tipo = geom = None
        geom_fichero = None
        for ident in d.get("identifications", []):
            for res in ident.get("resolutions", []):
                if res.get("lonlat") and not coords:
                    coords = res["lonlat"]
                    tipo = res.get("type")
                    geom = res.get("ancient_geometry")
                    roles = res.get("geojson_roles") or {}
                    for clave in ("precise", "geometry", "isobands"):
                        if clave in roles:
                            geom_fichero = roles[clave].get("id", "")
                            break
                    if not geom_fichero:
                        mod = res.get("modern_basis_id")
                        if mod and str(mod).startswith("m"):
                            geom_fichero = mod
        if not coords:
            continue
        lon, lat = (float(x) for x in coords.split(","))
        original = d.get("friendly_id") or ""
        nombre, adaptado = nombre_es(original)
        refs = []
        for v in d.get("verses", []):
            r = LE.referencia_a_es(v.get("osis")) or v.get("readable")
            if r and r not in refs:
                refs.append(r)
        refs.sort(key=lambda r: (LE.ORDEN.get(re.sub(r"\s+\d+:.*$", "", r), 99)))
        # identificaciones modernas (a qué lugar actual corresponde)
        modernos = []
        for mid, info in (d.get("modern_associations") or {}).items():
            if info.get("name"):
                modernos.append(info["name"])
        # fotografía de Wikimedia Commons (con autoría y licencia)
        foto = None
        mini = ((d.get("media") or {}).get("thumbnail") or {})
        if mini.get("image_id"):
            info = imagenes.get(mini["image_id"])
            if info:
                foto = {
                    "url": info.get("url") or mini.get("credit_url"),
                    "miniatura": info.get("miniatura") or info.get("url"),
                    "pagina": info.get("pagina") or mini.get("credit_url"),
                    "autor": info.get("autor") or mini.get("credit") or "",
                    "licencia": info.get("licencia") or "",
                    "descripcion": limpiar_texto(mini.get("description") or info.get("descripcion") or ""),
                }
                imagenes_usadas += 1
        tipos = d.get("types") or []
        if (tipos and tipos[0] in TIPOS_EXCLUIDOS) or original.lower() in NOMBRES_EXCLUIDOS:
            continue
        lugares.append({
            "id": d.get("url_slug") or d.get("id"),
            "nombre": nombre,
            "original": original,
            "adaptado": adaptado,
            "tipo": tipo_es(tipos[0] if tipos else tipo),
            "tipo_original": tipos[0] if tipos else (tipo or ""),
            "lon": round(lon, 5), "lat": round(lat, 5),
            "geometria": geom_fichero,
            "forma": geom,
            "refs": refs[:40],
            "total_refs": len(refs),
            "modernos": modernos[:6],
            "foto": foto,
            "credito_geometria": d.get("geometry_credit"),
        })
    lugares.sort(key=lambda l: -l["total_refs"])
    return lugares, imagenes_usadas


def construir_regiones(fuentes, lugares):
    """Polígonos/líneas de las regiones bíblicas (para el mapa interactivo)."""
    print("· Regiones y geometrías ...")
    base = fuentes / "Bible-Geocoding-Data-main"
    interesantes = {
        "israel", "judah", "judea", "samaria", "galilee", "canaan", "egypt", "moab",
        "edom", "ammon", "philistia", "assyria", "babylonia", "chaldea", "persia",
        "greece", "macedonia", "syria", "lebanon", "bashan", "gilead", "midian",
        "arabia", "negeb", "shephelah", "decapolis", "phoenicia", "italy", "asia",
        "achaia", "galatia", "cilicia", "mesopotamia", "cush", "amalek", "params",
        "bashan", "aram", "geshur", "paran", "sharon", "arabah", "sin",
    }
    regiones = []
    for lugar in lugares:
        if lugar["tipo_original"] not in ("region", "island", "body of water"):
            continue
        gid = lugar.get("geometria")
        if not gid:
            continue
        clave = sin_acentos(lugar["original"].lower().split()[0])
        if clave not in interesantes and lugar["tipo_original"] != "island":
            continue
        fichero = base / "geometry" / f"{gid}.geojson"
        if not fichero.exists() and (base / "geometry" / f"{gid}.isobands.geojson").exists():
            fichero = base / "geometry" / f"{gid}.isobands.geojson"
        if not fichero.exists():
            continue
        try:
            gj = json.load(open(fichero, encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        puntos = []
        features = gj.get("features") if gj.get("type") == "FeatureCollection" else [gj]
        for feat in features or []:
            g = feat.get("geometry") or {}
            tipos = g.get("type")
            coords = g.get("coordinates") or []
            anillos = []
            if tipos == "Polygon":
                anillos = coords
            elif tipos == "MultiPolygon":
                anillos = [a for poly in coords for a in poly]
            for anillo in anillos:
                anillo_simple = [[round(float(x), 4), round(float(y), 4)] for x, y in anillo]
                if len(anillo_simple) >= 4:
                    puntos.append(anillo_simple)
        if puntos:
            regiones.append({"id": lugar["id"], "nombre": lugar["nombre"], "anillos": puntos})
    return regiones


# ---------------------------------------------------------------------------
# 2. Temas (índice temático de Nave y Torrey)
# ---------------------------------------------------------------------------

def construir_temas(fuentes):
    print("· Índice temático (Nave 1896 / Torrey 1897) ...")
    raiz = fuentes / "bible-topics-dataset-main" / "data" / "01_parsed"
    temas = []
    refs_totales = 0
    for fichero in sorted(raiz.glob("*/*.json")):
        d = json.load(open(fichero, encoding="utf-8"))
        titulo_en = d.get("topic", "")
        titulo_es, faltan = traducir_texto_corto(titulo_en, titulo=True)
        aspectos = []
        for a in d.get("aspects", []):
            etiqueta_en = limpiar_texto(a.get("label", ""))
            etiqueta_es, restan = traducir_texto_corto(etiqueta_en)
            refs = []
            for r in a.get("references", []):
                es = LE.referencia_a_es(r)
                if es and es not in refs:
                    refs.append(es)
            if not refs and not etiqueta_en:
                continue
            refs_totales += len(refs)
            aspectos.append({
                "etiqueta": etiqueta_es,
                "etiqueta_original": etiqueta_en if restan or etiqueta_es != etiqueta_en else None,
                "refs": refs,
                "fuente": a.get("source"),
            })
        ver = []
        for v in d.get("see_also", []):
            v_es, _ = traducir_texto_corto(v, titulo=True)
            ver.append({"en": v, "es": v_es})
        temas.append({
            "id": d.get("slug"),
            "titulo": titulo_es,
            "titulo_original": titulo_en,
            "traduccion_completa": not faltan,
            "aspectos": aspectos,
            "ver_tambien": ver,
            "fuentes": d.get("sources", []),
            "total_refs": sum(len(a["refs"]) for a in aspectos),
            "libros": d.get("books_mentioned", []),
        })
    temas.sort(key=lambda t: (-t["total_refs"], t["titulo"]))
    return temas, refs_totales


# ---------------------------------------------------------------------------
# 3. Diccionarios históricos
# ---------------------------------------------------------------------------

DICCIONARIOS = [
    ("easton", "Diccionario Bíblico de Easton", "M. G. Easton", 1897,
     "Voz enciclopédica clásica sobre personas, lugares, objetos y doctrinas."),
    ("smith", "Diccionario Bíblico de Smith", "William Smith", 1863,
     "Diccionario histórico-geográfico con descripciones detalladas de lugares."),
    ("hastings", "Diccionario de la Biblia de Hastings", "James Hastings", 1898,
     "Artículo extenso de erudición bíblica de finales del siglo XIX."),
    ("hitchcock", "Nombres Bíblicos de Hitchcock", "Roswell D. Hitchcock", 1869,
     "Significado de los nombres propios hebreos y griegos de la Biblia."),
    ("schaff", "Diccionario de Schaff", "Philip Schaff", 1880,
     "Voces y artículos de la enciclopedia bíblica de Schaff (dominio público)."),
]


def construir_diccionarios(fuentes):
    print("· Diccionarios históricos (dominio público) ...")
    raiz = fuentes / "bible-dictionary-dataset-main" / "data" / "02_sources"
    resumen = []
    for codigo, titulo, autor, anio, descripcion in DICCIONARIOS:
        carpeta = raiz / codigo
        if not carpeta.exists():
            print(f"    (falta la fuente {codigo}, se omite)")
            continue
        entradas = []
        for fichero in sorted(carpeta.glob("*.json")):
            if fichero.name.startswith("_"):
                continue
            d = json.load(open(fichero, encoding="utf-8"))
            if not isinstance(d, dict):
                continue
            for clave, valor in d.items():
                if not isinstance(valor, dict) or "definitions" not in valor:
                    continue
                textos = [limpiar_texto(x.get("text", "")) for x in valor["definitions"]]
                textos = [t for t in textos if t]
                if not textos:
                    continue
                texto = " ".join(dict.fromkeys(textos))
                if len(texto) < 15:
                    continue
                refs = []
                refs_crudas = valor.get("scripture_refs_calculated") or valor.get("scripture_refs") or []
                for r in refs_crudas:
                    ref = r.get("reference") if isinstance(r, dict) else r
                    es = LE.referencia_a_es(ref)
                    if es and es not in refs:
                        refs.append(es)
                nombre = valor.get("name") or clave
                titulo_es, adaptado = nombre_es(nombre)
                entradas.append({
                    "id": valor.get("slug") or sin_acentos(clave.lower()).replace(" ", "-"),
                    "t": nombre,
                    "tes": titulo_es if not adaptado else None,
                    "texto": texto,
                    "refs": refs[:25],
                })
        entradas.sort(key=lambda e: e["t"].lower())
        escribir_json(SALIDA / "diccionarios" / f"{codigo}.json", entradas)
        resumen.append({
            "codigo": codigo, "titulo": titulo, "autor": autor, "anio": anio,
            "descripcion": descripcion, "entradas": len(entradas),
            "refs": sum(len(e["refs"]) for e in entradas),
        })
    return resumen


# ---------------------------------------------------------------------------
# 4. Biblia Reina-Valera 1960 (los JSON del repositorio del usuario)
# ---------------------------------------------------------------------------

def construir_biblia():
    print("· Biblia Reina-Valera 1960 (lector y concordancias) ...")
    destino = SALIDA / "biblia"
    if destino.exists():
        shutil.rmtree(destino)
    destino.mkdir(parents=True, exist_ok=True)
    libros = []
    total_versiculos = 0
    orden = 0
    for nombre in LE.ES_A_OSIS:
        fichero = REPO / f"{nombre}.json"
        if not fichero.exists():
            continue
        d = json.load(open(fichero, encoding="utf-8"))
        if not isinstance(d, dict) or "chapters" not in d:
            continue
        orden += 1
        caps = {str(k): {str(v): t for v, t in c.items()} for k, c in d["chapters"].items()}
        n_versiculos = sum(len(c) for c in caps.values())
        total_versiculos += n_versiculos
        libros.append({
            "nombre": nombre,
            "osis": LE.ES_A_OSIS[nombre],
            "abrev": LE.ABREV_ES[nombre],
            "testamento": LE.TESTAMENTO[nombre],
            "orden": orden,
            "capitulos": len(caps),
            "versiculos": n_versiculos,
            "version": d.get("version", "RVR1960"),
        })
        escribir_json(destino / f"{LE.ES_A_OSIS[nombre]}.json", caps, compacto=True)
    escribir_json(SALIDA / "biblia" / "libros.json", libros)
    faltan = [n for n in LE.ES_A_OSIS if not (REPO / f"{n}.json").exists()]
    if faltan:
        print(f"    Aviso: faltan en el repositorio {', '.join(faltan)}")
    return libros, total_versiculos, faltan


# ---------------------------------------------------------------------------
# 5. Catálogo de fotografías (Wikimedia Commons)
# ---------------------------------------------------------------------------

def construir_fotos(fuentes, lugares):
    print("· Fotografías de lugares (Wikimedia Commons) ...")
    fotos = []
    for lugar in lugares:
        if lugar.get("foto"):
            f = lugar["foto"]
            fotos.append({
                "id": lugar["id"], "lugar": lugar["nombre"], "original": lugar["original"],
                "url": f.get("url"), "miniatura": f.get("miniatura"), "pagina": f.get("pagina"),
                "autor": f.get("autor"), "licencia": f.get("licencia"),
                "descripcion": f.get("descripcion"), "tipo": lugar["tipo"],
            })
    return fotos


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Construye los datos de la aplicación")
    ap.add_argument("--fuentes", default=str(FUENTES_POR_DEFECTO))
    ap.add_argument("--sin-biblia", action="store_true")
    ap.add_argument("--sin-diccionarios", action="store_true")
    args = ap.parse_args()
    fuentes = Path(args.fuentes)

    print(f"Fuentes: {fuentes}")
    print(f"Salida : {SALIDA}")
    SALIDA.mkdir(parents=True, exist_ok=True)

    lugares, imagenes_usadas = construir_lugares(fuentes)
    escribir_json(SALIDA / "lugares.json", lugares)
    regiones = construir_regiones(fuentes, lugares)
    escribir_json(SALIDA / "regiones_crudas.json", regiones)

    temas, refs_temas = construir_temas(fuentes)
    escribir_json(SALIDA / "temas.json", temas)

    diccionarios = [] if args.sin_diccionarios else construir_diccionarios(fuentes)

    libros, total_versiculos, faltan = ([], 0, [])
    if not args.sin_biblia:
        libros, total_versiculos, faltan = construir_biblia()

    fotos = construir_fotos(fuentes, lugares)
    escribir_json(SALIDA / "fotos.json", fotos)

    enciclopedia = leer_json(CONTENIDO / "enciclopedia_es.json", [])
    escribir_json(SALIDA / "enciclopedia.json", enciclopedia)

    # galería de arte (la prepara construir_arte.py; si ya existe, se cuenta)
    obras_arte = 0
    if (SALIDA / "arte.json").exists():
        obras_arte = len(leer_json(SALIDA / "arte.json", {}).get("obras", []))

    indice = {
        "aplicacion": "Renacer · Atlas Bíblico y Biblioteca",
        "version": "1.0.0",
        "construido": date.today().isoformat(),
        "lugares": len(lugares),
        "lugares_con_foto": imagenes_usadas,
        "regiones": len(regiones),
        "temas": len(temas),
        "referencias_tematicas": refs_temas,
        "diccionarios": diccionarios,
        "libros_biblia": len(libros),
        "versiculos_biblia": total_versiculos,
        "libros_faltantes": faltan,
        "entradas_enciclopedia": len(enciclopedia),
        "fotos": len(fotos),
        "obras_arte": obras_arte,
        "fuentes": [
            {"nombre": "Bible-Geocoding-Data", "autor": "openbible.info (Stephen Smith)",
             "licencia": "CC BY 4.0", "url": "https://github.com/openbibleinfo/Bible-Geocoding-Data",
             "uso": "Lugares, coordenadas, referencias, geometrías y catálogo de fotografías de Wikimedia Commons"},
            {"nombre": "bible-dictionary-dataset", "autor": "NEUU", "licencia": "CC BY 4.0 (textos de dominio público)",
             "url": "https://github.com/neuu-org/bible-dictionary-dataset",
             "uso": "Voces de Easton (1897), Smith (1863), Hastings (1898), Hitchcock (1869) y Schaff"},
            {"nombre": "bible-topics-dataset", "autor": "NEUU", "licencia": "CC BY 4.0 (textos de dominio público)",
             "url": "https://github.com/neuu-org/bible-topics-dataset",
             "uso": "Índice temático de Nave (1896) y Torrey (1897) con sus referencias"},
            {"nombre": "Biblia Reina-Valera 1960 (JSON del repositorio del usuario)",
             "autor": "—", "licencia": "Texto aportado por el usuario",
             "url": "—", "uso": "Lectura de la Biblia y concordancias"},
            {"nombre": "Natural Earth", "autor": "Natural Earth", "licencia": "Dominio público",
             "url": "https://www.naturalearthdata.com",
             "uso": "Costas, ríos, lagos y fronteras modernas para el fondo de los mapas"},
            {"nombre": "La Grande Bible de Tours (grabados de Gustave Doré, 1866)",
             "autor": "Gustave Doré", "licencia": "Dominio público",
             "url": "https://github.com/Nainoia-Inc/AionianBible_GustaveDore_LaGrandeBibledeTours",
             "uso": "Galería de arte bíblico"},
        ],
    }
    escribir_json(SALIDA / "indice.json", indice, compacto=False)
    print("\nResumen:")
    for k, v in indice.items():
        if k in ("fuentes", "diccionarios"):
            continue
        print(f"  {k}: {v}")
    for d in diccionarios:
        print(f"  diccionario {d['codigo']}: {d['entradas']} voces / {d['refs']} referencias")


if __name__ == "__main__":
    main()
