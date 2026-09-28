#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
construir_base.py — Prepara la capa base de los mapas (costas, lagos, ríos y
fronteras modernas) a partir de Natural Earth (dominio público) y limpia las
geometrías de las regiones bíblicas (Bible-Geocoding-Data, CC BY 4.0).

El resultado son dos archivos pequeños que la aplicación usa para dibujar los
mapas en SVG: app/datos/base.json y app/datos/regiones.json.

Este script se ejecuta solo al construir la aplicación (necesita la librería
shapely). La aplicación instalada no necesita ninguna dependencia externa.
"""

import json
import math
import sys
from pathlib import Path

from shapely.geometry import shape, box, LineString, MultiLineString, Polygon, MultiPolygon, mapping
from shapely.ops import unary_union

AQUI = Path(__file__).resolve().parent
APP = AQUI.parent
FUENTES = Path(sys.argv[1] if len(sys.argv) > 1 else "/home/user/_fuentes")
SALIDA = APP / "app" / "datos"

# Ventana geográfica de trabajo: de la Península Ibérica a Persia y del Sahel a
# Escandinavia. Cubre todos los mapas bíblicos, desde Roma hasta Babilonia.
BBOX = (-11.0, 18.0, 68.0, 47.0)


def cargar(ruta):
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


def recortar_simplificar(geometria, tolerancia):
    try:
        g = geometria.intersection(box(*BBOX))
    except Exception:
        return None
    if g.is_empty:
        return None
    g = g.simplify(tolerancia, preserve_topology=True)
    if g.is_empty:
        return None
    return g


def anillos_de(geom):
    """Devuelve una lista de anillos exteriores [ [ [lon,lat], ... ], ... ]."""
    salida = []
    if geom is None or geom.is_empty:
        return salida

    def anillo_exterior(poly):
        xs, ys = poly.exterior.xy
        puntos = [[round(x, 4), round(y, 4)] for x, y in zip(xs, ys)]
        if len(puntos) >= 4:
            salida.append(puntos)

    if isinstance(geom, Polygon):
        anillo_exterior(geom)
    elif isinstance(geom, MultiPolygon):
        for poly in geom.geoms:
            anillo_exterior(poly)
    elif isinstance(geom, (LineString, MultiLineString)):
        salida.append([[round(x, 4), round(y, 4)] for x, y in geom.coords])
    return salida


def lineas_de(geom):
    salida = []
    if geom is None or geom.is_empty:
        return salida
    if isinstance(geom, LineString):
        salida.append([[round(x, 4), round(y, 4)] for x, y in geom.coords])
    elif isinstance(geom, MultiLineString):
        for linea in geom.geoms:
            salida.append([[round(x, 4), round(y, 4)] for x, y in linea.coords])
    elif isinstance(geom, (Polygon, MultiPolygon)):
        salida += anillos_de(geom)
    return salida


def construir_base():
    print("· Capa base (Natural Earth, dominio público) ...")
    ne = FUENTES / "naturalearth"
    base = {"tierra": [], "lagos": [], "rios": [], "fronteras": []}

    tierra = cargar(ne / "ne_10m_land.geojson")
    for feat in tierra["features"]:
        g = recortar_simplificar(shape(feat["geometry"]), 0.012)
        base["tierra"] += anillos_de(g)
    print(f"  · tierra: {len(base['tierra'])} polígonos")

    lagos = cargar(ne / "ne_50m_lakes.geojson")
    for feat in lagos["features"]:
        g = recortar_simplificar(shape(feat["geometry"]), 0.02)
        base["lagos"] += anillos_de(g)
    print(f"  · lagos: {len(base['lagos'])}")

    rios = cargar(ne / "ne_50m_rivers_lake_centerlines.geojson")
    for feat in rios["features"]:
        g = recortar_simplificar(shape(feat["geometry"]), 0.02)
        base["rios"] += lineas_de(g)
    print(f"  · ríos: {len(base['rios'])}")

    fronteras = cargar(ne / "ne_50m_admin_0_boundary_lines_land.geojson")
    for feat in fronteras["features"]:
        g = recortar_simplificar(shape(feat["geometry"]), 0.02)
        base["fronteras"] += lineas_de(g)
    print(f"  · fronteras modernas: {len(base['fronteras'])}")

    salida = SALIDA / "base.json"
    salida.parent.mkdir(parents=True, exist_ok=True)
    with open(salida, "w", encoding="utf-8") as f:
        json.dump(base, f, ensure_ascii=False, separators=(",", ":"))
    print(f"  · {salida.relative_to(APP)}  ({salida.stat().st_size / 1024:.0f} KB)")


def limpiar_regiones():
    print("· Regiones bíblicas (unión de anillos y simplificación) ...")
    crudas = SALIDA / "regiones_crudas.json"
    if not crudas.exists():
        print("  (no hay regiones_crudas.json; se omite)")
        return
    datos = cargar(crudas)
    salida = []
    for region in datos:
        poligonos = []
        for anillo in region["anillos"]:
            try:
                poly = Polygon(anillo)
                if not poly.is_valid:
                    poly = poly.buffer(0)
                if poly.is_valid and not poly.is_empty:
                    poligonos.append(poly)
            except Exception:
                continue
        if not poligonos:
            continue
        union = unary_union(poligonos)
        union = union.buffer(0)
        union = union.simplify(0.012, preserve_topology=True)
        if union.is_empty:
            continue
        centro = union.representative_point()
        limites = union.bounds
        salida.append({
            "id": region["id"],
            "nombre": region["nombre"],
            "anillos": anillos_de(union),
            "centro": [round(centro.x, 3), round(centro.y, 3)],
            "bbox": [round(v, 3) for v in limites],
        })
    salida.sort(key=lambda r: -(r["bbox"][2] - r["bbox"][0]) * (r["bbox"][3] - r["bbox"][1]))
    destino = SALIDA / "regiones.json"
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False, separators=(",", ":"))
    print(f"  · {len(salida)} regiones -> {destino.relative_to(APP)} "
          f"({destino.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    construir_base()
    limpiar_regiones()
