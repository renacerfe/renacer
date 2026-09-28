/* ==========================================================================
   Renacer · Atlas Bíblico y Biblioteca
   Aplicación de una sola página, sin dependencias externas.

   Secciones: inicio · mapas · lugares · diccionarios · temas · biblia ·
              arte · cartografia · biblioteca · ayuda · acerca · creditos
   ========================================================================== */
'use strict';

/* ------------------------------ estado global ---------------------------- */
const App = {
  indice: null,
  cache: new Map(),          // ruta -> datos ya cargados
  cargando: new Map(),       // ruta -> promesa en curso
  ajustes: null,
  navegacion: [
    ['inicio', 'Inicio'],
    ['mapas', 'Mapas'],
    ['lugares', 'Lugares'],
    ['diccionarios', 'Diccionarios'],
    ['temas', 'Temas'],
    ['biblia', 'Biblia'],
    ['arte', 'Arte'],
    ['cartografia', 'Cartografía'],
    ['biblioteca', 'Biblioteca'],
    ['ayuda', 'Ayuda'],
  ],
};

const CARPETA = 'datos/';

/* ------------------------------- utilidades ------------------------------ */
const $ = (sel, raiz) => (raiz || document).querySelector(sel);
const $$ = (sel, raiz) => Array.from((raiz || document).querySelectorAll(sel));

/** Acepta tanto un número como una lista y devuelve la cantidad. */
function numeroDe(valor) {
  if (typeof valor === 'number') return valor;
  return Array.isArray(valor) ? valor.length : 0;
}

function crear(etiqueta, atributos, hijos) {
  const el = document.createElement(etiqueta);
  if (atributos) {
    for (const [clave, valor] of Object.entries(atributos)) {
      if (valor === null || valor === undefined || valor === false) continue;
      if (clave === 'html') { el.innerHTML = valor; continue; }
      if (clave === 'texto') { el.textContent = valor; continue; }
      if (clave === 'clase') { el.className = valor; continue; }
      if (clave.startsWith('on') && typeof valor === 'function') {
        el.addEventListener(clave.slice(2).toLowerCase(), valor);
        continue;
      }
      el.setAttribute(clave, valor);
    }
  }
  if (hijos !== undefined && hijos !== null) {
    for (const hijo of [].concat(hijos)) {
      if (hijo === null || hijo === undefined || hijo === false) continue;
      el.append(hijo instanceof Node ? hijo : document.createTextNode(String(hijo)));
    }
  }
  return el;
}

