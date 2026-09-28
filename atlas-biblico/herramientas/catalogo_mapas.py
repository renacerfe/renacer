# -*- coding: utf-8 -*-
"""
catalogo_mapas.py — Catálogo de los mapas bíblicos que genera la aplicación.

Cada entrada define: título, referencia bíblica, categoría, descripción
redactada en español, la ventana geográfica (bbox), los lugares que se
etiquetan (con los identificadores de la base de datos de lugares conocidos),
las rutas y las regiones bíblicas que se resaltan.

Los textos de descripción son redacción propia y se apoyan en los datos
histórico-geográficos de dominio público y de licencia libre que cita
CREDITOS.md.
"""

MUNDO = [
    {
        "id": "mundo-antiguo-testamento",
        "titulo": "El mundo del Antiguo Testamento",
        "subtitulo": "De Egipto y Canaán a Mesopotamia y Persia",
        "categoria": "El mundo de la Biblia",
        "descripcion": "Escenario completo del Antiguo Testamento: el valle del Nilo, el Creciente Fértil, "
                       "Canaán y las tierras altas de Persia. Israel ocupa el corredor entre tres imperios "
                       "(Egipto, Asiria-Babilonia y Persia), lo que explica buena parte de su historia. "
                       "Las distancias se han medido sobre la proyección de este mapa.",
        "bbox": (25.0, 26.0, 56.0, 39.5),
        "lugares": ["memphis", "thebes", "zoan", "tahpanhes", "goshen-1", "ezion-geber", "elath",
                    "kadesh-barnea", "gaza", "jerusalem", "samaria-1", "hazor-1", "dan", "tyre",
                    "sidon", "damascus", "hamath-1", "carchemish", "haran", "nineveh", "ashur",
                    "babylon-1", "ur-1", "susa", "elam", "mount-sinai", "salt-sea", "jordan",
                    "euphrates", "nile", "great-sea", "red-sea-1", "argo", "paran"],
        "regiones": ["egypt", "canaan", "ammon", "moab-1", "edom", "assyria", "babylonia",
                     "chaldea", "persia", "elam", "media", "aram", "syria-1", "philistia", "arabia-1"],
        "refs": ["Génesis 15:18-21", "Éxodo 23:31", "1 Reyes 4:21"],
    },
    {
        "id": "mundo-nuevo-testamento",
        "titulo": "El mundo del Nuevo Testamento",
        "subtitulo": "El Imperio romano en tiempos de Jesús y de Pablo",
        "categoria": "El mundo de la Biblia",
        "descripcion": "El Mediterráneo oriental con las provincias por las que se extendió el evangelio: "
                       "Judea, Siria, Asia Menor, Macedonia, Acaya e Italia. La red de calzadas romanas y "
                       "la navegación de cabotaje hicieron posible que en una sola generación la fe "
                       "cristiana llegara de Jerusalén a Roma.",
        "bbox": (-7.0, 26.0, 42.0, 44.0),
        "lugares": ["jerusalem", "bethlehem-1", "nazareth", "capernaum", "caesarea", "damasco",
                    "antioch-1", "tarsus", "ephesus", "troas", "philippi", "thessalonica", "berea",
                    "athens", "corinth", "crete", "cyprus", "malta", "syracuse", "rome",
                    "alexandria", "laodicea", "sardis", "patmos", "mileto", "iconium", "lystra",
                    "derbe", "antioch-2", "perga", "salamis", "paphos", "smyrna", "pergamum",
                    "thyatira", "philadelphia-1", "nicopolis-1", "colossae-1"],
        "regiones": ["italy", "greece", "macedonia", "asia", "galatia", "cilicia", "syria-1",
                     "egypt", "judea-1", "achaia", "phrygia", "pontus"],
        "refs": ["Hechos 1:8", "Romanos 15:19-24", "1 Pedro 1:1"],
    },
    {
        "id": "imperio-romano",
        "titulo": "El Imperio romano en el siglo I",
        "subtitulo": "Augusto, Tiberio y los gobernadores de Judea",
        "categoria": "El mundo de la Biblia",
        "descripcion": "Extensión del Imperio romano cuando nació Jesús. Judea era una pequeña provincia "
                       "periférica gobernada primero por reyes clientes (Herodes el Grande y sus hijos) y "
                       "después por prefectos y procuradores romanos, como Poncio Pilato.",
        "bbox": (-10.0, 24.0, 46.0, 46.0),
        "lugares": ["rome", "athens", "corinth", "ephesus", "antioch-1", "jerusalem", "caesarea",
                    "alexandria", "thessalonica", "philippi", "tarsus", "damasco", "carthage",
                    "carthage", "sparta", "byzantium-1", "smyrna", "patmos", "crete", "cyprus",
                    "malta", "cyrene", "cirene-1"],
        "regiones": ["italy", "greece", "macedonia", "asia", "galatia", "cilicia", "syria-1",
                     "egypt", "judea-1", "achaia", "pontus", "libya", "phrygia"],
        "refs": ["Lucas 3:1", "Mateo 22:17-21", "Hechos 25:11-12"],
    },
    {
        "id": "imperio-asirio",
        "titulo": "El Imperio asirio",
        "subtitulo": "Tiglat-pileser III, Sargón II y Senaquerib",
        "categoria": "El mundo de la Biblia",
        "descripcion": "Asiria fue el primer gran imperio que sometió a Israel y Judá. Desde Nínive y "
                       "Calaj, sus ejércitos bajaban por el Éufrates y la costa fenicia hasta las puertas "
                       "de Jerusalén. Los profetas Amós, Oseas, Isaías y Miqueas predicaron en este "
                       "contexto de amenaza constante.",
        "bbox": (32.0, 28.5, 50.0, 39.5),
        "lugares": ["nineveh", "ashur", "calah-1", "dur-sharrukin-1", "calah-1", "haran",
                    "carchemish", "arpad", "hamath-1", "damascus", "samaria-1", "tyre", "sidon",
                    "ekron", "ashdod", "lachish", "libnah-1", "jerusalem", "babylon-1", "susa",
                    "elam", "media", "ur-1", "jericho-1", "megiddo"],
        "regiones": ["assyria", "babylonia", "elam", "media", "syria-1", "philistia", "ammon",
                     "moab-1", "edom", "israel", "judah"],
        "refs": ["2 Reyes 15:19-29", "2 Reyes 17:1-6", "Isaías 36-37"],
    },
    {
        "id": "imperio-babilonico",
        "titulo": "El Imperio neobabilónico",
        "subtitulo": "Nabopolasar y Nabucodonosor",
        "categoria": "El mundo de la Biblia",
        "descripcion": "Babilonia sustituyó a Asiria como potencia dominante. Nabucodonosor tomó Jerusalén "
                       "en el año 597 a.C. y la destruyó en el 586 a.C.; comenzó entonces el destierro, que "
                       "duró hasta el decreto de Ciro en el 539 a.C.",
        "bbox": (33.0, 28.0, 52.0, 39.0),
        "lugares": ["babylon-1", "ur-1", "nippur-1", "susa", "elam", "nineveh", "haran",
                    "carchemish", "riblah-1", "hamath-1", "damasco", "tyre", "jerusalem", "lachish",
                    "gaza", "tahpanhes", "memphis", "chebar", "euphrates", "tigris-1", "sodom"],
        "regiones": ["babylonia", "chaldea", "assyria", "elam", "media", "persia", "syria-1",
                     "judea-1", "egypt", "edom", "moab-1", "ammon"],
        "refs": ["2 Reyes 24-25", "Jeremías 39", "Daniel 1:1-2"],
    },
    {
        "id": "imperio-persa",
        "titulo": "El Imperio persa",
        "subtitulo": "Ciro, Darío I y Artajerjes",
        "categoria": "El mundo de la Biblia",
        "descripcion": "Ciro el Grande conquistó Babilonia en el 539 a.C. y autorizó el regreso de los "
                       "judíos a Jerusalén. Bajo los persas gobernaron Zorobabel, Esdras y Nehemías; en la "
                       "corte de Susa transcurre la historia de Ester.",
        "bbox": (25.0, 25.0, 60.0, 41.0),
        "lugares": ["susa", "persia", "pasargadae-1", "persepolis-1", "elam", "media", "ecbatana-1",
                    "babylon-1", "ur-1", "nineveh", "haran", "carchemish", "sardis", "ephesus",
                    "tyre", "damasco", "jerusalem", "samaria-1", "memphis", "tahpanhes", "gaza",
                    "euphrates", "tigris-1", "nile"],
        "regiones": ["persia", "elam", "media", "babylonia", "assyria", "syria-1", "judea-1",
                     "egypt", "asia", "phrygia", "cilicia"],
        "refs": ["2 Crónicas 36:22-23", "Esdras 1:1-4", "Ester 1:1-2"],
    },
    {
        "id": "imperio-griego",
        "titulo": "El Imperio griego de Alejandro",
        "subtitulo": "De Macedonia a la India (336-323 a.C.)",
        "categoria": "El mundo de la Biblia",
        "descripcion": "Alejandro Magno unió Grecia y derrotó a Persia; tras su muerte, sus generales se "
                       "repartieron el imperio. Los seléucidas gobernaron Siria y los lágidas Egipto. La "
                       "cultura griega (koiné, gimnasios, ciudades helenísticas) preparó el terreno "
                       "lingüístico en el que se escribió el Nuevo Testamento.",
        "bbox": (18.0, 28.0, 52.0, 42.0),
        "lugares": ["macedonia", "greece", "athens", "sparta", "thessalonica", "philippi", "troas",
                    "sardis", "ephesus", "tarsus", "antioch-1", "tyre", "gaza", "jerusalem",
                    "memphis", "alexandria", "babylon-1", "susa", "persepolis-1", "media",
                    "granicus-1", "issus-1", "tyre"],
        "regiones": ["macedonia", "greece", "asia", "phrygia", "cilicia", "syria-1", "judea-1",
                     "egypt", "babylonia", "persia", "media", "elam", "galatia"],
        "refs": ["Daniel 8:5-8", "Daniel 11:3-4", "1 Macabeos 1:1-9"],
    },
    {
        "id": "tierra-santa-fisica",
        "titulo": "La tierra de la Biblia: relieve y aguas",
        "subtitulo": "Del mar Mediterráneo al desierto de Siria",
        "categoria": "El mundo de la Biblia",
        "descripcion": "Cuatro franjas paralelas de norte a sur: la llanura costera, la cordillera central, "
                       "el valle del Jordán (la depresión más profunda de la tierra firme) y la meseta "
                       "oriental. El Jordán nace en el Hermón, atraviesa el lago de Galilea y desemboca en "
                       "el mar Muerto, a unos 430 m bajo el nivel del mar.",
        "bbox": (33.7, 30.5, 36.4, 33.8), "auto_encuadre": False,
        "lugares": ["mount-hermon", "dan", "hazor-1", "sea-of-galilee", "mount-tabor", "nazareth",
                    "mount-carmel", "megiddo", "jordan", "salt-sea", "jericho-1", "jerusalem",
                    "bethlehem-1", "hebron", "beersheba-1", "gaza", "joppa", "caesarea", "shiloh",
                    "shechem", "negeb", "arabah", "gilead-1", "bashan", "jabbok", "arnon",
                    "mount-nebo-1", "great-sea"],
        "regiones": ["galilee-1", "samaria-2", "judea-1", "philistia", "sharon-1", "shephelah",
                     "bashan", "gilead-1", "moab-1", "ammon"],
        "rios": True, "fronteras": False,
        "refs": ["Deuteronomio 8:7-9", "Josué 12", "Salmos 104:6-9"],
    },
]

