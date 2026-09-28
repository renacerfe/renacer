#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ampliar_vocabulario.py — Amplía el vocabulario español que se usa para traducir
los títulos y las etiquetas del índice temático.

El índice temático de Nave (1896) y Torrey (1897) está en inglés y sus
encabezados son frases cortas («Wicked practices of», «Objects of: The heavenly
bodies»). La traducción se hace palabra por palabra con
contenido/palabras_es.json; este programa añade a ese archivo las palabras que
más veces quedaban sin traducir (artículos, verbos, nombres comunes y gentilicios)
y muestra cuántas quedan pendientes.

Uso:
    python3 ampliar_vocabulario.py            # añade el vocabulario y resume
    python3 ampliar_vocabulario.py --listar 50
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

AQUI = Path(__file__).resolve().parent
APP = AQUI.parent
CONTENIDO = APP / "contenido"
TEMAS = APP / "app" / "datos" / "temas.json"

# ---------------------------------------------------------------------------
# Vocabulario añadido: artículos, preposiciones, verbos y nombres comunes
# ---------------------------------------------------------------------------
NUEVO = {
    # artículos y palabras gramaticales que en español se omiten o cambian
    "the": "", "a": "", "an": "", "of": "de", "in": "en", "on": "en", "at": "en",
    "to": "a", "for": "por", "with": "con", "by": "por", "from": "de", "into": "en",
    "upon": "sobre", "about": "acerca de", "against": "contra", "before": "ante",
    "after": "después de", "between": "entre", "among": "entre", "during": "durante",
    "through": "por", "under": "bajo", "over": "sobre", "without": "sin", "toward": "hacia",
    "towards": "hacia", "unto": "a", "than": "que", "as": "como", "and": "y", "or": "o",
    "but": "sino", "if": "si", "that": "que", "which": "que", "who": "que", "whom": "a quien",
    "whose": "cuyo", "when": "cuando", "where": "donde", "while": "mientras", "because": "porque",
    "therefore": "por tanto", "also": "también", "not": "no", "no": "ningún", "none": "ninguno",
    "all": "todos", "any": "cualquier", "some": "algunos", "every": "cada", "each": "cada",
    "both": "ambos", "other": "otros", "another": "otro", "such": "tal", "same": "mismo",
    "this": "este", "these": "estos", "those": "aquellos", "there": "allí", "here": "aquí",
    "his": "su", "her": "su", "their": "su", "its": "su", "my": "mi", "our": "nuestro",
    "your": "tu", "he": "él", "she": "ella", "they": "ellos", "we": "nosotros", "it": "ello",
    "him": "él", "them": "ellos", "us": "nosotros", "me": "me", "you": "tú", "i": "yo",
    "is": "es", "are": "son", "was": "fue", "were": "fueron", "be": "ser", "been": "sido",
    "being": "siendo", "am": "soy", "has": "ha", "have": "haber", "had": "había",
    "having": "habiendo", "do": "hacer", "does": "hace", "did": "hizo", "shall": "deberá",
    "will": "querrá", "would": "sería", "should": "debería", "may": "puede", "might": "podría",
    "must": "debe", "can": "puede", "could": "podría", "cannot": "no puede",
    "more": "más", "most": "la mayoría de", "much": "mucho", "many": "muchos", "little": "poco",
    "less": "menos", "few": "pocos", "very": "muy", "too": "demasiado", "so": "tan",
    "thus": "así", "then": "entonces", "now": "ahora", "yet": "aún", "still": "todavía",
    "again": "de nuevo", "always": "siempre", "never": "nunca", "often": "a menudo",
    "generally": "generalmente", "specially": "especialmente", "especially": "especialmente",
    "particularly": "particularmente", "originally": "originalmente", "miraculously": "milagrosamente",
    "according": "conforme", "instead": "en lugar", "indeed": "en efecto", "however": "sin embargo",
    "how": "cómo", "why": "por qué", "what": "qué", "whether": "si", "either": "tampoco",
    "neither": "ni", "nor": "ni", "per": "por", "via": "por", "etc": "etcétera",
    "one": "uno", "two": "dos", "three": "tres", "first": "primero", "second": "segundo",
    "third": "tercero", "last": "último", "former": "anterior", "latter": "posterior",
    "new": "nuevo", "old": "antiguo", "great": "grande", "grand": "grandioso", "small": "pequeño",
    "large": "grande", "chief": "principal", "minor": "menor", "inferior": "inferior",
    "secondary": "secundario", "true": "verdadero", "false": "falso", "good": "bueno",
    "bad": "malo", "evil": "mal", "holy": "santo", "sacred": "sagrado", "royal": "real",
    "national": "nacional", "special": "especial", "temporal": "temporal", "spiritual": "espiritual",
    "future": "futuro", "present": "presente", "past": "pasado", "ancient": "antiguo",
    "historical": "histórico", "artificial": "artificial", "natural": "natural", "common": "común",
    "public": "público", "private": "privado", "white": "blanco", "red": "rojo", "black": "negro",
    "full": "lleno", "strong": "fuerte", "mighty": "poderoso", "wise": "sabio", "proud": "soberbio",
    "poor": "pobre", "rich": "rico", "vain": "vano", "glorious": "glorioso", "right": "recto",
    "left": "izquierdo", "male": "varón", "female": "mujer", "greatest": "mayor",
    "abundant": "abundante", "extraordinary": "extraordinario", "remarkable": "notable",
    "special": "especial", "similar": "semejante", "different": "diferente", "sure": "seguro",
    # verbos
    "pray": "orar", "prayer": "oración", "offered": "ofrecidos", "offering": "ofrenda",
    "offers": "ofrece", "offer": "ofrecer", "characterised": "caracterizado",
    "characterized": "caracterizado", "effected": "efectuado", "includes": "incluye",
    "include": "incluir", "included": "incluido", "consists": "consiste", "consist": "consistir",
    "excludes": "excluye", "brings": "trae", "bring": "traer", "brought": "trajo",
    "carried": "llevado", "descended": "descendió", "ascended": "ascendió", "expressed": "expresado",
    "allotted": "repartido", "placed": "colocado", "held": "celebrado", "set": "puesto",
    "visited": "visitado", "denied": "negado", "preached": "predicó", "besieged": "sitiado",
    "taught": "enseñó", "practiced": "practicado", "practised": "practicado", "produces": "produce",
    "produced": "producido", "avoid": "evitar", "followed": "seguido", "caused": "causado",
    "plead": "suplicar", "blessed": "bendecido", "hired": "contratado", "prepared": "preparado",
    "governed": "gobernado", "furnished": "provisto", "causes": "causa", "conquered": "conquistado",
    "prophesies": "profetiza", "rejoice": "regocijarse", "possessed": "poseído", "seek": "buscar",
    "anointed": "ungido", "requires": "requiere", "conformity": "conformidad", "go": "ir",
    "led": "condujo", "chosen": "escogido", "performed": "realizado", "want": "querer",
    "refusing": "rehusando", "encamped": "acampó", "observed": "observado", "walking": "andando",
    "keep": "guardar", "keeping": "guardando", "assisted": "ayudó", "attended": "asistió",
    "speak": "hablar", "make": "hacer", "makes": "hace", "laid": "puso", "proceeds": "procede",
    "collected": "recogido", "accompanies": "acompaña", "hate": "aborrecer", "hateful": "aborrecible",
    "written": "escrito", "dwelt": "habitó", "receive": "recibir", "covered": "cubierto",
    "employed": "empleado", "excited": "suscitó", "fed": "alimentado", "formed": "formado",
    "despised": "despreciado", "surrounded": "rodeado", "contained": "contenía", "liable": "sujeto",
    "increase": "aumento", "considered": "considerado", "provided": "proveyó", "purified": "purificado",
    "opposed": "se opuso", "taking": "tomando", "obtained": "obtuvo", "recorded": "registrado",
    "sowing": "sembrar", "cultivated": "cultivado", "lives": "vidas", "builds": "edifica",
    "worshipping": "adorando", "worshiped": "adoró", "killing": "matando", "loving": "amando",
    "care": "cuidado", "supplied": "suministró", "uses": "usos", "use": "uso", "presented": "presentado",
    "live": "vivir", "commenced": "comenzó", "return": "regreso", "gives": "da", "comes": "viene",
    "neglect": "negligencia", "rebuked": "reprendió", "inflicted": "infligido", "eating": "comer",
    "bearing": "llevando", "sends": "envía", "accomplished": "cumplido", "cutting": "cortar",
    "separated": "separado", "putting": "poniendo", "know": "saber", "called": "llamado",
    "made": "hecho", "given": "dado", "taken": "tomado", "sent": "enviado", "found": "hallado",
    "sought": "buscó", "destroyed": "destruido", "delivered": "librado", "saved": "salvado",
    "killed": "mató", "slew": "mató", "reigned": "reinó", "built": "edificó", "buried": "sepultado",
    "married": "casado", "born": "nacido", "died": "murió", "rose": "resucitó", "saw": "vio",
    "said": "dijo", "spoke": "habló", "heard": "oyó", "came": "vino", "went": "fue",
    "gave": "dio", "took": "tomó", "brought": "trajo", "became": "llegó a ser", "began": "comenzó",
    # sustantivos
    "inhabitants": "habitantes", "objects": "objetos", "articles": "objetos", "things": "cosas",
    "motives": "motivos", "officers": "oficiales", "ceremonies": "ceremonias", "operations": "operaciones",
    "guilt": "culpa", "mode": "modo", "exhibits": "muestras", "denunciations": "denuncias",
    "expressions": "expresiones", "conquest": "conquista", "danger": "peligro", "prosperity": "prosperidad",
    "effects": "efectos", "enactments": "decretos", "vanity": "vanidad", "custom": "costumbre",
    "commerce": "comercio", "vessels": "vasijas", "implements": "útiles", "failure": "fracaso",
    "representations": "representaciones", "members": "miembros", "materials": "materiales",
    "traffic": "tráfico", "victory": "victoria", "care": "cuidado", "colours": "colores",
    "unbelief": "incredulidad", "necessity": "necesidad", "origin": "origen", "margin": "margen",
    "pieces": "piezas", "rulers": "gobernantes", "table": "mesa", "conformity": "conformidad",
    "conspiracies": "conspiraciones", "curse": "maldición", "woe": "ay", "armour": "armadura",
    "wine": "vino", "bread": "pan", "water": "agua", "house": "casa", "city": "ciudad",
    "land": "tierra", "people": "pueblo", "man": "hombre", "men": "hombres", "woman": "mujer",
    "women": "mujeres", "children": "niños", "father": "padre", "mother": "madre", "brother": "hermano",
    "sister": "hermana", "son": "hijo", "daughter": "hija", "wife": "esposa", "husband": "esposo",
    "king": "rey", "queen": "reina", "prince": "príncipe", "servant": "siervo", "slave": "esclavo",
    "prophet": "profeta", "priest": "sacerdote", "temple": "templo", "altar": "altar",
    "sacrifice": "sacrificio", "army": "ejército", "war": "guerra", "peace": "paz", "law": "ley",
    "word": "palabra", "works": "obras", "days": "días", "years": "años", "time": "tiempo",
    "morning": "mañana", "night": "noche", "sun": "sol", "moon": "luna", "stars": "estrellas",
    "heaven": "cielo", "earth": "tierra", "sea": "mar", "river": "río", "mountain": "monte",
    "valley": "valle", "field": "campo", "tree": "árbol", "stone": "piedra", "gold": "oro",
    "silver": "plata", "money": "dinero", "clothing": "vestido", "food": "alimento",
    "sickness": "enfermedad", "death": "muerte", "life": "vida", "soul": "alma", "heart": "corazón",
    "sin": "pecado", "grace": "gracia", "faith": "fe", "hope": "esperanza",
    "salvation": "salvación", "judgment": "juicio", "mercy": "misericordia", "glory": "gloria",
    "power": "poder", "wisdom": "sabiduría", "knowledge": "conocimiento", "truth": "verdad",
    "blessing": "bendición", "promise": "promesa", "covenant": "pacto", "commandment": "mandamiento",
    "circumcision": "circuncisión", "washing": "lavamiento", "eating": "comer", "sowing": "siembra",
    # gentilicios y adjetivos de pueblos
    "jewish": "judío", "gentile": "gentil", "egyptian": "egipcio", "egyptians": "egipcios",
    "syrian": "sirio", "syrians": "sirios", "assyrian": "asirio", "assyrians": "asirios",
    "babylonian": "babilonio", "babylonians": "babilonios", "roman": "romano", "romans": "romanos",
    "greek": "griego", "greeks": "griegos", "persian": "persa", "persians": "persas",
    "moabites": "moabitas", "midianites": "madianitas", "reubenites": "rubenitas",
    "reubenite": "rubenita", "ephraimites": "efraimitas", "gibeonites": "gabaonitas",
    "shechemites": "siquemitas", "simeonite": "simeonita", "merarite": "merarita",
    "gadite": "gadita", "nazarites": "nazareos", "idolaters": "idólatras", "hypocrites": "hipócritas",
    "shunammite": "sunamita", "mosaic": "mosaico", "levitical": "levítico", "ceremonial": "ceremonial",
    "baptist": "Bautista", "messiah": "Mesías", "antichrist": "anticristo", "jehovah": "Jehová",
    "prohibited": "prohibido", "forbidden": "prohibido", "sinful": "pecaminoso",
    "offensive": "ofensivo", "sacred": "sagrado", "ignorant": "ignorante", "proud": "soberbio",
    "called": "llamado", "named": "llamado", "denied": "negado", "ensures": "asegura",
    "walking": "andando", "living": "viviendo", "refusing": "rehusando",
    # segunda tanda: palabras frecuentes en las etiquetas temáticas
    "see": "Véase", "celebrated": "celebrado", "abounded": "abundó", "compared": "comparado",
    "subjects": "temas", "allusions": "alusiones", "destruction": "destrucción",
    "connected": "relacionado", "regard": "respecto", "give": "dar", "exhortations": "exhortaciones",
    "grandfather": "abuelo", "trust": "confianza", "preserved": "preservado", "particular": "particular",
    "following": "siguiendo", "doing": "haciendo", "preservation": "preservación", "overcome": "vencer",
    "order": "orden", "exhorted": "exhortó", "like": "como", "delight": "deleite", "grass": "hierba",
    "superstitious": "supersticioso", "drawing": "atraer", "corrupt": "corrupto", "domestic": "doméstico",
    "infested": "infestado", "afforded": "proporcionó", "revenues": "rentas", "giving": "dar",
    "design": "designio", "pillars": "columnas", "despise": "despreciar", "defeated": "derrotado",
    "becomes": "se convierte", "repaired": "reparado", "withheld": "retuvo", "maintained": "mantenido",
    "mediterranean": "Mediterráneo", "communicated": "comunicado", "obeying": "obedeciendo",
    "inhabited": "habitado", "touching": "en cuanto a", "suspected": "sospechoso", "predicted": "predicho",
    "beneficial": "beneficioso", "bounds": "límites", "assigned": "asignado", "zeal": "celo",
    "strengthened": "fortalecido", "hated": "aborrecido", "cast": "echado", "honour": "honor",
    "follow": "seguir", "author": "autor", "preaching": "predicación", "whatever": "cualquiera que",
    "chariots": "carros", "entered": "entró", "encouraged": "animado", "allowed": "permitido",
    "filled": "lleno", "enjoined": "mandado", "increased": "aumentó", "pure": "puro",
    "acceptable": "aceptable", "sprinkled": "rociado", "cruel": "cruel", "publicly": "públicamente",
    "calamities": "calamidades", "reject": "rechazar", "healing": "sanidad", "ruler": "gobernante",
    "burning": "arder", "purifying": "purificar", "corn": "trigo", "usually": "usualmente",
    "broken": "quebrantado", "results": "resultados", "exported": "exportado", "fond": "aficionado",
    "zealous": "celoso", "inconsistent": "inconsecuente", "instituted": "instituido", "swift": "veloz",
    "forgiving": "perdonador", "blind": "ciego", "destructive": "destructivo", "passage": "pasaje",
    "established": "establecido", "defensive": "defensivo", "wood": "madera", "join": "unirse",
    "home": "hogar", "assists": "ayuda", "father-in-law": "suegro", "nothing": "nada",
    "adopted": "adoptado", "captivity": "cautiverio", "restored": "restaurado", "beloved": "amado",
    "restoration": "restauración", "subjection": "sujeción", "overseer": "supervisor",
    "prayed": "oró", "revealed": "revelado", "raised": "levantado", "continued": "continuó",
    "fools": "necios", "dead": "muertos", "alone": "solo", "confusion": "confusión",
    "saviour": "Salvador", "centurion": "centurión", "come": "venir", "desire": "deseo",
    "commissioned": "comisionado", "obey": "obedecer", "magi": "magos", "watered": "regado",
    "subject": "sujeto", "subdued": "sojuzgado", "sanctified": "santificado", "extent": "alcance",
    "protected": "protegido", "persecution": "persecución", "triumph": "triunfo",
    "acknowledge": "reconocer", "perfect": "perfecto", "turned": "convertido", "consumed": "consumido",
    "deep": "profundo", "partaking": "participación", "unjust": "injusto", "rejection": "rechazo",
    "ornaments": "adornos", "green": "verde", "imposition": "imposición", "raising": "levantamiento",
    "foolish": "necio", "skins": "pieles", "bright": "brillante", "lighted": "encendido",
    "praised": "alabado", "condemned": "condenado", "reproved": "reprendido", "judged": "juzgado",
    "promised": "prometido", "warned": "advirtió", "delivered": "librado", "feared": "temido",
    "loved": "amado", "served": "sirvió", "reigned": "reinó", "fought": "peleó",
    # tercera tanda
    "honouring": "honrando", "explained": "explicado", "superior": "superior", "friends": "amigos",
    "obedient": "obediente", "later": "posterior", "justifiable": "justificable", "fierce": "feroz",
    "joined": "unido", "lake": "lago", "confirmed": "confirmado", "banks": "orillas",
    "inhabits": "habita", "twelve": "doce", "meets": "encuentra", "impressions": "impresiones",
    "borne": "llevado", "setting": "puesta", "unprofitable": "inútil", "look": "mirar",
    "warnings": "advertencias", "refuse": "rehusar", "seed": "simiente", "covetous": "codicioso",
    "oppressed": "oprimido", "persecuted": "perseguido", "regarded": "considerado",
    "rejected": "rechazado", "deprived": "privado", "ordinary": "ordinario", "numerous": "numeroso",
    "wore": "vestía", "produce": "producir", "announced": "anunciado", "confession": "confesión",
    "clothed": "vestido", "difficulty": "dificultad", "murmuring": "murmurador", "golden": "dorado",
    "abhorred": "aborrecido", "experienced": "experimentado", "exceeding": "sobremanera",
    "union": "unión", "fertility": "fertilidad", "fine": "fino", "postures": "posturas",
    "situated": "situado", "represented": "representado", "treatment": "trato", "rebuilt": "reedificado",
    "take": "tomar", "casting": "echar", "inhabit": "habitar", "building": "edificio", "mere": "mero",
    "permitted": "permitido", "fortified": "fortificado", "exercise": "ejercicio", "just": "justo",
    "merchandise": "mercancía", "overlaying": "sobreposición", "working": "obrando",
    "afford": "proporcionar", "acknowledged": "reconocido", "testament": "testamento",
    "bound": "atado", "frequented": "frecuentado", "upright": "recto", "encouragement": "ánimo",
    "various": "varios", "ordained": "ordenado", "neglected": "descuidado", "probable": "probable",
    "binding": "atadura", "extensive": "extenso", "pleasant": "agradable", "bringing": "trayendo",
    "heifer": "novilla", "horns": "cuernos", "soldiers": "soldados", "guests": "invitados",
    "provokes": "provoca", "consecrated": "consagrado", "overcoming": "venciendo", "sitting": "sentado",
    "going": "yendo", "shedding": "derramando", "tempted": "tentado", "keepers": "guardas",
    "substance": "sustancia", "evidence": "evidencia", "hoped": "esperadas", "seen": "vistas",
    "burnt": "encendido", "offerings": "ofrendas", "parents": "padres", "relating": "relacionadas",
    "licentiousness": "lascivia", "practices": "prácticas", "practices of": "prácticas de",
    "customs": "costumbres", "unbelieving": "incrédulo", "drunkenness": "embriaguez",
    "gluttony": "glotonería", "idleness": "ociosidad", "lying": "mentira", "stealing": "hurto",
    "sabbath": "sábado", "feasts": "fiestas", "festivals": "festividades", "harvest": "cosecha",
    "wilderness": "desierto", "captive": "cautivo", "captives": "cautivos", "exile": "destierro",
    "prophecy": "profecía", "prophecies": "profecías", "visions": "visiones", "dreams": "sueños",
    "angels": "ángeles", "demons": "demonios", "miracles": "milagros", "parables": "parábolas",
    "disciples": "discípulos", "apostles": "apóstoles", "elders": "ancianos", "deacons": "diáconos",
    "widows": "viudas", "orphans": "huérfanos", "stangers": "extranjeros", "stranger": "extranjero",
    "strangers": "extranjeros", "neighbours": "vecinos", "neighbors": "vecinos",
}

