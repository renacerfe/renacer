/* ==========================================================================
   Prueba automática de la interfaz — Renacer · Atlas Bíblico

   Carga app/index.html con jsdom, sirve los datos desde el disco (igual que el
   servidor local) y recorre todas las secciones comprobando que se pintan sin
   errores. Necesita Node.js y la biblioteca jsdom:

       cd herramientas && npm install jsdom      (una sola vez)
       node prueba_interfaz.js

   Devuelve 0 si todo está bien y 1 si encuentra algún problema.
   ========================================================================== */
const fs = require('fs');
const path = require('path');
const { JSDOM, VirtualConsole } = require('jsdom');

const APP = path.join(__dirname, '..', 'app');
const errores = [];
const avisos = [];

const consola = new VirtualConsole();
consola.on('jsdomError', (e) => errores.push('jsdomError: ' + (e && e.message)));
consola.on('error', (...a) => errores.push('console.error: ' + a.map(String).join(' ')));
consola.on('warn', (...a) => avisos.push('console.warn: ' + a.map(String).join(' ')));

function respuestaLocal(ruta, opciones) {
  const limpio = decodeURIComponent(ruta.replace(/^\.\//, '').split('?')[0]);
  const metodo = (opciones && opciones.method) || 'GET';
  // igual que el servidor real: además de la carpeta de la aplicación se mira la
  // carpeta contigua, que es donde vive el paquete de descarga (descargas/)
  const candidatos = [path.join(APP, limpio), path.join(APP, '..', limpio)];
  const archivo = candidatos.find((r) => fs.existsSync(r) && !fs.statSync(r).isDirectory());
  if (!archivo) {
    return Promise.resolve({ ok: false, status: 404, statusText: 'No encontrado',
      headers: { get: () => null },
      json: async () => { throw new Error('404 ' + limpio); }, text: async () => '' });
  }
  const tamano = fs.statSync(archivo).size;
  const cabeceras = { get: (n) => (String(n).toLowerCase() === 'content-length' ? String(tamano) : null) };
  if (metodo === 'HEAD') {
    return Promise.resolve({ ok: true, status: 200, statusText: 'OK', headers: cabeceras,
      json: async () => ({}), text: async () => '' });
  }
  const texto = fs.readFileSync(archivo, 'utf8');
  return Promise.resolve({
    ok: true, status: 200, statusText: 'OK', headers: cabeceras,
    json: async () => JSON.parse(texto),
    text: async () => texto,
  });
}

(async () => {
  const dom = await JSDOM.fromFile(path.join(APP, 'index.html'), {
    runScripts: 'dangerously',
    pretendToBeVisual: true,
    resources: undefined,
    virtualConsole: consola,
    url: 'http://localhost:8765/index.html',
    beforeParse(ventana) {
      ventana.fetch = (url, opciones) => respuestaLocal(String(url).replace(/^https?:\/\/[^/]+\//, ''), opciones);
      ventana.requestAnimationFrame = (fn) => setTimeout(fn, 0);
      ventana.HTMLElement.prototype.scrollIntoView = () => {};
      ventana.scrollTo = () => {};
      ventana.HTMLElement.prototype.requestFullscreen = () => Promise.resolve();
      ventana.console.error = (...a) => errores.push('console.error: ' + a.map(String).join(' '));
      ventana.console.warn = (...a) => avisos.push('console.warn: ' + a.map(String).join(' '));
      ventana.addEventListener('unhandledrejection', (e) => errores.push('promesa rechazada: ' + e.reason));
    },
  });
  const ventana = dom.window;
  const { document } = ventana;
  const esperar = (ms = 400) => new Promise((r) => setTimeout(r, ms));
  // se carga app.js a mano (jsdom no carga recursos externos por defecto)
  const script = document.createElement('script');
  script.textContent = fs.readFileSync(path.join(APP, 'app.js'), 'utf8');
  document.head.appendChild(script);
  document.dispatchEvent(new ventana.Event('DOMContentLoaded'));
  await esperar(900);

  const main = () => document.querySelector('#contenido');
  const rutas = [
    '#/inicio', '#/mapas', '#/mapas/egipto-biblico', '#/mapas/tierra-santa-fisica', '#/mapas/plano-tabernaculo',
    '#/mapas/viajes-pablo-1', '#/lugares', '#/lugares/jerusalem', '#/lugares/ephesus',
    '#/diccionarios', '#/diccionarios/easton', '#/diccionarios/smith/abraham',
    '#/temas', '#/temas/idolatry', '#/temas/love', '#/biblia', '#/biblia/Juan/3', '#/biblia/Sal/23',
    '#/arte', '#/cartografia', '#/biblioteca', '#/biblioteca?articulo=jerusalen', '#/ayuda', '#/acerca', '#/buscar?q=efeso',
    '#/buscar?q=justificacion', '#/buscar?q=diluvio',
  ];
  for (const ruta of rutas) {
    ventana.location.hash = ruta;
    await esperar(700);
    const contenido = main();
    const texto = (contenido.textContent || '').replace(/\s+/g, ' ').trim();
    const longitud = texto.length;
    const estado = longitud > 120 ? 'ok ' : 'CORTA';
    console.log(`${estado} ${ruta.padEnd(32)} ${String(longitud).padStart(6)} caracteres  |  ${texto.slice(0, 78)}`);
    if (longitud <= 120) errores.push(`contenido escaso en ${ruta}: «${texto}»`);
    if (/Cargando…$/.test(texto)) errores.push(`no terminó de cargar ${ruta}`);
  }

  // la caja de descarga del paquete debe aparecer en la portada y en la ayuda
  ventana.location.hash = '#/inicio';
  await esperar(900);
  const cajaInicio = document.querySelector('#caja-descarga');
  ventana.location.hash = '#/ayuda';
  await esperar(900);
  const cajaAyuda = document.querySelector('#caja-descarga');
  console.log(`     caja de descarga: portada ${cajaInicio ? 'sí' : 'NO'} · ayuda ${cajaAyuda ? 'sí' : 'NO'}`);
  if (!cajaInicio || !cajaAyuda) {
    errores.push('no aparece el botón de descarga del paquete');
  } else {
    const enlace = cajaInicio.querySelector('a[download]');
    console.log(`     enlace de descarga: ${enlace ? enlace.getAttribute('href') : 'ausente'}`);
    if (!enlace) errores.push('la caja de descarga no tiene enlace');
  }

  // la enciclopedia y el arte deben traer contenido real
  ventana.location.hash = '#/biblioteca';
  await esperar(800);
  const articulos = main().querySelectorAll('.entrada').length;
  const imagenesArte = document.querySelectorAll('#contenido img').length;
  console.log(`     enciclopedia: ${articulos} artículos, ${imagenesArte} imágenes en la sección`);
  if (articulos < 20) errores.push(`la biblioteca mostró solo ${articulos} artículos`);

  // el título de las secciones y los enlaces internos deben existir
  const enlacesRotos = new Set();
  for (const a of document.querySelectorAll('a[href^="#/"]')) {
    const destino = a.getAttribute('href');
    const seccion = destino.replace(/^#\/?/, '').split('/')[0].split('?')[0];
    if (!['inicio', 'mapas', 'lugares', 'diccionarios', 'temas', 'biblia', 'arte', 'cartografia',
      'biblioteca', 'ayuda', 'acerca', 'creditos', 'buscar'].includes(seccion)) enlacesRotos.add(destino);
  }
  if (enlacesRotos.size) errores.push('enlaces internos desconocidos: ' + [...enlacesRotos].join(', '));

  console.log('\nRESULTADO');
  console.log('  errores:', errores.length);
  errores.slice(0, 20).forEach((e) => console.log('   ✘', e));
  console.log('  avisos:', avisos.length);
  avisos.slice(0, 8).forEach((a) => console.log('   ·', a));
  process.exit(errores.length ? 1 : 0);
})();