PENTATEUCO = [
    {
        "id": "eden",
        "titulo": "Eden y los cuatro rios",
        "subtitulo": "Génesis 2:10-14",
        "categoria": "Génesis",
        "descripcion": "La Biblia sitúa el huerto de Edén en la cabecera de cuatro ríos: Pisón, Gihón, "
                       "Hidekel (Tigris) y Éufrates. La descripción apunta a la región montañosa de Armenia "
                       "y el norte de Mesopotamia, aunque su ubicación exacta es desconocida: los mapas "
                       "antiguos la dibujan de manera simbólica.",
        "bbox": (36.0, 30.0, 50.0, 42.0),
        "lugares": [{"n": "Edén (ubicación tradicional)", "lon": 44.95, "lat": 40.38, "tipo": "región",
                     "refs": ["Génesis 2:8-14"]},
                    "eden-2", "euphrates", "tigris-1", "babylon-1", "ur-1", "haran", "nineveh",
                    "ararat-1", "eden-2"],
        "regiones": ["babylonia", "assyria", "mesopotamia", "media"],
        "notas": ["El texto menciona también el oro de la tierra de Havila y el ónice (Génesis 2:11-12)."],
        "refs": ["Génesis 2:8-14", "Ezequiel 28:13", "Apocalipsis 22:1-2"],
    },
    {
        "id": "diluvio-ararat",
        "titulo": "El diluvio y el arca sobre Ararat",
        "subtitulo": "Génesis 6-9",
        "categoria": "Génesis",
        "descripcion": "Tras cuarenta días de lluvia y el descenso de las aguas, el arca reposó «sobre los "
                       "montes de Ararat», en el altiplano de Armenia, entre el Tigris y el Éufrates. La "
                       "tradición identifica el monte con el Gran Ararat (5.137 m).",
        "bbox": (37.0, 35.0, 48.0, 41.5),
        "lugares": ["ararat-1", "mount-ararat-1", "nineveh", "ashur", "haran", "carchemish",
                    "euphrates", "tigris-1", "ur-1", "babylon-1", "eden-2"],
        "regiones": ["assyria", "mesopotamia", "media", "babylonia"],
        "refs": ["Génesis 8:4", "Génesis 9:1-17", "1 Pedro 3:20"],
    },
    {
        "id": "torre-de-babel",
        "titulo": "La torre de Babel y la dispersion",
        "subtitulo": "Génesis 11:1-9",
        "categoria": "Génesis",
        "descripcion": "Los descendientes de Noé se establecieron en la llanura de Sinar (Babilonia) y "
                       "comenzaron a construir una ciudad y una torre «cuya cúspide llegue al cielo». La "
                       "confusión de las lenguas dispersó a la humanidad. Los zigurats mesopotámicos, como "
                       "el de Babilonia o el de Ur, están en el trasfondo del relato.",
        "bbox": (41.0, 29.5, 49.0, 35.0),
        "lugares": ["babylon-1", "ur-1", "eridu-1", "shinar", "nippur-1", "euphrates", "tigris-1",
                    "ur-1", "kish-1"],
        "regiones": ["babylonia", "chaldea", "elam", "mesopotamia"],
        "notas": ["Nabucodonosor I y Nabucodonosor II reconstruyeron la torre escalonada de Babilonia "
                  "«Etemenanki», que pudo medir unos 90 metros de lado por 90 de altura."],
        "refs": ["Génesis 10:8-10", "Génesis 11:1-9"],
    },
    {
        "id": "viaje-abraham",
        "titulo": "El viaje de Abraham",
        "subtitulo": "De Ur a la tierra prometida (Génesis 11-13)",
        "categoria": "Génesis",
        "descripcion": "Abrahán salió de «Ur de los caldeos» con su familia, se detuvo en Harán y, tras la "
                       "muerte de su padre Taré, entró en Canaán: Siquem, Betel, el Neguev y finalmente "
                       "Egipto por causa del hambre. Después se separó de Lot y volvió a Hebrón.",
        "bbox": (28.0, 27.5, 48.0, 38.5),
        "lugares": ["ur-1", "eridu-1", "haran", "carchemish", "alepo-1", "damascus", "shechem",
                    "bethel-1", "ai-1", "hebron", "gaza", "beersheba-1", "memphis", "zoan",
                    "goshen-1", "euphrates", "nile", "sodom"],
        "rutas": [{"nombre": "Ruta de Abraham", "color": "#a8320d",
                   "puntos": ["ur-1", "eridu-1", "babylon-1", "kish-1", "haran", "carchemish",
                              "alepo-1", "damascus", "shechem", "bethel-1", "beersheba-1",
                              "gaza", "tahpanhes", "memphis"]}],
        "regiones": ["babylonia", "chaldea", "mesopotamia", "canaan", "egypt", "philistia", "negeb"],
        "refs": ["Génesis 11:31-32", "Génesis 12:1-9", "Hechos 7:2-4"],
    },
    {
        "id": "sodoma-gomorra",
        "titulo": "Sodoma, Gomorra y el valle de Sidim",
        "subtitulo": "Génesis 14 y 19",
        "categoria": "Génesis",
        "descripcion": "Las «ciudades de la llanura» (Sodoma, Gomorra, Adma, Zeboim y Zoar) se situaban al "
                       "sur del mar Muerto, en el valle de Sidim. Lot escapó a Zoar cuando la ciudad fue "
                       "destruida; su mujer miró atrás. La geografía de la zona (asfalto, azufre y pozos "
                       "de betún) explica las imágenes del relato.",
        "bbox": (34.6, 30.7, 36.1, 32.1),
        "lugares": ["sodom", "gomorrah", "adma-1", "zeboiim-1", "zoar", "valley-of-siddim-1",
                    "salt-sea", "hebron", "engedi", "mamre", "jordan"],
        "notas": ["La batalla de los reyes de Génesis 14 se libró en el valle de Sidim, donde había "
                  "«muchos pozos de betún»."],
        "refs": ["Génesis 14:1-12", "Génesis 19:23-29", "Lucas 17:28-30", "2 Pedro 2:6"],
    },
    {
        "id": "jacob-y-esau",
        "titulo": "Jacob y Esau: Canaán, Haran y el Jabboc",
        "subtitulo": "Génesis 25-35",
        "categoria": "Génesis",
        "descripcion": "Jacob huyó de Esaú hacia Harán, y al volver luchó con Dios en Peniel, junto al río "
                       "Jaboc, donde recibió el nombre de Israel. Vivió en Siquem y Betel, y terminó sus "
                       "días en Egipto, en la tierra de Gosén.",
        "bbox": (30.0, 28.0, 42.0, 37.0),
        "lugares": ["beersheba-1", "hebron", "bethel-1", "shechem", "penuel", "mahanaim",
                    "sucot-2", "paddan-aram", "haran", "damascus", "jabbok", "jordan",
                    "gosen-1", "memphis", "sodom"],
        "rutas": [{"nombre": "Ida a Harán", "color": "#1f6f8b",
                   "puntos": ["beersheba-1", "hebron", "bethel-1", "shechem", "damascus", "paddan-aram", "haran"]},
                  {"nombre": "Regreso a Canaán", "color": "#a8320d",
                   "puntos": ["haran", "paddan-aram", "mahanaim", "penuel", "sucot-2", "shechem", "bethel-1", "hebron"]},
                  {"nombre": "Descenso a Egipto", "color": "#5c7a29",
                   "puntos": ["hebron", "beersheba-1", "gosen-1", "memphis"]}],
        "regiones": ["canaan", "gilead-1", "bashan", "egypt", "negeb", "edyon"],
        "refs": ["Génesis 28:10-22", "Génesis 32:22-32", "Génesis 46:1-7"],
    },
    {
        "id": "jose-en-egipto",
        "titulo": "Jose en Egipto",
        "subtitulo": "Génesis 37-50",
        "categoria": "Génesis",
        "descripcion": "José fue vendido por sus hermanos y llevado a Egipto, donde llegó a ser gobernador "
                       "del país. Su familia se estableció en Gosén, en el delta oriental, la región de los "
                       "pastores y la frontera con Canaán.",
        "bbox": (29.5, 28.5, 36.5, 32.5),
        "lugares": ["goshen-1", "heliopolis", "memphis", "zoan", "tahpanhes", "pithom-1", "rameses-1",
                    "thebes", "nile", "mount-sinai", "heliopolis-1"],
        "rutas": [{"nombre": "José llevado a Egipto", "color": "#a8320d",
                   "puntos": ["hebron", "beersheba-1", "gaza", "tahpanhes", "heliopolis", "memphis"]}],
        "regiones": ["egypt", "goshen-2"],
        "refs": ["Génesis 37:12-36", "Génesis 41:39-46", "Génesis 47:1-11"],
    },
    {
        "id": "exodo-ruta",
        "titulo": "La salida de Egipto",
        "subtitulo": "Éxodo 12-15",
        "categoria": "Éxodo",
        "descripcion": "Israel salió de Ramesés, acampó en Sucot y en Etam, y acampó junto al mar delante "
                       "de Baal-zefón. Allí el mar se abrió y el ejército del faraón fue destruido. La "
                       "ruta exacta es objeto de debate: este mapa muestra la situación geográfica de los "
                       "topónimos citados por el texto.",
        "bbox": (31.0, 27.5, 36.0, 33.0),
        "lugares": ["rameses-1", "pithom-1", "goshen-1", "sucot-3", "etham", "pi-hahiroth",
                    "baal-zephon", "migdol-1", "marah", "elim", "rephidim", "dophka-1",
                    "sin-2", "mount-sinai", "wilderness-of-sinai", "red-sea-1", "nile"],
        "rutas": [{"nombre": "Ruta del Éxodo", "color": "#a8320d",
                   "puntos": ["rameses-1", "sucot-3", "etham", "pi-hahiroth", "marah", "elim",
                              "dophka-1", "rephidim", "mount-sinai"]}],
        "regiones": ["egypt"],
        "refs": ["Éxodo 12:37-42", "Éxodo 13:17-22", "Éxodo 14:1-31", "Números 33:1-15"],
    },
    {
        "id": "monte-sinai",
        "titulo": "Alrededor del monte Sinai",
        "subtitulo": "Éxodo 19-34",
        "categoria": "Éxodo",
        "descripcion": "Al pie del Sinaí (también llamado Horeb) Israel acampó un año: recibió la ley, "
                       "construyó el tabernáculo y celebró el pacto. La tradición identifica el monte con "
                       "el Yébel Musa (2.285 m) y Santa Catalina, en la península del Sinaí.",
        "bbox": (33.0, 27.3, 36.2, 30.5),
        "lugares": ["mount-sinai", "mount-horeb", "wilderness-of-sinai", "rephidim", "meribah-2",
                    "dophka-1", "elim", "sin-2", "hazerot", "saint-catherine-1", "red-sea-1",
                    "elath", "ezion-geber", "hazerot"],
        "regiones": ["egypt"],
        "refs": ["Éxodo 19:1-25", "Éxodo 20:1-17", "Éxodo 40:34-38", "1 Reyes 8:9"],
    },
    {
        "id": "desierto-cuarenta-anos",
        "titulo": "Los cuarenta años en el desierto",
        "subtitulo": "Números 13-36",
        "categoria": "Éxodo",
        "descripcion": "Después de la exploración de Canaán y la negativa del pueblo, Israel permaneció "
                       "cuarenta años en el desierto. Rodeó Edom y Moab, acampó en Cades-barnea y en el "
                       "Arabá, y acampó en las llanuras de Moab frente a Jericó, donde Moisés subió al "
                       "Nebo y murió.",
        "bbox": (33.0, 28.0, 37.0, 34.0),
        "lugares": ["kadesh-barnea", "zin-1", "mount-hor-1", "ezion-geber", "elath", "punon-1",
                    "arabah", "edom", "moab-1", "arnon", "dibon-1", "heshbon", "nebo-1",
                    "pisgah", "abarim", "hazerot", "meribah-1", "wilderness-of-sinai", "hazerot",
                    "hor-haggidgad", "jotbathah", "ezion-geber", "salt-sea", "jericho-1", "jordan"],
        "rutas": [{"nombre": "Itinerario de Números 33", "color": "#a8320d",
                   "puntos": ["mount-sinai", "hazerot", "jotbathah", "hor-haggidgad", "ezion-geber",
                              "kadesh-barnea", "mount-hor-1", "punon-1", "arabah", "dibon-1",
                              "heshbon", "pisgah"]}],
        "regiones": ["edom", "moab-1", "arann", "negeb", "arabia-1", "param-1"],
        "refs": ["Números 14:26-35", "Números 33", "Deuteronomio 2:1-8", "Deuteronomio 34:1-8"],
    },
    {
        "id": "conquista-canaan",
        "titulo": "La conquista de Canaán",
        "subtitulo": "Josué 1-12",
        "categoria": "Josué",
        "descripcion": "Tras cruzar el Jordán frente a Jericó, Israel tomó la ciudad, sufrió la derrota y "
                       "la restauración en Hai, hizo alianza con Gabaón y libró las batallas del sur "
                       "(Ajalón, Laquis, Hebrón) y del norte (Hazor).",
        "bbox": (34.2, 30.8, 36.4, 33.6),
        "lugares": ["gilgal-1", "jericho-1", "ai-1", "bethel-1", "gibeon", "ajalon-1", "azekah",
                    "makkedah", "libnah-1", "lachish", "eglon", "hebron", "debir-1", "hazor-1",
                    "madon-1", "merom-1", "dan", "shechem", "shiloh", "jerusalem", "jordan",
                    "salt-sea", "gaza", "ashkelon", "asdod", "ekron", "gath-1"],
        "rutas": [{"nombre": "Campaña del sur", "color": "#a8320d",
                   "puntos": ["gilgal-1", "jericho-1", "ai-1", "gibeon", "ajalon-1", "azekah",
                              "makkedah", "libnah-1", "lachish", "eglon", "hebron", "debir-1"]},
                  {"nombre": "Campaña del norte", "color": "#1f6f8b",
                   "puntos": ["gilgal-1", "shechem", "shiloh", "megiddo", "hazor-1", "dan"]}],
        "regiones": ["canaan", "philistia", "gilead-1", "bashan", "moab-1", "ammon"],
        "refs": ["Josué 3:14-17", "Josué 6:20-21", "Josué 10:1-14", "Josué 11:1-11"],
    },
    {
        "id": "tribus-de-israel",
        "titulo": "El reparto de la tierra entre las tribus",
        "subtitulo": "Josué 13-19",
        "categoria": "Josué",
        "descripcion": "La tierra se repartió por suertes entre las doce tribus, con ciudades para los "
                       "levitas y ciudades de refugio. Judá recibió el sur montañoso, Efraín y Manasés el "
                       "centro, y las tribus del norte la Galilea y el valle de Jezreel.",
        "bbox": (34.1, 30.6, 36.4, 33.6), "auto_encuadre": False,
        "lugares": ["jerusalem", "hebron", "beersheba-1", "gaza", "jericho-1", "bethel-1",
                    "shechem", "shiloh", "megiddo", "jezreel-2", "hazor-1", "dan", "nazareth",
                    "mount-tabor", "beth-shan", "gath-1", "lachish", "asdod", "jordan", "salt-sea",
                    "sea-of-galilee"],
        "rutas": [],
        "regiones": ["galilee-1", "samaria-2", "judea-1", "thilistia", "shephelah", "negeb",
                     "bashan", "gilead-1", "sharon-1"],
        "etiquetas_extra": [
            {"n": "Aser", "lon": 35.2, "lat": 33.05}, {"n": "Neftalí", "lon": 35.55, "lat": 32.95},
            {"n": "Zabulón", "lon": 35.3, "lat": 32.7}, {"n": "Isacar", "lon": 35.35, "lat": 32.55},
            {"n": "Manasés (oeste)", "lon": 35.05, "lat": 32.35},
            {"n": "Efraín", "lon": 35.05, "lat": 32.05}, {"n": "Dan", "lon": 34.95, "lat": 31.95},
            {"n": "Benjamín", "lon": 35.22, "lat": 31.9}, {"n": "Judá", "lon": 34.95, "lat": 31.55},
            {"n": "Simeón", "lon": 34.95, "lat": 31.25}, {"n": "Rubén", "lon": 35.7, "lat": 31.9},
            {"n": "Gad", "lon": 35.8, "lat": 32.4}, {"n": "Manasés (este)", "lon": 35.9, "lat": 32.65},
        ],
        "refs": ["Josué 14-19", "Josué 20-21", "Números 34"],
    },
    {
        "id": "ciudades-de-refugio",
        "titulo": "Las ciudades de refugio y los levitas",
        "subtitulo": "Josué 20-21; Números 35",
        "categoria": "Josué",
        "descripcion": "Seis ciudades de refugio protegían a quien mataba sin intención: tres al oriente "
                       "del Jordán (Golán, Ramot de Galaad y Beser) y tres al occidente (Cedes, Siquem y "
                       "Hebrón). Los levitas recibieron además cuarenta y ocho ciudades.",
        "bbox": (34.0, 30.8, 36.8, 33.5),
        "lugares": ["kedesh-4", "shechem", "hebron", "golan-1", "ramoth-gilead", "boser-1",
                    "jerusalem", "jericho-1", "beersheba-1", "hazor-1", "beth-shan", "jordan",
                    "salt-sea", "sea-of-galilee"],
        "regiones": ["galilee-1", "samaria-2", "judea-1", "bashan", "gilead-1"],
        "refs": ["Números 35:9-15", "Josué 20:1-9", "Josué 21:41-43"],
    },
]

