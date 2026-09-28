/* Renacer · Atlas Bíblico — trabajador de servicio (funcionamiento sin conexión)
   Guarda en caché todo lo que la aplicación carga desde el propio equipo:
   la interfaz, los mapas, los datos y las ilustraciones.                       */

const CACHE = 'renacer-atlas-v2';
const ESENCIALES = [
  './',
  'index.html',
  'estilo.css',
  'app.js',
  'manifest.webmanifest',
  'imagenes/icono.png',
  'imagenes/portada.jpg',
];

self.addEventListener('install', (evento) => {
  evento.waitUntil(
    caches.open(CACHE)
      .then((cache) => cache.addAll(ESENCIALES).catch(() => undefined))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (evento) => {
  evento.waitUntil(
    caches.keys()
      .then((claves) => Promise.all(claves.filter((c) => c !== CACHE).map((c) => caches.delete(c))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (evento) => {
  const peticion = evento.request;
  if (peticion.method !== 'GET') return;
  const url = new URL(peticion.url);
  // lo que no sea del propio equipo (fotografías y enlaces externos) no se guarda
  if (url.origin !== self.location.origin) return;
  // el paquete de descarga se sirve directo, sin pasar por la caché
  if (url.pathname.includes('/descargas/') || url.pathname.endsWith('.zip')) return;

  // datos y mapas: primero la copia guardada, para que abran al instante
  const esDato = /\/(datos|mapas|arte)\//.test(url.pathname);
  if (esDato) {
    evento.respondWith(
      caches.match(peticion).then((guardada) => guardada || fetch(peticion).then((respuesta) => {
        if (respuesta && respuesta.ok) {
          const copia = respuesta.clone();
          caches.open(CACHE).then((cache) => cache.put(peticion, copia));
        }
        return respuesta;
      }))
    );
    return;
  }

  // la interfaz: primero la red y, si falla, la copia guardada
  evento.respondWith(
    fetch(peticion)
      .then((respuesta) => {
        if (respuesta && respuesta.ok) {
          const copia = respuesta.clone();
          caches.open(CACHE).then((cache) => cache.put(peticion, copia));
        }
        return respuesta;
      })
      .catch(() => caches.match(peticion).then((guardada) => guardada || caches.match('index.html')))
  );
});
