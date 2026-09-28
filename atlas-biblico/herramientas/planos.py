# -*- coding: utf-8 -*-
"""
planos.py — Planos esquemáticos dibujados a mano en SVG: el tabernáculo, el
templo de Herodes y la Jerusalén del primer siglo. Las medidas proceden de los
textos bíblicos (Éxodo 25-40; 1 Reyes 6; Ezequiel 40-42) y de las descripciones
históricas de Josefo y de la arqueología. Son esquemas didácticos, no
levantamientos topográficos.
"""

ANCHO, ALTO = 1200, 820

ESTILO = """
  text { font-family: "Noto Serif", "DejaVu Serif", Georgia, serif; }
  .titulo { font-size: 26px; font-weight: 700; fill: #4a3410; text-anchor: middle; }
  .subtitulo { font-size: 14px; fill: #6b5b45; text-anchor: middle; font-style: italic; }
  .pie { font-size: 11px; fill: #6b5b45; text-anchor: middle; }
  .rot { font-size: 13px; fill: #2b2013; font-weight: 600; text-anchor: middle; paint-order: stroke; stroke: #fdf9ef; stroke-width: 3.4px; }
  .rot-izq { font-size: 12.5px; fill: #2b2013; font-weight: 600; text-anchor: end; paint-order: stroke; stroke: #fdf9ef; stroke-width: 3.4px; }
  .rot-der { font-size: 12.5px; fill: #2b2013; font-weight: 600; text-anchor: start; paint-order: stroke; stroke: #fdf9ef; stroke-width: 3.4px; }
  .rot-peq { font-size: 11.5px; fill: #4b3a1e; text-anchor: middle; paint-order: stroke; stroke: #fdf9ef; stroke-width: 3px; }
  .medida { font-size: 11px; fill: #7a5c33; text-anchor: middle; }
  .nota { font-size: 11.5px; fill: #4b5563; }
"""

PIE = ("Planos esquemáticos de Renacer · Atlas Bíblico · medidas tomadas de Éxodo 25-40, "
       "1 Reyes 6-7 y Ezequiel 40-42, con las descripciones de Josefo")


def _cabecera(titulo, subtitulo, pie=PIE):
    return (f'<rect x="0" y="0" width="{ANCHO}" height="88" fill="rgba(250,246,236,0.96)"/>'
            f'<text x="{ANCHO/2}" y="42" class="titulo">{titulo}</text>'
            f'<text x="{ANCHO/2}" y="70" class="subtitulo">{subtitulo}</text>'
            f'<line x1="0" y1="88" x2="{ANCHO}" y2="88" stroke="#b98a2b" stroke-width="2"/>'
            f'<rect x="0" y="{ALTO-64}" width="{ANCHO}" height="64" fill="rgba(250,246,236,0.96)"/>'
            f'<line x1="0" y1="{ALTO-64}" x2="{ANCHO}" y2="{ALTO-64}" stroke="#b98a2b" stroke-width="1.4"/>'
            f'<text x="{ANCHO/2}" y="{ALTO-16}" class="pie">{pie}</text>'
            f'<rect x="0" y="0" width="{ANCHO}" height="{ALTO}" fill="none" stroke="#c9bb97" stroke-width="6"/>')


def _caja(x, y, w, h, relleno="#f4ecd8", borde="#8a6b2f", grosor=2.4, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{relleno}" stroke="{borde}" '
            f'stroke-width="{grosor}"{d}/>')


def _texto(x, y, clase, contenido, tam=None):
    t = f' font-size="{tam}"' if tam else ""
    return f'<text x="{x}" y="{y}" class="{clase}"{t}>{contenido}</text>'


def _notas(notas, y0=636):
    """Notas al pie en una sola columna, con líneas ya cortas."""
    partes = []
    y = y0
    for n in notas:
        partes.append(_texto(66, y, "nota", "• " + n))
        y += 23
    return partes


def _svg(partes):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{ANCHO}" height="{ALTO}" '
            f'viewBox="0 0 {ANCHO} {ALTO}"><defs><style>{ESTILO}</style></defs>'
            f'{"".join(partes)}</svg>')


