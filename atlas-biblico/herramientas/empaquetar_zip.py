#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
empaquetar_zip.py — Empaqueta toda la aplicación en un solo archivo ZIP que el
usuario puede descargar y descomprimir en su equipo.

El paquete se guarda en  descargas/atlas-biblico.zip  y conserva los permisos de
ejecución del instalador. El propio archivo de salida y las carpetas de trabajo
(__pycache__, descargas) quedan siempre fuera del paquete.

Uso:
    python3 herramientas/empaquetar_zip.py            # crea el paquete
    python3 herramientas/empaquetar_zip.py --salida /ruta/otro.zip
"""

import argparse
import os
import sys
import zipfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
APP = AQUI.parent
SALIDA = APP / "descargas" / "atlas-biblico.zip"

EXCLUIR_CARPETAS = {"__pycache__", "descargas", ".git", "node_modules"}
EXCLUIR_SUFIJOS = {".pyc", ".pyo", ".zip", ".xz", ".tar", ".gz"}


def reunir(raiz):
    """Lista los archivos que forman el paquete, bien ordenados."""
    archivos = []
    for carpeta, subcarpetas, ficheros in os.walk(raiz):
        subcarpetas[:] = sorted(d for d in subcarpetas if d not in EXCLUIR_CARPETAS)
        for nombre in sorted(ficheros):
            ruta = Path(carpeta) / nombre
            if ruta.suffix in EXCLUIR_SUFIJOS:
                continue
            archivos.append(ruta)
    return archivos


def es_ejecutable(ruta):
    """Qué archivos deben llegar al equipo del usuario con permiso de ejecución."""
    if ruta.suffix == ".sh" or ruta.name in ("INSTALAR.desktop", "compositor.py"):
        return True
    return ruta.suffix == ".py" and ruta.parent.name == "herramientas"


def empaquetar(destino=SALIDA):
    archivos = reunir(APP)
    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as paquete:
        for ruta in archivos:
            relativa = Path("atlas-biblico") / ruta.relative_to(APP)
            info = zipfile.ZipInfo.from_file(ruta, arcname=str(relativa))
            if es_ejecutable(ruta):
                info.external_attr = (0o755 << 16) | 0o100000
            with open(ruta, "rb") as f:
                paquete.writestr(info, f.read(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
    tam = destino.stat().st_size
    print(f"  · {destino}  ({len(archivos)} archivos, {tam / 1024 / 1024:.1f} MB)")
    return destino


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Empaqueta la aplicación en un ZIP")
    ap.add_argument("--salida", default=str(SALIDA))
    args = ap.parse_args()
    print("· Empaquetando la aplicación ...")
    empaquetar(args.salida)
    sys.exit(0)
