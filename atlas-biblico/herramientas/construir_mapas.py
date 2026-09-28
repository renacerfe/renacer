#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
construir_mapas.py — Genera todos los mapas del atlas en SVG y el catálogo
app/datos/mapas.json que consume la aplicación.

Uso:
    python3 construir_mapas.py            # genera todo
    python3 construir_mapas.py --revisar  # solo informa de identificadores dudosos
"""

import argparse
import json
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
APP = AQUI.parent
sys.path.insert(0, str(AQUI))

import motor_mapas as MM                                    # noqa: E402
from catalogo_mapas import MUNDO, PENTATEUCO, REYES         # noqa: E402
from catalogo_mapas_nt import (JUDEA, CIUDADES, MAPAS_ANTIGUOS, EXTRA_LUGARES)  # noqa: E402
from planos import PLANOS                                   # noqa: E402

CATALOGO = MUNDO + PENTATEUCO + REYES + JUDEA + CIUDADES + MAPAS_ANTIGUOS
SALIDA_MAPAS = APP / "app" / "mapas"
SALIDA_DATOS = APP / "app" / "datos"


def limpiar_titulo(t):
    """Escribe con tildes correctas los títulos definidos sin ellas."""
    correcciones = {
        "Eden": "Edén", "Jonas": "Jonás", "Jose": "José", "Egipto": "Egipto",
        "Isaias": "Isaías", "Ezequiel": "Ezequiel", "Salomon": "Salomón", "Elias": "Elías",
        "Esau": "Esaú", "Jabboc": "Jaboc", "Sinai": "Sinaí", "Galilea": "Galilea",
        "Babilonia": "Babilonia", "Nehemias": "Nehemías", "Senaquerib": "Senaquerib",
        "Jesus": "Jesús", "Jerusalen": "Jerusalén", "Mision": "Misión", "Huida": "Huida",
        "Efeso": "Éfeso", "Sermon": "Sermón", "Pablo": "Pablo", "Crucifixion": "Crucifixión",
        "Resurreccion": "Resurrección", "Ascension": "Ascensión", "Tentacion": "Tentación",
        "Ultimo": "Último", "Camino": "Camino", "Romanos": "Romanos", "Cartas": "Cartas",
        "Escribio": "Escribió", "Adonde": "Adónde", "Ciudades": "Ciudades", "Jordan": "Jordán",
        "Jerico": "Jericó", "Siquem": "Siquem", "Samaria": "Samaria", "Cartografia": "Cartografía",
        "biblica": "bíblica", "traves": "través", "siglos": "siglos", "division": "división",
        "dispersion": "dispersión", "reconstruccion": "reconstrucción", "muros": "muros",
        "ministerio": "ministerio", "Sinai": "Sinaí", "exodo": "éxodo", "Exodo": "Éxodo",
        "Areopago": "Areópago", "Mileto": "Mileto", "Filipos": "Filipos", "Tesalonica": "Tesalónica",
        "Atenas": "Atenas", "Corinto": "Corinto", "Roma": "Roma", "Malta": "Malta",
        "Naufragio": "Naufragio", "Apocalipsis": "Apocalipsis", "Iglesias": "Iglesias",
        "Armagedon": "Armagedón", "Pedro": "Pedro", "Templo": "Templo", "Tabernaculo": "Tabernáculo",
        "Explanada": "Explanada", "Plano": "Plano", "Antiguo": "Antiguo", "Testamento": "Testamento",
        "Nuevo": "Nuevo", "Imperio": "Imperio", "Reino": "Reino", "Tierra": "Tierra",
        "Reparto": "Reparto", "Refugio": "Refugio", "Jueces": "Jueces", "Saul": "Saúl",
        "David": "David", "Goliat": "Goliat", "Valle": "Valle", "Ela": "Ela",
        "Cana": "Caná", "Conquista": "Conquista", "Cuarenta": "Cuarenta", "Anos": "Años",
        "Desierto": "Desierto", "Sodoma": "Sodoma", "Gomorra": "Gomorra", "Torre": "Torre",
        "Babel": "Babel", "Diluvio": "Diluvio", "Arca": "Arca", "Ararat": "Ararat",
        "Viaje": "Viaje", "Abraham": "Abraham", "Jacob": "Jacob", "Rutas": "Rutas",
        "Amos": "Amós", "Oseas": "Oseas", "Rut": "Rut", "Moabita": "Moabita",
        "Jose": "José", "Faraon": "Faraón", "Prometida": "Prometida", "Espias": "Espías",
        "Madian": "Madián", "Filisteos": "Filisteos", "Reyes": "Reyes", "Profetas": "Profetas",
        "Daniel": "Daniel", "Imperios": "Imperios", "Exilio": "Exilio", "Destierro": "Destierro",
        "Restauracion": "Restauración", "Regreso": "Regreso", "Ester": "Ester", "Persa": "Persa",
        "Ciudad": "Ciudad", "Pais": "País", "Mapa": "Mapa", "Mapas": "Mapas",
        "Espanol": "Español", "Espanola": "Española",
    }
    for a, b in correcciones.items():
        t = re.sub(rf"\b{a}\b", b, t)
    return t


def generar_todo(revisar=False):
    base, regiones, lugares = MM.cargar_entorno()
    SALIDA_MAPAS.mkdir(parents=True, exist_ok=True)
    catalogo = []
    problemas = {}
    aspecto = 1076.0 / 528.0     # proporción útil del lienzo (1200x820 menos márgenes)
    for def_mapa in CATALOGO:
        d = dict(def_mapa)
        d["titulo"] = limpiar_titulo(d.get("titulo", ""))
        d["subtitulo"] = limpiar_titulo(d.get("subtitulo", ""))
        d["descripcion"] = limpiar_titulo(d.get("descripcion", ""))
        if d.get("auto_encuadre", True) and d.get("lugares"):
            bbox = MM.bbox_de_lugares(d["lugares"], EXTRA_LUGARES, aspecto)
            if bbox:
                # nunca encoger por debajo de lo que pide el propio catálogo
                manual = def_mapa["bbox"]
                d["bbox"] = (min(manual[0], bbox[0]), min(manual[1], bbox[1]),
                             max(manual[2], bbox[2]), max(manual[3], bbox[3]))
        objeto = MM.Mapa(base, regiones, lugares, d, extras=EXTRA_LUGARES)
        svg, avisos = objeto.construir(), objeto.avisos
        # relación de lugares y rutas tal como quedaron dibujados (para la aplicación)
        lista_lugares, vistos = [], set()
        for referencia in d.get("lugares", []):
            lug = objeto.resolver_lugar(referencia)
            if not lug:
                continue
            clave = lug.get("id") or lug["nombre"]
            if clave in vistos:
                continue
            vistos.add(clave)
            lista_lugares.append({
                "id": lug.get("id"), "nombre": lug["nombre"], "original": lug.get("original", ""),
                "tipo": lug.get("tipo", ""), "lon": lug.get("lon"), "lat": lug.get("lat"),
                "refs": (lug.get("refs") or [])[:8],
            })
        lista_rutas = []
        for ruta in (d.get("rutas") or []):
            if isinstance(ruta, dict):
                lista_rutas.append({"nombre": ruta.get("nombre", ""), "color": ruta.get("color", "#7a2e12"),
                                    "nota": ruta.get("nota", ""), "puntos": len(ruta.get("puntos", []) or [])})
        fallos = [a for a in avisos if a.startswith("NO ENCONTRADO")]
        if fallos:
            problemas[d["id"]] = fallos
        if not revisar:
            destino = SALIDA_MAPAS / f"{d['id']}.svg"
            destino.write_text(svg, encoding="utf-8")
        catalogo.append({
            "id": d["id"],
            "titulo": d["titulo"],
            "subtitulo": d.get("subtitulo", ""),
            "categoria": d.get("categoria", "Mapas"),
            "descripcion": d.get("descripcion", ""),
            "archivo": f"mapas/{d['id']}.svg",
            "bbox": [round(v, 3) for v in d["bbox"]],
            "lugares": len(d.get("lugares", [])),
            "rutas": len(d.get("rutas", []) or []),
            "lista_lugares": lista_lugares,
            "lista_rutas": lista_rutas,
            "refs": d.get("refs", []),
            "notas": d.get("notas", []) or [],
        })
    # planos dibujados a mano (tabernáculo, templo, Jerusalén...)
    for def_plano in PLANOS:
        svg = def_plano["generar"]()
        if not revisar:
            (SALIDA_MAPAS / f"{def_plano['id']}.svg").write_text(svg, encoding="utf-8")
        catalogo.append({
            "id": def_plano["id"],
            "titulo": def_plano["titulo"],
            "subtitulo": def_plano["subtitulo"],
            "categoria": def_plano["categoria"],
            "descripcion": def_plano["descripcion"],
            "archivo": f"mapas/{def_plano['id']}.svg",
            "bbox": None,
            "lugares": def_plano.get("elementos", 0),
            "rutas": 0,
            "lista_lugares": [],
            "lista_rutas": [],
            "refs": def_plano.get("refs", []),
            "notas": def_plano.get("notas", []),
        })
    catalogo.sort(key=lambda m: (m["categoria"], m["titulo"]))
    if not revisar:
        with open(SALIDA_DATOS / "mapas.json", "w", encoding="utf-8") as f:
            json.dump(catalogo, f, ensure_ascii=False, separators=(",", ":"))
        print(f"  · {len(catalogo)} mapas generados en app/mapas/")
    if problemas:
        print("\nIdentificadores de lugar no encontrados:")
        for mid, fallos in problemas.items():
            print(f"  {mid}: {', '.join(f.split(': ')[1] for f in fallos)}")
    else:
        print("Todos los identificadores de lugar se resolvieron correctamente.")
    return problemas


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--revisar", action="store_true")
    args = ap.parse_args()
    generar_todo(revisar=args.revisar)