# ---------------------------------------------------------------------------
# 1. El tabernáculo
# ---------------------------------------------------------------------------
def plano_tabernaculo():
    partes = [_cabecera("El tabernáculo del desierto",
                        "Éxodo 25-40 · el atrio a escala (1 codo = 5 px); el tabernáculo va ampliado para poder leerlo")]
    # Atrio: 100 x 50 codos (1 codo = 5 px) -> 500 x 250 px
    ox, oy, a, b = 350, 180, 500, 250
    partes.append(_caja(ox, oy, a, b, "#f9f4e6", "#8a6b2f", 3, "12,6"))
    partes.append(_texto(ox + a / 2 + 90, oy - 14, "rot",
                         "Atrio: 100 × 50 codos (unos 50 × 25 m) · cortinas de lino sobre 60 columnas"))
    # Puerta oriental (20 codos = 100 px)
    partes.append(_caja(ox + a / 2 - 50, oy + b - 6, 100, 12, "#b98a2b", "#6b4c11", 2))
    partes.append(_texto(ox + a / 2, oy + b + 32, "rot", "Puerta del atrio (20 codos)"))
    # Tabernáculo: 30 x 10 codos, ampliado
    tx, ty, tw, th = 450, 210, 300, 95
    partes.append(_caja(tx, ty, tw, th, "#efe2c4", "#6b4c11", 2.8))
    partes.append(_caja(tx, ty, 100, th, "#e3d3ab", "#6b4c11", 2.4))
    partes.append(f'<line x1="{tx+100}" y1="{ty-10}" x2="{tx+100}" y2="{ty+th+10}" stroke="#8b2f1f" '
                  f'stroke-width="3" stroke-dasharray="7,4"/>')
    partes.append(_texto(tx + 50, ty + 40, "rot-peq", "Lugar"))
    partes.append(_texto(tx + 50, ty + 58, "rot-peq", "Santísimo"))
    partes.append(_texto(tx + 200, ty + 40, "rot-peq", "Lugar Santo"))
    partes.append(_texto(tx + 100, ty - 18, "medida", "Velo (Éxodo 26:31-33)"))
    # Arca, mesa y candelabro
    partes.append(_caja(tx + 26, ty + 60, 48, 20, "#c9a227", "#6b4c11", 1.8))
    partes.append(_texto(tx + 50, ty + 92, "medida", "Arca"))
    partes.append(_caja(tx + 140, ty + 56, 34, 20, "#e0cf9a", "#6b4c11", 1.8))
    partes.append(_texto(tx + 157, ty + 92, "medida", "Mesa de los panes"))
    partes.append(f'<circle cx="{tx+245}" cy="{ty+60}" r="10" fill="none" stroke="#8a6b2f" stroke-width="2.4"/>'
                  f'<line x1="{tx+245}" y1="{ty+70}" x2="{tx+245}" y2="{ty+80}" stroke="#8a6b2f" stroke-width="2.4"/>')
    partes.append(_texto(tx + 245, ty + 92, "medida", "Candelabro"))
    # Altar del holocausto y fuente, en la mitad oriental del atrio
    partes.append(_caja(450, 340, 42, 42, "#cbb08a", "#7a5c33", 2.2))
    partes.append(_texto(471, 330, "medida", "Altar del holocausto"))
    partes.append(_texto(471, 398, "medida", "5 × 5 codos"))
    partes.append(f'<circle cx="620" cy="361" r="17" fill="#cfe3f0" stroke="#4a7fa5" stroke-width="2.4"/>')
    partes.append(_texto(620, 330, "medida", "Fuente de bronce"))
    # Orientación
    partes.append(_texto(ox - 20, 250, "rot-izq", "← Oeste"))
    partes.append(_texto(ox - 20, 272, "rot-izq", "Lugar Santísimo"))
    partes.append(_texto(ox + a + 20, 250, "rot-der", "Este →"))
    partes.append(_texto(ox + a + 20, 272, "rot-der", "puerta y altar"))
    partes += _notas([
        "El atrio se cerraba con cortinas de lino colgadas de sesenta columnas con basas de bronce.",
        "El pueblo permanecía en el atrio; los sacerdotes entraban al Lugar Santo y solo el sumo",
        "sacerdote al Lugar Santísimo, una vez al año (Levítico 16).",
        "La nube de la gloria de Dios llenó el tabernáculo cuando Moisés lo terminó (Éxodo 40:34-38).",
    ], y0=660)
    return _svg(partes)


