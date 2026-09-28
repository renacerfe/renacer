#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
construir_indices.py — Crea los índices ligeros que usa el buscador de la
aplicación (títulos de lugares, temas y voces de diccionario) y el texto
completo de la Biblia en formato compacto para las búsquedas rápidas.

Se ejecuta después de construir_datos.py y construir_mapas.py.
"""

import json
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
APP = AQUI.parent
sys.path.insert(0, str(AQUI))
import libros_es as LE            # noqa: E402

DATOS = APP / "app" / "datos"


def leer(ruta, defecto=None):
    try:
        with open(ruta, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return defecto


def escribir(ruta, datos):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, separators=(",", ":"))
    print(f"  · {ruta.relative_to(APP)}  ({ruta.stat().st_size / 1024:.0f} KB)")


def indice_lugares():
    lugares = leer(DATOS / "lugares.json", [])
    ligero = [{"id": l["id"], "n": l["nombre"], "o": l["original"], "t": l["tipo"],
               "lon": l["lon"], "lat": l["lat"], "r": l["total_refs"], "a": l["adaptado"]}
              for l in lugares]
    escribir(DATOS / "lugares_indice.json", ligero)


def indice_temas():
    temas = leer(DATOS / "temas.json", [])
    indice = [{"id": t["id"], "t": t["titulo"], "to": t["titulo_original"],
               "r": t["total_refs"], "tc": t["traduccion_completa"]} for t in temas]
    escribir(DATOS / "temas_indice.json", indice)


def indice_diccionarios():
    salida = {}
    for fichero in sorted((DATOS / "diccionarios").glob("*.json")):
        codigo = fichero.stem
        entradas = leer(fichero, [])
        salida[codigo] = [[e["id"], e["t"], e.get("tes")] for e in entradas]
    escribir(DATOS / "diccionarios_indice.json", salida)


def texto_biblia():
    """Une la Biblia en un solo archivo compacto para las búsquedas."""
    carpeta = DATOS / "biblia"
    libros = leer(carpeta / "libros.json", [])
    if not libros:
        print("  (no hay Biblia construida; se omite la búsqueda bíblica)")
        return
    filas = []          # [osis, capítulo, versículo, texto]
    for libro in libros:
        datos = leer(carpeta / f"{libro['osis']}.json", {})
        for cap in sorted(datos, key=lambda c: int(c)):
            versiculos = datos[cap]
            for ver in sorted(versiculos, key=lambda v: int(v)):
                filas.append([libro["osis"], int(cap), int(ver), versiculos[ver]])
    escribir(DATOS / "biblia_busqueda.json", filas)
    print(f"    {len(filas)} versículos preparados para la búsqueda")


def indice_general():
    """Índice con las cifras de la aplicación para las pantallas de inicio."""
    indice = leer(DATOS / "indice.json", {})
    indice["mapas"] = len(leer(DATOS / "mapas.json", []))
    arte = leer(DATOS / "arte.json", {}) or {}
    indice["obras_arte"] = arte.get("total", 0)
    escribir(DATOS / "indice.json", indice)
    with open(DATOS / "indice.json", "w", encoding="utf-8") as f:
        json.dump(indice, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    print("· Índices ligeros ...")
    indice_lugares()
    indice_temas()
    indice_diccionarios()
    texto_biblia()
    indice_general()