REYES = [
    {
        "id": "jueces",
        "titulo": "Los jueces de Israel",
        "subtitulo": "Jueces 1-21",
        "categoria": "Jueces y Reyes",
        "descripcion": "En un tiempo sin rey, Dios levantó jueces: Débora y Barac contra Sísara en el "
                       "Quisón, Gedeón contra Madián en el valle de Jezreel, Jefté en Galaad y Sansón "
                       "contra los filisteos. Los enemigos venían de todas partes: filisteos al oeste, "
                       "moabitas y amonitas al este, madianitas y amalecitas desde el desierto.",
        "bbox": (34.2, 30.8, 36.6, 33.4),
        "lugares": ["zorah", "eshtaol", "timnah-1", "gaza", "asdod", "ekron", "beth-shemesh-1",
                    "ajalon-1", "gibeon", "mizpah-1", "shiloh", "bethel-1", "jericho-1", "gilgal-1",
                    "mount-tabor", "mount-gilboa", "jezreel-2", "megiddo", "mount-carmel",
                    "harosheth-hagoyim", "jabesh-gilead", "mahanaim", "succoth-1", "penuel",
                    "ramoth-gilead", "dan", "jordan", "salt-sea", "sea-of-galilee"],
        "regiones": ["philistia", "philistia", "gilead-1", "moab-1", "ammon", "edom", "bashan"],
        "refs": ["Jueces 4:1-16", "Jueces 7:1-22", "Jueces 13-16", "Jueces 21:25"],
    },
    {
        "id": "samuel-saul",
        "titulo": "Samuel y el reinado de Saul",
        "subtitulo": "1 Samuel 1-31",
        "categoria": "Jueces y Reyes",
        "descripcion": "Samuel juzgó a Israel desde Ramá, Mizpa y Betel. Saúl fue ungido rey en Mizpa y "
                       "combatió en Micmas, el Neguev y el valle de Ela, hasta caer herido en el monte "
                       "Gilboa. David, su rival y sucesor, huyó por el desierto de Judá y el Neguev.",
        "bbox": (34.3, 30.8, 36.4, 33.3),
        "lugares": ["ramah-1", "mizpah-1", "bethel-1", "gilgal-1", "gibeon", "gibeah-1", "geba-1",
                    "michmash", "michmash", "ai-1", "jerusalem", "bethlehem-1", "valley-of-elah-1",
                    "soco-1", "azekah", "gath-1", "ekron", "adullam", "engedi", "maon", "ziklag",
                    "beersheba-1", "jabesh-gilead", "beth-shan", "mount-gilboa", "jezreel-2",
                    "jordan", "salt-sea"],
        "regiones": ["philistia", "moab-1", "ammon", "edom", "gilead-1"],
        "refs": ["1 Samuel 7:15-17", "1 Samuel 10:17-24", "1 Samuel 17", "1 Samuel 31:1-6"],
    },
    {
        "id": "david-y-goliat",
        "titulo": "David y Goliat: el valle de Ela",
        "subtitulo": "1 Samuel 17",
        "categoria": "Jueces y Reyes",
        "descripcion": "Los ejércitos de Israel y de los filisteos se enfrentaron en el valle de Ela: los "
                       "filisteos en un monte y los israelitas en otro. El arroyo que separaba ambos "
                       "campamentos fue donde David escogió sus cinco piedras; Goliat salió de Gat.",
        "bbox": (34.75, 31.35, 35.45, 32.05),
        "lugares": ["soco-1", "azekah", "valley-of-elah-1", "gath-1", "ekron", "adullam",
                    "bethlehem-1", "laquis", "moresheth-gath", "adullam", "keilah", "hebron"],
        "regiones": ["philistia", "shephelah", "judea-1"],
        "refs": ["1 Samuel 17:1-11", "1 Samuel 17:40-51", "2 Samuel 21:19"],
    },
    {
        "id": "david-rey",
        "titulo": "El reino de David",
        "subtitulo": "2 Samuel 5-10; 1 Crónicas 18",
        "categoria": "Jueces y Reyes",
        "descripcion": "David conquistó Jerusalén y la hizo capital; derrotó a los filisteos, sometió a "
                       "Moab, Amón, Edom y los arameos, y extendió su dominio «desde el río de Egipto "
                       "hasta el Éufrates». Llevó el arca a Sion y reunió los materiales para el templo.",
        "bbox": (32.5, 28.5, 40.0, 36.5),
        "lugares": ["jerusalem", "hebron", "gath-1", "gaza", "ziklag", "adullam", "rabbah-1",
                    "bozrah-1", "damascus", "zobah", "lebo-hamat", "hamath-1", "tadmor-1",
                    "ezion-geber", "elath", "ammon", "moab-1", "heshbon", "ramoth-gilead",
                    "mahanaim", "jordan", "euphrates", "salt-sea", "great-sea"],
        "rutas": [{"nombre": "Campañas de David", "color": "#a8320d", "estilo": "punteada",
                   "puntos": ["jerusalem", "gath-1", "gaza", "heshbon", "rabbah-1", "bozrah-1",
                              "damascus", "lebo-hamat"]}],
        "regiones": ["philistia", "moab-1", "ammon", "edom", "aram", "zobah-1", "geshur",
                     "gilead-1", "bashan", "judea-1", "israel"],
        "refs": ["2 Samuel 5:6-10", "2 Samuel 8:1-14", "2 Samuel 24:1-9"],
    },
    {
        "id": "reino-salomon",
        "titulo": "El reino de Salomon y su comercio",
        "subtitulo": "1 Reyes 4-11",
        "categoria": "Jueces y Reyes",
        "descripcion": "El reino de Salomón se extendió del Éufrates a la frontera de Egipto. Construyó el "
                       "templo, el palacio y la «casa del bosque del Líbano», edificó ciudades fortificadas "
                       "(Hazor, Meguido y Gezer) y organizó una flota en Ezión-geber que traía oro de Ofir.",
        "bbox": (30.0, 27.5, 44.0, 37.0),
        "lugares": ["jerusalem", "gibeon", "hebron", "gezer", "megiddo", "hazor-1", "dan",
                    "tadmor-1", "ezion-geber", "elath", "ophir", "tarsish-1", "tyre", "sidon",
                    "damascus", "lebo-hamat", "gaza", "philistia", "jordan", "euphrates",
                    "red-sea-1", "great-sea"],
        "rutas": [{"nombre": "Flota de Tarsis y Ofir", "color": "#1f6f8b",
                   "puntos": ["ezion-geber", [34.6, 28.5], [36.0, 22.0], [40.0, 20.0], [42.5, 18.2]]}],
        "regiones": ["israel", "judah", "philistia", "moab-1", "ammon", "edom", "aram", "geshur",
                     "bashan", "gilead-1"],
        "refs": ["1 Reyes 4:21-25", "1 Reyes 7:1-12", "1 Reyes 9:15-28", "1 Reyes 10:14-29"],
    },
    {
        "id": "reino-dividido",
        "titulo": "La division del reino",
        "subtitulo": "1 Reyes 12; 2 Crónicas 10",
        "categoria": "Jueces y Reyes",
        "descripcion": "Tras la muerte de Salomón, diez tribus siguieron a Jeroboam y formaron el reino de "
                       "Israel, con capitales sucesivas en Siquem, Tirsa y Samaria. Judá y Benjamín "
                       "permanecieron fieles a Roboam, con centro en Jerusalén y su templo. Jeroboam erigió "
                       "becerros de oro en Betel y Dan para evitar las peregrinaciones al sur.",
        "bbox": (34.1, 30.6, 36.5, 33.6),
        "lugares": ["jerusalem", "shechem", "tirzah", "samaria-1", "bethel-1", "dan", "penuel",
                    "gibeah-1", "mizpah-1", "ramoth-gilead", "megiddo", "jezreel-2", "shiloh",
                    "hebron", "beersheba-1", "bethlehem-1", "lachish", "jordan", "salt-sea",
                    "sea-of-galilee"],
        "regiones": ["galilee-1", "samaria-2", "judea-1", "gilead-1", "bashan", "negeb",
                     "philistia", "moab-1", "ammon"],
        "refs": ["1 Reyes 11:29-39", "1 Reyes 12:16-33", "1 Reyes 15:25-34"],
    },
    {
        "id": "elias-eliseo",
        "titulo": "El ministerio de Elias y Eliseo",
        "subtitulo": "1 Reyes 17-19; 2 Reyes 2-8",
        "categoria": "Profetas",
        "descripcion": "Elías anunció la sequía en Samaria, fue alimentado por los cuervos en el arroyo de "
                       "Querit y por una viuda en Sarepta; en el Carmelo se enfrentó a los profetas de Baal "
                       "y huyó a Horeb, donde oyó el «silencio suave». Eliseo, su sucesor, sirvió en Sunem, "
                       "Damascus y Samaria y curó a Naamán el sirio.",
        "bbox": (34.4, 30.4, 37.0, 34.0),
        "lugares": ["tishbe", "zarephath", "mount-carmel", "jezreel-2", "samaria-1", "shunem",
                    "mount-gilboa", "beth-shan", "jordan", "jericho-1", "gilgal-1", "bethel-1",
                    "mount-horeb", "beersheba-1", "abel-meholah", "mahanaim", "ramoth-gilead",
                    "damascus", "dotan-1", "salt-sea", "great-sea"],
        "rutas": [{"nombre": "Huida de Elías", "color": "#5c7a29",
                   "puntos": ["jezreel-2", "beersheba-1", "mount-horeb"]},
                  {"nombre": "Camino de Eliseo", "color": "#1f6f8b",
                   "puntos": ["abel-meholah", "jericho-1", "gilgal-1", "bethel-1", "samaria-1",
                              "shunem", "damascus"]}],
        "regiones": ["israel", "judah", "gilead-1", "bashan", "ammon", "moab-1", "aram"],
        "refs": ["1 Reyes 17:1-6", "1 Reyes 18:20-46", "1 Reyes 19:8-13", "2 Reyes 5:1-14"],
    },
    {
        "id": "jonas",
        "titulo": "La huida y la mision de Jonas",
        "subtitulo": "Jonás 1-4",
        "categoria": "Profetas",
        "descripcion": "Jonás huyó «de la presencia de Jehová» hacia Tarsis, embarcando en Jope. Una "
                       "tempestad lo llevó al mar y un gran pez lo devolvió a tierra; entonces predicó en "
                       "Nínive, la gran ciudad de Asiria, que se arrepintió.",
        "bbox": (29.0, 28.0, 46.0, 39.0),
        "lugares": ["joppa", "tarshish-1", "nineveh", "gaza", "jerusalem", "bethel-1", "gath-hepher-1",
                    "damascus", "carchemish", "haran", "nile", "euphrates"],
        "rutas": [{"nombre": "Huida hacia Tarsis", "color": "#5c7a29",
                   "puntos": ["gath-hepher-1", "joppa", [31.0, 33.5], [20.0, 35.0], [-6.9, 37.3]]},
                  {"nombre": "Predicación en Nínive", "color": "#a8320d",
                   "puntos": ["joppa", [35.5, 34.5], "carchemish", "harran", "nineveh"]}],
        "regiones": ["assyria", "syria-1", "philistia", "judea-1", "israel"],
        "refs": ["Jonás 1:1-3", "Jonás 3:1-10", "Mateo 12:39-41"],
    },
    {
        "id": "amos-oseas",
        "titulo": "Amos y Oseas: profetas del reino del norte",
        "subtitulo": "Amós 1-9; Oseas 1-14",
        "categoria": "Profetas",
        "descripcion": "Amós era un boyero de Tecoa, en Judá, enviado a predicar en Betel contra la "
                       "injusticia social del reino de Israel. Oseas, llamado a casarse con una mujer "
                       "infiel como señal del amor de Dios, denunció el culto a Baal en Samaria, Betel, "
                       "Gilgal y Dan.",
        "bbox": (34.3, 30.8, 37.2, 33.8),
        "lugares": ["tekoa", "bethel-1", "gilgal-1", "dan", "beersheba-1", "samaria-1", "jezreel-2",
                    "jerusalem", "gaza", "asdod", "damascus", "heshbon", "jabesh-gilead",
                    "ramoth-gilead", "tekoa", "jordan", "salt-sea", "sea-of-galilee"],
        "regiones": ["israel", "judah", "gilead-1", "bashan", "moab-1", "ammon", "philistia",
                     "syria-1", "edom"],
        "refs": ["Amós 1:1", "Amós 7:10-17", "Oseas 1:2-9", "Oseas 4:1-19"],
    },
    {
        "id": "isaias-asiria",
        "titulo": "Isaias ante Asiria",
        "subtitulo": "Isaías 7-39",
        "categoria": "Profetas",
        "descripcion": "Isaías aconsejó a Acaz que no temiera a Siria e Israel, y a Ezequías que confiara "
                       "en Dios frente a Senaquerib. El profeta anunció el juicio sobre Asiria, la caída de "
                       "Babilonia y la restauración por medio de Ciro, nombrado siglos antes.",
        "bbox": (32.0, 28.5, 47.5, 38.5),
        "lugares": ["jerusalem", "samaria-1", "damascus", "arpad", "hamath-1", "carchemish",
                    "nineveh", "ashur", "babylon-1", "susa", "elam", "media", "sidon", "tyre",
                    "asdod", "ekron", "lachish", "libnah-1", "tahpanhes", "zoan", "nile",
                    "euphrates", "great-sea", "salt-sea"],
        "rutas": [{"nombre": "Campaña de Senaquerib (701 a.C.)", "color": "#a8320d",
                   "puntos": ["nineveh", "carchemish", "arpad", "hamath-1", "damascus", "sidon",
                              "asdod", "ekron", "lachish", "libnah-1", "jerusalem"]}],
        "regiones": ["assyria", "babylonia", "elam", "media", "syria-1", "philistia", "judea-1",
                     "israel", "moab-1", "ammon", "edom", "egypt"],
        "refs": ["Isaías 7:1-9", "Isaías 20:1-6", "Isaías 36-37", "Isaías 44:28-45:4"],
    },
    {
        "id": "sennacherib-701",
        "titulo": "La invasion de Senaquerib y el sitio de Laquis",
        "subtitulo": "2 Reyes 18-19; Isaías 36-37; 2 Crónicas 32",
        "categoria": "Profetas",
        "descripcion": "En el año 701 a.C. Senaquerib tomó las ciudades fuertes de Judá y sitió Laquis, "
                       "donde instaló su campamento; desde allí envió a su copero mayor a pedir la "
                       "rendición de Jerusalén. El profeta Isaías anunció la liberación, y el ejército "
                       "asirio se retiró.",
        "bbox": (34.4, 31.0, 36.4, 32.6),
        "lugares": ["lachish", "libnah-1", "ekron", "asdod", "timnah-1", "jerusalem", "bethlehem-1",
                    "hebron", "azekah", "moresheth-gath", "adullam", "jordan", "salt-sea",
                    "gaza", "ashkelon"],
        "regiones": ["philistia", "shephelah", "judea-1"],
        "notas": ["Los relieves asirios del palacio de Nínive, hoy en el Museo Británico, representan el "
                  "asedio de Laquis."],
        "refs": ["2 Reyes 18:13-16", "2 Reyes 19:32-36", "Isaías 37:33-38"],
    },
    {
        "id": "caida-samaria",
        "titulo": "La caida de Samaria (722 a.C.)",
        "subtitulo": "2 Reyes 17",
        "categoria": "Profetas",
        "descripcion": "Salmanasar V sitió Samaria durante tres años y Sargón II la tomó; las diez tribus "
                       "del norte fueron deportadas a Halah, Habor, Gozán y las ciudades de Media. Junto a "
                       "la deportación llegaron colonos extranjeros, origen de los samaritanos.",
        "bbox": (34.0, 30.8, 45.0, 38.5),
        "lugares": ["samaria-1", "siquem-1", "tirzah", "jezreel-2", "megiddo", "dan", "hazor-1",
                    "beth-shan", "jericho-1", "jerusalem", "nineveh", "ashur", "calah-1",
                    "gozan-1", "habor-1", "hala-1", "media", "damascus", "gaza", "tyre", "sidon"],
        "rutas": [{"nombre": "Deportación a Asiria", "color": "#a8320d",
                   "puntos": ["samaria-1", "damascus", "carchemish", "harran", "gozan-1", "nineveh",
                              "calah-1", "hala-1", "media"]}],
        "regiones": ["israel", "judah", "assyria", "syria-1", "gilead-1", "bashan", "philistia"],
        "refs": ["2 Reyes 17:1-6", "2 Reyes 17:24-41", "2 Reyes 18:9-12"],
    },
    {
        "id": "caida-jerusalen-586",
        "titulo": "La caida de Jerusalen (586 a.C.)",
        "subtitulo": "2 Reyes 24-25; Jeremías 39",
        "categoria": "Profetas",
        "descripcion": "Nabucodonosor sitió Jerusalén, rompió el muro, quemó el templo y el palacio y "
                       "deportó a Babilonia al rey Sedequías, cegado en Ribla. El gobernador Gedalías fue "
                       "asesinado y el resto del pueblo huyó a Egipto, llevando consigo a Jeremías a "
                       "Tafnes.",
        "bbox": (33.5, 28.5, 44.5, 36.0),
        "lugares": ["jerusalem", "lachish", "azekah", "libnah-1", "hebron", "riblah-1", "hamath-1",
                    "babylon-1", "damasco", "tahpanhes", "memphis", "gaza", "moab-1", "ammon",
                    "edom", "euphrates", "salt-sea", "great-sea", "nile"],
        "rutas": [{"nombre": "Deportación del 597 y 586 a.C.", "color": "#a8320d",
                   "puntos": ["jerusalem", "riblah-1", "hamath-1", "damascus", "carchemish", "babylon-1"]},
                  {"nombre": "Huida a Egipto", "color": "#5c7a29",
                   "puntos": ["jerusalem", "gaza", "tahpanhes", "memphis"]}],
        "regiones": ["judea-1", "moab-1", "ammon", "edom", "philistia", "syria-1", "babylonia",
                     "egypt"],
        "refs": ["2 Reyes 25:1-11", "2 Reyes 25:22-26", "Jeremías 43:5-7", "Lamentaciones 1:1-3"],
    },
    {
        "id": "exilio-babilonia",
        "titulo": "El destierro en Babilonia",
        "subtitulo": "Salmo 137; Ezequiel 1-3",
        "categoria": "Profetas",
        "descripcion": "Los desterrados de Judá se establecieron en Babilonia, junto al río Quebar y en "
                       "las aldeas de la región (Tel-abib, Casifia). Allí Ezequiel tuvo sus visiones y "
                       "Daniel sirvió en la corte. El salmo 137 recuerda el llanto «junto a los ríos de "
                       "Babilonia».",
        "bbox": (33.5, 29.0, 48.5, 36.5),
        "lugares": ["babylon-1", "chebar", "nippur-1", "ur-1", "eridu-1", "susa", "elam", "jerusalem",
                    "riblah-1", "hamath-1", "damasco", "euphrates", "tigris-1", "tel-aviv-1",
                    "nippur-1"],
        "rutas": [{"nombre": "Ruta del destierro", "color": "#a8320d",
                   "puntos": ["jerusalem", "riblah-1", "damasco", "carchemish", "babylon-1"]}],
        "regiones": ["babylonia", "chaldea", "assyria", "elam", "syria-1", "judea-1", "moab-1"],
        "refs": ["Salmo 137:1-4", "Ezequiel 1:1-3", "Ezequiel 3:15", "Daniel 1:1-7"],
    },
    {
        "id": "ezequiel-visiones",
        "titulo": "Las visiones de Ezequiel",
        "subtitulo": "Ezequiel 1; 8-11; 37; 40-48",
        "categoria": "Profetas",
        "descripcion": "Junto al río Quebar, entre los desterrados, Ezequiel vio la gloria de Dios sobre "
                       "el carro de los querubines. Después fue llevado en visión a Jerusalén, al templo "
                       "corrompido, y más tarde contempló el valle de los huesos secos y el templo futuro, "
                       "del que salía un río que sanaba las aguas del mar Muerto.",
        "bbox": (33.5, 29.0, 48.0, 36.5),
        "lugares": ["chebar", "babylon-1", "jerusalem", "tel-aviv-1", "ur-1", "temple-mount-1",
                    "salt-sea", "euphrates", "tigris-1", "nippur-1"],
        "regiones": ["babylonia", "chaldea", "judea-1", "syria-1"],
        "refs": ["Ezequiel 1:1-28", "Ezequiel 8:1-18", "Ezequiel 37:1-14", "Ezequiel 47:1-12"],
    },
    {
        "id": "daniel-imperios",
        "titulo": "Daniel y los imperios",
        "subtitulo": "Daniel 2; 7-8; 10-12",
        "categoria": "Profetas",
        "descripcion": "La estatua de Daniel 2 y las cuatro bestias de Daniel 7 representan la sucesión de "
                       "los imperios: Babilonia, Media y Persia, Grecia y Roma. Daniel sirvió en las cortes "
                       "de Nabucodonosor, Belsasar, Darío y Ciro, en Babilonia y en Susa.",
        "bbox": (34.0, 27.0, 54.0, 39.0),
        "lugares": ["babylon-1", "susa", "elam", "persia", "media", "ecbatana-1", "persepolis-1",
                    "jerusalem", "memphis", "ur-1", "nineveh", "hamath-1", "tigris-1", "euphrates",
                    "syene", "thebes"],
        "regiones": ["babylonia", "chaldea", "elam", "persia", "media", "assyria", "syria-1",
                     "judea-1", "egypt", "macedonia", "greece", "italy"],
        "refs": ["Daniel 2:36-45", "Daniel 7:1-8", "Daniel 8:20-22", "Daniel 10:1-14"],
    },
    {
        "id": "restauracion",
        "titulo": "El regreso del destierro",
        "subtitulo": "Esdras 1-6; Nehemías 1-2",
        "categoria": "Profetas",
        "descripcion": "Ciro decretó en el 538 a.C. el regreso de los judíos y la reconstrucción del "
                       "templo. Zorobabel dirigió el primer grupo, Esdras el segundo y Nehemías, copero del "
                       "rey Artajerjes, reedificó los muros de Jerusalén en cincuenta y dos días.",
        "bbox": (34.0, 29.0, 52.0, 36.5),
        "lugares": ["susa", "babylon-1", "elam", "jerusalem", "samaria-1", "jericho-1", "bethel-1",
                    "hebron", "tyre", "sidon", "damasco", "hamath-1", "carchemish", "euphrates",
                    "tigris-1", "salt-sea"],
        "rutas": [{"nombre": "Regreso (Zorobabel, Esdras, Nehemías)", "color": "#1f6f8b",
                   "puntos": ["susa", "babylon-1", "euphrates", "carchemish", "hamath-1", "damasco",
                              "jerusalem"]}],
        "regiones": ["babylonia", "elam", "persia", "judea-1", "samaria-2", "syria-1", "moab-1",
                     "edom", "ammon"],
        "refs": ["Esdras 1:1-11", "Esdras 3:8-13", "Nehemías 2:1-20", "Hageo 1:1-15"],
    },
    {
        "id": "ester-persia",
        "titulo": "Ester y el imperio persa",
        "subtitulo": "Ester 1-10",
        "categoria": "Profetas",
        "descripcion": "La historia de Ester transcurre en Susa, la capital invernal de los reyes persas, "
                       "durante el reinado de Asuero (Jerjes I). El imperio se extendía «desde la India "
                       "hasta Etiopía», con caminos reales y un sistema de correos que el libro menciona.",
        "bbox": (40.0, 25.0, 60.0, 40.0),
        "lugares": ["susa", "persia", "elam", "media", "ecbatana-1", "persepolis-1", "babylon-1",
                    "ur-1", "jerusalem", "tigris-1"],
        "regiones": ["persia", "elam", "media", "babylonia", "chaldea", "assyria"],
        "refs": ["Ester 1:1-9", "Ester 4:1-17", "Ester 9:20-32"],
    },
    {
        "id": "rut-moab",
        "titulo": "Rut la moabita",
        "subtitulo": "Rut 1-4",
        "categoria": "Profetas",
        "descripcion": "En los días de los jueces, Noemí y su familia emigraron de Belén a Moab por el "
                       "hambre. Rut se unió a Noemí («tu pueblo será mi pueblo»), espigó en los campos de "
                       "Booz y llegó a ser bisabuela de David, bisnieto de inmigrantes.",
        "bbox": (34.8, 30.9, 36.2, 32.2),
        "lugares": ["bethlehem-1", "hebron", "moab-1", "kir-hareseth-1", "arnon", "salt-sea",
                    "valley-of-siddim-1", "jerusalem", "jericho-1", "engedi"],
        "rutas": [{"nombre": "Ida y vuelta a Moab", "color": "#5c7a29",
                   "puntos": ["bethlehem-1", "engedi", "arnon", "kir-hareseth-1"]}],
        "regiones": ["moab-1", "judea-1", "edom", "ammon"],
        "refs": ["Rut 1:1-5", "Rut 1:16-18", "Rut 4:13-22", "Mateo 1:5"],
    },
    {
        "id": "nehemias-muros",
        "titulo": "Nehemias y la reconstruccion de los muros",
        "subtitulo": "Nehemías 2-6",
        "categoria": "Profetas",
        "descripcion": "Nehemías inspeccionó de noche los muros derruidos y organizó la obra por familias y "
                       "puertas: la de las Ovejas, la del Pescado, la Vieja, la del Valle, la del "
                       "Muladar, la de la Fuente, la del Agua y la de los Caballos. La obra se terminó en "
                       "cincuenta y dos días, con los obreros trabajando con la espada al cinto.",
        "bbox": (35.15, 31.71, 35.31, 31.83),
        "lugares": ["jerusalem", "jericho-1", "tekoa", "bethel-1", "gibeon", "gibeah-1", "anathoth"],
        "regiones": [],
        "refs": ["Nehemías 2:11-18", "Nehemías 3:1-32", "Nehemías 4:15-23", "Nehemías 6:15-16"],
    },
]
