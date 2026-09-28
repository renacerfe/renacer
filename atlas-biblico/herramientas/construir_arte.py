#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
construir_arte.py — Extrae la galería de arte bíblico de dominio público
(los grabados de Gustave Doré para La Grande Bible de Tours, 1866) a partir del
archivo comprimido descargado, reduce las imágenes a un tamaño adecuado y crea
app/datos/arte.json con los títulos y las referencias ya en español.

Uso:
    python3 construir_arte.py [--archivo /ruta/dore.tar.gz] [--ancho 620] [--calidad 72]

Las láminas se guardan a 620 píxeles de ancho (unos 26 MB en total), tamaño
suficiente para la galería y para verlas a pantalla completa sin llenar el disco.
"""

import argparse
import json
import re
import sys
import tarfile
import unicodedata
from io import BytesIO
from pathlib import Path

AQUI = Path(__file__).resolve().parent
APP = AQUI.parent
sys.path.insert(0, str(AQUI))
from dore import GRABADOS, LEYENDA      # noqa: E402

try:
    from PIL import Image
except ImportError:                     # pragma: no cover
    print("Se necesita Pillow para reducir las imágenes: pip install Pillow", file=sys.stderr)
    raise

SALIDA_IMG = APP / "app" / "arte"
SALIDA_JSON = APP / "app" / "datos" / "arte.json"

# Grabadores citados por la fuente original para algunos grabados
GRABADORES = {
    "Pisan", "Pannemaker", "Laplante", "Best", "Jonnard", "Méaulle", "Rouget",
    "Baude", "Dumont", "Sargent", "Berveiller", "Hurel", "Barbant",
}


def sin_acentos(t):
    return "".join(c for c in unicodedata.normalize("NFKD", t)
                   if not unicodedata.combining(c))


def nombre_archivo(titulo, numero):
    base = sin_acentos(titulo.lower())
    base = re.sub(r"[^a-z0-9]+", "-", base).strip("-")[:60]
    return f"dore-{numero:03d}-{base}.jpg"


def construir(archivo, ancho=620, calidad=72):
    archivo = Path(archivo)
    if not archivo.exists():
        print(f"No se encuentra el archivo de origen: {archivo}", file=sys.stderr)
        return 1
    SALIDA_IMG.mkdir(parents=True, exist_ok=True)
    entradas = []
    print(f"· Extrayendo {len(GRABADOS)} grabados de {archivo.name} ...")
    with tarfile.open(archivo, "r:gz") as tar:
        # el archivo trae dos copias de cada lámina: el original en alta
        # resolución y una reducida en web/; se prefiere siempre la mayor
        miembros = {}
        for m in tar.getmembers():
            if not m.isfile() or not m.name.lower().endswith(".jpg"):
                continue
            base = Path(m.name).name
            num = re.search(r"-(\d{3})-", base)
            if not num:
                continue
            numero = int(num.group(1))
            anterior = miembros.get(numero)
            if anterior is None or m.size > anterior.size:
                miembros[numero] = m
        extraidos = 0
        for numero, titulo, refs in GRABADOS:
            m = miembros.get(numero)
            if m is None:
                print(f"    (falta el grabado {numero})")
                continue
            datos = tar.extractfile(m).read()
            try:
                im = Image.open(BytesIO(datos))
                im = im.convert("RGB")
                factor = ancho / im.width
                if factor < 1:
                    im = im.resize((ancho, max(1, int(im.height * factor))), Image.LANCZOS)
                destino = SALIDA_IMG / nombre_archivo(titulo, numero)
                im.save(destino, "JPEG", quality=calidad, optimize=True, progressive=True)
            except Exception as exc:                    # imagen ilegible: se omite
                print(f"    (error con el grabado {numero}: {exc})")
                continue
            extraidos += 1
            entradas.append({
                "id": f"dore-{numero:03d}",
                "numero": numero,
                "titulo": titulo,
                "refs": [refs] if isinstance(refs, str) else list(refs),
                "archivo": f"arte/{destino.name}",
                "autor": "Gustave Doré",
                "obra": LEYENDA["obra"],
                "fecha": LEYENDA["fecha"],
                "licencia": LEYENDA["licencia"],
                "archivo_original": Path(m.name).name,
            })
    catalogo = {"leyenda": LEYENDA, "obras": entradas, "total": len(entradas)}
    SALIDA_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(SALIDA_JSON, "w", encoding="utf-8") as f:
        json.dump(catalogo, f, ensure_ascii=False, separators=(",", ":"))
    peso = sum((SALIDA_IMG / Path(e["archivo"]).name).stat().st_size for e in entradas)
    print(f"  · {extraidos} ilustraciones ({peso / 1024 / 1024:.1f} MB) en {SALIDA_IMG}")
    print(f"  · {SALIDA_JSON.relative_to(APP)}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--archivo", default="/home/user/_fuentes/dore.tar.gz")
    ap.add_argument("--ancho", type=int, default=620)
    ap.add_argument("--calidad", type=int, default=72)
    args = ap.parse_args()
    sys.exit(construir(args.archivo, args.ancho, args.calidad))
