# -*- coding: utf-8 -*-
"""
libros_es.py — Nombres de los libros de la Biblia en español y conversión de
referencias bíblicas escritas en inglés (Easton, Smith, Nave, Torrey, OSIS)
al formato español: "Génesis 12:1-3", "1 Corintios 13:4-7", "Salmos 119:105".

Todas las referencias que muestra la aplicación pasan por este módulo, de modo
que el usuario siempre las ve en español, con los nombres acentuados y en el
orden habitual de las Biblias en castellano (RVR1960, Reina-Valera, NVI...).
"""

import re
import unicodedata

# ---------------------------------------------------------------------------
# Tabla canónica de los 66 libros
#   osis   : código estándar OSIS (usado por Bible-Geocoding-Data)
#   es     : nombre en español (uso normal)
#   abrev  : abreviatura española habitual
#   en     : nombre canónico en inglés
#   aliases: otras formas que aparecen en las fuentes antiguas (dominio público)
# ---------------------------------------------------------------------------
LIBROS = [
    # --- Antiguo Testamento -------------------------------------------------
    ("Gen", "Génesis", "Gn", "Genesis", ["Gen", "Ge", "Gen.", "Genesis"]),
    ("Exod", "Éxodo", "Éx", "Exodus", ["Exod", "Exo", "Ex", "Exodus"]),
    ("Lev", "Levítico", "Lv", "Leviticus", ["Lev", "Le", "Leviticus"]),
    ("Num", "Números", "Nm", "Numbers", ["Num", "Nu", "Numbers"]),
    ("Deut", "Deuteronomio", "Dt", "Deuteronomy", ["Deut", "De", "Deuteronomy"]),
    ("Josh", "Josué", "Jos", "Joshua", ["Josh", "Jos", "Joshua", "Josue"]),
    ("Judg", "Jueces", "Jue", "Judges", ["Judg", "Jdg", "Judges"]),
    ("Ruth", "Rut", "Rt", "Ruth", ["Ruth", "Rut", "Ru"]),
    ("1Sam", "1 Samuel", "1 S", "1 Samuel", ["1 Sam", "1Sam", "I Samuel", "1st Samuel", "First Samuel"]),
    ("2Sam", "2 Samuel", "2 S", "2 Samuel", ["2 Sam", "2Sam", "II Samuel", "2nd Samuel", "Second Samuel"]),
    ("1Kgs", "1 Reyes", "1 R", "1 Kings", ["1 Kings", "1Kgs", "I Kings", "1st Kings", "First Kings", "1 Ki"]),
    ("2Kgs", "2 Reyes", "2 R", "2 Kings", ["2 Kings", "2Kgs", "II Kings", "2nd Kings", "Second Kings", "2 Ki"]),
    ("1Chr", "1 Crónicas", "1 Cr", "1 Chronicles", ["1 Chron", "1 Chron.", "1 Chronicles", "1Chr", "I Chronicles", "1st Chronicles"]),
    ("2Chr", "2 Crónicas", "2 Cr", "2 Chronicles", ["2 Chron", "2 Chron.", "2 Chronicles", "2Chr", "II Chronicles", "2nd Chronicles"]),
    ("Ezra", "Esdras", "Esd", "Ezra", ["Ezra", "Esdras"]),
    ("Neh", "Nehemías", "Neh", "Nehemiah", ["Neh", "Nehemiah"]),
    ("Esth", "Ester", "Est", "Esther", ["Esth", "Esther", "Est"]),
    ("Job", "Job", "Job", "Job", ["Job"]),
    ("Ps", "Salmos", "Sal", "Psalms", ["Ps", "Psalm", "Psa", "Pss", "Psalms", "The Psalms"]),
    ("Prov", "Proverbios", "Pr", "Proverbs", ["Prov", "Pro", "Proverbs"]),
    ("Eccl", "Eclesiastés", "Ec", "Ecclesiastes", ["Eccl", "Ecc", "Ecclesiastes", "Eccles"]),
    ("Song", "Cantares", "Cnt", "Song of Solomon",
     ["Song", "Song of Songs", "Canticles", "Song of Solomon", "Cant", "SS"]),
    ("Isa", "Isaías", "Is", "Isaiah", ["Isa", "Is", "Isaiah"]),
    ("Jer", "Jeremías", "Jer", "Jeremiah", ["Jer", "Jeremiah"]),
    ("Lam", "Lamentaciones", "Lm", "Lamentations", ["Lam", "Lamentations", "Lament"]),
    ("Ezek", "Ezequiel", "Ez", "Ezekiel", ["Ezek", "Eze", "Ezekiel", "Ezechiel"]),
    ("Dan", "Daniel", "Dn", "Daniel", ["Dan", "Da", "Daniel"]),
    ("Hos", "Oseas", "Os", "Hosea", ["Hos", "Hosea", "Osee"]),
    ("Joel", "Joel", "Jl", "Joel", ["Joel"]),
    ("Amos", "Amós", "Am", "Amos", ["Amos", "Am"]),
    ("Obad", "Obadías", "Abd", "Obadiah", ["Obad", "Obadiah", "Abdias"]),
    ("Jonah", "Jonás", "Jon", "Jonah", ["Jonah", "Jonas", "Jon"]),
    ("Mic", "Miqueas", "Miq", "Micah", ["Mic", "Micah", "Micheas"]),
    ("Nah", "Nahúm", "Nah", "Nahum", ["Nah", "Nahum"]),
    ("Hab", "Habacuc", "Hab", "Habakkuk", ["Hab", "Habakkuk", "Habacuc"]),
    ("Zeph", "Sofonías", "Sof", "Zephaniah", ["Zeph", "Zep", "Zephaniah", "Sophonias"]),
    ("Hag", "Hageo", "Hag", "Haggai", ["Hag", "Haggai", "Aggeus"]),
    ("Zech", "Zacarías", "Zac", "Zechariah", ["Zech", "Zec", "Zechariah", "Zacharias"]),
    ("Mal", "Malaquías", "Mal", "Malachi", ["Mal", "Malachi", "Malachias"]),
    # --- Nuevo Testamento ---------------------------------------------------
    ("Matt", "Mateo", "Mt", "Matthew", ["Matt", "Mat", "Matthew"]),
    ("Mark", "Marcos", "Mr", "Mark", ["Mark", "Mar", "Marc"]),
    ("Luke", "Lucas", "Lc", "Luke", ["Luke", "Luk"]),
    ("John", "Juan", "Jn", "John", ["John", "Joh", "Jn"]),
    ("Acts", "Hechos", "Hch", "Acts",
     ["Acts", "Act", "Acts of the Apostles", "The Acts"]),
    ("Rom", "Romanos", "Ro", "Romans", ["Rom", "Ro", "Romans"]),
    ("1Cor", "1 Corintios", "1 Co", "1 Corinthians", ["1 Cor", "1Cor", "I Corinthians", "1st Corinthians", "First Corinthians"]),
    ("2Cor", "2 Corintios", "2 Co", "2 Corinthians", ["2 Cor", "2Cor", "II Corinthians", "2nd Corinthians", "Second Corinthians"]),
    ("Gal", "Gálatas", "Gá", "Galatians", ["Gal", "Ga", "Galatians"]),
    ("Eph", "Efesios", "Ef", "Ephesians", ["Eph", "Ephesians"]),
    ("Phil", "Filipenses", "Fil", "Philippians", ["Phil", "Php", "Philippians"]),
    ("Col", "Colosenses", "Col", "Colossians", ["Col", "Colossians"]),
    ("1Thess", "1 Tesalonicenses", "1 Ts", "1 Thessalonians",
     ["1 Thess", "1Thess", "1 Thes", "I Thessalonians", "1st Thessalonians"]),
    ("2Thess", "2 Tesalonicenses", "2 Ts", "2 Thessalonians",
     ["2 Thess", "2Thess", "2 Thes", "II Thessalonians", "2nd Thessalonians"]),
    ("1Tim", "1 Timoteo", "1 Ti", "1 Timothy", ["1 Tim", "1Tim", "I Timothy", "1st Timothy"]),
    ("2Tim", "2 Timoteo", "2 Ti", "2 Timothy", ["2 Tim", "2Tim", "II Timothy", "2nd Timothy"]),
    ("Titus", "Tito", "Tit", "Titus", ["Titus", "Tit"]),
    ("Phlm", "Filemón", "Flm", "Philemon", ["Philem", "Philemon", "Phlm", "Flm"]),
    ("Heb", "Hebreos", "He", "Hebrews", ["Heb", "Hebrews", "He"]),
    ("Jas", "Santiago", "Stg", "James", ["Jas", "James", "Jam"]),
    ("1Pet", "1 Pedro", "1 P", "1 Peter", ["1 Pet", "1Pet", "I Peter", "1st Peter"]),
    ("2Pet", "2 Pedro", "2 P", "2 Peter", ["2 Pet", "2Pet", "II Peter", "2nd Peter"]),
    ("1John", "1 Juan", "1 Jn", "1 John", ["1 John", "1John", "I John", "1st John"]),
    ("2John", "2 Juan", "2 Jn", "2 John", ["2 John", "2John", "II John", "2nd John"]),
    ("3John", "3 Juan", "3 Jn", "3 John", ["3 John", "3John", "III John", "3rd John"]),
    ("Jude", "Judas", "Jud", "Jude", ["Jude", "Jud"]),
    ("Rev", "Apocalipsis", "Ap", "Revelation",
     ["Rev", "Revelation", "Revelations", "The Revelation", "Apocalypse", "Rev."]),
]

