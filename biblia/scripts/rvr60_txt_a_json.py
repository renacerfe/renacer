import os
import json
import re

# -----------------------------
# CONFIGURACIÓN
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_DIR = os.path.join(
    BASE_DIR, "original", "TextosBiblicos", "RVR60"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR, "procesada", "RVR60"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------
# MAPA DE LIBROS (abreviaturas)
# -----------------------------
BOOK_NAMES = {
    "Gn": "Génesis",
    "Ex": "Éxodo",
    "Lv": "Levítico",
    "Nm": "Números",
    "Dt": "Deuteronomio",
    "Jos": "Josué",
    "Jue": "Jueces",
    "Rt": "Rut",
    "1S": "1 Samuel",
    "2S": "2 Samuel",
    "1R": "1 Reyes",
    "2R": "2 Reyes",
    "1C": "1 Crónicas",
    "2C": "2 Crónicas",
    "Esd": "Esdras",
    "Neh": "Nehemías",
    "Est": "Ester",
    "Job": "Job",
    "Sal": "Salmos",
    "Pr": "Proverbios",
    "Ec": "Eclesiastés",
    "Cnt": "Cantares",
    "Is": "Isaías",
    "Jer": "Jeremías",
    "Lm": "Lamentaciones",
    "Ez": "Ezequiel",
    "Dan": "Daniel",
    "Os": "Oseas",
    "Jl": "Joel",
    "Am": "Amós",
    "Abd": "Abdías",
    "Jon": "Jonás",
    "Mi": "Miqueas",
    "Nah": "Nahúm",
    "Hab": "Habacuc",
    "Sof": "Sofonías",
    "Hag": "Hageo",
    "Zac": "Zacarías",
    "Mal": "Malaquías",
    "Mt": "Mateo",
    "Mr": "Marcos",
    "Lc": "Lucas",
    "Jn": "Juan",
    "Ac": "Hechos",
    "Rom": "Romanos",
    "1Cor": "1 Corintios",
    "2Cor": "2 Corintios",
    "Ga": "Gálatas",
    "Ef": "Efesios",
    "Fil": "Filipenses",
    "Col": "Colosenses",
    "1Ts": "1 Tesalonicenses",
    "2Ts": "2 Tesalonicenses",
    "1Tim": "1 Timoteo",
    "2Tim": "2 Timoteo",
    "Tit": "Tito",
    "Flm": "Filemón",
    "Heb": "Hebreos",
    "Jac": "Santiago",
    "1P": "1 Pedro",
    "2P": "2 Pedro",
    "1Jn": "1 Juan",
    "2Jn": "2 Juan",
    "3Jn": "3 Juan",
    "Jud": "Judas",
    "Rev": "Apocalipsis"
}

# -----------------------------
# PARSER
# -----------------------------
VERSE_PATTERN = re.compile(r"^(\d+):(\d+)\s+(.*)$")

for filename in sorted(os.listdir(INPUT_DIR)):
    if not filename.endswith(".txt"):
        continue

    parts = filename.replace("_RVR60.txt", "").split("_", 1)
    book_id = int(parts[0])
    abbrev = parts[1]

    book_name = BOOK_NAMES.get(abbrev, abbrev)

    chapters = {}

    input_path = os.path.join(INPUT_DIR, filename)

    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            match = VERSE_PATTERN.match(line)
            if not match:
                continue

            chapter, verse, text = match.groups()

            chapters.setdefault(chapter, {})
            chapters[chapter][verse] = text

    book_json = {
        "version": "RVR60",
        "language": "es",
        "book": {
            "id": book_id,
            "name": book_name,
            "abbrev": abbrev
        },
        "chapters": chapters
    }

    output_filename = f"{abbrev.lower()}.json"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    with open(output_path, "w", encoding="utf-8") as out:
        json.dump(book_json, out, ensure_ascii=False, indent=2)

    print(f"✔ Generado: {output_filename}")

print("\n✅ Conversión completa.")

