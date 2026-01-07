const CACHE_NAME = "arbol-de-la-vida-v1";

const FILES_TO_CACHE = [
  "./",
  "./index.html",
  "./menu-index.html",
  "./menu-juegos.html",
  "./metodo-estudio.html",
  "./style.css",
  "./juego-style.css",
  "./juego-game.js",
  "./manifest.json",
  "./logo.png"
];

// Instalar
self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(FILES_TO_CACHE);
    })
  );
  self.skipWaiting();
});

// Activar
self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.map(key => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      )
    )
  );
  self.clients.claim();
});

// Fetch
self.addEventListener("fetch", event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    })
  );
});