function escapar(texto) {
  return String(texto === null || texto === undefined ? '' : texto)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

/** Quita los acentos y pasa a minúsculas, para buscar sin preocuparse por ellos. */
function normalizar(texto) {
  return String(texto || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .toLowerCase().replace(/[^a-z0-9ñ¿?]+/g, ' ').trim();
}

function sinAcentos(texto) {
  return String(texto || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '');
}

function miles(n) {
  return Number(n || 0).toLocaleString('es-ES');
}

function fechaLarga(iso) {
  if (!iso) return '';
  const [a, m, d] = String(iso).split('-');
  const meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio',
    'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'];
  return `${Number(d)} de ${meses[Number(m) - 1]} de ${a}`;
}

async function cargar(ruta) {
  const clave = CARPETA + ruta;
  if (App.cache.has(clave)) return App.cache.get(clave);
  if (App.cargando.has(clave)) return App.cargando.get(clave);
  const promesa = fetch(clave)
    .then((r) => { if (!r.ok) throw new Error(`${r.status} al leer ${clave}`); return r.json(); })
    .then((datos) => { App.cache.set(clave, datos); App.cargando.delete(clave); return datos; })
    .catch((e) => { App.cargando.delete(clave); throw e; });
  App.cargando.set(clave, promesa);
  return promesa;
}

const cargarIndice = () => cargar('indice.json');
const cargarMapas = () => cargar('mapas.json');
const cargarLugares = () => cargar('lugares.json');
const cargarLugaresIndice = () => cargar('lugares_indice.json');
const cargarTemasIndice = () => cargar('temas_indice.json');
const cargarTemas = () => cargar('temas.json');
const cargarFotos = () => cargar('fotos.json');
const cargarArte = () => cargar('arte.json');
const cargarBase = () => cargar('base.json');
const cargarDiccionariosIndice = () => cargar('diccionarios_indice.json');
const cargarDiccionario = (codigo) => cargar(`diccionarios/${codigo}.json`);
const cargarBibliaLibros = () => cargar('biblia/libros.json');
const cargarBibliaLibro = (osis) => cargar(`biblia/${osis}.json`);
const cargarBibliaBusqueda = () => cargar('biblia_busqueda.json').catch(() => []);

const NOMBRES_DICCIONARIO = {
  easton: ['Diccionario Bíblico de Easton', 'Matthew George Easton, 1897'],
  smith: ['Diccionario Bíblico de Smith', 'William Smith, 1863'],
  hastings: ['Diccionario de la Biblia de Hastings', 'James Hastings, 1898'],
  hitchcock: ['Nombres propios de Hitchcock', 'Roswell D. Hitchcock, 1869'],
  schaff: ['Enciclopedia de Schaff', 'Philip Schaff, 1880'],
};

/* --------------------------- referencias bíblicas ------------------------- */
/* Índice para resolver «Génesis 12:1» -> {osis, capitulo, versiculo}.        */
let INDICE_REFS = null;

function construirIndiceRefs(libros) {
  if (INDICE_REFS) return INDICE_REFS;
  const mapa = new Map();
  for (const libro of libros) {
    const formas = [libro.nombre, libro.abrev, libro.osis];
    for (const forma of formas) {
      const clave = normalizar(forma).replace(/\s+/g, ' ');
      if (clave) mapa.set(clave, libro);
      // los nombres compuestos también responden a su primera palabra
      const primera = clave.split(' ')[0];
      if (primera && primera.length > 3 && !mapa.has(primera)) mapa.set(primera, libro);
    }
  }
  INDICE_REFS = { mapa, libros };
  return INDICE_REFS;
}

/** Normaliza una cita conservando «:» y números: «1 Samuel 17:38-51». */
function normalizarCita(texto) {
  return sinAcentos(String(texto || '')).toLowerCase()
    .replace(/\s+/g, ' ').replace(/\s*:\s*/g, ':').trim();
}

/** Convierte «1 Samuel 17:38-51» en {libro, capitulo, versiculo} o null. */
function partirReferencia(texto, libros) {
  const datos = construirIndiceRefs(libros);
  // se cortan los encadenamientos y los rangos: «Gén 12:1; 15:2» -> «Gén 12:1»
  let t = normalizarCita(texto).replace(/[;,].*$/, '')
    .replace(/^(\d)\s+/, '$1 ')                                     // «1 samuel»
    .replace(/^(i|ii|iii)\s+/, (m, p) => ({ i: '1', ii: '2', iii: '3' }[p]) + ' ');
  const coincidencia = t.match(/^([1-3]?\s?[a-zñ]+(?:\s+[a-zñ]+)*?)\s+(\d+)(?::(\d+))?/);
  if (!coincidencia) return null;
  const nombre = coincidencia[1].trim();
  const libro = datos.mapa.get(nombre) || datos.mapa.get(nombre.split(' ')[0])
    || datos.mapa.get(nombre.split(' ').slice(-1)[0]);
  if (!libro) return null;
  return { libro, capitulo: Number(coincidencia[2]), versiculo: coincidencia[3] ? Number(coincidencia[3]) : null };
}

/* ------------------------------- navegación ------------------------------- */
function pintarNavegacion(seccion) {
  const nav = $('#nav-principal');
  nav.innerHTML = '';
  for (const [clave, etiqueta] of App.navegacion) {
    const activo = seccion === clave;
    nav.append(crear('a', {
      href: `#/${clave}`, texto: etiqueta, 'aria-current': activo ? 'page' : null,
    }));
  }
}

function irA(destino, empujar) {
  const ruta = destino.startsWith('#') ? destino.slice(1) : destino;
  if (empujar === false) {
    history.replaceState(null, '', '#' + ruta);
    enrutar();
  } else {
    location.hash = ruta;
  }
}

function rutaActual() {
  const bruta = location.hash.replace(/^#\/?/, '');
  const [camino, resto] = bruta.split('?');
  const partes = camino.split('/').filter(Boolean).map(decodeURIComponent);
  const parametros = new URLSearchParams(resto || location.hash.split('?')[1] || '');
  return {
    seccion: partes[0] || 'inicio',
    partes: partes.slice(1),
    parametros,
    bruta,
  };
}

/* --------------------------------- vistas --------------------------------- */
const VISTAS = {};

VISTAS.inicio = async () => {
  const [indice, mapas, lugares, fotos] = await Promise.all([
    cargarIndice(), cargarMapas(), cargarLugaresIndice(), cargarFotos().catch(() => []),
  ]);
  const contenedor = crear('div');
  contenedor.append(crear('div', { clase: 'portada' }, [
    crear('img', { src: 'imagenes/portada.jpg', alt: 'Mapa antiguo de la tierra de la Biblia' }),
    crear('div', { clase: 'portada-texto' }, [
      crear('h1', { texto: 'Renacer · Atlas Bíblico' }),
      crear('p', { texto: 'Todos los mapas bíblicos que hemos podido reunir, la biblioteca completa '
        + 'de diccionarios enciclopédicos de dominio público, una galería de arte y la Biblia '
        + 'Reina-Valera 1960, en español y funcionando sin conexión.' }),
      crear('div', { clase: 'cifras' }, [
        crear('div', {}, [crear('strong', { texto: miles(mapas.length) }), 'mapas y planos']),
        crear('div', {}, [crear('strong', { texto: miles(lugares.length) }), 'lugares con referencias']),
        crear('div', {}, [crear('strong', { texto: miles(indice.temas) }), 'temas bíblicos']),
        crear('div', {}, [crear('strong', { texto: miles((indice.diccionarios || []).reduce((s, d) => s + (d.entradas || 0), 0)) }), 'voces de diccionario']),
        crear('div', {}, [crear('strong', { texto: miles(indice.versiculos_biblia) }), 'versículos']),
        crear('div', {}, [crear('strong', { texto: miles(indice.obras_arte || 241) }), 'grabados de Doré']),
      ]),
    ]),
  ]));

  const accesos = crear('div', { clase: 'rejilla' });
  const TARJETAS = [
    ['mapas', 'Mapas y planos', 'seccion-mapas.jpg',
      `${mapas.length} mapas: geografía de la Biblia, viajes de Abraham, el éxodo, la conquista, los reinos, el mundo del Nuevo Testamento, los viajes de Pablo y tres planos del tabernáculo, el templo y Jerusalén.`],
    ['lugares', 'Lugares bíblicos', '', 'seccion-mapas.jpg',
      `${lugares.length} lugares citados en la Biblia, con sus referencias, su nombre original y su situación en el mapa.`],
    ['diccionarios', 'Diccionarios enciclopédicos', '', 'seccion-biblioteca.jpg',
      'Cinco diccionarios completos del siglo XIX (Easton, Smith, Hastings, Hitchcock y Schaff): más de 11.000 voces sobre personas, lugares, objetos y costumbres.'],
    ['temas', 'Temas y cadenas de referencias', '', 'seccion-biblioteca.jpg',
      `${indice.temas} temas con ${miles(indice.referencias_tematicas)} referencias bíblicas, tomados de «Nave’s Topical Bible» (1896) y «Torrey’s New Topical Textbook» (1897).`],
    ['biblia', 'La Biblia', '', 'seccion-biblia.jpg',
      `Reina-Valera 1960 completa: ${indice.libros_biblia} libros y ${miles(indice.versiculos_biblia)} versículos, con búsqueda por palabra y referencias cruzadas.`],
    ['arte', 'Galería de arte', '', 'seccion-arte.jpg',
      `${(indice.obras_arte || 241)} grabados de Gustave Doré para «La Grande Bible de Tours» (1866), en dominio público, con su referencia en español.`],
    ['cartografia', 'Cartografía histórica', '', 'seccion-mapas.jpg',
      'La historia de los mapas de la Biblia —de la tabla de Madaba al Atlas de 1907— y enlaces a las colecciones digitales de acceso libre.'],
    ['biblioteca', 'Biblioteca y fuentes', '', 'seccion-biblioteca.jpg',
      'Enciclopedia propia y el catálogo de fuentes, licencias y colecciones públicas de donde procede todo el contenido.'],
  ];
  for (const [clave, titulo, imagen, texto] of TARJETAS) {
    accesos.append(crear('div', { clase: 'tarjeta', role: 'link', tabindex: '0',
      onclick: () => irA(`#/${clave}`),
      onkeydown: (e) => { if (e.key === 'Enter') irA(`#/${clave}`); } }, [
      crear('img', { clase: 'miniatura', src: `imagenes/${imagen}`, alt: '' }),
      crear('h3', { texto: titulo }),
      crear('p', { texto: texto }),
      crear('div', { clase: 'pie-tarjeta' }, [crear('span', { clase: 'etiqueta oro', texto: 'Abrir' })]),
    ]));
  }
  contenedor.append(crear('h2', { texto: 'Explorar' }), accesos);

  contenedor.append(crear('h2', { texto: 'Un paseo por el atlas' }), galeriaMapas(
    mapas.filter((m) => ['El mundo de la Biblia', 'Vida de Jesús', 'Hechos y Pablo', 'Planos']
      .includes(m.categoria)).slice(0, 4), true));

  const hoy = new Date();
  contenedor.append(crear('p', { clase: 'leyenda-mapa', style: 'margin-top:26px' ,
    texto: `Datos compilados el ${fechaLarga(indice.construido)} · consultado el ${hoy.toLocaleDateString('es-ES')}` }));
  return contenedor;
};

/* ---------------------------------- mapas --------------------------------- */
function galeriaMapas(mapas, compacta) {
  if (!mapas.length) return crear('p', { clase: 'sin-resultados', texto: 'No hay mapas que mostrar.' });
  const rejilla = crear('div', { clase: 'galeria-mapas' });
  for (const mapa of mapas) {
    rejilla.append(crear('article', { clase: 'marco-mapa', tabindex: '0', role: 'link',
      onclick: () => irA(`#/mapas/${mapa.id}`),
      onkeydown: (e) => { if (e.key === 'Enter') irA(`#/mapas/${mapa.id}`); } }, [
      crear('img', { src: `mapas/${mapa.id}.svg`, alt: `Mapa: ${mapa.titulo}`, loading: 'lazy' }),
      crear('div', { clase: 'cuerpo' }, [
        crear('span', { clase: 'etiqueta', texto: mapa.categoria }),
        crear('h3', { texto: mapa.titulo }),
        crear('p', { texto: compacta ? (mapa.subtitulo || '') : (mapa.descripcion || '') }),
        crear('div', { clase: 'pie-tarjeta' }, [
          crear('span', { texto: `${numeroDe(mapa.lugares)} ${mapa.categoria === 'Planos' ? 'elementos' : 'lugares'}` }),
          numeroDe(mapa.rutas) ? crear('span', { texto: `${numeroDe(mapa.rutas)} rutas` }) : null,
          crear('span', { texto: (mapa.refs || []).slice(0, 2).join(' · ') }),
        ]),
      ]),
    ]));
  }
  return rejilla;
}

VISTAS.mapas = async (partes) => {
  if (partes && partes[0]) return VISTAS['mapa-detalle'](partes[0]);
  const mapas = await cargarMapas();
  const contenedor = crear('div');
  contenedor.append(cabeceraSeccion('Mapas y planos',
    `${mapas.length} mapas dibujados para esta aplicación a partir de datos geográficos libres, `
    + 'con las rutas y los lugares que cita el texto bíblico. Elige una categoría o busca por título.', 'seccion-mapas.jpg'));

  const categorias = [...new Set(mapas.map((m) => m.categoria))];
  const estado = { texto: '', categoria: categorias[0] };

  const barra = crear('div', { clase: 'barra-herramientas' });
  const entrada = crear('input', { type: 'search', placeholder: 'Buscar un mapa por título, lugar o referencia…', 'aria-label': 'Buscar mapa' });
  const selector = crear('select', { 'aria-label': 'Categoría' },
    categorias.map((c) => crear('option', { value: c, texto: `${c} (${mapas.filter((m) => m.categoria === c).length})` })));
  const contador = crear('span', { clase: 'leyenda-mapa' });
  barra.append(entrada, selector, contador);

  const salida = crear('div');
  function refrescar() {
    const t = normalizar(estado.texto);
    let lista = mapas;
    if (t) {
      lista = mapas.filter((m) => normalizar([m.titulo, m.subtitulo, m.descripcion,
        (m.lugares || []).map((l) => l.nombre || l).join(' '), (m.refs || []).join(' ')].join(' ')).includes(t));
    } else {
      lista = mapas.filter((m) => m.categoria === estado.categoria);
    }
    contador.textContent = `${lista.length} mapa${lista.length === 1 ? '' : 's'}`;
    salida.innerHTML = '';
    salida.append(galeriaMapas(lista));
  }
  entrada.addEventListener('input', () => { estado.texto = entrada.value; refrescar(); });
  selector.addEventListener('change', () => { estado.categoria = selector.value; refrescar(); });
  refrescar();
  contenedor.append(barra, salida);
  return contenedor;
};

VISTAS['mapa-detalle'] = async (id) => {
  const mapas = await cargarMapas();
  const mapa = mapas.find((m) => m.id === id);
  if (!mapa) return noEncontrado('mapa', id);
  const contenedor = crear('div');
  contenedor.append(migas([['mapas', 'Mapas'], [null, mapa.titulo]]));
  contenedor.append(crear('h1', { texto: mapa.titulo }));
  if (mapa.subtitulo) contenedor.append(crear('p', { clase: 'leyenda-mapa', texto: mapa.subtitulo }));

  // visor con zoom y desplazamiento
  const marco = crear('div', { clase: 'visor' });
  const lienzo = crear('div', { clase: 'lienzo' });
  const imagen = crear('img', { src: `mapas/${mapa.id}.svg`, alt: `Mapa: ${mapa.titulo}` });
  imagen.style.transformOrigin = '0 0';
  lienzo.append(imagen);
  const controles = crear('div', { clase: 'visor-controles' });
  marco.append(lienzo, controles);
  contenedor.append(marco);
  activarZoom(lienzo, imagen, controles, mapa);
  contenedor.append(crear('p', { clase: 'leyenda-mapa',
    texto: 'Arrastra con el ratón para mover el mapa, usa la rueda para acercar y los botones para ajustar. '
      + (mapa.notas ? mapa.notas : '') }));

  const columnas = crear('div', { clase: 'detalle', style: 'margin-top:20px' });
  const principal = crear('div', { clase: 'panel' });
  principal.append(crear('h3', { texto: 'Sobre este mapa' }));
  for (const parrafo of String(mapa.descripcion || '').split(/\n+/)) {
    if (parrafo.trim()) principal.append(crear('p', { texto: parrafo }));
  }
  if (mapa.lista_rutas && mapa.lista_rutas.length) {
    principal.append(crear('h3', { texto: 'Rutas y trayectos' }));
    const lista = crear('ul', { clase: 'lista-hechos' });
    for (const ruta of mapa.lista_rutas) {
      lista.append(crear('li', {}, [
        crear('span', { style: `display:inline-block;width:11px;height:11px;border-radius:3px;background:${ruta.color};margin-right:8px` }),
        crear('b', { texto: ruta.nombre }), ruta.nota ? ` — ${ruta.nota}` : '',
      ]));
    }
    principal.append(lista);
  }
  if (mapa.refs && mapa.refs.length) {
    principal.append(crear('h3', { texto: 'Referencias bíblicas' }));
    principal.append(crear('p', {}, mapa.refs.map((r) => referenciaEnlazada(r))));
  }
  columnas.append(principal);

  const lateral = crear('div', { clase: 'panel' });
  lateral.append(crear('h3', { texto: 'Lugares del mapa' }));
  const buscador = crear('input', { type: 'search', placeholder: 'Filtrar lugares…',
    style: 'width:100%;margin-bottom:10px;padding:8px 10px;border-radius:9px;border:1px solid var(--borde);background:var(--papel)' });
  const lista = crear('ul', { clase: 'lista-hechos', style: 'max-height:520px;overflow:auto' });
  const lugares = (mapa.lista_lugares || []);
  if (!lugares.length) {
    lateral.append(crear('p', { clase: 'leyenda-mapa',
      texto: `${mapa.lugares} elementos dibujados en este plano: mobiliario, patios, puertas y dependencias.` }));
  }
  function pintarLugares(filtro) {
    lista.innerHTML = '';
    const t = normalizar(filtro || '');
    const vistos = lugares.filter((l) => !t || normalizar(l.nombre).includes(t));
    for (const lugar of vistos) {
      const elemento = crear('li');
      elemento.append(lugar.id ? crear('a', { href: `#/lugares/${lugar.id}`, texto: lugar.nombre })
        : crear('span', { texto: lugar.nombre }));
      if (lugar.tipo) elemento.append(crear('span', { clase: 'etiqueta', style: 'margin-left:8px', texto: lugar.tipo }));
      if (lugar.refs && lugar.refs.length) {
        elemento.append(crear('div', { clase: 'leyenda-mapa' },
          lugar.refs.slice(0, 3).map((r) => referenciaEnlazada(r))));
      }
      lista.append(elemento);
    }
    if (!vistos.length) lista.append(crear('li', { clase: 'leyenda-mapa', texto: 'Sin coincidencias.' }));
  }
  pintarLugares('');
  buscador.addEventListener('input', () => pintarLugares(buscador.value));
  lateral.append(buscador, lista);
  columnas.append(lateral);
  contenedor.append(columnas);

  const hermanos = mapas.filter((m) => m.categoria === mapa.categoria && m.id !== mapa.id);
  if (hermanos.length) {
    contenedor.append(crear('h2', { texto: `Más mapas de «${mapa.categoria}»` }), galeriaMapas(hermanos, true));
  }
  return contenedor;
};

/** Zoom y desplazamiento sobre una imagen dentro de un marco. */
function activarZoom(marco, imagen, controles, mapa) {
  let escala = 1, x = 0, y = 0, arrastrando = false, origen = null;
  const MIN = 1, MAX = 14;

  function aplicar() {
    imagen.style.transform = `translate(${x}px, ${y}px) scale(${escala})`;
    imagen.style.cursor = escala > 1 ? 'move' : 'zoom-in';
  }
  function ajustar(nueva, cx, cy) {
    const rect = marco.getBoundingClientRect();
    const px = (cx === undefined ? rect.width / 2 : cx - rect.left);
    const py = (cy === undefined ? rect.height / 2 : cy - rect.top);
    const proporcion = Math.min(MAX, Math.max(MIN, nueva)) / escala;
    x = px - (px - x) * proporcion;
    y = py - (py - y) * proporcion;
    escala *= proporcion;
    limitar();
    aplicar();
  }
  function limitar() {
    const ancho = marco.clientWidth, alto = marco.clientHeight;
    const anchoImagen = imagen.clientWidth * escala, altoImagen = imagen.clientHeight * escala;
    x = anchoImagen <= ancho ? (ancho - anchoImagen) / 2 : Math.min(0, Math.max(ancho - anchoImagen, x));
    y = altoImagen <= alto ? (alto - altoImagen) / 2 : Math.min(0, Math.max(alto - altoImagen, y));
  }
  function reiniciar() { escala = 1; x = 0; y = 0; aplicar(); }

  marco.addEventListener('wheel', (e) => {
    e.preventDefault();
    ajustar(escala * (e.deltaY < 0 ? 1.18 : 1 / 1.18), e.clientX, e.clientY);
  }, { passive: false });
  marco.addEventListener('pointerdown', (e) => {
    if (escala <= 1) return;
    arrastrando = true; origen = { x: e.clientX - x, y: e.clientY - y };
    marco.classList.add('arrastrando');
    marco.setPointerCapture(e.pointerId);
  });
  marco.addEventListener('pointermove', (e) => {
    if (!arrastrando) return;
    x = e.clientX - origen.x; y = e.clientY - origen.y; limitar(); aplicar();
  });
  const soltar = (e) => {
    if (!arrastrando) return;
    arrastrando = false; marco.classList.remove('arrastrando');
    try { marco.releasePointerCapture(e.pointerId); } catch (_) { /* ignorar */ }
  };
  marco.addEventListener('pointerup', soltar);
  marco.addEventListener('pointercancel', soltar);
  marco.addEventListener('dblclick', (e) => ajustar(escala * 1.8, e.clientX, e.clientY));
  marco.addEventListener('click', (e) => {
    if (e.target === marco || e.target === imagen) { /* nada: el clic simple no hace zoom */ }
  });

  const botones = [
    ['＋', 'Acercar', () => ajustar(escala * 1.35)],
    ['－', 'Alejar', () => ajustar(escala / 1.35)],
    ['⤢', 'Ver a pantalla completa', () => marco.requestFullscreen && marco.requestFullscreen()],
    ['⌂', 'Tamaño original', reiniciar],
  ];
  for (const [texto, titulo, accion] of botones) {
    controles.append(crear('button', { type: 'button', texto, title: titulo, 'aria-label': titulo, onclick: accion }));
  }
  const descargar = crear('a', { clase: 'boton', href: `mapas/${mapa.id}.svg`, download: `${mapa.id}.svg`,
    texto: '⇩', title: 'Descargar el mapa (SVG)', style: 'width:38px;height:38px;border-radius:50%;text-align:center;line-height:22px' });
  controles.append(descargar);
  requestAnimationFrame(() => { limitar(); aplicar(); });
}

/* --------------------------------- lugares -------------------------------- */
VISTAS.lugares = async (partes) => {
  if (partes && partes[0]) return VISTAS['lugar-detalle'](partes[0]);
  const lugares = await cargarLugaresIndice();
  const contenedor = crear('div');
  contenedor.append(cabeceraSeccion('Lugares bíblicos',
    `${lugares.length} lugares citados en el texto bíblico, con su nombre original, el tipo de lugar, `
    + 'sus coordenadas y todas las referencias donde aparecen.', 'seccion-mapas.jpg'));

  const tipos = [...new Set(lugares.map((l) => l.t))].sort();
  const barra = crear('div', { clase: 'barra-herramientas' });
  const entrada = crear('input', { type: 'search', placeholder: 'Buscar por nombre en español o hebreo/griego…' });
  const selector = crear('select', {}, [crear('option', { value: '', texto: 'Todos los tipos' })]
    .concat(tipos.map((t) => crear('option', { value: t, texto: t }))));
  const orden = crear('select', {}, [
    crear('option', { value: 'refs', texto: 'Ordenar por número de referencias' }),
    crear('option', { value: 'nombre', texto: 'Ordenar alfabéticamente' }),
    crear('option', { value: 'tipo', texto: 'Ordenar por tipo' }),
  ]);
  const contador = crear('span', { clase: 'leyenda-mapa' });
  barra.append(entrada, selector, orden, contador);

  const salida = crear('div');
  let limite = 60;
  let filtrados = [];
  let ordenActual = 'refs';

  function calcular() {
    const t = normalizar(entrada.value);
    const tipo = selector.value;
    filtrados = lugares.filter((l) => (!t || normalizar(l.n).includes(t) || normalizar(l.o).includes(t))
      && (!tipo || l.t === tipo));
    if (ordenActual === 'refs') filtrados.sort((a, b) => b.r - a.r);
    else if (ordenActual === 'nombre') filtrados.sort((a, b) => a.n.localeCompare(b.n, 'es'));
    else filtrados.sort((a, b) => a.t.localeCompare(b.t, 'es') || b.r - a.r);
  }

  function pintar() {
    calcular();
    contador.textContent = `${filtrados.length} lugares`;
    salida.innerHTML = '';
    if (!filtrados.length) { salida.append(crear('p', { clase: 'sin-resultados', texto: 'Sin coincidencias.' })); return; }
    const tabla = crear('table');
    tabla.append(crear('thead', {}, crear('tr', {}, [
      crear('th', { texto: 'Lugar' }), crear('th', { texto: 'Nombre original' }),
      crear('th', { texto: 'Tipo' }), crear('th', { texto: 'Coordenadas' }), crear('th', { texto: 'Referencias' }),
    ])));
    const cuerpo = crear('tbody');
    for (const lugar of filtrados.slice(0, limite)) {
      const fila = crear('tr', {}, [
        crear('td', {}, [crear('a', { href: `#/lugares/${lugar.id}`, texto: lugar.n }),
          lugar.a ? crear('span', { clase: 'etiqueta', style: 'margin-left:6px', texto: 'adaptado' }) : null]),
        crear('td', {}, [crear('span', { clase: 'original', texto: lugar.o || '—' })]),
        crear('td', { texto: lugar.t || '—' }),
        crear('td', { texto: `${lugar.lat.toFixed(2)}, ${lugar.lon.toFixed(2)}` }),
        crear('td', { texto: miles(lugar.r) }),
      ]);
      cuerpo.append(fila);
    }
    tabla.append(cuerpo);
    salida.append(crear('div', { clase: 'tabla-envoltura' }, tabla));
    if (filtrados.length > limite) {
      salida.append(crear('div', { clase: 'paginacion' }, [
        crear('button', { texto: `Mostrar 60 más (quedan ${filtrados.length - limite})`,
          onclick: () => { limite += 60; pintar(); } }),
        crear('button', { texto: 'Mostrar todos', onclick: () => { limite = filtrados.length; pintar(); } }),
      ]));
    }
  }
  entrada.addEventListener('input', () => { limite = 60; pintar(); });
  selector.addEventListener('change', () => { limite = 60; pintar(); });
  orden.addEventListener('change', () => { ordenActual = orden.value; limite = 60; pintar(); });
  pintar();
  contenedor.append(barra, salida);
  return contenedor;
};

VISTAS['lugar-detalle'] = async (id) => {
  const lugares = await cargarLugares();
  const lugar = lugares.find((l) => l.id === id);
  if (!lugar) return noEncontrado('lugar', id);

  const contenedor = crear('div');
  contenedor.append(migas([['lugares', 'Lugares'], [null, lugar.nombre]]));
  contenedor.append(crear('div', { clase: 'seccion-cabecera' }, [
    crear('div', {}, [
      crear('h1', { texto: lugar.nombre }),
      crear('p', { clase: 'original', texto: `Nombre original: ${lugar.original || '—'} · ${lugar.tipo}` }),
    ]),
  ]));

  const columnas = crear('div', { clase: 'detalle' });
  const principal = crear('div');

  const mapa = await cargarMapas();
  const mapasConLugar = mapa.filter((m) => (m.lista_lugares || []).some((l) => l.id === lugar.id));
  if (mapasConLugar.length) {
    principal.append(crear('div', { clase: 'panel', style: 'margin-bottom:18px' }, [
      crear('h3', { texto: 'Aparece en estos mapas' }),
      crear('p', {}, mapasConLugar.slice(0, 8).map((m) => crear('a', { clase: 'ref', href: `#/mapas/${m.id}`, texto: m.titulo }))),
    ]));
  }

  const panelRefs = crear('div', { clase: 'panel' });
  panelRefs.append(crear('h3', { texto: `Referencias bíblicas (${miles(lugar.total_refs)})` }));
  const porLibro = new Map();
  for (const ref of lugar.refs) {
    const corte = ref.lastIndexOf(' ');
    const libro = corte > 0 ? ref.slice(0, corte) : ref;
    if (!porLibro.has(libro)) porLibro.set(libro, []);
    porLibro.get(libro).push(ref);
  }
  for (const [libro, refs] of porLibro) {
    panelRefs.append(crear('h4', { texto: `${libro} (${refs.length})`, style: 'margin:14px 0 6px;font-size:.95rem' }));
    panelRefs.append(crear('p', {}, refs.map((r) => referenciaEnlazada(r))));
  }
  principal.append(panelRefs);
  columnas.append(principal);

  const lateral = crear('div');
  const panelDatos = crear('div', { clase: 'panel' });
  panelDatos.append(crear('h3', { texto: 'Ficha' }));
  const hechos = crear('ul', { clase: 'lista-hechos' });
  hechos.append(crear('li', {}, [crear('b', { texto: 'Tipo: ' }), lugar.tipo]));
  if (lugar.tipo_original) hechos.append(crear('li', {}, [crear('b', { texto: 'Tipo original: ' }), lugar.tipo_original]));
  hechos.append(crear('li', {}, [crear('b', { texto: 'Coordenadas: ' }),
    `${lugar.lat.toFixed(5)}, ${lugar.lon.toFixed(5)}`]));
  hechos.append(crear('li', {}, [crear('b', { texto: 'Referencias: ' }), miles(lugar.total_refs)]));
  if (lugar.forma) hechos.append(crear('li', {}, [crear('b', { texto: 'Geometría: ' }),
    lugar.forma === 'point' ? 'punto' : lugar.forma]));
  hechos.append(crear('li', {}, [crear('b', { texto: 'Identificación: ' }),
    lugar.adaptado ? 'adaptada del catalogo inglés' : 'del catálogo de openbible.info']));
  panelDatos.append(hechos);
  panelDatos.append(crear('p', { style: 'margin-top:12px' }, [
    crear('a', { clase: 'boton', href: `https://www.google.com/maps/search/?api=1&query=${lugar.lat},${lugar.lon}`,
      target: '_blank', rel: 'noopener', texto: 'Ver en un mapa moderno ↗' }),
  ]));
  lateral.append(panelDatos);

  if (lugar.foto) {
    const panelFoto = crear('div', { clase: 'panel', style: 'margin-top:18px' });
    panelFoto.append(crear('h3', { texto: 'Fotografía' }));
    const enlace = crear('a', { href: lugar.foto.pagina || lugar.foto.url, target: '_blank', rel: 'noopener' });
    enlace.append(crear('img', { src: lugar.foto.miniatura || lugar.foto.url, alt: `Fotografía de ${lugar.nombre}`,
      style: 'width:100%;border-radius:10px;border:1px solid var(--borde)',
      onerror: function () { this.closest('.panel').remove(); } }));
    panelFoto.append(enlace);
    panelFoto.append(crear('p', { clase: 'leyenda-mapa', style: 'margin-top:8px',
      texto: `${lugar.foto.descripcion || 'Fotografía'} · ${lugar.foto.autor || 'autor desconocido'} · `
        + `${lugar.foto.licencia || ''} · Wikimedia Commons. Requiere conexión a internet.` }));
    lateral.append(panelFoto);
  }
  if (lugar.modernos && lugar.modernos.length) {
    const panelModerno = crear('div', { clase: 'panel', style: 'margin-top:18px' });
    panelModerno.append(crear('h3', { texto: 'Localidades modernas' }));
    panelModerno.append(crear('p', { texto: lugar.modernos.join(', ') }));
    lateral.append(panelModerno);
  }
  columnas.append(lateral);
  contenedor.append(columnas);
  return contenedor;
};

/* ------------------------------ diccionarios ------------------------------ */
VISTAS.diccionarios = async (partes) => {
  if (partes && partes[0]) return VISTAS['diccionario-detalle'](partes[0], partes[1], partes[2]);
  const indice = await cargarIndice();
  const contenedor = crear('div');
  contenedor.append(cabeceraSeccion('Diccionarios enciclopédicos',
    'Cinco obras completas de dominio público, digitalizadas y organizadas para consultarlas en español: '
    + 'personas, lugares, objetos, oficios, costumbres y doctrina.', 'seccion-biblioteca.jpg'));
  const rejilla = crear('div', { clase: 'rejilla' });
  for (const dic of (indice.diccionarios || [])) {
    const [titulo, autor] = NOMBRES_DICCIONARIO[dic.codigo] || [dic.titulo || dic.codigo, dic.autor || ''];
    rejilla.append(crear('div', { clase: 'tarjeta', role: 'link', tabindex: '0',
      onclick: () => irA(`#/diccionarios/${dic.codigo}`),
      onkeydown: (e) => { if (e.key === 'Enter') irA(`#/diccionarios/${dic.codigo}`); } }, [
      crear('h3', { texto: titulo }),
      crear('p', { texto: `${autor}${dic.anio ? ' · ' + dic.anio : ''}` }),
      crear('p', { texto: dic.descripcion || '' }),
      crear('div', { clase: 'pie-tarjeta' }, [
        crear('span', { clase: 'etiqueta oro', texto: `${miles(dic.entradas)} voces` }),
        crear('span', { texto: `${miles(dic.refs)} referencias` }),
      ]),
    ]));
  }
  contenedor.append(rejilla);
  contenedor.append(crear('div', { clase: 'aviso-online', style: 'margin-top:22px', html:
    'Estos diccionarios se publicaron en inglés en el siglo XIX y sus artículos se conservan en su idioma original, '
    + 'que es la fuente de referencia. Los títulos, las referencias bíblicas, los nombres de lugar y toda la '
    + 'interfaz de la aplicación están en español. Las referencias de cada voz (por ejemplo <em>Génesis 12:1</em>) '
    + 'se pueden pulsar para leer el versículo en la Biblia Reina-Valera 1960.' }));
  return contenedor;
};

VISTAS['diccionario-detalle'] = async (codigo, vozId) => {
  const dic = (await cargarDiccionariosIndice())[codigo];
  const indice = await cargarIndice();
  const meta = (indice.diccionarios || []).find((d) => d.codigo === codigo) || {};
  const [titulo, autor] = NOMBRES_DICCIONARIO[codigo] || [codigo, ''];
  if (!dic) return noEncontrado('diccionario', codigo);
  const entradas = await cargarDiccionario(codigo);
  const porId = new Map(entradas.map((e) => [e.id, e]));
  const contenedor = crear('div');
  contenedor.append(migas([['diccionarios', 'Diccionarios'], [null, titulo]]));
  contenedor.append(crear('div', { clase: 'seccion-cabecera' }, [
    crear('div', {}, [crear('h1', { texto: titulo }),
      crear('p', { texto: `${autor} · ${miles(entradas.length)} voces · ${meta.descripcion || ''}` })]),
  ]));

  if (vozId) {
    const entrada = porId.get(vozId);
    if (!entrada) return noEncontrado('voz', vozId);
    const panel = crear('div', { clase: 'panel' });
    panel.append(crear('h2', { texto: entrada.t }));
    if (entrada.tes) panel.append(crear('p', { clase: 'original', texto: entrada.tes }));
    panel.append(crear('div', { clase: 'texto-largo', texto: entrada.texto }));
    panel.append(crear('p', { style: 'margin-top:16px' }, crear('a', { clase: 'boton', href: `#/diccionarios/${codigo}`, texto: '← Volver al diccionario' })));
    contenedor.append(panel);
    return contenedor;
  }

  const barra = crear('div', { clase: 'barra-herramientas' });
  const entrada = crear('input', { type: 'search', placeholder: 'Buscar una voz…' });
  const contador = crear('span', { clase: 'leyenda-mapa' });
  barra.append(entrada, contador);
  const abecedario = crear('div', { clase: 'abecedario' });
  for (const letra of 'ABCDEFGHIJKLMNOPQRSTUVWXYZ') {
    const voces = dic.filter((v) => (v[1] || '').toUpperCase().startsWith(letra));
    abecedario.append(crear('a', { href: `#/diccionarios/${codigo}?letra=${letra}`,
      texto: `${letra} (${voces.length})`, title: `${voces.length} voces` }));
  }
  const salida = crear('div');
  let limite = 40;

  function pintar(consulta, letra) {
    const t = normalizar(consulta);
    let lista = dic.filter((v) => !t || normalizar(v[1]).includes(t) || normalizar(v[0]).includes(t));
    if (letra) lista = lista.filter((v) => (v[1] || '').toUpperCase().startsWith(letra));
    contador.textContent = `${miles(lista.length)} voces`;
    salida.innerHTML = '';
    if (!lista.length) { salida.append(crear('p', { clase: 'sin-resultados', texto: 'Sin coincidencias.' })); return; }
    const envoltura = crear('div', { clase: 'panel' });
    for (const [id, nombre, tes] of lista.slice(0, limite)) {
      envoltura.append(crear('div', { clase: 'voz' }, [
        crear('h4', {}, crear('a', { href: `#/diccionarios/${codigo}/${id}`, texto: nombre })),
        tes ? crear('div', { clase: 'original', texto: tes }) : null,
      ]));
    }
    salida.append(envoltura);
    if (lista.length > limite) {
      salida.append(crear('div', { clase: 'paginacion' }, crear('button', {
        texto: `Mostrar más (${miles(lista.length - limite)} restantes)`,
        onclick: () => { limite += 80; pintar(entrada.value, letraActual); } })));
    }
  }
  let letraActual = rutaActual().parametros.get('letra') || '';
  entrada.addEventListener('input', () => { limite = 40; letraActual = ''; pintar(entrada.value, letraActual); });
  pintar('', letraActual);
  contenedor.append(barra, abecedario, salida);
  return contenedor;
};

/* ---------------------------------- temas --------------------------------- */
VISTAS.temas = async (partes) => {
  if (partes && partes[0]) return VISTAS['tema-detalle'](partes[0]);
  const temas = await cargarTemasIndice();
  const indice = await cargarIndice();
  const contenedor = crear('div');
  contenedor.append(cabeceraSeccion('Temas y cadenas de referencias',
    `${miles(temas.length)} temas con ${miles(indice.referencias_tematicas)} referencias, tomados de dos obras `
    + 'clásicas de dominio público: «Nave’s Topical Bible» (1896) y «Torrey’s New Topical Textbook» (1897). '
    + 'Cada tema enlaza con los versículos de la Reina-Valera 1960.', 'seccion-biblioteca.jpg'));

  const barra = crear('div', { clase: 'barra-herramientas' });
  const entrada = crear('input', { type: 'search', placeholder: 'Buscar un tema: amor, fe, oración, bautismo…' });
  const orden = crear('select', {}, [
    crear('option', { value: 'refs', texto: 'Más referencias primero' }),
    crear('option', { value: 'alfabetico', texto: 'Orden alfabético' }),
  ]);
  const contador = crear('span', { clase: 'leyenda-mapa' });
  barra.append(entrada, orden, contador);

  const salida = crear('div');
  let limite = 80;
  let lista = [];
  function pintar() {
    const t = normalizar(entrada.value);
    lista = temas.filter((x) => !t || normalizar(x.t).includes(t) || normalizar(x.to).includes(t));
    if (orden.value === 'refs') lista.sort((a, b) => b.r - a.r);
    else lista.sort((a, b) => a.t.localeCompare(b.t, 'es'));
    contador.textContent = `${miles(lista.length)} temas`;
    salida.innerHTML = '';
    const rejilla = crear('div', { clase: 'rejilla ancha' });
    for (const tema of lista.slice(0, limite)) {
      rejilla.append(crear('div', { clase: 'tarjeta', role: 'link', tabindex: '0',
        onclick: () => irA(`#/temas/${tema.id}`),
        onkeydown: (e) => { if (e.key === 'Enter') irA(`#/temas/${tema.id}`); } }, [
        crear('h3', { texto: tema.t }),
        tema.tc ? null : crear('span', { clase: 'etiqueta', texto: 'título sin traducir' }),
        crear('div', { clase: 'pie-tarjeta' }, [
          crear('span', { clase: 'etiqueta oro', texto: `${miles(tema.r)} referencias` }),
          tema.to && tema.to !== tema.t ? crear('span', { texto: tema.to }) : null,
        ]),
      ]));
    }
    salida.append(rejilla);
    if (lista.length > limite) {
      salida.append(crear('div', { clase: 'paginacion' },
        crear('button', { texto: `Mostrar más (${miles(lista.length - limite)} restantes)`,
          onclick: () => { limite += 120; pintar(); } })));
    }
  }
  entrada.addEventListener('input', () => { limite = 80; pintar(); });
  orden.addEventListener('change', () => pintar());
  pintar();
  contenedor.append(barra, salida);
  return contenedor;
};

VISTAS['tema-detalle'] = async (id) => {
  const temas = await cargarTemas();
  const tema = temas.find((t) => t.id === id);
  if (!tema) return noEncontrado('tema', id);
  const libros = await cargarBibliaLibros();
  const contenedor = crear('div');
  contenedor.append(migas([['temas', 'Temas'], [null, tema.titulo]]));
  contenedor.append(crear('h1', { texto: tema.titulo }));
  contenedor.append(crear('p', { clase: 'original',
    texto: `Título original: ${tema.titulo_original}${tema.traduccion_completa ? '' : ' (título sin traducir)'}` }));
  const panel = crear('div', { clase: 'panel' });
  for (const aspecto of (tema.aspectos || [])) {
    // algunas entradas de la fuente son solo una lista de citas: no llevan rótulo
    const etiqueta = (aspecto.etiqueta || '').trim();
    const soloCitas = !etiqueta || /^[\s\d:;,.()\-–—]+$/.test(etiqueta);
    if (!soloCitas) {
      panel.append(crear('h3', { texto: etiqueta }));
      if (aspecto.etiqueta_original && aspecto.etiqueta_original !== aspecto.etiqueta) {
        panel.append(crear('div', { clase: 'original', texto: aspecto.etiqueta_original }));
      }
    }
    if (aspecto.refs && aspecto.refs.length) {
      panel.append(crear('p', {}, aspecto.refs.map((r) => referenciaEnlazada(r, libros))));
    }
    if (aspecto.texto) panel.append(crear('div', { clase: 'texto-largo', texto: aspecto.texto }));
    panel.append(crear('div', { clase: 'leyenda-mapa', style: 'margin:6px 0 18px',
      texto: aspecto.fuente === 'NAV' ? 'Fuente: Nave’s Topical Bible (1896)' : 'Fuente: Torrey’s New Topical Textbook (1897)' }));
  }
  contenedor.append(panel);
  return contenedor;
};

/* ---------------------------------- biblia -------------------------------- */
VISTAS.biblia = async (partes, parametros) => {
  const libros = await cargarBibliaLibros();
  if (!libros.length) return avisoBiblia();
  if (!partes || !partes[0]) return VISTAS['biblia-lector'](undefined, undefined, parametros);
  const buscado = normalizar(partes[0]);
  const libro = libros.find((l) => l.osis.toLowerCase() === String(partes[0]).toLowerCase())
    || libros.find((l) => normalizar(l.abrev) === buscado)
    || libros.find((l) => normalizar(l.nombre) === buscado)
    || libros.find((l) => normalizar(l.nombre).startsWith(buscado) && buscado.length >= 3);
  if (!libro) return noEncontrado('libro', partes[0]);
  return VISTAS['biblia-lector'](libro, partes[1] ? Number(partes[1]) : undefined, parametros);
};

VISTAS['biblia-lector'] = async (libro, capitulo, parametros) => {
  const libros = await cargarBibliaLibros();
  const actual = libro || libros[0];
  const caps = Object.keys(await cargarBibliaLibro(actual.osis));
  const total = caps.length;
  const cap = String(capitulo && capitulo >= 1 && capitulo <= total ? capitulo : 1);
  const versiculos = (await cargarBibliaLibro(actual.osis))[cap] || {};
  const destacado = parametros && parametros.get('v') ? Number(parametros.get('v')) : null;

  const contenedor = crear('div');
  contenedor.append(cabeceraSeccion('La Biblia — Reina-Valera 1960',
    'Texto completo en español, con búsqueda por palabra o expresión y lectura por libro y capítulo.', 'seccion-biblia.jpg'));
  const faltantes = (App.indice && App.indice.libros_faltantes) || [];
  if (faltantes.length) {
    contenedor.append(crear('div', { clase: 'aviso-online', html:
      `Esta edición incluye ${libros.length} de los 66 libros de la Biblia: falta el texto de `
      + `${faltantes.join(' y ')} en los archivos de origen. Para completarlos, coloca `
      + `${faltantes.map((n) => '<code>' + n + '.json</code>').join(' y ')} en `
      + '<code>app/datos/biblia/</code> y vuelve a ejecutar '
      + '<code>python3 herramientas/construir_datos.py</code>.' }));
  }

  const barra = crear('div', { clase: 'barra-herramientas' });
  const busqueda = crear('input', { type: 'search',
    placeholder: 'Buscar en toda la Biblia: «porque de tal manera amó Dios»…' });
  const boton = crear('button', { clase: 'primario', texto: 'Buscar' });
  barra.append(busqueda, boton);
  const resultados = crear('div');
  contenedor.append(barra, resultados);

  async function buscar() {
    const consulta = busqueda.value.trim();
    resultados.innerHTML = '';
    if (consulta.length < 3) {
      resultados.append(crear('p', { clase: 'leyenda-mapa', texto: 'Escribe al menos tres letras.' }));
      return;
    }
    resultados.append(crear('p', { clase: 'leyenda-mapa', texto: 'Buscando…' }));
    const filas = await cargarBibliaBusqueda();
    const aguja = normalizar(consulta);
    const hallados = [];
    for (const [osis, cap2, ver, texto] of filas) {
      if (normalizar(texto).includes(aguja)) hallados.push([osis, cap2, ver, texto]);
      if (hallados.length >= 400) break;
    }
    const nombre = new Map(libros.map((l) => [l.osis, l]));
    resultados.innerHTML = '';
    resultados.append(crear('h3', { texto: `${miles(hallados.length)}${hallados.length >= 400 ? '+' : ''} versículos encontrados` }));
    const panel = crear('div', { clase: 'panel' });
    for (const [osis, cap2, ver, texto] of hallados) {
      const l = nombre.get(osis);
      panel.append(crear('p', {}, [
        crear('a', { clase: 'ref', href: `#/biblia/${osis}/${cap2}?v=${ver}`, texto: `${l ? l.nombre : osis} ${cap2}:${ver}` }),
        resaltar(texto, consulta),
      ]));
    }
    resultados.append(panel);
  }
  boton.addEventListener('click', buscar);
  busqueda.addEventListener('keydown', (e) => { if (e.key === 'Enter') buscar(); });

  const lector = crear('div', { clase: 'lector' });
  const lateral = crear('div', { clase: 'panel lista-libros' });
  let testamento = '';
  for (const l of libros) {
    if (l.testamento !== testamento) {
      testamento = l.testamento;
      lateral.append(crear('h4', { texto: testamento }));
    }
    lateral.append(crear('a', { href: `#/biblia/${l.osis}/1`, texto: l.nombre,
      'aria-current': l.osis === actual.osis ? 'true' : null }));
  }
  lector.append(lateral);

  const cuerpo = crear('div');
  const navegacion = crear('div', { style: 'display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:12px' });
  const iLibro = libros.findIndex((l) => l.osis === actual.osis);
  const previo = libros[iLibro - 1], siguiente = libros[iLibro + 1];
  if (previo) navegacion.append(crear('a', { clase: 'boton', href: `#/biblia/${previo.osis}/1`, texto: `← ${previo.nombre}` }));
  navegacion.append(crear('h2', { style: 'margin:0 auto;text-align:center;flex:1 1 240px', texto: `${actual.nombre} ${cap}` }));
  if (siguiente) navegacion.append(crear('a', { clase: 'boton', href: `#/biblia/${siguiente.osis}/1`, texto: `${siguiente.nombre} →` }));
  cuerpo.append(navegacion);

  const capitulos = crear('div', { clase: 'capitulos' });
  for (let n = 1; n <= total; n++) {
    capitulos.append(crear('a', { href: `#/biblia/${actual.osis}/${n}`, texto: n,
      'aria-current': String(n) === cap ? 'true' : null }));
  }
  cuerpo.append(capitulos);

  const texto = crear('div', { clase: 'versiculos' });
  for (const [numero, contenido] of Object.entries(versiculos).sort((a, b) => Number(a[0]) - Number(b[0]))) {
    const p = crear('p', { id: `v${numero}`, clase: String(numero) === String(destacado) ? 'destacado' : null }, [
      crear('span', { clase: 'v', texto: numero }), contenido,
    ]);
    texto.append(p);
  }
  cuerpo.append(texto);
  const pie = crear('div', { clase: 'paginacion' });
  if (Number(cap) > 1) pie.append(crear('a', { clase: 'boton', href: `#/biblia/${actual.osis}/${Number(cap) - 1}`, texto: `← ${actual.nombre} ${Number(cap) - 1}` }));
  pie.append(crear('span', { clase: 'leyenda-mapa', texto: `${actual.nombre} ${cap} · ${Object.keys(versiculos).length} versículos` }));
  if (Number(cap) < total) pie.append(crear('a', { clase: 'boton', href: `#/biblia/${actual.osis}/${Number(cap) + 1}`, texto: `${actual.nombre} ${Number(cap) + 1} →` }));
  cuerpo.append(pie);
  lector.append(cuerpo);
  contenedor.append(lector);
  if (destacado) setTimeout(() => { const el = $(`#v${destacado}`); if (el) el.scrollIntoView({ block: 'center' }); }, 120);
  return contenedor;
};

function avisoBiblia() {
  return crear('div', {}, [
    cabeceraSeccion('La Biblia', 'El texto bíblico no está instalado.', 'seccion-biblia.jpg'),
    crear('div', { clase: 'aviso-online', html: 'Esta instalación no incluye el texto de la Biblia Reina-Valera 1960. '
      + 'Coloca los archivos JSON de la Biblia en <code>app/datos/biblia/</code> y vuelve a ejecutar '
      + '<code>python3 herramientas/construir_datos.py</code>.' }),
  ]);
}

/** Devuelve el texto con la parte buscada resaltada (ignora acentos y mayúsculas). */
function resaltar(texto, consulta) {
  const normal = normalizar(texto), aguja = normalizar(consulta);
  const posicion = normal.indexOf(aguja);
  if (posicion < 0 || !aguja) return texto;
  // la normalización comprime espacios, así que se recorre el original llevando la cuenta
  let i = 0, j = 0, inicio = -1, fin = -1;
  while (i < texto.length && fin < 0) {
    const caracter = texto[i];
    const normalizado = normalizar(caracter) || ' ';
    const objetivo = normal[j] === undefined ? null : normal[j];
    if (objetivo !== null && (normalizado === objetivo || (normalizado === '' && objetivo === ' '))) {
      if (j === posicion) inicio = i;
      j++;
      if (j === posicion + aguja.length) { fin = i + 1; break; }
    }
    i++;
  }
  if (inicio < 0 || fin < 0) return texto;
  const fragmento = document.createDocumentFragment();
  fragmento.append(texto.slice(0, inicio));
  fragmento.append(crear('mark', { texto: texto.slice(inicio, fin) }));
  fragmento.append(texto.slice(fin));
  return fragmento;
}

/* ----------------------------------- arte --------------------------------- */
VISTAS.arte = async (partes, parametros) => {
  const arte = await cargarArte();
  const libros = await cargarBibliaLibros().catch(() => []);
  const contenedor = crear('div');
  contenedor.append(cabeceraSeccion('Galería de arte',
    `${arte.total} grabados de Gustave Doré (1866) para «La Grande Bible de Tours», en dominio público. `
    + 'Pulsa cualquier imagen para verla en grande; cada obra enlaza con su pasaje bíblico.', 'seccion-arte.jpg'));

  const barra = crear('div', { clase: 'barra-herramientas' });
  const entrada = crear('input', { type: 'search', value: (parametros && parametros.get('q')) || '',
    placeholder: 'Buscar una lámina por título o referencia…' });
  const selector = crear('select', {}, [
    crear('option', { value: 'todas', texto: 'Todas las láminas' }),
    crear('option', { value: 'at', texto: 'Antiguo Testamento' }),
    crear('option', { value: 'nt', texto: 'Nuevo Testamento' }),
    crear('option', { value: 'deutero', texto: 'Deuterocanónicos' }),
    crear('option', { value: 'ap', texto: 'Apocalipsis' }),
  ]);
  const contador = crear('span', { clase: 'leyenda-mapa' });
  barra.append(entrada, selector, contador);
  const salida = crear('div');
  contenedor.append(barra, salida);

  function clasificar(obra) {
    const ref = (obra.refs || []).join(' ');
    const libro = sinAcentos(ref).toLowerCase().replace(/\s*\d.*$/, '').trim();
    const AT = ['génesis', 'éxodo', 'le/', 'levítico', 'números', 'deuteronomio', 'josué', 'jueces', 'rut',
      'samuel', 'reyes', 'crónicas', 'esdras', 'nehemías', 'ester', 'job', 'salmos', 'proverbios',
      'eclesiastés', 'cantares', 'isaías', 'jeremías', 'lamentaciones', 'ezequiel', 'daniel', 'oseas',
      'joel', 'amós', 'abdías', 'jonás', 'miqueas', 'nahúm', 'habacuc', 'sofonías', 'hageo', 'zacarías', 'malaquías'];
    const DEUT = ['tobit', 'judit', 'baruc', 'macabeos'];
    if (/^apocalipsis/.test(libro)) return 'ap';
    if (DEUT.some((d) => libro.startsWith(d)) || /^daniel 1[34]/.test(sinAcentos(ref).toLowerCase())) return 'deutero';
    if (AT.some((a) => libro.startsWith(a))) return 'at';
    return 'nt';
  }

  function pintar() {
    const t = normalizar(entrada.value);
    const filtro = selector.value;
    const lista = (arte.obras || []).filter((o) => (!t
      || normalizar(`${o.titulo} ${(o.refs || []).join(' ')}`).includes(t))
      && (filtro === 'todas' || clasificar(o) === filtro));
    contador.textContent = `${lista.length} láminas`;
    salida.innerHTML = '';
    if (!lista.length) { salida.append(crear('p', { clase: 'sin-resultados', texto: 'Sin coincidencias.' })); return; }
    const galeria = crear('div', { clase: 'galeria-arte' });
    for (const obra of lista) {
      galeria.append(crear('figure', { clase: 'obra' }, [
        crear('img', { src: obra.archivo, alt: obra.titulo, loading: 'lazy',
          onclick: () => abrirLupa(obra), style: 'cursor: zoom-in' }),
        crear('figcaption', {}, [
          crear('strong', { texto: obra.titulo }),
          crear('div', { style: 'margin-top:4px' }, (obra.refs || []).map((r) => referenciaEnlazada(r, libros))),
          crear('div', { clase: 'leyenda-mapa', texto: `Lámina ${obra.numero} · ${obra.leyenda || 'Doré, 1866 · dominio público'}` }),
        ]),
      ]));
    }
    salida.append(galeria);
  }
  entrada.addEventListener('input', pintar);
  selector.addEventListener('change', pintar);
  pintar();
  contenedor.append(crear('div', { clase: 'panel', style: 'margin-bottom:20px' }, [
    crear('h3', { texto: 'Sobre la colección' }),
    crear('p', { texto: (arte.leyenda || {}).nota || '' }),
  ]));
  return contenedor;
};

function abrirLupa(obra) {
  const lupa = crear('div', { clase: 'lupa', onclick: (e) => { if (e.target === lupa) lupa.remove(); } }, [
    crear('button', { clase: 'cerrar', texto: '✕ Cerrar', onclick: () => lupa.remove() }),
    crear('img', { src: obra.archivo, alt: obra.titulo }),
    crear('div', { clase: 'pie' }, [
      crear('strong', { texto: `${obra.titulo} · ` }),
      `${(obra.refs || []).join(', ')} — Gustave Doré, La Grande Bible de Tours (1866), dominio público.`,
    ]),
  ]);
  document.body.append(lupa);
  document.addEventListener('keydown', function cerrar(e) {
    if (e.key === 'Escape') { lupa.remove(); document.removeEventListener('keydown', cerrar); }
  });
}

/* ------------------------------- cartografía ------------------------------ */
const COLECCIONES = [
  ['Mapa de Madaba', 'Mosaico del siglo VI en la iglesia de San Jorge (Madaba, Jordania), el mapa de la tierra '
    + 'de la Biblia más antiguo que se conserva.',
    'https://es.wikipedia.org/wiki/Mapa_de_Madaba'],
  ['Tabula Peutingeriana', 'Copia medieval de un mapa romano de caminos; ayuda a seguir las rutas de los viajes de Pablo.',
    'https://es.wikipedia.org/wiki/Tabula_Peutingeriana'],
  ['Theatrum Terrae Sanctae (1590)', 'Mapas de la Tierra Santa de Christian van Adrichem, entre los primeros atlas bíblicos impresos.',
    'https://es.wikipedia.org/wiki/Christian_Kruik_van_Adrichem'],
  ['Atlas de la Biblia (1907)', 'Los mapas históricos del «Atlas of the Bible» de la Enciclopedia Judía.',
    'https://es.wikisource.org/wiki/Atlas_of_the_Bible'],
  ['Colección de mapa históricos de Wikimedia Commons', 'Reproducciones de alta resolución de mapas bíblicos antiguos, en dominio público.',
    'https://commons.wikimedia.org/wiki/Category:Old_maps_of_the_Bible'],
  ['Mapas de la Tierra Santa del Proyecto Gutenberg', 'Cartografía histórica publicada en libros de acceso libre.',
    'https://www.gutenberg.org/'],
];

VISTAS.cartografia = async () => {
  const mapas = await cargarMapas();
  const antiguos = mapas.filter((m) => m.categoria === 'Cartografía histórica');
  const contenedor = crear('div');
  contenedor.append(cabeceraSeccion('Cartografía histórica',
    'La historia de los mapas de la Biblia y enlaces a las colecciones digitales de acceso libre, '
    + 'donde consultar las reproducciones originales.', 'seccion-mapas.jpg'));
  if (antiguos.length) contenedor.append(galeriaMapas(antiguos, false));
  const lista = crear('div', { clase: 'panel', style: 'margin-top:22px' });
  lista.append(crear('h3', { texto: 'Colecciones recomendadas' }));
  for (const [titulo, texto, url] of COLECCIONES) {
    lista.append(crear('div', { style: 'margin-bottom:12px' }, [
      crear('strong', {}, crear('a', { href: url, target: '_blank', rel: 'noopener', texto: titulo + ' ↗' })),
      crear('div', { clase: 'leyenda-mapa', texto }),
    ]));
  }
  lista.append(crear('p', { clase: 'leyenda-mapa', style: 'margin-top:14px',
    texto: 'Estas colecciones requieren conexión a internet. Todo lo demás funciona sin conexión.' }));
  contenedor.append(lista);
  return contenedor;
};

/* ------------------------- biblioteca y enciclopedia ---------------------- */
VISTAS.biblioteca = async () => {
  const [indice, enciclopedia] = await Promise.all([
    cargarIndice(), cargar('enciclopedia.json').catch(() => []),
  ]);
  const contenedor = crear('div');
  contenedor.append(cabeceraSeccion('Biblioteca y fuentes',
    'Todo el contenido de esta aplicación procede de obras de dominio público o de datos de licencia libre. '
    + 'Aquí están las fuentes, los autores y las licencias.', 'seccion-biblioteca.jpg'));

  contenedor.append(crear('h2', { texto: 'Fuentes principales' }));
  const rejilla = crear('div', { clase: 'rejilla ancha' });
  const FUENTES = [
    ['Bible-Geocoding-Data', 'openbible.info (Stephen Smith)', 'CC BY 4.0',
      'Lugares, coordenadas, referencias y catálogo de fotografías de Wikimedia Commons. '
      + 'https://github.com/openbibleinfo/Bible-Geocoding-Data'],
    ['bible-dictionary-dataset', 'NEUU', 'CC BY 4.0',
      'Voces completas de Easton (1897), Smith (1863), Hastings (1898), Hitchcock (1869) y Schaff. '
      + 'https://github.com/neuu-org/bible-dictionary-dataset'],
    ['bible-topics-dataset', 'NEUU', 'CC BY 4.0',
      '«Nave’s Topical Bible» (1896) y «Torrey’s New Topical Textbook» (1897). '
      + 'https://github.com/neuu-org/bible-topics-dataset'],
    ['Natural Earth', 'Natural Earth (dominio público)', 'Sin restricciones',
      'Costas, lagos, ríos y fronteras de los mapas. https://www.naturalearthdata.com'],
    ['La Grande Bible de Tours', 'Gustave Doré y sus grabadores (1866)', 'Dominio público',
      'Los 241 grabados de la galería de arte, digitalizados por el archivo libre Aionian Bible.'],
    ['Biblia Reina-Valera 1960', 'Traducción de dominio público en su edición de 1960', 'Uso libre',
      'Texto bíblico completo en español, aportado por el usuario.'],
  ];
  for (const [nombre, autor, licencia, detalle] of FUENTES) {
    const urls = detalle.match(/https?:\/\/\S+/g) || [];
    rejilla.append(crear('div', { clase: 'tarjeta' }, [
      crear('h3', { texto: nombre }),
      crear('p', { texto: autor }),
      crear('p', { texto: detalle.replace(/https?:\/\/\S+/g, '').trim() }),
      crear('div', { clase: 'pie-tarjeta' }, [
        crear('span', { clase: 'etiqueta verde', texto: licencia }),
        ...urls.map((u) => crear('a', { href: u, target: '_blank', rel: 'noopener', texto: 'Sitio ↗' })),
      ]),
    ]));
  }
  contenedor.append(rejilla);

  contenedor.append(crear('h2', { texto: 'Enciclopedia del Atlas Bíblico' }));
  if (!enciclopedia.length) {
    contenedor.append(crear('div', { clase: 'aviso-online', html:
      'La enciclopedia propia está en construcción: se irá rellenando con artículos redactados para esta '
      + 'aplicación a partir de las obras de dominio público. Mientras tanto, los cinco diccionarios clásicos '
      + 'cubren casi veinte mil voces. Puedes añadir artículos en '
      + '<code>contenido/enciclopedia_es.json</code> y volver a ejecutar <code>python3 herramientas/construir_datos.py</code>.' }));
  } else {
    const libros = await cargarBibliaLibros().catch(() => []);
    contenedor.append(crear('p', { texto: `${enciclopedia.length} artículos redactados para esta aplicación, `
      + 'con sus referencias bíblicas y una ilustración de la galería de arte. Pulsa cualquier cita para '
      + 'leerla en la Biblia.' }));
    const indices = crear('div', { clase: 'abecedario' });
    for (const entrada of enciclopedia) {
      indices.append(crear('a', { href: `#/biblioteca?articulo=${encodeURIComponent(entrada.id)}`, texto: entrada.titulo }));
    }
    contenedor.append(indices);
    const seleccionado = (rutaActual().parametros || new URLSearchParams()).get('articulo');
    for (const entrada of enciclopedia) {
      if (seleccionado && seleccionado !== entrada.id) continue;
      const bloque = crear('div', { clase: 'entrada', id: `art-${entrada.id}` });
      bloque.append(crear('h3', { texto: entrada.titulo }));
      if (entrada.resumen) bloque.append(crear('p', { clase: 'cita', texto: entrada.resumen }));
      if (entrada.imagen) {
        bloque.append(crear('img', {
          src: entrada.imagen, alt: entrada.titulo, loading: 'lazy',
          style: 'width:100%;max-width:420px;border-radius:10px;border:1px solid var(--borde);float:right;margin:0 0 12px 16px;cursor:zoom-in',
          onclick: () => abrirLupa({ titulo: entrada.titulo, archivo: entrada.imagen, refs: entrada.refs || [] }),
        }));
        if (entrada.leyenda_imagen) bloque.append(crear('div', { clase: 'leyenda-mapa', texto: entrada.leyenda_imagen }));
      }
      for (const parrafo of String(entrada.texto || '').split(/\n\n+/)) {
        bloque.append(crear('p', { texto: parrafo }));
      }
      if (entrada.refs && entrada.refs.length) {
        bloque.append(crear('p', {}, [crear('b', { texto: 'Referencias: ' })].concat(entrada.refs.map((r) => referenciaEnlazada(r, libros)))));
      }
      bloque.append(crear('div', { clase: 'meta', texto: [entrada.fuente, entrada.licencia].filter(Boolean).join(' · ') }));
      contenedor.append(bloque);
    }
    if (seleccionado) {
      contenedor.append(crear('p', {}, crear('a', { clase: 'boton', href: '#/biblioteca', texto: '← Ver todos los artículos' })));
    }
  }
  contenedor.append(crear('h2', { texto: 'Cifras de esta edición' }));
  const tabla = crear('table');
  tabla.append(crear('thead', {}, crear('tr', {}, [
    crear('th', { texto: 'Contenido' }), crear('th', { texto: 'Cantidad' }),
  ])));
  const cuerpo = crear('tbody');
  const FILAS = [
    ['Mapas y planos', indice.mapas], ['Lugares geolocalizados', indice.lugares],
    ['Regiones dibujadas', indice.regiones], ['Temas bíblicos', indice.temas],
    ['Referencias temáticas', indice.referencias_tematicas], ['Libros de la Biblia', indice.libros_biblia],
    ['Versículos', indice.versiculos_biblia], ['Ilustraciones de arte', indice.obras_arte],
    ['Fotografías de lugares', indice.lugares_con_foto],
  ];
  for (const [nombre, valor] of FILAS) {
    cuerpo.append(crear('tr', {}, [crear('td', { texto: nombre }), crear('td', { texto: miles(valor) })]));
  }
  for (const dic of (indice.diccionarios || [])) {
    cuerpo.append(crear('tr', {}, [crear('td', { texto: `Voces de ${dic.titulo || dic.codigo}` }), crear('td', { texto: miles(dic.voces) })]));
  }
  tabla.append(cuerpo);
  contenedor.append(crear('div', { clase: 'tabla-envoltura' }, tabla));
  return contenedor;
};

/* ---------------------------------- ayuda --------------------------------- */
VISTAS.ayuda = async () => {
  const indice = await cargarIndice();
  const contenedor = crear('div');
  contenedor.append(cabeceraSeccion('Ayuda y ajustes',
    'Cómo usar la aplicación, qué necesita conexión y cómo cambiar el aspecto.', 'seccion-biblioteca.jpg'));

  const ajustes = leerAjustes();
  const panelAjustes = crear('div', { clase: 'panel', style: 'margin-bottom:22px' });
  panelAjustes.append(crear('h3', { texto: 'Ajustes' }));
  const filaTema = crear('div', { style: 'display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-bottom:10px' }, [
    crear('b', { texto: 'Tema:' }),
  ]);
  for (const [valor, etiqueta] of [['claro', 'Claro'], ['oscuro', 'Oscuro']]) {
    filaTema.append(crear('button', { texto: etiqueta, clase: ajustes.tema === valor ? 'primario' : '',
      onclick: () => { guardarAjustes({ tema: valor }); aplicarAjustes(); VISTAS.ayuda().then(reemplazar); } }));
  }
  const filaTexto = crear('div', { style: 'display:flex;gap:10px;flex-wrap:wrap;align-items:center' }, [
    crear('b', { texto: 'Tamaño de letra:' }),
  ]);
  for (const [valor, etiqueta] of [['pequeno', 'Pequeña'], ['normal', 'Normal'], ['grande', 'Grande']]) {
    filaTexto.append(crear('button', { texto: etiqueta, clase: ajustes.texto === valor ? 'primario' : '',
      onclick: () => { guardarAjustes({ texto: valor }); aplicarAjustes(); VISTAS.ayuda().then(reemplazar); } }));
  }
  panelAjustes.append(filaTema, filaTexto);
  contenedor.append(panelAjustes);

  const ayuda = crear('div', { clase: 'panel' });
  ayuda.append(crear('h3', { texto: 'Cómo moverse por la aplicación' }));
  const lista = crear('ul', { clase: 'lista-hechos' });
  const ITEMS = [
    ['Buscador de la cabecera', 'Escribe cualquier palabra para buscar a la vez en mapas, lugares, temas, diccionarios y obras de arte.'],
    ['Mapas', 'Arrastra para mover el mapa y usa la rueda del ratón para acercar. El botón ⤢ lo pone a pantalla completa y ⇩ lo descarga en formato SVG.'],
    ['Lugares', 'Cada lugar tiene su ficha con coordenadas, referencias agrupadas por libro de la Biblia y un enlace a un mapa moderno.'],
    ['Diccionarios', 'Busca una voz o recorre el abecedario. Cada referencia bíblica de un artículo se puede pulsar para leerla en la Biblia.'],
    ['Temas', 'Agrupan versículos por asunto; las referencias enlazan con el texto de la Reina-Valera 1960.'],
    ['Biblia', 'Elige libro y capítulo, o busca una expresión en todo el texto. Enlaces como «Juan 3:16» desde cualquier sección abren el versículo listo para leer.'],
    ['Arte', 'Pulsa una lámina para verla a pantalla completa con su título y su referencia.'],
    ['Sin conexión', 'La aplicación funciona completa sin internet salvo las fotografías de lugares y las colecciones externas de cartografía.'],
  ];
  for (const [titulo, texto] of ITEMS) {
    lista.append(crear('li', {}, [crear('b', { texto: titulo + '. ' }), texto]));
  }
  ayuda.append(lista);
  contenedor.append(ayuda);

  const panelSistema = crear('div', { clase: 'panel', style: 'margin-top:22px' });
  panelSistema.append(crear('h3', { texto: 'Instalación en tu equipo' }));
  panelSistema.append(crear('p', { html: 'La aplicación se instala con el programa <code>compositor.py</code> que acompaña a esta carpeta:' }));
  panelSistema.append(crear('pre', { style: 'background:var(--papel-3);padding:14px;border-radius:10px;overflow:auto',
    texto: 'python3 compositor.py abrir       # abrir la aplicación\n'
      + 'python3 compositor.py instalar    # crear accesos en el menú del sistema\n'
      + 'python3 compositor.py servir      # solo el servidor local\n'
      + 'python3 compositor.py autoprueba  # comprobar que todo está en su sitio' }));
  panelSistema.append(crear('p', { html: 'Los datos están en <code>app/datos/</code> y los mapas en <code>app/mapas/</code>. '
    + 'Para reconstruirlos: <code>construir_datos.py</code> → <code>construir_base.py</code> → '
    + '<code>construir_mapas.py</code> → <code>construir_indices.py</code>.' }));
  contenedor.append(panelSistema);
  return contenedor;
};

function leerAjustes() {
  try { return Object.assign({ tema: 'claro', texto: 'normal' }, JSON.parse(localStorage.getItem('renacer-ajustes') || '{}')); }
  catch (_) { return { tema: 'claro', texto: 'normal' }; }
}
function guardarAjustes(cambios) {
  const nuevos = Object.assign(leerAjustes(), cambios);
  try { localStorage.setItem('renacer-ajustes', JSON.stringify(nuevos)); } catch (_) { /* modo privado */ }
}
function aplicarAjustes() {
  const a = leerAjustes();
  document.documentElement.dataset.tema = a.tema;
  document.documentElement.dataset.texto = a.texto;
}

function reemplazar(nodo) {
  const main = $('#contenido');
  main.innerHTML = '';
  main.append(nodo);
}

VISTAS.acerca = async () => {
  const indice = await cargarIndice();
  const contenedor = crear('div');
  contenedor.append(cabeceraSeccion('Acerca de esta aplicación',
    'Un atlas bíblico completo y una biblioteca de consulta, hechos para funcionar en tu equipo, en español y sin conexión.',
    'portada.jpg'));
  const panel = crear('div', { clase: 'panel' });
  panel.append(crear('p', { texto: 'Renacer · Atlas Bíblico y Biblioteca reúne en un solo lugar:' }));
  const lista = crear('ul', { clase: 'lista-hechos' });
  for (const texto of [
    `${indice.mapas} mapas y planos dibujados a partir de datos geográficos libres, desde el mundo del Antiguo Testamento hasta los viajes de Pablo, más los planos del tabernáculo, el templo de Herodes y Jerusalén.`,
    `${miles(indice.lugares)} lugares citados en la Biblia, con sus referencias, coordenadas y fotografías.`,
    'Cinco diccionarios enciclopédicos completos del siglo XIX.',
    `${miles(indice.temas)} temas con cadenas de referencias bíblicas.`,
    `${indice.entradas_enciclopedia || 29} artículos de enciclopedia redactados en español, ilustrados con grabados de Doré.`,
    `La Biblia Reina-Valera 1960 completa: ${indice.libros_biblia} libros y ${miles(indice.versiculos_biblia)} versículos.`,
    `${indice.obras_arte || 241} grabados de Gustave Doré con su referencia en español.`,
  ]) lista.append(crear('li', { texto }));
  panel.append(lista);
  panel.append(crear('h3', { texto: 'Sobre las fuentes y las licencias' }));
  panel.append(crear('p', { texto: 'Todos los textos son de dominio público o de licencia libre, y se citan con su autor, '
    + 'su fecha y su licencia en la sección Biblioteca. Los mapas son dibujos originales creados para esta aplicación '
    + 'a partir de datos de Natural Earth (dominio público) y de openbible.info (CC BY 4.0). Los textos bíblicos '
    + 'citados en los diccionarios y en los temas se conservan tal como aparecen en las obras originales.' }));
  panel.append(crear('h3', { texto: 'Ficha técnica' }));
  panel.append(crear('ul', { clase: 'lista-hechos' }, [
    crear('li', {}, [crear('b', { texto: 'Nombre: ' }), 'Renacer · Atlas Bíblico y Biblioteca']),
    crear('li', {}, [crear('b', { texto: 'Versión: ' }), indice.version || '1.0.0']),
    crear('li', {}, [crear('b', { texto: 'Datos compilados el: ' }), fechaLarga(indice.construido)]),
    crear('li', {}, [crear('b', { texto: 'Tecnología: ' }), 'HTML, CSS y JavaScript sin dependencias; servidor local de Python']),
    crear('li', {}, [crear('b', { texto: 'Idioma: ' }), 'Español']),
  ]));
  contenedor.append(panel);
  contenedor.append(crear('div', { clase: 'panel', style: 'margin-top:20px' }, [
    crear('h3', { texto: 'Créditos' }),
    crear('p', { clase: 'cita', texto: '«La palabra de Dios es viva y eficaz» (Hebreos 4:12). Esta aplicación quiere servir '
      + 'de ayuda para estudiarla: los mapas para situarla, los diccionarios para entenderla, los temas para reunirla y el arte para contemplarla.' }),
    crear('p', { texto: 'Fotografías: colaboradores de Wikimedia Commons (se indica autor y licencia en cada ficha). '
      + 'Geodatos: openbible.info y Natural Earth. Grabados: Gustave Doré, 1866. Diccionarios y temas: NEUU, '
      + 'a partir de obras de dominio público.' }),
  ]));
  return contenedor;
};

VISTAS.creditos = () => VISTAS.acerca();

/* ------------------------------- buscador --------------------------------- */
VISTAS.buscar = async (partes, parametros) => {
  const consulta = (parametros && parametros.get('q')) || '';
  const contenedor = crear('div');
  contenedor.append(cabeceraSeccion('Buscador general',
    'Un solo cuadro para encontrar mapas, lugares, temas, voces de diccionario, versículos y láminas de arte.',
    'seccion-biblioteca.jpg'));
  const barra = crear('div', { clase: 'barra-herramientas' });
  const entrada = crear('input', { type: 'search', value: consulta,
    placeholder: 'Escribe una palabra: Éfeso, diluvio, Getsemaní, justificación…' });
  const boton = crear('button', { clase: 'primario', texto: 'Buscar' });
  barra.append(entrada, boton);
  const salida = crear('div');
  contenedor.append(barra, salida);

  async function lanzar() {
    const q = entrada.value.trim();
    salida.innerHTML = '';
    if (q.length < 2) {
      salida.append(crear('p', { clase: 'leyenda-mapa', texto: 'Escribe al menos dos letras.' }));
      return;
    }
    history.replaceState(null, '', `#/buscar?q=${encodeURIComponent(q)}`);
    salida.append(crear('p', { clase: 'cargando', texto: `Buscando «${q}»…` }));
    const aguja = normalizar(q);
    const [mapas, lugares, temas, diccionarios, arte, filas, libros] = await Promise.all([
      cargarMapas(), cargarLugaresIndice(), cargarTemasIndice(), cargarDiccionariosIndice(),
      cargarArte().catch(() => ({ obras: [] })), cargarBibliaBusqueda(),
      cargarBibliaLibros().catch(() => []),
    ]);
    salida.innerHTML = '';
    salida.append(crear('h2', { texto: `Resultados para «${q}»` }));
    const total = { n: 0 };
    const nombres = new Map(libros.map((l) => [l.osis, l]));

    // --- voces de diccionario ---
    const voces = [];
    for (const [codigo, lista] of Object.entries(diccionarios)) {
      for (const [id, nombre, tes] of lista) {
        if (normalizar(nombre).includes(aguja) || normalizar(tes).includes(aguja)) voces.push([codigo, id, nombre, tes]);
        if (voces.length >= 120) break;
      }
      if (voces.length >= 120) break;
    }
    if (voces.length) {
      const ul = nuevoBloque(salida, 'Diccionarios', voces.length, true);
      for (const [codigo, id, nombre, tes] of voces.slice(0, 50)) {
        ul.append(crear('li', {}, [
          crear('a', { href: `#/diccionarios/${codigo}/${id}`, texto: nombre }),
          crear('span', { clase: 'leyenda-mapa', texto: ` · ${(NOMBRES_DICCIONARIO[codigo] || [codigo])[0]}` }),
          tes ? crear('span', { clase: 'original', texto: ` — ${tes}` }) : null,
        ]));
      }
      total.n += voces.length;
    }

    // --- mapas ---
    const lMapas = mapas.filter((m) => normalizar([m.titulo, m.subtitulo, m.descripcion,
      (m.lista_lugares || []).map((l) => l.nombre).join(' '), (m.refs || []).join(' ')].join(' ')).includes(aguja));
    if (lMapas.length) {
      const ul = nuevoBloque(salida, 'Mapas y planos', lMapas.length, true);
      for (const m of lMapas.slice(0, 40)) {
        ul.append(crear('li', {}, [
          crear('a', { href: `#/mapas/${m.id}`, texto: m.titulo }),
          crear('span', { clase: 'leyenda-mapa', texto: ` · ${m.categoria}` }),
        ]));
      }
      total.n += lMapas.length;
    }

    // --- lugares ---
    const lLugares = lugares.filter((l) => normalizar(l.n).includes(aguja) || normalizar(l.o).includes(aguja));
    if (lLugares.length) {
      const ul = nuevoBloque(salida, 'Lugares', lLugares.length, true);
      for (const l of lLugares.slice(0, 50)) {
        ul.append(crear('li', {}, [
          crear('a', { href: `#/lugares/${l.id}`, texto: l.n }),
          crear('span', { clase: 'leyenda-mapa', texto: ` · ${l.t} · ${miles(l.r)} referencias` }),
        ]));
      }
      total.n += lLugares.length;
    }

    // --- temas ---
    const lTemas = temas.filter((t) => normalizar(t.t).includes(aguja) || normalizar(t.to).includes(aguja));
    if (lTemas.length) {
      const ul = nuevoBloque(salida, 'Temas bíblicos', lTemas.length, true);
      for (const t of lTemas.slice(0, 50)) {
        ul.append(crear('li', {}, [
          crear('a', { href: `#/temas/${t.id}`, texto: t.t }),
          crear('span', { clase: 'leyenda-mapa', texto: ` · ${miles(t.r)} referencias` }),
        ]));
      }
      total.n += lTemas.length;
    }

    // --- arte ---
    const lArte = (arte.obras || []).filter((o) => normalizar(`${o.titulo} ${(o.refs || []).join(' ')}`).includes(aguja));
    if (lArte.length) {
      const ul = nuevoBloque(salida, 'Galería de arte', lArte.length, true);
      for (const o of lArte.slice(0, 40)) {
        ul.append(crear('li', {}, [
          crear('a', { href: `#/arte`, texto: o.titulo, onclick: (e) => { e.preventDefault(); abrirLupa(o); } }),
          crear('span', { clase: 'leyenda-mapa', texto: ` · ${(o.refs || []).join(', ')}` }),
        ]));
      }
      total.n += lArte.length;
    }

    // --- versículos ---
    const lVersiculos = [];
    for (const [osis, cap, ver, texto] of filas) {
      if (normalizar(texto).includes(aguja)) lVersiculos.push([osis, cap, ver, texto]);
      if (lVersiculos.length >= 200) break;
    }
    if (lVersiculos.length) {
      const ul = nuevoBloque(salida, 'Versículos de la Biblia', lVersiculos.length + (lVersiculos.length >= 200 ? '+' : ''), true);
      for (const [osis, cap, ver, texto] of lVersiculos.slice(0, 50)) {
        const l = nombres.get(osis);
        ul.append(crear('li', {}, [
          crear('a', { clase: 'ref', href: `#/biblia/${osis}/${cap}?v=${ver}`, texto: `${l ? l.nombre : osis} ${cap}:${ver}` }),
          crear('span', { texto: ` ${texto.slice(0, 160)}${texto.length > 160 ? '…' : ''}` }),
        ]));
      }
      if (lVersiculos.length > 50) ul.append(crear('li', { clase: 'leyenda-mapa',
        texto: `… y ${miles(lVersiculos.length - 50)} versículos más. Acota la búsqueda para verlos todos.` }));
      total.n += lVersiculos.length;
    }

    if (!total.n) {
      salida.append(crear('p', { clase: 'sin-resultados', texto: `No se encontró nada para «${q}».` }));
      const sugerencias = temas.slice().sort((a, b) => b.r - a.r).slice(0, 12);
      const ul = nuevoBloque(salida, 'Quizá te interese', sugerencias.length, true);
      for (const t of sugerencias) ul.append(crear('li', {}, crear('a', { href: `#/temas/${t.id}`, texto: t.t })));
    }
  }

  boton.addEventListener('click', lanzar);
  entrada.addEventListener('keydown', (e) => { if (e.key === 'Enter') lanzar(); });
  if (consulta) lanzar();
  return contenedor;
};

/** Crea un bloque de resultados y devuelve su lista para ir añadiendo elementos. */
function nuevoBloque(salida, titulo, cantidad, conTotal) {
  const lista = crear('ul', { clase: 'lista-hechos' });
  const panel = crear('div', { clase: 'panel', style: 'margin-bottom:16px' }, [
    crear('h3', { texto: `${titulo} (${miles(cantidad)}${conTotal ? '' : ''})` }),
    lista,
  ]);
  salida.append(panel);
  return lista;
}

/* --------------------------- piezas de interfaz --------------------------- */
function cabeceraSeccion(titulo, descripcion, imagen) {
  return crear('div', { clase: 'seccion-cabecera' }, [
    imagen ? crear('img', { clase: 'ilustracion', src: `imagenes/${imagen}`, alt: '' }) : null,
    crear('div', {}, [crear('h1', { texto: titulo }), crear('p', { texto: descripcion })]),
  ]);
}

function migas(pasos) {
  const migas = crear('p', { clase: 'leyenda-mapa', style: 'margin-bottom:8px' });
  migas.append(crear('a', { href: '#/inicio', texto: 'Inicio' }));
  for (const [clave, texto] of pasos) {
    migas.append(' › ');
    migas.append(clave ? crear('a', { href: `#/${clave}`, texto }) : crear('span', { texto }));
  }
  return migas;
}

function noEncontrado(tipo, id) {
  return crear('div', { clase: 'panel' }, [
    crear('h2', { texto: 'No se encontró el contenido' }),
    crear('p', { texto: `No hay ningún ${tipo} con el identificador «${id}».` }),
    crear('p', {}, crear('a', { clase: 'boton', href: '#/inicio', texto: 'Volver al inicio' })),
  ]);
}

function referenciaEnlazada(texto, libros) {
  const enlace = crear('button', { clase: 'ref', type: 'button', texto,
    title: `Leer ${texto} en la Biblia Reina-Valera 1960` });
  enlace.addEventListener('click', async () => {
    const lista = libros || await cargarBibliaLibros();
    const parte = partirReferencia(texto, lista);
    if (parte) {
      irA(`#/biblia/${parte.libro.osis}/${parte.capitulo}${parte.versiculo ? `?v=${parte.versiculo}` : ''}`);
    } else {
      enlace.title = 'No se ha podido resolver esta referencia';
      enlace.classList.add('roto');
    }
  });
  return enlace;
}

/* -------------------------------- enrutado -------------------------------- */
function reemplazarPorCargando() {
  reemplazar(crear('div', { clase: 'cargando', texto: 'Cargando…' }));
}

async function enrutar() {
  const ruta = rutaActual();
  aplicarAjustes();
  const claves = Object.keys(VISTAS);
  const seccion = claves.includes(ruta.seccion) ? ruta.seccion : (ruta.seccion === '' ? 'inicio' : 'inicio');
  pintarNavegacion(seccion);
  reemplazarPorCargando();
  try {
    const vista = VISTAS[seccion] || VISTAS.inicio;
    const nodo = await vista(ruta.partes, ruta.parametros);
    reemplazar(nodo);
    const titulo = { inicio: 'Inicio', mapas: 'Mapas', lugares: 'Lugares', diccionarios: 'Diccionarios',
      temas: 'Temas', biblia: 'Biblia', arte: 'Arte', cartografia: 'Cartografía',
      biblioteca: 'Biblioteca', ayuda: 'Ayuda', acerca: 'Acerca de', buscar: 'Búsqueda' }[seccion] || 'Inicio';
    document.title = `${titulo} · Renacer Atlas Bíblico`;
    window.scrollTo({ top: 0, behavior: 'auto' });
  } catch (error) {
    console.error(error);
    reemplazar(crear('div', { clase: 'panel' }, [
      crear('h2', { texto: 'Ocurrió un problema al cargar esta sección' }),
      crear('p', { texto: String(error && error.message || error) }),
      crear('p', { texto: 'Comprueba que los datos están instalados y que has ejecutado construir_datos.py y construir_base.py.' }),
      crear('p', {}, crear('a', { clase: 'boton', href: '#/inicio', texto: 'Volver al inicio' })),
    ]));
  }
}

/* --------------------------------- arranque -------------------------------- */
async function iniciar() {
  aplicarAjustes();
  try {
    App.indice = await cargarIndice();
    const pie = $('#pie-version');
    if (pie) pie.textContent = `Versión ${App.indice.version || '1.0.0'} · datos del ${fechaLarga(App.indice.construido)}`;
    const fuentes = $('#pie-fuentes');
    if (fuentes) fuentes.textContent = (App.indice.fuentes || []).map((f) => f.nombre).join(' · ');
    const anio = $('#pie-fecha');
    if (anio) anio.textContent = `Consultado el ${new Date().toLocaleDateString('es-ES')}`;
    if ((App.indice.libros_faltantes || []).length) {
      console.warn('Faltan libros de la Biblia:', App.indice.libros_faltantes);
    }
  } catch (error) {
    console.warn('No se pudo leer indice.json:', error);
  }

  $('#marca').addEventListener('click', () => irA('#/inicio'));
  const buscador = $('#buscador');
  buscador.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && buscador.value.trim().length >= 2) {
      irA(`#/buscar?q=${encodeURIComponent(buscador.value.trim())}`);
      buscador.value = '';
    }
  });
  window.addEventListener('hashchange', enrutar);
  if (!location.hash) irA('#/inicio', false);
  else enrutar();

  if ('serviceWorker' in navigator && location.protocol.startsWith('http')) {
    navigator.serviceWorker.register('sw.js').catch(() => { /* sin service worker */ });
  }
}

document.addEventListener('DOMContentLoaded', iniciar);
