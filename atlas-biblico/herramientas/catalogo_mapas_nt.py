# -*- coding: utf-8 -*-
"""
catalogo_mapas_nt.py — Mapas del Nuevo Testamento, de las ciudades y planos,
y el diccionario de lugares complementarios (sitios citados en los mapas que no
figuran en la base principal de lugares bíblicos; se dan con coordenadas
aproximadas conocidas y se marcan como tales).

Todas las descripciones están redactadas en español.
"""

# Lugares citados en los mapas que no están en Bible-Geocoding-Data.
# Las coordenadas son las de la identificación habitual de cada yacimiento.
EXTRA_LUGARES = {
    "ashur": {"n": "Assur", "lon": 43.26, "lat": 35.46, "tipo": "ciudad o poblado"},
    "calah-1": {"n": "Calaj", "lon": 43.33, "lat": 36.10, "tipo": "ciudad o poblado"},
    "dur-sharrukin-1": {"n": "Dur-Sharrukin", "lon": 43.23, "lat": 36.51, "tipo": "ciudad o poblado"},
    "eridu-1": {"n": "Eridú", "lon": 45.99, "lat": 30.81, "tipo": "ciudad o poblado"},
    "kish-1": {"n": "Kish", "lon": 44.60, "lat": 32.55, "tipo": "ciudad o poblado"},
    "nippur-1": {"n": "Nippur", "lon": 45.23, "lat": 32.13, "tipo": "ciudad o poblado"},
    "alepo-1": {"n": "Alepo", "lon": 37.16, "lat": 36.20, "tipo": "ciudad o poblado"},
    "tadmor-1": {"n": "Tadmor", "lon": 38.28, "lat": 34.55, "tipo": "ciudad o poblado"},
    "tigris-1": {"n": "Río Tigris", "lon": 43.20, "lat": 34.30, "tipo": "río"},
    "gozan-1": {"n": "Gozán", "lon": 40.05, "lat": 36.84, "tipo": "ciudad o poblado"},
    "habor-1": {"n": "Río Habor", "lon": 40.70, "lat": 36.80, "tipo": "río"},
    "hala-1": {"n": "Halah", "lon": 43.50, "lat": 35.80, "tipo": "ciudad o poblado"},
    "rameses-1": {"n": "Ramesés", "lon": 30.80, "lat": 30.80, "tipo": "ciudad o poblado"},
    "pithom-1": {"n": "Pitón", "lon": 32.05, "lat": 30.55, "tipo": "ciudad o poblado"},
    "sucot-3": {"n": "Sucot", "lon": 32.19, "lat": 30.55, "tipo": "ciudad o poblado"},
    "migdol-1": {"n": "Migdol", "lon": 32.35, "lat": 31.10, "tipo": "fortaleza"},
    "dophka-1": {"n": "Dofca", "lon": 33.05, "lat": 29.05, "tipo": "campamento"},
    "sin-2": {"n": "Desierto de Sin", "lon": 33.35, "lat": 29.35, "tipo": "desierto"},
    "saint-catherine-1": {"n": "Santa Catalina", "lon": 33.95, "lat": 28.55, "tipo": "monte"},
    "mount-ararat-1": {"n": "Monte Ararat", "lon": 44.30, "lat": 39.70, "tipo": "monte"},
    "punon-1": {"n": "Punón", "lon": 35.42, "lat": 30.62, "tipo": "campamento"},
    "boser-1": {"n": "Beser", "lon": 35.87, "lat": 31.72, "tipo": "ciudad o poblado"},
    "golan-1": {"n": "Golán", "lon": 35.78, "lat": 32.90, "tipo": "ciudad o poblado"},
    "madon-1": {"n": "Madón", "lon": 35.42, "lat": 32.79, "tipo": "ciudad o poblado"},
    "merom-1": {"n": "Aguas de Merom", "lon": 35.60, "lat": 33.06, "tipo": "mar o lago"},
    "kir-hareseth-1": {"n": "Kir-hareset", "lon": 35.68, "lat": 31.18, "tipo": "ciudad o poblado"},
    "gath-hepher-1": {"n": "Gat-hefer", "lon": 35.25, "lat": 32.74, "tipo": "ciudad o poblado"},
    "dotan-1": {"n": "Dotán", "lon": 35.24, "lat": 32.41, "tipo": "ciudad o poblado"},
    "tel-aviv-1": {"n": "Tel-abib", "lon": 44.90, "lat": 32.30, "tipo": "ciudad o poblado"},
    "temple-mount-1": {"n": "Explanada del Templo", "lon": 35.2354, "lat": 31.7780, "tipo": "fortaleza"},
    "persepolis-1": {"n": "Persépolis", "lon": 52.89, "lat": 29.94, "tipo": "ciudad o poblado"},
    "pasargadae-1": {"n": "Pasargada", "lon": 53.18, "lat": 30.19, "tipo": "ciudad o poblado"},
    "ecbatana-1": {"n": "Ecbatana", "lon": 48.51, "lat": 34.80, "tipo": "ciudad o poblado"},
    "granicus-1": {"n": "Río Granico", "lon": 27.15, "lat": 40.25, "tipo": "río"},
    "issus-1": {"n": "Issos", "lon": 36.17, "lat": 36.75, "tipo": "ciudad o poblado"},
    "byzantium-1": {"n": "Bizancio", "lon": 28.98, "lat": 41.01, "tipo": "ciudad o poblado"},
    "philadelphia-1": {"n": "Filadelfia", "lon": 28.45, "lat": 38.35, "tipo": "ciudad o poblado"},
    "nicopolis-1": {"n": "Nicópolis", "lon": 20.75, "lat": 39.02, "tipo": "ciudad o poblado"},
    "colossae-1": {"n": "Colosas", "lon": 29.24, "lat": 37.79, "tipo": "ciudad o poblado"},
    "hierapolis-1": {"n": "Hierápolis", "lon": 29.13, "lat": 37.93, "tipo": "ciudad o poblado"},
    "magdala-1": {"n": "Magdala", "lon": 35.58, "lat": 32.83, "tipo": "ciudad o poblado"},
    "chorazin-1": {"n": "Corazín", "lon": 35.55, "lat": 32.91, "tipo": "ciudad o poblado"},
    "nain-1": {"n": "Naín", "lon": 35.35, "lat": 32.63, "tipo": "ciudad o poblado"},
    "gadara-1": {"n": "Gadara", "lon": 35.68, "lat": 32.65, "tipo": "ciudad o poblado"},
    "caesarea-philippi": {"n": "Cesarea de Filipo", "lon": 35.70, "lat": 33.25, "tipo": "ciudad o poblado"},
    "bethesda-1": {"n": "Betesda", "lon": 35.2360, "lat": 31.7810, "tipo": "estanque"},
    "gethsemane-1": {"n": "Getsemaní", "lon": 35.2400, "lat": 31.7794, "tipo": "huerto"},
    "cenaculo-1": {"n": "Cenáculo (sala alta)", "lon": 35.2290, "lat": 31.7710, "tipo": "sala"},
    "golgota-1": {"n": "Gólgota (Calvario)", "lon": 35.2295, "lat": 31.7784, "tipo": "colina"},
    "sepulcro-1": {"n": "Santo Sepulcro", "lon": 35.2297, "lat": 31.7784, "tipo": "sepulcro"},
    "betania-jordan-1": {"n": "Betania del Jordán", "lon": 35.55, "lat": 31.84, "tipo": "ciudad o poblado"},
    "aenon-1": {"n": "Enón, junto a Salim", "lon": 35.40, "lat": 32.36, "tipo": "manantial"},
    "bienaventuranzas-1": {"n": "Monte de las Bienaventuranzas", "lon": 35.5556, "lat": 32.8808, "tipo": "monte"},
    "ascension-1": {"n": "Monte de la Ascensión", "lon": 35.2456, "lat": 31.7792, "tipo": "colina"},
    "ason-1": {"n": "Asón", "lon": 26.35, "lat": 39.49, "tipo": "puerto"},
    "mitilene-1": {"n": "Mitilene", "lon": 26.55, "lat": 39.10, "tipo": "puerto"},
    "quios-1": {"n": "Quío", "lon": 26.14, "lat": 38.37, "tipo": "isla"},
    "samos-1": {"n": "Samos", "lon": 26.98, "lat": 37.70, "tipo": "isla"},
    "cnido-1": {"n": "Cnido", "lon": 27.37, "lat": 36.68, "tipo": "puerto"},
    "mira-1": {"n": "Mira", "lon": 29.98, "lat": 36.26, "tipo": "puerto"},
    "buenos-puertos-1": {"n": "Buenos Puertos", "lon": 24.72, "lat": 34.93, "tipo": "puerto"},
    "fenice-1": {"n": "Fénix", "lon": 23.90, "lat": 35.20, "tipo": "puerto"},
    "puteoli-1": {"n": "Puteoli", "lon": 14.12, "lat": 40.83, "tipo": "puerto"},
    "foro-apio-1": {"n": "Foro de Apio", "lon": 12.83, "lat": 41.47, "tipo": "camino"},
    "tres-tabernas-1": {"n": "Tres Tabernas", "lon": 12.80, "lat": 41.67, "tipo": "camino"},
    "regio-1": {"n": "Regio", "lon": 15.65, "lat": 38.11, "tipo": "puerto"},
    "antipatris-1": {"n": "Antípatris", "lon": 34.93, "lat": 32.10, "tipo": "ciudad o poblado"},
    "guerar-1": {"n": "Guerar", "lon": 34.61, "lat": 31.38, "tipo": "ciudad o poblado"},
    "gaza-antigua-1": {"n": "Gaza antigua", "lon": 34.47, "lat": 31.47, "tipo": "ciudad o poblado"},
    "ascension-jerusalen-1": {"n": "Jerusalén (Hechos 1)", "lon": 35.2342, "lat": 31.7767, "tipo": "ciudad o poblado"},
    "monte-guerizin-1": {"n": "Monte Gerizim", "lon": 35.27, "lat": 32.20, "tipo": "monte"},
    "sicar-1": {"n": "Sicar", "lon": 35.28, "lat": 32.21, "tipo": "ciudad o poblado"},
    "emaus-nicopolis-1": {"n": "Emaús", "lon": 34.98, "lat": 31.84, "tipo": "ciudad o poblado"},
    "betania-galilea-1": {"n": "Betania", "lon": 35.57, "lat": 32.86, "tipo": "ciudad o poblado"},
    "armagedon-1": {"n": "Armagedón", "lon": 35.18, "lat": 32.58, "tipo": "valle"},
    "nilo-delta-1": {"n": "Delta del Nilo", "lon": 31.20, "lat": 30.90, "tipo": "región"},
    "elefantina-1": {"n": "Elefantina", "lon": 32.88, "lat": 24.09, "tipo": "isla"},
    "ain-karem-1": {"n": "Ain Karem", "lon": 35.16, "lat": 31.77, "tipo": "aldea"},
    "maqueronte-1": {"n": "Maqueronte", "lon": 35.62, "lat": 31.60, "tipo": "fortaleza"},
    "qumran-1": {"n": "Qumrán", "lon": 35.46, "lat": 31.74, "tipo": "ruinas"},
    "azoto-1": {"n": "Azoto", "lon": 34.65, "lat": 31.79, "tipo": "ciudad o poblado"},
    "cencreas-1": {"n": "Cencreas", "lon": 22.99, "lat": 37.89, "tipo": "puerto"},
    "samotracia-1": {"n": "Samotracia", "lon": 25.53, "lat": 40.50, "tipo": "isla"},
    "areopago-1": {"n": "Areópago", "lon": 23.7236, "lat": 37.9722, "tipo": "colina"},
    "ataleia-1": {"n": "Atalia", "lon": 30.70, "lat": 36.88, "tipo": "puerto"},
    "bitinia-1": {"n": "Bitinia", "lon": 31.00, "lat": 40.50, "tipo": "región"},
    "capadocia-1": {"n": "Capadocia", "lon": 35.00, "lat": 38.70, "tipo": "región"},
    "seforis-1": {"n": "Séforis", "lon": 35.28, "lat": 32.75, "tipo": "ciudad o poblado"},
    "millo-1": {"n": "Milo", "lon": 35.2342, "lat": 31.7733, "tipo": "fortaleza"},
    "topheth-1": {"n": "Tofet", "lon": 35.2281, "lat": 31.7692, "tipo": "altar"},
    "arbela-1": {"n": "Arbela", "lon": 35.42, "lat": 32.72, "tipo": "fortaleza"},
    "perea-1": {"n": "Perea", "lon": 35.75, "lat": 31.85, "tipo": "región"},
    "gaulanitis-1": {"n": "Gaulanítide", "lon": 35.90, "lat": 32.90, "tipo": "región"},
    "trachonitis-1": {"n": "Traconítide", "lon": 36.30, "lat": 32.90, "tipo": "región"},
    "pisidia-1": {"n": "Pisidia", "lon": 30.60, "lat": 37.60, "tipo": "región"},
    "lycaonia-1": {"n": "Licaonia", "lon": 32.80, "lat": 37.60, "tipo": "región"},
    "pafos-1": {"n": "Pafos", "lon": 32.42, "lat": 34.77, "tipo": "puerto"},
    "attalia-1": {"n": "Atalia", "lon": 30.70, "lat": 36.88, "tipo": "puerto"},
    "fenice-2": {"n": "Fenicia", "lon": 35.30, "lat": 33.40, "tipo": "región"},
    "phoenicia-1": {"n": "Fenicia", "lon": 35.30, "lat": 33.40, "tipo": "región"},
    "neapolis-1": {"n": "Neápolis", "lon": 24.42, "lat": 40.94, "tipo": "puerto"},
    "mitylene-2": {"n": "Mitilene", "lon": 26.55, "lat": 39.10, "tipo": "puerto"},
    "samos-2": {"n": "Samos", "lon": 26.98, "lat": 37.70, "tipo": "isla"},
    "lydia-1": {"n": "Lidia", "lon": 28.20, "lat": 38.60, "tipo": "región"},
    "mysia-1": {"n": "Misia", "lon": 28.00, "lat": 39.60, "tipo": "región"},
    "ionia-1": {"n": "Jonia", "lon": 27.30, "lat": 38.20, "tipo": "región"},
    "chalda-1": {"n": "Caldea", "lon": 46.10, "lat": 30.96, "tipo": "región"},
    "ponto-1": {"n": "Ponto", "lon": 37.83, "lat": 40.68, "tipo": "región"},
    "crete-2": {"n": "Creta", "lon": 24.89, "lat": 35.31, "tipo": "isla"},
    "sicilia-1": {"n": "Sicilia", "lon": 14.50, "lat": 37.50, "tipo": "isla"},
    "ephrain-1": {"n": "Efraín", "lon": 35.35, "lat": 31.88, "tipo": "ciudad o poblado"},
    "jerusalen-1": {"n": "Jerusalén", "lon": 35.2342, "lat": 31.7767, "tipo": "ciudad o poblado"},
}

