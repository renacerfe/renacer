#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
escribir_enciclopedia.py — Redacta contenido/enciclopedia_es.json, la
enciclopedia propia de la aplicación: artículos breves en español sobre los
lugares, las obras y las rutas de la Biblia, ilustrados con los grabados de
Gustave Doré y enlazados con las citas bíblicas.

Cada artículo declara su fuente y su licencia. Las ilustraciones se toman de la
galería de arte (app/arte/) y se referencian por el número de lámina.
"""

import json
import unicodedata
from pathlib import Path

AQUI = Path(__file__).resolve().parent
APP = AQUI.parent
ARTE = APP / "app" / "datos" / "arte.json"
DESTINO = APP / "contenido" / "enciclopedia_es.json"

FUENTE = "Enciclopedia del Atlas Bíblico (redactada para esta aplicación)"
LICENCIA = "Texto propio, de libre uso; ilustraciones en dominio público"

# ---------------------------------------------------------------------------
# Artículos: (título, resumen, párrafos, referencias, número de lámina de Doré)
# ---------------------------------------------------------------------------
ARTICULOS = [
    ("Jerusalén",
     "La ciudad santa: capital de David, sede del templo y centro de la pasión de Jesús.",
     ["Jerusalén se levanta sobre una meseta de los montes de Judá, a unos 800 metros sobre el nivel "
      "del mar. En la Biblia aparece por primera vez con el nombre de Salem, y más tarde como la "
      "fortaleza jebusea que David conquistó y convirtió en capital de Israel.",
      "Salomón edificó allí el templo, y desde entonces la ciudad fue el corazón religioso del pueblo: "
      "subían a ella tres veces al año para las fiestas de peregrinación. Fue destruida por Nabucodonosor "
      "en el año 586 a. C. y reconstruida tras el destierro; Herodes el Grande la engrandeció con obras "
      "como el templo que conocieron Jesús y los apóstoles.",
      "La ciudad aparece en más de novecientas referencias bíblicas. En ella murió y resucitó Jesús, y "
      "en ella nació la primera comunidad cristiana."],
     ["2 Samuel 5:6-10", "1 Reyes 6:1-38", "2 Reyes 25:8-10", "Salmo 122:1-9", "Lucas 19:28-44"],
     198),

    ("El templo de Jerusalén",
     "La casa de Dios: del templo de Salomón al templo de Herodes.",
     ["El primer templo lo edificó Salomón en el monte Moriah hacia el año 960 a. C. Constaba del atrio, "
      "el lugar santo y el lugar santísimo, donde se guardaba el arca del pacto. Babilonia lo incendió en "
      "586 a. C. y las obras de reconstrucción se hicieron en tiempos de Zorobabel y de Esdras y Nehemías.",
      "Herodes el Grande comenzó hacia el año 20 a. C. una ampliación colosal: plataformas, pórticos, "
      "patios y el santuario mismo. Ese es el templo en cuyas puertas predicaron Pedro y Juan, y el que "
      "Jesús anunció que sería destruido. Los romanos lo arrasaron en el año 70 d. C.",
      "Del conjunto se conserva hoy el muro occidental, llamado también muro de las Lamentaciones, y "
      "el plano que acompaña a esta explicación reconstruye su planta en tiempos de Jesús."],
     ["1 Reyes 6:1-38", "Esdras 3:10-13", "Marcos 13:1-2", "Hechos 3:1-10"],
     199),

    ("El tabernáculo del desierto",
     "La tienda de reunión, el santuario portátil que acompañó a Israel por el desierto.",
     ["Mientras el pueblo caminaba cuarenta años por el desierto, no tenía templo: tenía una tienda. "
      "Dios dio a Moisés las medidas exactas del tabernáculo, y los artesanos Bezaleel y Aholiab lo "
      "construyeron con los materiales que el pueblo ofrendó.",
      "El tabernáculo se dividía en el atrio, el lugar santo —con el candelabro, la mesa de los panes y "
      "el altar del incienso— y el lugar santísimo, separado por un velo, donde estaba el arca del pacto "
      "con los querubines. Todo el conjunto se desmontaba y se transportaba sobre carros y varas.",
      "El Apocalipsis y la carta a los Hebreos leen el tabernáculo como figura de Cristo y de la presencia "
      "de Dios en medio de su pueblo."],
     ["Éxodo 25:1-9", "Éxodo 40:34-38", "Hebreos 9:1-12", "Apocalipsis 21:3"],
     118),

    ("Belén",
     "Ciudad de David y lugar del nacimiento de Jesús.",
     ["Belén de Judá, también llamada Efrata, se encuentra a unos diez kilómetros al sur de Jerusalén. "
      "En sus campos pastoreaba Rut cuando conoció a Booz, y en ella nació David, el pastor que llegó a "
      "ser rey.",
      "El evangelio de Lucas sitúa allí el nacimiento de Jesús, porque José y María subieron a empadronarse "
      "en la ciudad de la familia de David. Los magos de oriente llegaron guiados por una estrella, y "
      "Herodes ordenó la matanza de los niños de la comarca.",
      "Constantino mandó edificar sobre la gruta de la natividad la basílica que todavía hoy se conserva."],
     ["Rut 4:11-17", "1 Samuel 16:1-13", "Lucas 2:1-20", "Mateo 2:1-18"],
     162),

    ("Nazaret y Galilea",
     "La comarca donde Jesús creció y comenzó su ministerio.",
     ["Galilea es la región montañosa y fértil del norte de Israel, en torno al lago de Genesaret. "
      "Nazaret, un pueblo pequeño de la baja Galilea, fue el hogar de José y María y el lugar donde "
      "Jesús creció.",
      "En Cafarnaúm, junto al lago, estuvo su casa durante el ministerio: allí sanó a la suegra de Pedro, "
      "llamó a los pescadores y enseñó en la sinagoga. Desde Caná hasta el monte de las Bienaventuranzas, "
      "casi todos los episodios de la vida pública suceden en esta comarca.",
      "El mar de Galilea, de unos veinte kilómetros de largo, aparece en los evangelios con sus tormentas "
      "repentinas, sus barcas de pesca y la pesca milagrosa."],
     ["Mateo 2:19-23", "Mateo 4:12-25", "Marcos 4:35-41", "Juan 21:1-14"],
     174),

    ("El río Jordán",
     "La frontera de la tierra prometida y las aguas del bautismo.",
     ["El Jordán nace al pie del monte Hermón y desciende por el valle del Rift hasta el mar Muerto, "
      "en el punto más bajo de la tierra firme. Sus aguas separan la tierra de Canaán de los desiertos "
      "del este.",
      "Israel lo cruzó en seco con Josué, y en sus aguas se bañó Naamán el sirio, que quedó limpio de su "
      "lepra. Elías y Eliseo lo atravesaron; Eliseo hizo flotar el hacha de hierro.",
      "Juan el Bautista predicó junto a sus orillas, en Betábara, y allí bautizó a Jesús."],
     ["Josué 3:14-17", "2 Reyes 5:1-14", "2 Reyes 2:8-14", "Marcos 1:9-11"],
     168),

    ("El monte Sinaí",
     "El monte donde Dios entregó la ley a Moisés.",
     ["El Sinaí —también llamado Horeb— es la montaña del desierto donde Moisés vio la zarza que ardía "
      "sin consumirse y donde el pueblo acampó al salir de Egipto.",
      "Allí, entre truenos y fuego, Dios entregó los diez mandamientos y concertó su pacto con Israel. "
      "Moisés subió al monte y permaneció cuarenta días; el pueblo, mientras tanto, fabricó el becerro "
      "de oro.",
      "La tradición identifica el lugar con el monte de Santa Catalina, en la península del Sinaí, donde "
      "se levanta un monasterio con la biblioteca más antigua del mundo cristiano."],
     ["Éxodo 3:1-12", "Éxodo 19:16-25", "Éxodo 20:1-17", "Deuteronomio 5:1-22"],
     39),

    ("El éxodo de Egipto",
     "La salida de Israel de la esclavitud y los cuarenta años por el desierto.",
     ["Después de siglos en Egipto, el pueblo de Israel fue liberado bajo la guía de Moisés. Las diez "
      "plagas, la noche de la pascua y el paso del mar Rojo son los hitos de la salida.",
      "El itinerario tradicional lleva desde Ramesés hasta Succot, el mar Rojo, Mara, el Sinaí y "
      "Cades-barnea, en el borde del desierto de Parán. Desde allí los espías entraron en la tierra "
      "prometida y volvieron con un racimo gigantesco de uvas.",
      "Por la falta de fe de aquella generación, el pueblo caminó cuarenta años por el desierto hasta "
      "que Josué lo condujo a cruzar el Jordán."],
     ["Éxodo 12:29-42", "Éxodo 14:21-31", "Números 13:1-33", "Números 14:26-35", "Deuteronomio 8:1-10"],
     37),

    ("Canaán y la tierra prometida",
     "La tierra que mana leche y miel, repartida entre las doce tribus.",
     ["Canaán es la franja de tierra entre el mar Mediterráneo y el desierto, atravesada de norte a sur "
      "por el Jordán. Al norte está Galilea, en el centro Samaria, al sur Judea y más allá el Neguev.",
      "Josué dirigió la conquista y el reparto del territorio entre las doce tribus, con las ciudades de "
      "refugio y las ciudades levíticas. La agricultura mediterránea —trigo, olivo, vid, higuera y "
      "granado— da color a las parábolas de Jesús.",
      "El mapa físico que acompaña a esta entrada muestra el relieve: el monte Hermón al norte, el valle "
      "del Jordán, la llanura costera de Sarón y las alturas de Judá."],
     ["Josué 1:1-9", "Josué 15:1-12", "Deuteronomio 8:7-10", "Ezequiel 34:13-14"],
     46),

    ("Jericó",
     "La primera ciudad conquistada por Israel y escenario de dos milagros del evangelio.",
     ["Jericó, en el valle del Jordán, es una de las ciudades habitadas más antiguas del mundo. Sus "
      "murallas cayeron ante el pueblo de Israel después de siete días de marcha y de trompetas, y la "
      "casa de Rahab la ramera fue salvada.",
      "Milenios después, Jesús pasó por allí: devolvió la vista a Bartimeo y se hospedó en casa de "
      "Zaqueo, el cobrador de impuestos."],
     ["Josué 6:1-25", "Marcos 10:46-52", "Lucas 19:1-10"],
     48),

    ("Samaria",
     "La capital del reino del norte y la región de los samaritanos.",
     ["Tras el cisma de los diez tribus, Omri compró el monte de Samaria y edificó allí la capital del "
      "reino del norte. En sus palacios predicaron Elías, Eliseo y Amós, y junto a sus puertas se produjo "
      "el sitio que dejó hambre en la ciudad.",
      "En tiempos de Jesús, samaritanos y judíos no se trataban; precisamente por eso sus parábolas del "
      "buen samaritano y su encuentro con la mujer junto al pozo de Sicar resultan tan llamativos."],
     ["1 Reyes 16:23-24", "2 Reyes 6:24-33", "Lucas 10:25-37", "Juan 4:1-42"],
     171),

    ("Éfeso",
     "La ciudad del templo de Diana y una de las iglesias del Apocalipsis.",
     ["Éfeso fue la ciudad más importante de Asia Menor: puerto, centro comercial y sede del templo de "
      "Artemisa (Diana), una de las siete maravillas del mundo antiguo.",
      "Pablo permaneció allí más de dos años y la predicación del evangelio provocó el motín de los "
      "plateros, que veían peligrar su negocio de imágenes de la diosa. Allí vivió también la comunidad "
      "a la que Juan dirigió su carta primera.",
      "En el Apocalipsis, Éfeso recibe el primero de los mensajes a las siete iglesias: elogio por su "
      "trabajo y su paciencia, y llamada a recuperar el primer amor."],
     ["Hechos 19:1-41", "Efesios 1:1-2", "Apocalipsis 2:1-7"],
     233),

    ("Antioquía de Siria",
     "La ciudad donde los discípulos fueron llamados cristianos por primera vez.",
     ["Antioquía, sobre el río Orontes, era la tercera ciudad del imperio romano después de Roma y "
      "Alejandría. Allí se refugiaron algunos discípulos tras la muerte de Esteban y allí nació la "
      "primera iglesia formada por judíos y griegos.",
      "De Antioquía salieron Bernabé y Pablo en sus viajes misioneros, y a ella volvieron para contar "
      "lo que Dios había hecho entre los gentiles. La ciudad fue también el lugar donde empezó a "
      "utilizarse el nombre de «cristianos»."],
     ["Hechos 11:19-26", "Hechos 13:1-3", "Hechos 15:1-35"],
     229),

    ("Corinto",
     "La ciudad de los dos puertos y las dos cartas de Pablo.",
     ["Corinto estaba en el istmo que une el Peloponeso con el resto de Grecia, y tenía dos puertos: "
      "uno hacia el mar Egeo y otro hacia el Jónico. Su riqueza y su vida comercial hicieron de ella "
      "una ciudad famosa y también famosa por su vida licenciosa.",
      "Pablo llegó en su segundo viaje misionero y se quedó año y medio, trabajando como tejedor de "
      "tiendas junto a Aquila y Priscila. De allí salieron las dos cartas a los corintios, que tratan "
      "de la unidad de la iglesia, de la resurrección y del amor."],
     ["Hechos 18:1-18", "1 Corintios 13:1-13", "2 Corintios 1:1-11"],
     232),

    ("Roma",
     "La capital del imperio donde Pablo anunció el evangelio y murió.",
     ["Roma era el centro del mundo de entonces: un millón de habitantes, el foro, el circo y las "
      "legiones que llevaban el orden romano de un extremo al otro del Mediterráneo.",
      "Pablo llegó a ella como prisionero, tras el naufragio narrado en los Hechos, y pudo predicar "
      "libremente durante dos años. A la comunidad de Roma dirigió la carta más extensa y sistemática "
      "de todas las suyas.",
      "La tradición sitúa en las afueras de la ciudad, junto a la vía Ostiense, el lugar de su martirio, "
      "durante la persecución de Nerón."],
     ["Hechos 28:11-31", "Romanos 1:1-17", "2 Timoteo 4:6-8"],
     225),

    ("Babilonia",
     "La ciudad del destierro y símbolo del poder contrario a Dios.",
     ["Babilonia, sobre el Éufrates, fue la capital del imperio de Nabucodonosor. En el año 586 a. C. "
      "sus ejércitos tomaron Jerusalén, incendiaron el templo y llevaron al pueblo al destierro.",
      "Junto a los ríos de Babilonia, como canta el salmo 137, los desterrados lloraron recordando Sion. "
      "Allí predicaron Ezequiel y Daniel; allí se escribieron buena parte de los salmos y las "
      "profecías de la esperanza.",
      "Ciro el persa conquistó la ciudad en el año 539 a. C. y permitió el regreso de los judíos a "
      "Jerusalén."],
     ["2 Reyes 25:1-11", "Salmo 137:1-9", "Daniel 1:1-21", "Esdras 1:1-11"],
     127),

    ("Egipto y el Nilo",
     "La tierra de la esclavitud y el lugar donde se refugió el niño Jesús.",
     ["Egipto, regado por el Nilo, era el granero del mundo antiguo. Allí encontró refugio Abraham en "
      "tiempos de hambre, y allí fue vendido José, que llegó a ser gobernador del país.",
      "Siglos después, el pueblo de Israel fue esclavizado en las obras de Ramesés y Pitón, hasta que "
      "Moisés lo sacó con mano poderosa.",
      "El evangelio de Mateo cuenta que José, avisado en sueños, huyó con María y el niño a Egipto para "
      "escapar de la matanza ordenada por Herodes."],
     ["Génesis 41:39-57", "Éxodo 1:8-14", "Mateo 2:13-15"],
     30),

    ("Nínive",
     "La capital de Asiria y la ciudad que se arrepintió con Jonás.",
     ["Nínive estaba a orillas del Tigris y fue la capital del imperio asirio, famoso por su poder y su "
      "crueldad. Sus murallas y sus palacios son hoy un yacimiento arqueológico en las cercanías de "
      "Mosul.",
      "El profeta Jonás fue enviado a anunciar su destrucción, y toda la ciudad —desde el rey hasta el "
      "ganado— se arrepintió y se vistió de cilicio. Este es uno de los pocos episodios bíblicos en que "
      "una ciudad gentil se vuelve a Dios."],
     ["Jonás 1:1-2", "Jonás 3:1-10", "Nahúm 1:1-15"],
     139),

    ("Patmos y las siete iglesias",
     "La isla del destierro de Juan y las siete comunidades del Apocalipsis.",
     ["Patmos es una isla pequeña y rocosa del mar Egeo, donde la tradición sitúa el destierro del "
      "apóstol Juan durante la persecución de Domiciano. Allí escribió el Apocalipsis.",
      "El libro comienza con siete cartas dirigidas a siete iglesias de Asia Menor: Éfeso, Esmirna, "
      "Pérgamo, Tiatira, Sardis, Filadelfia y Laodicea. Cada carta elogia, corrige y promete, y todas "
      "terminan con la misma llamada: «el que tiene oído, oiga».",
      "El mapa de las siete iglesias permite recorrer en orden las ciudades a las que fueron enviadas."],
     ["Apocalipsis 1:9-20", "Apocalipsis 2:1-29", "Apocalipsis 3:1-22"],
     236),

    ("Los viajes misioneros de Pablo",
     "Del camino de Damasco a la prisión en Roma: el evangelio cruza el Mediterráneo.",
     ["Saulo de Tarso perseguía a los cristianos cuando, camino de Damasco, una luz lo derribó y oyó la "
      "voz de Jesús. A partir de entonces se llamó Pablo y dedicó su vida a anunciar el evangelio.",
      "Los Hechos describen tres grandes viajes: el primero por Chipre y el sur de Asia Menor; el segundo "
      "por Galacia, Macedonia y Grecia, hasta Atenas y Corinto; y el tercero de nuevo por Éfeso, donde "
      "se produjo el motín de los plateros.",
      "Detenido en Jerusalén, apeló al César y viajó a Roma como prisionero, tras el naufragio en la "
      "isla de Malta. Los mapas de esta sección siguen cada etapa con las escalas que mencionan los "
      "Hechos."],
     ["Hechos 9:1-19", "Hechos 13:1-14:28", "Hechos 15:36-18:22", "Hechos 18:23-21:17", "Hechos 27:1-28:31"],
     235),

    ("El caminó del Calvario",
     "Las últimas horas de Jesús, desde el huerto hasta el sepulcro.",
     ["La noche del jueves, después de la última cena, Jesús oró en Getsemaní, al pie del monte de los "
      "Olivos, mientras los discípulos dormían. Allí fue arrestado.",
      "El viernes fue juzgado ante el sanedrín y ante Pilato, azotado y coronado de espinas. Cargó con "
      "la cruz por la vía Dolorosa hasta el Gólgota, fuera de las murallas, y fue crucificado entre dos "
      "ladrones.",
      "El sepulcro estaba en un huerto cercano, y el domingo muy temprano las mujeres lo encontraron "
      "vacío. El plano de Jerusalén en tiempos de Jesús permite seguir todo el recorrido."],
     ["Mateo 26:36-46", "Juan 19:1-22", "Lucas 23:26-49", "Mateo 28:1-10"],
     214),

    ("El monte de los Olivos y Getsemaní",
     "El huerto de la oración, frente a las murallas de Jerusalén.",
     ["El monte de los Olivos se alza al este de Jerusalén, separado de la ciudad por el valle de "
      "Cedrón. Sus laderas estaban cubiertas de olivares y desde su cumbre se contempla todo el recinto "
      "del templo.",
      "Jesús subía con frecuencia a Betania, en la vertiente oriental, y se reunía con sus discípulos en "
      "el huerto de Getsemaní. Desde allí ascendió a los cielos, según los Hechos, y allí volverá, según "
      "la profecía de Zacarías."],
     ["Zacarías 14:1-4", "Lucas 22:39-46", "Hechos 1:9-12"],
     203),

    ("Ur, Harán y el camino de Abraham",
     "La ruta que siguió Abraham desde Mesopotamia hasta la tierra de Canaán.",
     ["Abraham salió de Ur de los caldeos, en el sur de Mesopotamia, y se detuvo en Harán, en el norte, "
      "antes de entrar en Canaán. Con él iban Sarai, su esposa, y Lot, su sobrino.",
      "El mapa del viaje sigue la gran curva del Éufrates, la entrada por Siquem, Betel y el Neguev, y "
      "el descenso a Egipto durante el hambre. La promesa que lo acompañó fue la de una descendencia "
      "tan numerosa como las estrellas."],
     ["Génesis 11:31-32", "Génesis 12:1-9", "Hechos 7:2-5"],
     11),

    ("José en Egipto",
     "El hijo de Jacob vendido por sus hermanos llega a ser gobernador de Egipto.",
     ["José era el hijo predilecto de Jacob, y sus hermanos, celosos, lo vendieron a unos mercaderes "
      "que iban a Egipto. Allí sirvió en casa de Potifar, fue encarcelado injustamente y salió de la "
      "cárcel al interpretar los sueños del faraón.",
      "Siete años de abundancia y siete de hambre: su administración salvó a Egipto y llevó a su padre "
      "y a sus hermanos a establecerse en la tierra de Gosén. El perdón que concede a sus hermanos es "
      "una de las páginas más hermosas del Génesis."],
     ["Génesis 37:12-36", "Génesis 41:1-57", "Génesis 45:1-15", "Génesis 50:15-21"],
     27),

    ("Los reinos de Israel y Judá",
     "La división del reino después de Salomón y los profetas que la anunciaron.",
     ["A la muerte de Salomón, en el año 931 a. C., el reino se partió: al norte, Israel, con capital en "
      "Samaria y diez tribus; al sur, Judá, con capital en Jerusalén y las tribus de Judá y Benjamín.",
      "Israel cayó ante Asiria en 722 a. C. y sus habitantes fueron deportados; Judá resistió hasta 586 "
      "a. C., cuando Babilonia destruyó el templo. Los profetas —Amós, Oseas, Isaías, Jeremías, "
      "Ezequiel— interpretaron estos acontecimientos como llamadas al arrepentimiento y anuncios de "
      "restauración."],
     ["1 Reyes 12:1-24", "2 Reyes 17:1-23", "2 Reyes 25:1-21", "Jeremías 31:31-34"],
     112),

    ("Damasco",
     "La ciudad más antigua habitada y el escenario de la conversión de Pablo.",
     ["Damasco, al pie del monte Hermón, es una de las ciudades habitadas más antiguas del mundo. "
      "Abraham la persiguió cuando rescató a Lot, y Eliseo fue enviado a ungir a Hazael como rey de "
      "Siria en ella.",
      "Camino de Damasco, Saulo de Tarso fue derribado por una luz y oyó la voz de Jesús. Cegado, entró "
      "en la ciudad, fue bautizado por Ananías y comenzó a predicar en las sinagogas que Jesús era el "
      "Cristo. Desde una ventana de la muralla escapó en un cesto, cuando los judíos querían matarlo."],
     ["Génesis 14:14-16", "Hechos 9:1-25", "2 Corintios 11:32-33"],
     229),

    ("El mar Muerto y el desierto de Judá",
     "El punto más bajo de la tierra y los refugios de David y de los esenios.",
     ["El mar Muerto recibe las aguas del Jordán y no tiene salida al mar: la evaporación concentra tal "
      "cantidad de sales que ningún pez puede vivir en él. Sus orillas están a unos 430 metros bajo el "
      "nivel del mar.",
      "Junto a sus cuevas se refugiaron David y sus hombres cuando huían de Saúl, y allí, en Qumrán, "
      "vivió la comunidad que escondió los rollos del mar Muerto, descubiertos en 1947.",
      "Las ciudades de Sodoma y Gomorra, en la llanura que hoy cubre el sur del mar, son el fondo de "
      "una de las historias más conocidas del Génesis."],
     ["Génesis 19:15-29", "1 Samuel 24:1-22", "Salmo 63:1-11"],
     13),

    ("Los imperios de Daniel",
     "Las cuatro bestias, los imperios sucesivos y la esperanza de un reino que no acaba.",
     ["El libro de Daniel presenta la historia de los imperios mediante sueños y visiones: la estatua de "
      "los cuatro metales, las cuatro bestias que salen del mar y el carnero y el macho cabrío.",
      "Babilonia, Media y Persia, Grecia y Roma se suceden en los mapas de esta sección. Daniel sirvió "
      "en las cortes de Babilonia y de Persia, y fue librado del foso de los leones.",
      "En medio de los imperios, la visión del Hijo del hombre que recibe el dominio eterno sostiene la "
      "esperanza del pueblo."],
     ["Daniel 2:31-45", "Daniel 7:1-14", "Daniel 8:1-27", "Daniel 6:16-24"],
     126),

    ("El mundo del Nuevo Testamento",
     "La tierra de Israel bajo Roma y las rutas del evangelio por el Mediterráneo.",
     ["En tiempos de Jesús, la tierra de Israel formaba parte del imperio romano: Galilea y Judea eran "
      "reinos y provincias bajo la autoridad de Herodes y de los procuradores, y las calzadas romanas "
      "recorrían el país.",
      "El griego era la lengua común del comercio y de la cultura, y el Mediterráneo, «nuestro mar», "
      "unía las ciudades donde se establecieron las primeras comunidades cristianas: Antioquía, Éfeso, "
      "Corinto, Tesalónica, Filipos y Roma.",
      "Los mapas de esta sección muestran esa red de ciudades y caminos que hizo posibles los viajes de "
      "Pablo y la difusión del evangelio."],
     ["Lucas 2:1-2", "Hechos 13:1-3", "Romanos 15:23-29"],
     12),
]


def cargar_archivo_por_numero():
    if not ARTE.exists():
        return {}
    datos = json.load(open(ARTE, encoding="utf-8"))
    return {obra["numero"]: obra["archivo"] for obra in datos.get("obras", [])}


def main():
    archivos = cargar_archivo_por_numero()
    articulos = []
    for titulo, resumen, parrafos, refs, lamina in ARTICULOS:
        articulos.append({
            "id": "".join(c for c in unicodedata.normalize("NFKD", titulo.lower())
                          if not unicodedata.combining(c)).replace(" ", "-"),
            "titulo": titulo,
            "resumen": resumen,
            "texto": "\n\n".join(parrafos),
            "refs": refs,
            "imagen": archivos.get(lamina),
            "leyenda_imagen": f"Grabado de Gustave Doré, lámina {lamina} (1866, dominio público)",
            "fuente": FUENTE,
            "licencia": LICENCIA,
        })
    with open(DESTINO, "w", encoding="utf-8") as f:
        json.dump(articulos, f, ensure_ascii=False, indent=1)
    print(f"  · {DESTINO.relative_to(APP)}  ({len(articulos)} artículos)")
    sin_imagen = [a["titulo"] for a in articulos if not a["imagen"]]
    if sin_imagen:
        print(f"    (sin ilustración: {', '.join(sin_imagen)})")


if __name__ == "__main__":
    main()