OSIS_A_ES = {b[0]: b[1] for b in LIBROS}
ES_A_OSIS = {b[1]: b[0] for b in LIBROS}
ABREV_ES = {b[1]: b[2] for b in LIBROS}
TESTAMENTO = {}
for _i, _b in enumerate(LIBROS):
    TESTAMENTO[_b[1]] = "Antiguo Testamento" if _i < 39 else "Nuevo Testamento"

ORDEN = {b[1]: i + 1 for i, b in enumerate(LIBROS)}


def _sin_acentos(texto):
    return "".join(c for c in unicodedata.normalize("NFKD", texto)
                   if not unicodedata.combining(c))


# Diccionario de alias -> nombre español. Se generan variantes con y sin punto,
# con y sin acento, y en minúsculas, para tolerar las formas de las fuentes.
_ALIAS = {}


def _registrar(clave, destino):
    if not clave:
        return
    k = clave.strip().rstrip(".").lower()
    _ALIAS[k] = destino
    _ALIAS[_sin_acentos(k)] = destino
    _ALIAS[_sin_acentos(k).replace(" ", "")] = destino
    _ALIAS[_sin_acentos(k).replace(".", "")] = destino


for _osis, _es, _ab, _en, _aliases in LIBROS:
    for _forma in [_es, _ab, _en, _osis] + list(_aliases):
        _registrar(_forma, _es)
    # "I Samuel", "II Kings" y demás numerales romanos, y abreviaturas
    # inglesas cortas del tipo "1 Chr", "2 Kgs" o "1 Cor" que usan las
    # fuentes antiguas (Easton, Smith, Nave, Torrey).
    if _es[0].isdigit():
        _resto = _es[1:].strip()
        for _romano, _num in (("I", "1"), ("II", "2"), ("III", "3")):
            if _es.startswith(_num):
                _registrar(f"{_romano} {_resto}", _es)
                _registrar(f"{_romano}{_resto}", _es)
        _en_sin_num = _en.split(" ", 1)[1] if " " in _en else _en
        for _corto in {_en_sin_num[:3], _en_sin_num[:4], _en_sin_num[:5]}:
            _registrar(f"{_es[0]} {_corto}", _es)
            _registrar(f"{_es[0]}{_corto}", _es)