JUDEA = [
    {
        "id": "nacimiento-de-jesus",
        "titulo": "El nacimiento de Jesus",
        "subtitulo": "Lucas 1-2; Mateo 1-2",
        "categoria": "Vida de Jesús",
        "descripcion": "El ángel Gabriel anunció a María en Nazaret el nacimiento virginal; Jesús nació en "
                       "Belén de Judá, «la ciudad de David», y fue adorado por pastores y por magos de "
                       "oriente que llegaron siguiendo una estrella.",
        "bbox": (34.6, 31.2, 36.2, 32.5),
        "lugares": ["nazareth", "bethlehem-1", "jerusalem", "hebron", "ain-karem-1", "beth-zur-1",
                    "jericho-1", "capernaum", "egipto-2", "gaza", "joppa"],
        "regiones": ["judea-1", "samaria-2", "galilee-1", "philistia"],
        "refs": ["Lucas 1:26-38", "Lucas 2:1-20", "Mateo 2:1-12"],
    },
    {
        "id": "huida-a-egipto",
        "titulo": "La huida a Egipto y el regreso",
        "subtitulo": "Mateo 2:13-23",
        "categoria": "Vida de Jesús",
        "descripcion": "José, avisado en sueños, huyó con María y el niño a Egipto para escapar de Herodes "
                       "el Grande, que mandó matar a los niños de Belén. Al morir Herodes, la familia "
                       "regresó, pero se estableció en Nazaret de Galilea por temor a Arquelao.",
        "bbox": (29.5, 28.5, 36.5, 33.0),
        "lugares": ["bethlehem-1", "gaza", "tahpanhes", "memphis", "heliopolis", "goshen-1",
                    "nile", "nazareth", "jerusalem", "antipatris-1"],
        "rutas": [{"nombre": "Ida a Egipto", "color": "#a8320d",
                   "puntos": ["bethlehem-1", "gaza", "antipatris-1", "tahpanhes", "memphis", "heliopolis"]},
                  {"nombre": "Regreso a Nazaret", "color": "#1f6f8b", "estilo": "punteada",
                   "puntos": ["heliopolis", "memphis", "tahpanhes", "gaza", "nazareth"]}],
        "regiones": ["egypt", "judea-1", "philistia", "negeb", "goshen-2"],
        "refs": ["Mateo 2:13-15", "Mateo 2:19-23", "Oseas 11:1"],
    },
    {
        "id": "juan-bautista",
        "titulo": "Juan el Bautista y el desierto de Judea",
        "subtitulo": "Lucas 3:1-20; Juan 1:19-34",
        "categoria": "Vida de Jesús",
        "descripcion": "Juan, hijo de Zacarías y Elisabet, predicó en el desierto de Judea y bautizó en el "
                       "Jordán, en Betania y en Enón junto a Salim. Su mensaje de arrepentimiento y su "
                       "denuncia de Herodes Antipas lo llevaron a la prisión en Maqueronte.",
        "bbox": (34.6, 31.0, 36.4, 32.5),
        "lugares": ["betania-jordan-1", "aenon-1", "jordan", "jericho-1", "jerusalem",
                    "bethlehem-1", "hebron", "engedi", "salt-sea", "maqueronte-1", "qumran-1",
                    "wilderness-of-sinai"],
        "regiones": ["judea-1", "samaria-2", "perea-1", "moab-1"],
        "refs": ["Mateo 3:1-6", "Juan 1:28", "Juan 3:23", "Marcos 6:17-29"],
    },
    {
        "id": "bautismo-tentacion",
        "titulo": "El bautismo y la tentacion de Jesus",
        "subtitulo": "Mateo 3:13-4:11",
        "categoria": "Vida de Jesús",
        "descripcion": "Jesús fue bautizado por Juan en el Jordán y el Espíritu descendió sobre él como "
                       "paloma. Después, llevado por el Espíritu al desierto de Judea, ayunó cuarenta días "
                       "y fue tentado.",
        "bbox": (34.9, 31.4, 35.9, 32.2),
        "lugares": ["betania-jordan-1", "jordan", "jericho-1", "jerusalem", "jeshimon", "engedi",
                    "adummim-1", "bethany-1", "gethsemane-1"],
        "regiones": ["judea-1", "perea-1"],
        "refs": ["Mateo 3:13-17", "Mateo 4:1-11", "Lucas 4:1-13"],
    },
    {
        "id": "galilea-ministerio",
        "titulo": "El ministerio en Galilea",
        "subtitulo": "Mateo 4:12-18:35; Marcos 1-9",
        "categoria": "Vida de Jesús",
        "descripcion": "Jesús dejó Nazaret y se estableció en Cafarnaún, «junto al mar, en la frontera de "
                       "Zabulón y Neftalí». Recorrió toda Galilea enseñando en las sinagogas, llamó a sus "
                       "discípulos junto al lago y pasó a la otra orilla, a la región de los gadarenos.",
        "bbox": (35.0, 32.4, 36.0, 33.5),
        "lugares": ["nazareth", "cana", "capernaum", "chorazin-1", "magdala-1", "bethsaida-2",
                    "bienaventuranzas-1", "nain-1", "gadara-1", "gerasa", "sea-of-galilee",
                    "gennesaret", "mount-tabor", "daberath", "caesarea-philippi", "dan",
                    "hazor-1", "jordan", "bienaventuranzas-1", "arbela-1"],
        "regiones": ["galilee-1", "decapolis", "gaulanitis-1", "trachonitis-1"],
        "refs": ["Mateo 4:12-17", "Marcos 1:21-34", "Lucas 4:14-22", "Juan 2:1-11"],
    },
    {
        "id": "mar-de-galilea",
        "titulo": "El lago de Galilea",
        "subtitulo": "Marcos 4-6; Lucas 8",
        "categoria": "Vida de Jesús",
        "descripcion": "El lago de Genesaret, a 210 m bajo el nivel del mar, es escenario de gran parte del "
                       "ministerio de Jesús: la tempestad calmada, la pesca milagrosa, la multiplicación de "
                       "los panes y el caminar sobre las aguas, entre Cafarnaún, Betsaida y Genesaret.",
        "bbox": (35.40, 32.62, 35.78, 32.98),
        "lugares": ["capernaum", "magdala-1", "bethsaida-2", "chorazin-1", "genesaret", "gerasa",
                    "gadara-1", "sea-of-galilee", "jordan"],
        "regiones": ["galilee-1", "decapolis", "gaulanitis-1"],
        "notas": ["Por sus aguas dulces abundantes en peces, la región sostenía una activa industria "
                  "pesquera administrada desde Cafarnaún."],
        "refs": ["Marcos 4:35-41", "Lucas 5:1-11", "Juan 6:1-21", "Mateo 14:34-36"],
    },
    {
        "id": "sermon-del-monte",
        "titulo": "El Sermon del Monte",
        "subtitulo": "Mateo 5-7",
        "categoria": "Vida de Jesús",
        "descripcion": "Jesús subió a un monte junto al lago y pronunció el discurso más conocido del "
                       "evangelio: las bienaventuranzas, el padrenuestro y la regla de oro. Las "
                       "bienaventuranzas se recuerdan en el monte que lleva su nombre, frente a Cafarnaún.",
        "bbox": (35.42, 32.70, 35.72, 32.95),
        "lugares": ["bienaventuranzas-1", "capernaum", "magdala-1", "genesaret", "sea-of-galilee",
                    "daberath", "nain-1"],
        "regiones": ["galilee-1"],
        "refs": ["Mateo 5:1-16", "Mateo 6:9-13", "Mateo 7:24-29", "Lucas 6:20-49"],
    },
    {
        "id": "viaje-final-jerusalen",
        "titulo": "El ultimo viaje a Jerusalen",
        "subtitulo": "Lucas 9:51-19:28; Juan 7-11",
        "categoria": "Vida de Jesús",
        "descripcion": "«Cuando se cumplieron los días de su ascensión, Jesús volvió su rostro para ir a "
                       "Jerusalén.» Pasó por Samaria y por Perea, al otro lado del Jordán, y subió por "
                       "Jericó, donde sanó a Bartimeo y visitó a Zaqueo. En Betania resucitó a Lázaro.",
        "bbox": (34.9, 31.2, 36.0, 32.9),
        "lugares": ["capernaum", "nazareth", "samaria-1", "sicar-1", "jerusalem", "jericho-1",
                    "bethany-1", "bethphage", "mount-of-olives", "betania-jordan-1", "jordan",
                    "salt-sea", "sea-of-galilee", "emaus-nicopolis-1", "ephrain-1"],
        "rutas": [{"nombre": "Camino de Jesús (Lucas)", "color": "#a8320d",
                   "puntos": ["capernaum", "nazareth", "samaria-1", "sicar-1", "jericho-1",
                              "bethany-1", "mount-of-olives", "jerusalem"]}],
        "regiones": ["galilee-1", "samaria-2", "judea-1", "perea-1"],
        "refs": ["Lucas 9:51", "Lucas 18:35-19:10", "Juan 11:1-44", "Juan 4:4-6"],
    },
    {
        "id": "ultima-semana",
        "titulo": "La ultima semana en Jerusalen",
        "subtitulo": "Mateo 21-27; Marcos 11-15; Lucas 19-23; Juan 12-19",
        "categoria": "Vida de Jesús",
        "descripcion": "Jesús entró en Jerusalén desde Betfagé y el monte de los Olivos, entre aclamaciones "
                       "con ramos de olivo. Limpió el templo, celebró la última cena, oró en Getsemaní, fue "
                       "arrestado junto al Cedrón y juzgado por Caifás y por Pilato.",
        "bbox": (35.15, 31.72, 35.30, 31.83),
        "lugares": ["bethphage", "bethany-1", "mount-of-olives", "gethsemane-1", "kidron",
                    "jerusalem", "temple-mount-1", "golgota-1", "bethesda-1", "siloam", "cenaculo-1",
                    "zion", "city-of-david", "valley-of-hinnom"],
        "refs": ["Marcos 11:1-11", "Marcos 14:32-52", "Lucas 22:39-53", "Juan 18:1-14"],
    },
    {
        "id": "crucifixion-resurreccion",
        "titulo": "Crucifixion, resurreccion y ascension",
        "subtitulo": "Mateo 27:32-28:20; Lucas 23:26-24:53; Hechos 1",
        "categoria": "Vida de Jesús",
        "descripcion": "Jesús fue crucificado en el Gólgota, junto a la puerta de la ciudad, y sepultado en "
                       "un sepulcro nuevo. Al tercer día resucitó; se apareció a las mujeres, a los "
                       "discípulos de Emaús y a los once en Galilea, y cuarenta días después ascendió desde "
                       "el monte de los Olivos.",
        "bbox": (34.8, 31.3, 35.6, 32.4),
        "lugares": ["jerusalem", "golgota-1", "sepulcro-1", "mount-of-olives", "ascension-1",
                    "bethany-1", "bethphage", "emmaus", "emaus-nicopolis-1", "bethlehem-1",
                    "gaza", "joppa", "sea-of-galilee", "bienaventuranzas-1", "siloam"],
        "refs": ["Lucas 23:33-46", "Lucas 24:13-35", "Mateo 28:16-20", "Hechos 1:9-12"],
    },
    {
        "id": "iglesia-primitiva",
        "titulo": "La iglesia primitiva",
        "subtitulo": "Hechos 1-11",
        "categoria": "Hechos y Pablo",
        "descripcion": "En Pentecostés el Espíritu descendió sobre los discípulos reunidos en Jerusalén. La "
                       "iglesia creció allí, y la persecución la dispersó por Judea y Samaria: Felipe "
                       "bautizó al etíope en el camino de Gaza, Pedro sanó en Lida y resucitó a Tabita en "
                       "Jope, y Cornelio fue bautizado en Cesarea. En Antioquía se llamó cristianos por "
                       "primera vez a los discípulos.",
        "bbox": (34.3, 31.0, 37.5, 33.6),
        "lugares": ["jerusalem", "bethany-1", "gaza", "lod", "joppa", "caesarea", "samaria-1",
                    "sicar-1", "antioch-1", "damasco", "temple-mount-1", "azoto-1", "tarsus",
                    "seleucia-1", "emaus-nicopolis-1", "bethlehem-1"],
        "rutas": [{"nombre": "Dispersión tras la persecución", "color": "#1f6f8b", "estilo": "punteada",
                   "puntos": ["jerusalem", "samaria-1", "caesarea", "joppa", "gaza"]},
                  {"nombre": "Felipe en el camino de Gaza", "color": "#5c7a29",
                   "puntos": ["jerusalem", "bethlehem-1", "gaza", "azoto-1", "caesarea"]}],
        "regiones": ["judea-1", "samaria-2", "galilee-1", "syria-1", "philistia", "perea-1"],
        "refs": ["Hechos 2:1-13", "Hechos 8:4-40", "Hechos 9:32-43", "Hechos 11:19-26"],
    },
    {
        "id": "viajes-pablo-1",
        "titulo": "El primer viaje misionero de Pablo",
        "subtitulo": "Hechos 13-14 (46-48 d.C.)",
        "categoria": "Hechos y Pablo",
        "descripcion": "Enviados desde Antioquía de Siria, Pablo y Bernabé embarcaron en Seleucia, "
                       "predicaron en Salamina y Pafos (Chipre), y subieron a Perge y Antioquía de "
                       "Pisidia. En Iconio, Listra y Derbe los persiguieron; en Listra Pablo fue apedreado. "
                       "Volvieron por donde habían ido para confirmar a las iglesias.",
        "bbox": (29.5, 31.5, 39.5, 39.5),
        "lugares": ["antioch-1", "seleucia-1", "salamis", "paphos", "perga", "antioch-2", "iconium",
                    "lystra", "derbe", "tarsus", "attalia-1", "cyprus", "cirene-1", "pisidia-1",
                    "lycaonia-1", "pafos-1"],
        "rutas": [{"nombre": "Primer viaje", "color": "#a8320d",
                   "puntos": ["antioch-1", "seleucia-1", "salamis", "paphos", "perga", "antioch-2",
                              "iconium", "lystra", "derbe", "lystra", "iconium", "antioch-2",
                              "perga", "attalia-1", "antioch-1"]}],
        "regiones": ["syria-1", "cilicia", "galatia", "pamphylia-1", "phrygia", "asia"],
        "refs": ["Hechos 13:1-12", "Hechos 14:1-23", "Hechos 14:24-28"],
    },
    {
        "id": "concilio-jerusalen",
        "titulo": "El concilio de Jerusalen",
        "subtitulo": "Hechos 15:1-35 (49 d.C.)",
        "categoria": "Hechos y Pablo",
        "descripcion": "Surgió una disputa en Antioquía sobre la circuncisión de los gentiles. Pablo, "
                       "Bernabé, Tito y otros subieron a Jerusalén, donde Pedro, Santiago y los ancianos "
                       "decidieron no imponer a los gentiles la ley ceremonial, y les enviaron una carta "
                       "con cuatro recomendaciones.",
        "bbox": (34.5, 31.2, 37.5, 34.0),
        "lugares": ["antioch-1", "jerusalem", "sidon", "tyre", "caesarea", "samaria-1", "damasco",
                    "fenice-2", "temple-mount-1"],
        "rutas": [{"nombre": "Viaje al concilio", "color": "#1f6f8b",
                   "puntos": ["antioch-1", "fenice-2", "samaria-1", "jerusalem"]},
                  {"nombre": "Regreso con la carta", "color": "#5c7a29", "estilo": "punteada",
                   "puntos": ["jerusalem", "antioch-1"]}],
        "regiones": ["syria-1", "judea-1", "samaria-2", "phoenicia-1"],
        "refs": ["Hechos 15:1-11", "Hechos 15:22-29", "Gálatas 2:1-10"],
    },
    {
        "id": "viajes-pablo-2",
        "titulo": "El segundo viaje misionero: el evangelio en Europa",
        "subtitulo": "Hechos 15:36-18:22 (49-52 d.C.)",
        "categoria": "Hechos y Pablo",
        "descripcion": "Pablo y Silas recorrieron Siria y Cilicia, y en Listra se les unió Timoteo. "
                       "Impedidos de ir a Asia, pasaron a Troas y de allí a Filipos, donde se bautizaron "
                       "Lidia y el carcelero. Siguieron por Tesalónica y Berea hasta Atenas, donde Pablo "
                       "habló en el Areópago, y se detuvo año y medio en Corinto.",
        "bbox": (18.0, 33.0, 38.0, 42.0),
        "lugares": ["antioch-1", "tarsus", "derbe", "lystra", "iconium", "troas", "philippi",
                    "thessalonica", "berea", "athens", "corinth", "ephesus", "caesarea", "jerusalem",
                    "antioch-1", "neapolis-1", "samotracia-1", "cencreas-1", "areopago-1"],
        "rutas": [{"nombre": "Segundo viaje", "color": "#a8320d",
                   "puntos": ["antioch-1", "tarsus", "derbe", "lystra", "iconium", "troas",
                              "neapolis-1", "philippi", "thessalonica", "berea", "athens", "corinth",
                              "cencreas-1", "ephesus", "caesarea", "jerusalem", "antioch-1"]}],
        "regiones": ["syria-1", "cilicia", "galatia", "asia", "macedonia", "greece", "achaia"],
        "refs": ["Hechos 16:9-15", "Hechos 17:16-34", "Hechos 18:1-11", "Hechos 18:22"],
    },
    {
        "id": "viajes-pablo-3",
        "titulo": "El tercer viaje misionero y Efeso",
        "subtitulo": "Hechos 18:23-21:16 (53-57 d.C.)",
        "categoria": "Hechos y Pablo",
        "descripcion": "Pablo recorrió Galacia y Frigia y se estableció tres años en Éfeso, donde el "
                       "evangelio transformó la ciudad: los libros de magia se quemaron y los plateros, "
                       "arruinados, provocaron un motín en el teatro. Después visitó Macedonia y Grecia y "
                       "regresó a Jerusalén, despidiéndose de los ancianos de Éfeso en Mileto.",
        "bbox": (18.0, 31.0, 38.0, 42.0),
        "lugares": ["antioch-1", "ephesus", "troas", "philippi", "thessalonica", "berea", "corinth",
                    "miletus", "caesarea", "jerusalem", "colossae-1", "laodicea", "hierapolis-1",
                    "galatia", "ason-1", "mitylene-2", "samos-2", "miletus"],
        "rutas": [{"nombre": "Tercer viaje", "color": "#a8320d",
                   "puntos": ["antioch-1", "tarsus", "iconium", "ephesus", "troas", "philippi",
                              "thessalonica", "berea", "corinth", "miletus", "caesarea", "jerusalem"]}],
        "regiones": ["syria-1", "galatia", "asia", "macedonia", "greece", "achaia", "judea-1",
                     "cilicia", "phrygia"],
        "refs": ["Hechos 19:8-20", "Hechos 20:17-38", "Hechos 21:8-16"],
    },
    {
        "id": "viaje-a-roma",
        "titulo": "Pablo, prisionero, camino de Roma",
        "subtitulo": "Hechos 21:27-28:31 (57-60 d.C.)",
        "categoria": "Hechos y Pablo",
        "descripcion": "Detenido en Jerusalén y juzgado en Cesarea ante Félix, Festo y Agripa, Pablo "
                       "apeló al César. Embarcó hacia Roma, sufrió un naufragio de catorce días y llegó a "
                       "la isla de Malta, desde donde siguió por Siracusa, Puteoli y el Foro de Apio hasta "
                       "Roma, donde predicó dos años sin impedimento.",
        "bbox": (-2.0, 30.0, 38.0, 43.0),
        "lugares": ["jerusalem", "caesarea", "sidon", "mira-1", "cnido-1", "buenos-puertos-1",
                    "fenice-1", "malta", "syracuse", "regio-1", "puteoli-1", "foro-apio-1",
                    "tres-tabernas-1", "rome", "myra-1", "crete", "tres-tabernas-1"],
        "rutas": [{"nombre": "Viaje y naufragio", "color": "#a8320d",
                   "puntos": ["caesarea", "sidon", "myra-1", "cnido-1", "buenos-puertos-1",
                              "malta", "syracuse", "regio-1", "puteoli-1", "foro-apio-1",
                              "tres-tabernas-1", "rome"]}],
        "regiones": ["judea-1", "syria-1", "cilicia", "asia", "crete-2", "italy", "sicilia-1"],
        "refs": ["Hechos 25:11-12", "Hechos 27:27-44", "Hechos 28:11-16", "Hechos 28:30-31"],
    },
    {
        "id": "siete-iglesias",
        "titulo": "Las siete iglesias del Apocalipsis",
        "subtitulo": "Apocalipsis 2-3",
        "categoria": "Hechos y Pablo",
        "descripcion": "Juan escribió desde la isla de Patmos a siete iglesias de la provincia de Asia: "
                       "Éfeso, Esmirna, Pérgamo, Tiatira, Sardis, Filadelfia y Laodicea. Las siete estaban "
                       "unidas por los caminos romanos y por la ruta postal que recorría el valle del "
                       "Lico y la costa del Egeo.",
        "bbox": (25.5, 36.8, 30.5, 39.8),
        "lugares": ["patmos", "ephesus", "smyrna", "pergamum", "thyatira", "sardis",
                    "philadelphia-1", "laodicea", "miletus", "troas", "colossae-1", "hierapolis-1",
                    "smyrna", "ataleia-1"],
        "rutas": [{"nombre": "Ruta de las siete iglesias", "color": "#a8320d",
                   "puntos": ["ephesus", "smyrna", "pergamum", "thyatira", "sardis",
                              "philadelphia-1", "laodicea"]}],
        "regiones": ["asia", "lydia-1", "mysia-1", "ionia-1"],
        "refs": ["Apocalipsis 1:9-11", "Apocalipsis 2:1-7", "Apocalipsis 3:14-22"],
    },
    {
        "id": "apocalipsis-armagedon",
        "titulo": "Las visiones del Apocalipsis",
        "subtitulo": "Apocalipsis 6-22",
        "categoria": "Hechos y Pablo",
        "descripcion": "El Apocalipsis reúne lugares de toda la Biblia: el Éufrates, Babilonia, Armagedón "
                       "(el valle de Meguido), Jerusalén y la nueva Jerusalén que desciende del cielo como "
                       "una novia. Las siete copas y las trompetas se derraman sobre la tierra conocida por "
                       "los primeros lectores.",
        "bbox": (25.0, 28.0, 52.0, 40.0),
        "lugares": ["patmos", "ephesus", "armagedon-1", "jerusalem", "babylon-1", "euphrates",
                    "susa", "rome", "tigris-1", "salt-sea", "sea-of-galilee", "mount-sinai",
                    "temple-mount-1", "smyrna"],
        "regiones": ["asia", "macedonia", "italy", "egypt", "judea-1", "babylonia", "persia",
                     "assyria", "syria-1", "media", "galatia", "greece", "chalda-1"],
        "refs": ["Apocalipsis 16:12-16", "Apocalipsis 17:1-6", "Apocalipsis 21:1-4"],
    },
    {
        "id": "pedro-y-el-evangelio",
        "titulo": "Pedro: de Jerusalen a Roma",
        "subtitulo": "Hechos 1-12; 1 Pedro 5:13",
        "categoria": "Hechos y Pablo",
        "descripcion": "Pedro predicó en Pentecostés, sanó al paralítico en la puerta del templo y abrió "
                       "el evangelio a los gentiles con Cornelio en Cesarea. Visitó Lida, Jope, Samaria y "
                       "Antioquía, y su primera carta saluda a las iglesias del Ponto, Galacia, Capadocia, "
                       "Asia y Bitinia; la tradición lo sitúa en Roma.",
        "bbox": (25.0, 30.0, 45.0, 43.0),
        "lugares": ["jerusalem", "lod", "joppa", "caesarea", "samaria-1", "antioch-1", "rome",
                    "babylon-1", "corinth", "babylon-1", "ponto-1", "capadocia-1", "bitinia-1",
                    "galatia", "asia"],
        "regiones": ["judea-1", "samaria-2", "syria-1", "pontus", "galatia", "asia", "cilicia",
                     "italy", "macedonia"],
        "refs": ["Hechos 2:14-41", "Hechos 10:1-48", "1 Pedro 1:1", "1 Pedro 5:13"],
    },
    {
        "id": "cartas-de-pablo",
        "titulo": "A donde escribio Pablo",
        "subtitulo": "Romanos a Filemón",
        "categoria": "Hechos y Pablo",
        "descripcion": "Las trece cartas de Pablo se dirigieron a comunidades concretas: Roma, Corinto, "
                       "Filipos, Éfeso (Asia), Colosas, Tesalónica, Galacia y Creta, además de las cartas a "
                       "Timoteo, Tito y Filemón. El mapa permite ver la red de iglesias de mediados del "
                       "siglo I.",
        "bbox": (18.0, 30.0, 45.0, 43.0),
        "lugares": ["rome", "corinth", "cencreas-1", "philippi", "ephesus", "colossae-1",
                    "thessalonica", "galatia", "crete", "laodicea", "antioch-1", "jerusalem",
                    "miletus", "nicopolis-1", "troas", "troas"],
        "regiones": ["italy", "greece", "achaia", "macedonia", "asia", "galatia", "crete-2",
                     "syria-1", "judea-1", "cilicia", "phrygia"],
        "refs": ["Romanos 1:1-15", "1 Corintios 1:1-2", "Efesios 1:1", "Tito 1:5"],
    },
]