# ---------------------------------------------------------------------------
# 2. El templo de Herodes
# ---------------------------------------------------------------------------
def plano_templo_herodes():
    partes = [_cabecera("El templo de Herodes y su explanada",
                        "Siglo I · Josefo, Antigüedades XV-XVII, y la arqueología de Jerusalén")]
    # Explanada (atrio de los gentiles)
    px, py, pw, ph = 270, 200, 760, 330
    partes.append(_caja(px, py, pw, ph, "#f9f4e6", "#8a6b2f", 3))
    partes.append(_texto(px + 16, py + 26, "rot-der", "Atrio de los gentiles y pórticos reales"))
    partes.append(_texto(px + pw - 16, py + 26, "rot-izq", "Explanada: unos 480 × 300 m"))
    # Torre Antonia y Betesda (al norte)
    partes.append(_caja(px + 30, py - 66, 150, 60, "#d9cbb0", "#7a5c33", 2.4))
    partes.append(_texto(px + 105, py - 76, "rot", "Torre Antonia (guarnición romana)"))
    partes.append(_caja(px + 520, py - 60, 140, 54, "#cfe3f0", "#4a7fa5", 2.2))
    partes.append(_texto(px + 590, py - 70, "rot", "Estanque de Betesda"))
    # Atrio de las mujeres
    partes.append(_caja(px + 400, py + 70, 330, 240, "#efe2c4", "#b98a2b", 2.4, "9,5"))
    partes.append(_texto(px + 565, py + 122, "rot-peq", "Atrio de las mujeres"))
    # Atrio de Israel y de los sacerdotes
    partes.append(_caja(px + 450, py + 100, 240, 180, "#e9dcb8", "#8a6b2f", 2.2))
    partes.append(_texto(px + 462, py + 266, "rot-peq", "Atrio de Israel y de los sacerdotes"))
    # Santuario
    sx, sy, sw, sh = px + 500, py + 118, 140, 110
    partes.append(_caja(sx, sy, sw, sh, "#fdf9ef", "#6b4c11", 3))
    partes.append(_texto(sx + 70, sy - 10, "rot", "Santuario: 100 codos de alto"))
    partes.append(_texto(sx + sw - 14, sy + 30, "rot-der", "Lugar Santo"))
    partes.append(_texto(sx + 14, sy + 30, "rot-der", "Lugar"))
    partes.append(_texto(sx + 14, sy + 48, "rot-der", "Santísimo"))
    partes.append(f'<line x1="{sx+42}" y1="{sy}" x2="{sx+42}" y2="{sy+sh}" stroke="#6b4c11" stroke-width="2"/>')
    # Altar
    partes.append(_caja(px + 540, py + 288, 60, 34, "#cbb08a", "#7a5c33", 2.2))
    partes.append(_texto(px + 570, py + 336, "rot-peq", "Altar de los holocaustos"))
    # Puertas
    partes.append(_caja(px + pw - 6, py + 130, 12, 70, "#b98a2b", "#6b4c11", 1.6))
    partes.append(_texto(px + pw + 20, py + 170, "rot-der", "Puerta Dorada (este)"))
    partes.append(_caja(px - 6, py + 130, 12, 70, "#b98a2b", "#6b4c11", 1.6))
    partes.append(_texto(px - 20, py + 170, "rot-izq", "Puerta de Suse (oeste)"))
    partes.append(_caja(px + 340, py + ph - 6, 70, 12, "#b98a2b", "#6b4c11", 1.6))
    partes.append(_texto(px + 375, py + ph + 26, "rot-peq", "Puerta de Hulda (sur)"))
    # Siloé y túnel de Ezequías
    partes.append(_caja(px - 200, py + 240, 130, 50, "#cfe3f0", "#4a7fa5", 2.2))
    partes.append(_texto(px - 200, py + 226, "rot-der", "Estanque de Siloé"))
    partes.append(f'<path d="M{px - 70} {py + 258} C {px - 20} {py + 232}, {px + 60} {py + 240}, '
                  f'{px + 210} {py + 276}" fill="none" stroke="#4a7fa5" stroke-width="2.6" stroke-dasharray="8,5"/>')
    partes.append(_texto(px + 60, py + 226, "rot-peq", "Túnel de Ezequías (533 m)"))
    partes += _notas([
        "El santuario seguía las proporciones del de Salomón (1 Reyes 6) con un pórtico de 100 codos de alto.",
        "Una balaustrada (soreg) separaba el atrio de los gentiles con avisos en griego y en latín.",
        "Jesús enseñó en el pórtico de Salomón, en el atrio de los gentiles (Juan 10:23; Hechos 3:11).",
        "Los romanos destruyeron el templo en el año 70 d.C.; solo queda en pie el muro occidental.",
    ])
    return _svg(partes)