# Nombres alternativos muy frecuentes en las fuentes antiguas en inglés
_ALIAS.update({
    # abreviaturas cortas inglesas de las cartas
    "1 th": "1 Tesalonicenses", "2 th": "2 Tesalonicenses",
    "1 thes": "1 Tesalonicenses", "2 thes": "2 Tesalonicenses",
    "1 thess": "1 Tesalonicenses", "2 thess": "2 Tesalonicenses",
    "1 tes": "1 Tesalonicenses", "2 tes": "2 Tesalonicenses",
    "1 tess": "1 Tesalonicenses", "2 tess": "2 Tesalonicenses",
    # libros deuterocanónicos citados por los diccionarios históricos
    "tob": "Tobit", "tobit": "Tobit",
    "jdt": "Judit", "judith": "Judit", "judth": "Judit",
    "sir": "Eclesiástico", "sirach": "Eclesiástico", "ecclus": "Eclesiástico",
    "wis": "Sabiduría", "wisd": "Sabiduría", "wisd of sol": "Sabiduría",
    "1esd": "1 Esdras", "2esd": "2 Esdras", "4esd": "2 Esdras",
    "1 macc": "1 Macabeos", "2 macc": "2 Macabeos", "3 macc": "3 Macabeos",
    "4 macc": "4 Macabeos", "1mac": "1 Macabeos", "2mac": "2 Macabeos",
    "3mac": "3 Macabeos", "bar": "Baruc", "baruch": "Baruc",
    "ep jer": "Epístola de Jeremías", "pr azar": "Oración de Azarías",
    "sus": "Susana", "bel": "Bel y el dragón", "ps 151": "Salmos 151",
    "canticle": "Cantares",
    "song of solomon": "Cantares",
    "the song of solomon": "Cantares",
    "acts of the apostles": "Hechos",
    "the acts": "Hechos",
    "revelation of john": "Apocalipsis",
    "the apocalypse": "Apocalipsis",
    "the gospel according to matthew": "Mateo",
    "the gospel according to mark": "Marcos",
    "the gospel according to luke": "Lucas",
    "the gospel according to john": "Juan",
    "1st book of kings": "1 Reyes",
    "2nd book of kings": "2 Reyes",
    "1st book of samuel": "1 Samuel",
    "2nd book of samuel": "2 Samuel",
    "first book of kings": "1 Reyes",
    "second book of kings": "2 Reyes",
    "first book of samuel": "1 Samuel",
    "second book of samuel": "2 Samuel",
    "pentateuch": "Génesis",
    "sirach": "Eclesiástico",
    "ecclesiasticus": "Eclesiástico",
    "wisdom": "Sabiduría",
    "wisdom of solomon": "Sabiduría",
    "1 maccabees": "1 Macabeos",
    "2 maccabees": "2 Macabeos",
    "1 macc": "1 Macabeos",
    "2 macc": "2 Macabeos",
    "tobit": "Tobit",
    "judith": "Judit",
    "baruch": "Baruc",
})