CIUDADES = [
    {
        "id": "jerusalen-primera",
        "titulo": "Jerusalen hasta el destierro",
        "subtitulo": "2 Samuel 5-24; 2 Reyes 18-25",
        "categoria": "Ciudades",
        "descripcion": "David tomó la fortaleza de Sion y unió la ciudad baja y el monte del templo. "
                       "Salomón edificó el templo y el palacio. Ezequías horadó el túnel de Siloé para "
                       "asegurar el agua, y la ciudad fue destruida por Nabucodonosor en el 586 a.C. El "
                       "mapa reúne los puntos citados por el texto bíblico en torno a la ciudad.",
        "bbox": (35.19, 31.72, 35.30, 31.82),
        "lugares": ["city-of-david", "mount-zion", "temple-mount-1", "mount-of-olives", "kidron",
                    "valley-of-hinnom", "siloam", "en-rogel", "gihon-2", "millo-1", "ophel-1",
                    "bethany-1", "bethphage", "gethsemane-1", "bethesda-1", "golgota-1",
                    "cenaculo-1", "valley-of-rephaim", "topheth-1", "upper-pool-1"],
        "refs": ["2 Samuel 5:6-9", "1 Reyes 6:1-38", "2 Reyes 20:20", "2 Reyes 25:8-10"],
    },
    {
        "id": "jerusalen-jesus",
        "titulo": "Jerusalen en tiempos de Jesus",
        "subtitulo": "Los evangelios y el segundo templo",
        "categoria": "Ciudades",
        "descripcion": "La Jerusalén del siglo I tenía una población estimada de entre 40.000 y 80.000 "
                       "habitantes, que se multiplicaban en las fiestas. Herodes el Grande reconstruyó el "
                       "templo y su explanada; junto a ella estaban la torre Antonia, el estanque de "
                       "Betesda, el túnel y el estanque de Siloé, y fuera de las murallas el Gólgota.",
        "bbox": (35.19, 31.72, 35.31, 31.83),
        "lugares": ["temple-mount-1", "bethesda-1", "siloam", "kidron", "mount-of-olives",
                    "gethsemane-1", "city-of-david", "mount-zion", "cenaculo-1", "golgota-1",
                    "sepulcro-1", "upper-pool-1", "valley-of-hinnom", "valley-of-rephaim",
                    "bethany-1", "bethphage", "ascension-1", "valley-of-rephaim"],
        "refs": ["Marcos 13:1-2", "Juan 5:1-9", "Juan 9:1-11", "Lucas 19:41-44"],
    },
    {
        "id": "tierra-de-galilea-ciudades",
        "titulo": "Las ciudades de Galilea",
        "subtitulo": "Mateo 4:12-16; Lucas 4:16-31",
        "categoria": "Ciudades",
        "descripcion": "Galilea era la región más fértil y poblada de la tierra de Israel, con ciudades "
                       "helenísticas (Séforis, Tiberíades) y pueblos judíos (Nazaret, Caná, Naín). Jesús "
                       "creció en Nazaret, a unos 6 km de Séforis, y enseñó en las sinagogas de la comarca.",
        "bbox": (35.0, 32.5, 35.8, 33.2),
        "lugares": ["nazareth", "cana", "capernaum", "chorazin-1", "magdala-1", "bethsaida-2",
                    "nain-1", "bienaventuranzas-1", "mount-tabor", "daberath", "seforis-1",
                    "tiberias-1", "gennesaret", "sea-of-galilee", "jordan", "arbela-1"],
        "refs": ["Mateo 4:13-16", "Juan 1:45-46", "Juan 7:52", "Lucas 8:1-3"],
    },
    {
        "id": "samaria-siquem",
        "titulo": "Samaria y Siquem",
        "subtitulo": "1 Reyes 16; Juan 4",
        "categoria": "Ciudades",
        "descripcion": "Omri compró el monte de Samaria y edificó su capital, destruida en el 722 a.C. y "
                       "reconstruida por Herodes como Sebaste. En Siquem, entre el Ebal y el Gerizim, "
                       "Josué renovó el pacto; junto al pozo de Jacob, Jesús habló con la mujer samaritana.",
        "bbox": (34.95, 32.0, 35.45, 32.45),
        "lugares": ["samaria-1", "shechem", "sicar-1", "mount-gerizim-1", "mount-ebal-1", "shiloh",
                    "tirzah", "dotan-1", "jordan", "gibeon-1"],
        "refs": ["1 Reyes 16:23-24", "2 Reyes 17:5-6", "Josué 24:1", "Juan 4:4-26"],
    },
    {
        "id": "jerico-y-valle-jordan",
        "titulo": "El valle del Jordan y Jerico",
        "subtitulo": "Josué 2-6; Lucas 19:1-10",
        "categoria": "Ciudades",
        "descripcion": "El valle del Jordán es un corredor de unos 100 km entre el lago de Galilea y el "
                       "mar Muerto. Jericó, la «ciudad de las palmeras», es el asentamiento habitado "
                       "continuo más antiguo conocido, y fue la puerta de entrada de Israel a la tierra "
                       "prometida.",
        "bbox": (35.3, 31.6, 35.7, 32.0),
        "lugares": ["jericho-1", "gilgal-1", "jordan", "salt-sea", "qumran-1", "bethany-1",
                    "adummim-1", "beth-hoglah", "city-of-palms-1", "maqueronte-1"],
        "refs": ["Josué 3:14-17", "Josué 6:20-25", "2 Reyes 2:4-14", "Lucas 19:1-10"],
    },
    {
        "id": "egipto-biblico",
        "titulo": "Egipto en la Biblia",
        "subtitulo": "Génesis 12; Éxodo 1-12; Mateo 2",
        "categoria": "Ciudades",
        "descripcion": "Egipto aparece desde Abraham hasta el nacimiento de Jesús: refugio en tiempos de "
                       "hambre, tierra de esclavitud y de las plagas, y lugar de exilio del niño Jesús. Los "
                       "textos citan el delta (Gosén, Ramesés, Pitón, Tafnes), Menfis y Tebas, y la "
                       "frontera oriental en Siene.",
        "bbox": (29.5, 23.5, 34.5, 32.0),
        "lugares": ["memphis", "thebes", "zoan", "tahpanhes", "goshen-1", "rameses-1", "pithom-1",
                    "heliopolis", "elefantina-1", "nile", "red-sea-1", "cirene-1", "pithom-1",
                    "syene"],
        "refs": ["Génesis 12:10-20", "Éxodo 1:8-14", "Éxodo 12:29-36", "Mateo 2:13-15"],
    },
]