# ---------------------------------------------------------------------------
# 3. Jerusalén en tiempos de Jesús
# ---------------------------------------------------------------------------
def plano_jerusalen():
    partes = [_cabecera("Jerusalén en tiempos de Jesús",
                        "Plano esquemático de la ciudad, sus murallas y sus valles")]
    # Valles (Cedrón al este, Hinom al sur y oeste)
    partes.append('<path d="M150 110 C 250 290, 265 445, 210 570 L 300 570 C 355 445, 340 290, 235 110 Z" '
                  'fill="#cfe3f0" fill-opacity="0.8"/>')
    partes.append(_texto(200, 240, "rot", "Valle del Cedrón"))
    partes.append('<path d="M700 590 C 780 495, 900 440, 1090 420 L 1090 485 C 930 505, 850 550, 800 590 Z" '
                  'fill="#cfe3f0" fill-opacity="0.8"/>')
    partes.append(_texto(950, 532, "rot", "Valle de Hinom (Gehena)"))
    # Ciudad alta, ciudad baja y monte del templo
    partes.append('<path d="M300 190 L 560 170 L 690 285 L 690 440 L 520 565 L 300 525 Z" fill="#f9f4e6" '
                  'stroke="#8a6b2f" stroke-width="3"/>')
    partes.append('<path d="M690 285 L 860 320 L 900 440 L 690 440 Z" fill="#efe2c4" stroke="#8a6b2f" stroke-width="3"/>')
    partes.append(_texto(470, 315, "rot", "Ciudad alta"))
    partes.append(_texto(795, 400, "rot", "Ciudad baja"))
    partes.append(_caja(690, 190, 230, 145, "#e3d3ab", "#6b4c11", 3))
    partes.append(_texto(805, 178, "rot", "Explanada del templo"))
    partes.append(_caja(770, 224, 80, 76, "#fdf9ef", "#6b4c11", 2.4))
    partes.append(_texto(810, 266, "rot-peq", "Santuario"))
    # Torre Antonia
    partes.append(_caja(640, 188, 52, 40, "#d9cbb0", "#7a5c33", 2))
    partes.append(_texto(634, 168, "rot-der", "Torre Antonia"))
    # Palacio de Herodes
    partes.append(_caja(340, 202, 130, 80, "#e8dcc0", "#7a5c33", 2))
    partes.append(_texto(405, 246, "rot-peq", "Palacio de Herodes"))
    # Cenáculo, Betesda y Siloé
    partes.append(f'<circle cx="420" cy="490" r="7" fill="#8b2f1f"/>')
    partes.append(_texto(420, 476, "rot", "Monte Sion · cenáculo"))
    partes.append(_caja(950, 196, 110, 46, "#cfe3f0", "#4a7fa5", 2.2))
    partes.append(_texto(1005, 184, "rot", "Estanque de Betesda"))
    partes.append(_caja(620, 578, 130, 46, "#cfe3f0", "#4a7fa5", 2.2))
    partes.append(_texto(700, 646, "rot", "Estanque de Siloé"))
    # Getsemaní y Gólgota
    partes.append(f'<circle cx="900" cy="120" r="7" fill="#5c7a29"/>')
    partes.append(_texto(900, 106, "rot", "Getsemaní"))
    partes.append(f'<circle cx="600" cy="130" r="7" fill="#8b2f1f"/>')
    partes.append(_texto(600, 116, "rot", "Gólgota"))
    # Puertas
    puertas = [("Puerta de Damasco", 470, 174, "arriba"),
               ("Puerta de Jaffa", 318, 400, "izquierda"),
               ("Puerta de Sion", 460, 556, "abajo"),
               ("Puerta del Estiércol", 620, 574, "abajo"),
               ("Puerta de la Fuente", 700, 540, "abajo"),
               ("Puerta del Agua", 700, 424, "derecha"),
               ("Puerta de las Ovejas", 700, 240, "derecha"),
               ("Puerta Dorada", 920, 250, "derecha")]
    for nombre, gx, gy, pos in puertas:
        partes.append(f'<circle cx="{gx}" cy="{gy}" r="5.5" fill="#b98a2b" stroke="#6b4c11" stroke-width="1"/>')
        if pos == "arriba":
            partes.append(_texto(gx, gy - 12, "rot-peq", nombre))
        elif pos == "abajo":
            partes.append(_texto(gx, gy + 22, "rot-peq", nombre))
        elif pos == "izquierda":
            partes.append(_texto(gx - 12, gy + 4, "rot-izq", nombre))
        else:
            partes.append(_texto(gx + 12, gy + 4, "rot-der", nombre))
    partes += _notas([
        "La ciudad ocupaba unas 100 hectáreas y en el siglo I estaba rodeada por tres murallas.",
        "El Cedrón separa la ciudad del monte de los Olivos; el Hinom (Gehena) la rodea por el sur.",
        "El túnel de Ezequías llevaba el agua del manantial de Gihón hasta el estanque de Siloé.",
    ])
    return _svg(partes)