# Libros deuterocanónicos / no protestantes: se mantienen por fidelidad a las
# citas de los diccionarios históricos (Apócrifos), marcados como tales.
DEUTEROCANONICOS = {"1 Macabeos", "2 Macabeos", "Tobit", "Judit", "Baruc",
                    "Sabiduría", "Eclesiástico"}

def _extraer_libro(texto):
    """
    Busca al principio del texto el nombre de un libro usando la coincidencia
    más larga posible (de 5 palabras a 1). Devuelve (nombre_es, resto) o
    (None, texto) si no reconoce ninguno.
    """
    palabras = texto.split()
    for n in range(min(5, len(palabras)), 0, -1):
        candidato = " ".join(palabras[:n])
        candidato = re.sub(r"[,:]$", "", candidato)
        libro = libro_a_espor_nombre(candidato)
        if libro:
            resto = " ".join(palabras[n:]).strip()
            return libro, resto
    # Casos con numeral antepuesto unido: "1Kings 3:1" -> "1 Kings 3:1"
    m = re.match(r"^([1-3])([A-Za-zÁÉÍÓÚÜÑáéíóúüñ].*)$", texto)
    if m:
        normalizado = f"{m.group(1)} {m.group(2)}"
        if normalizado != texto:
            libro, resto = _extraer_libro(normalizado)
            if libro:
                return libro, resto
    return None, texto


def libro_a_espor_nombre(nombre):
    """Devuelve el nombre español de un libro a partir de cualquier forma."""
    if not nombre:
        return None
    n = nombre.strip().rstrip(".").lower()
    for forma in (n, _sin_acentos(n), n.replace(".", " ").replace("  ", " ").strip()):
        if forma in _ALIAS:
            return _ALIAS[forma]
    # quitar puntos de abreviaturas: "1 Ki." -> "1 ki"
    limpio = re.sub(r"\.", "", n).replace("  ", " ").strip()
    if limpio in _ALIAS:
        return _ALIAS[limpio]
    limpio2 = _sin_acentos(limpio)
    if limpio2 in _ALIAS:
        return _ALIAS[limpio2]
    return None