MAPAS_ANTIGUOS = [
    {
        "id": "mapas-antiguos-portada",
        "titulo": "La cartografía bíblica a través de los siglos",
        "subtitulo": "De la tabla de Madaba (siglo VI) al Atlas de 1907",
        "categoria": "Cartografía histórica",
        "descripcion": "Los mapas bíblicos tienen su propia historia. El mosaico de Madaba (Jordania, "
                       "siglo VI) representa la tierra de la Biblia con Jerusalén en el centro; los "
                       "cartógrafos flamencos del siglo XVI (Ortelius, van Adrichem) dibujaron Canaán con "
                       "las doce tribus, y en 1770 Thomas Fuller publicó un mapa con la circunnavegación "
                       "desde el Sinaí. En el siglo XIX, los mapas de la Palestina Exploration Fund "
                       "acompañaron los estudios de campo. La aplicación incluye una galería para abrir "
                       "estos mapas antiguos de dominio público desde Wikimedia Commons, con su ficha de "
                       "autoría y licencia.",
        "bbox": (33.5, 29.0, 37.0, 33.8),
        "lugares": ["jerusalem", "jericho-1", "bethlehem-1", "nazareth", "capernaum", "dan",
                    "beersheba-1", "gaza", "mount-sinai", "jordan", "salt-sea", "sea-of-galilee",
                    "damascus", "tyre", "sidon", "joppa", "caesarea", "hebron"],
        "regiones": ["galilee-1", "samaria-2", "judea-1", "perea-1", "gilead-1", "moab-1", "bashan"],
        "notas": ["La galería de cartografía histórica se abre desde el menú «Mapas antiguos»: allí se "
                  "pueden buscar y descargar mapas de dominio público desde Wikimedia Commons."],
        "refs": ["Ezequiel 5:5", "Salmos 48:2"],
    },
]