# Nombres propios que se añaden a los listados correspondientes
LUGARES = {
    "moab": "Moab", "jerusalem": "Jerusalén", "palestine": "Palestina", "syria": "Siria",
    "rome": "Roma", "dan": "Dan", "eden": "Edén", "edom": "Edom", "sinai": "Sinaí",
    "galilee": "Galilea", "damascus": "Damasco", "zion": "Sion", "corinth": "Corinto",
    "ephesus": "Éfeso", "philippi": "Filipos", "hebron": "Hebrón", "gilgal": "Gilgal",
    "bethlehem": "Belén", "gilead": "Galaad", "macedonia": "Macedonia", "persia": "Persia",
    "lebanon": "Líbano", "bashan": "Basán", "tyre": "Tiro", "antioch": "Antioquía",
    "tarshish": "Tarsis", "gerizim": "Gerizim", "shechem": "Siquem", "ziklag": "Siclag",
    "beth-el": "Betel", "asia": "Asia", "egypt": "Egipto", "babylon": "Babilonia",
    "babel": "Babel", "sheba": "Seba", "gibeah": "Gabaa", "jericho": "Jericó",
    "nineveh": "Nínive", "shiloh": "Silo", "bethel": "Betel", "eglon": "Eglón",
    "gibeon": "Gabaón", "mediterranean": "Mediterráneo", "horeb": "Horeb", "ebal": "Ebal",
    "zarephath": "Sarepta", "ammon": "Amón", "midian": "Madián", "nineveh": "Nínive",
}