def _normaliza_numeros(parte):
    """'6:16-20' -> '6:16-20' | ' comma separados ya vienen resueltos fuera."""
    parte = parte.strip()
    parte = parte.replace("–", "-").replace("—", "-")
    parte = re.sub(r"\s*-\s*", "-", parte)
    parte = re.sub(r"\s*,\s*", ",", parte)
    parte = re.sub(r"\s*;\s*", "; ", parte)
    return parte


def referencia_a_es(referencia):
    """
    Convierte una referencia en inglés al formato español.
    'Rev. 1:8, 11'            -> 'Apocalipsis 1:8,11'
    'Genesis 8:4'             -> 'Génesis 8:4'
    '1 Chronicles 6:2,3'      -> '1 Crónicas 6:2,3'
    'Acts of the Apostles 2'  -> 'Hechos 2'
    Devuelve None si no se reconoce.
    """
    if not referencia:
        return None
    ref = re.sub(r"\s+", " ", str(referencia).strip())
    # OSIS: "2Kgs.5.12" o "2Kgs.5"
    m = re.match(r"^([1-3]?[A-Za-z]{2,4})\.(\d+)(?:\.(\d+))?(?:\.(\d+))?$", ref)
    if m and m.group(1) in OSIS_A_ES:
        cap, ver, ver2 = m.group(2), m.group(3), m.group(4)
        if ver2:
            return f"{OSIS_A_ES[m.group(1)]} {cap}:{ver}-{int(ver2) + 1}" if ver2 == str(int(ver2)) else f"{OSIS_A_ES[m.group(1)]} {cap}:{ver}"
        if ver:
            return f"{OSIS_A_ES[m.group(1)]} {cap}:{ver}"
        return f"{OSIS_A_ES[m.group(1)]} {cap}"

    # Varios pasajes separados por punto y coma: "John 3:16; 1 John 4:8"
    partes = [p.strip() for p in re.split(r"[;]", ref) if p.strip()]
    salida = []
    libro_actual = None
    for parte in partes:
        libro, resto = _extraer_libro(parte)
        if libro and resto and re.match(r"^\d", resto):
            libro_actual = libro
            salida.append(f"{libro} {_normaliza_numeros(resto)}")
            continue
        if libro and not resto:
            libro_actual = libro
            salida.append(libro)
            continue
        # Sin nombre de libro: continuar con el último citado ("Rev 1:8; 2:3")
        m2 = re.match(r"^(\d+(?::.*)?)$", parte)
        if m2 and libro_actual:
            salida.append(f"{libro_actual} {_normaliza_numeros(m2.group(1))}")
            continue
        # Referencia suelta con el libro al final o dentro del texto
        m3 = re.search(r"([1-3]?\s?[A-Za-zÁÉÍÓÚÜÑáéíóúüñ][A-Za-zÁÉÍÓÚÜÑáéíóúüñ.]*(?:\s+of\s+[A-Za-z]+)?)\.?\s+(\d+(?::[0-9,\-–\s]+)?)$", parte)
        if m3 and libro_a_espor_nombre(m3.group(1)):
            salida.append(f"{libro_a_espor_nombre(m3.group(1))} "
                          f"{_normaliza_numeros(m3.group(2))}")
            continue
        if libro_actual:
            limpieza = re.sub(r"[^0-9:,\-–\s]", "", parte).strip()
            if limpieza:
                salida.append(f"{libro_actual} {_normaliza_numeros(limpieza)}")
    if not salida:
        return None
    return "; ".join(salida)


def abreviatura(nombre_es):
    return ABREV_ES.get(nombre_es, nombre_es[:3])


def osis(partes):
    """('Juan', 3, 16) -> 'John.3.16'"""
    return f"{ES_A_OSIS.get(partes[0], partes[0])}.{partes[1]}.{partes[2]}"


if __name__ == "__main__":  # pequeña prueba de humo
    pruebas = ["Rev. 1:8, 11", "Genesis 8:4", "1 Chronicles 6:2,3",
               "Acts of the Apostles 2:38", "Psalms 119:105",
               "Song of Solomon 2:1", "2Kgs.5.12", "1 Kings 17:1; 2 Kings 2:1",
               "Exodus 6:23,25", "Isaiah 41:4", "Mark 1:2-3",
               "1 Corinthians 13:4-7", "Eph. 6:10-18"]
    for p in pruebas:
        print(f"{p:32s} -> {referencia_a_es(p)}")
