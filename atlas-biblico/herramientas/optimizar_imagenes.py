#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
optimizar_imagenes.py — Prepara las imágenes de la interfaz.

Las ilustraciones originales (grandes, generadas para la portada y las
secciones) viven en contenido/imagenes_fuente/. Este programa crea a partir de
ellas versiones ligeras en app/imagenes/, que son las que carga la aplicación:

    portada.png         ->  portada.jpg          (1400 px de ancho)
    seccion-*.png       ->  seccion-*.jpg        (500 x 500)
    icono.png           ->  icono.png (512), icono-192.png, icono-96.png,
                            icono.ico (Windows)

Uso:
    python3 optimizar_imagenes.py
"""

import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:                     # pragma: no cover
    print("Se necesita Pillow: pip install Pillow", file=sys.stderr)
    raise SystemExit(1)

AQUI = Path(__file__).resolve().parent
APP = AQUI.parent
ORIGEN = APP / "contenido" / "imagenes_fuente"
DESTINO = APP / "app" / "imagenes"


def buscar(nombre):
    """Devuelve el archivo fuente, en PNG o JPEG."""
    for extension in (".png", ".jpg", ".jpeg", ".webp"):
        ruta = ORIGEN / (nombre + extension)
        if ruta.exists():
            return ruta
    return ORIGEN / (nombre + ".png")


def reducir(origen, destino, tamano, formato="JPEG", calidad=82):
    if not origen.exists():
        print(f"  (falta {origen.name}, se omite)")
        return None
    im = Image.open(origen)
    im = im.convert("RGB") if formato == "JPEG" else im.convert("RGBA")
    if isinstance(tamano, int):
        tamano = (tamano, max(1, round(tamano * im.height / im.width))) if im.width >= im.height \
            else (max(1, round(tamano * im.width / im.height)), tamano)
    copia = im.copy()
    copia.thumbnail(tamano, Image.LANCZOS)
    destino.parent.mkdir(parents=True, exist_ok=True)
    if formato == "JPEG":
        copia.save(destino, "JPEG", quality=calidad, optimize=True, progressive=True)
    else:
        copia.save(destino, "PNG", optimize=True)
    print(f"  · {destino.name}  {copia.width}x{copia.height}  "
          f"({destino.stat().st_size / 1024:.0f} KB)")
    return copia


def main():
    print("· Imágenes de la interfaz ...")
    reducir(buscar("portada"), DESTINO / "portada.jpg", 1400)
    for nombre in ("seccion-mapas", "seccion-biblioteca", "seccion-biblia", "seccion-arte"):
        reducir(buscar(nombre), DESTINO / f"{nombre}.jpg", (500, 500))
    icono = reducir(buscar("icono"), DESTINO / "icono.png", (512, 512), formato="PNG")
    reducir(buscar("icono"), DESTINO / "icono-192.png", (192, 192), formato="PNG")
    reducir(buscar("icono"), DESTINO / "icono-96.png", (96, 96), formato="PNG")
    if icono is not None:
        icono.save(DESTINO / "icono.ico", sizes=[(48, 48), (64, 64), (128, 128), (256, 256)])
        print(f"  · icono.ico  ({(DESTINO / 'icono.ico').stat().st_size / 1024:.0f} KB)")
    peso = sum(f.stat().st_size for f in DESTINO.glob("*"))
    print(f"  · {len(list(DESTINO.glob('*')))} archivos, {peso / 1024 / 1024:.1f} MB en app/imagenes/")


if __name__ == "__main__":
    main()