PLANOS = [
    {
        "id": "plano-tabernaculo", "titulo": "El tabernáculo del desierto",
        "subtitulo": "Éxodo 25-40", "categoria": "Planos",
        "descripcion": "Plano del santuario portátil que Israel construyó en el desierto: el atrio de "
                       "100 × 50 codos, el tabernáculo de 30 × 10 × 10 codos con el Lugar Santo y el "
                       "Lugar Santísimo, el velo, el arca, la mesa de los panes, el candelabro, el altar "
                       "del holocausto y la fuente de bronce. Las medidas son las del texto de Éxodo.",
        "elementos": 14, "refs": ["Éxodo 25:1-9", "Éxodo 40:1-38", "Hebreos 9:1-5"],
        "notas": ["El tabernáculo se levantó el primer día del primer mes del segundo año (Éxodo 40:17)."],
        "generar": plano_tabernaculo,
    },
    {
        "id": "plano-templo-herodes", "titulo": "El templo de Herodes",
        "subtitulo": "Siglo I · Josefo y la arqueología", "categoria": "Planos",
        "descripcion": "Esquema de la explanada del templo tal como la conoció Jesús: el atrio de los "
                       "gentiles, el atrio de las mujeres, el atrio de Israel, el santuario con el Lugar "
                       "Santo y el Lugar Santísimo, el altar de los holocaustos, la torre Antonia, los "
                       "estanques de Betesda y Siloé y el túnel de Ezequías.",
        "elementos": 16, "refs": ["Marcos 13:1-2", "Juan 2:20", "Hechos 3:1-10"],
        "notas": ["Herodes el Grande comenzó la obra hacia el año 20 a.C. y aún continuaba en tiempos de "
                  "Jesús (Juan 2:20)."],
        "generar": plano_templo_herodes,
    },
    {
        "id": "plano-jerusalen", "titulo": "Jerusalén en tiempos de Jesús",
        "subtitulo": "Murallas, valles y puertas", "categoria": "Planos",
        "descripcion": "Plano esquemático de la ciudad con la ciudad alta y la baja, el monte del templo y "
                       "la torre Antonia, los valles del Cedrón y de Hinom, los estanques de Betesda y "
                       "Siloé, Getsemaní y el Gólgota, y las puertas que aparecen en los evangelios y en "
                       "Nehemías.",
        "elementos": 20, "refs": ["Nehemías 3:1-32", "Lucas 19:28-44", "Hechos 2:1-13"],
        "notas": ["En las fiestas de peregrinación la población de Jerusalén podía multiplicarse por tres."],
        "generar": plano_jerusalen,
    },
]