PERSONAS = {
    "ahasuerus": "Asuero", "adonijah": "Adonías", "amaziah": "Amasías", "gehazi": "Giezi",
    "bezaleel": "Bezaleel", "joram": "Joram", "jotham": "Jotán", "pekah": "Peka",
    "jehoiada": "Joiada", "ben-hadad": "Ben-adad", "ehud": "Aod", "artaxerxes": "Artajerjes",
    "elkanah": "Elcana", "zacharias": "Zacarías", "achan": "Acán", "abel": "Abel",
    "ahithophel": "Ahitofel", "barzillai": "Barzilai", "uzzah": "Uza", "amasa": "Amasá",
    "bath-sheba": "Betsabé", "dagon": "Dagón", "jehoahaz": "Joacaz", "nathanael": "Natanael",
    "potiphar": "Potifar", "leah": "Lea", "hazael": "Hazael", "abijah": "Abías", "elah": "Ela",
    "balak": "Balac", "ananias": "Ananías", "melchizedek": "Melquisedec", "ish-bosheth": "Is-boset",
    "gadites": "gaditas", "rechabites": "recabitas", "ninevites": "ninivitas",
    "corinthians": "corintios", "asherite": "asherita",
    "shalmaneser": "Salmanasar", "eliphaz": "Elifaz", "chedorlaomer": "Quedorlaomer",
    "zelophehad": "Zelofehad", "shemaiah": "Semaías", "menahem": "Menahem", "shadrach": "Sadrac",
    "jael": "Jael", "lamech": "Lamec", "manoah": "Manoa", "onesiphorus": "Onesíforo",
    "gershonite": "gersoneo", "kohathite": "cohatita", "korhite": "coreíta",
}


def palabras_sin_traducir(vocabulario, personas, lugares):
    """Cuenta las palabras inglesas que aún quedan sin traducir en las etiquetas."""
    if not TEMAS.exists():
        print("  (no hay temas.json; ejecuta antes construir_datos.py)")
        return Counter()
    temas = json.load(open(TEMAS, encoding="utf-8"))
    restos = Counter()
    for tema in temas:
        for aspecto in tema.get("aspectos", []):
            etiqueta = aspecto.get("etiqueta") or ""
            original = aspecto.get("etiqueta_original") or ""
            if not original:
                continue
            for palabra in re.findall(r"[A-Za-z][A-Za-z'\-]*", original):
                baja = palabra.lower()
                if len(baja) < 2 or baja in vocabulario or baja in personas or baja in lugares:
                    continue
                if re.search(r"\b" + re.escape(palabra) + r"\b", etiqueta):
                    restos[baja] += 1
    return restos


def main():
    ap = argparse.ArgumentParser(description="Amplía el vocabulario español del índice temático")
    ap.add_argument("--listar", type=int, default=25, help="cuántas palabras pendientes mostrar")
    args = ap.parse_args()

    ruta_palabras = CONTENIDO / "palabras_es.json"
    ruta_lugares = CONTENIDO / "nombres_lugares_es.json"
    ruta_personas = CONTENIDO / "nombres_biblicos_es.json"

    palabras = json.load(open(ruta_palabras, encoding="utf-8"))
    lugares = json.load(open(ruta_lugares, encoding="utf-8"))
    personas = json.load(open(ruta_personas, encoding="utf-8"))
    antes = palabras_sin_traducir(palabras, personas, lugares)

    nuevas = 0
    for ingles, castellano in NUEVO.items():
        if ingles not in palabras:
            palabras[ingles] = castellano
            nuevas += 1
    nuevos_lugares = 0
    for ingles, castellano in LUGARES.items():
        if ingles not in lugares:
            lugares[ingles] = castellano
            nuevos_lugares += 1
    nuevos_personas = 0
    for ingles, castellano in PERSONAS.items():
        if ingles not in personas:
            personas[ingles] = castellano
            nuevos_personas += 1

    # el orden de las claves se conserva: primero la nota, después por alfabeto
    def ordenar(diccionario):
        nota = diccionario.pop("_nota", None)
        salida = {}
        if nota:
            salida["_nota"] = nota
        for clave in sorted(diccionario):
            salida[clave] = diccionario[clave]
        return salida

    with open(ruta_palabras, "w", encoding="utf-8") as f:
        json.dump(ordenar(palabras), f, ensure_ascii=False, indent=1)
    with open(ruta_lugares, "w", encoding="utf-8") as f:
        json.dump(ordenar(lugares), f, ensure_ascii=False, indent=1)
    with open(ruta_personas, "w", encoding="utf-8") as f:
        json.dump(ordenar(personas), f, ensure_ascii=False, indent=1)

    print(f"· Palabras nuevas: {nuevas} (total {len(palabras)})")
    print(f"· Lugares nuevos: {nuevos_lugares} (total {len(lugares)})")
    print(f"· Nombres de persona nuevos: {nuevos_personas} (total {len(personas)})")
    despues = palabras_sin_traducir(palabras, personas, lugares)
    print(f"· Palabras inglesas sin traducir: {sum(antes.values())} -> {sum(despues.values())} "
          f"({len(antes)} -> {len(despues)} distintas)")
    if despues and args.listar:
        print("  Pendientes más frecuentes:")
        for palabra, veces in despues.most_common(args.listar):
            print(f"    {palabra:20} {veces}")


if __name__ == "__main__":
    sys.exit(main())
