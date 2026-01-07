const CACHE_NAME = "renacer-pwa-v4";

const CORE_FILES = [
  "/renacer/",
  "/renacer/index.html",
  "/renacer/menu-index.html",
  "/renacer/menu-juegos.html",
  "/renacer/metodo-estudio.html",
  "/renacer/juego.html",

  "/renacer/style.css",
  "/renacer/juego-style.css",
  "/renacer/juego-game.js",

  "/renacer/logo.png",
  "/renacer/manifest.json",
  "/renacer/offline.html"
];

// INSTALL
self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(CORE_FILES))
  );
  self.skipWaiting();
});

// ACTIVATE
self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.map(key => {
          if (key !== CACHE_NAME) return caches.delete(key);
        })
      )
    )
  );
  self.clients.claim();
});

// FETCH (DINÁMICO)
self.addEventListener("fetch", event => {
  if (event.request.method !== "GET") return;

  event.respondWith(
    caches.match(event.request).then(cached => {
      if (cached) return cached;

      return fetch(event.request)
        .then(response => {
          return caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, response.clone());
            return response;
          });
        })
        .catch(() => caches.match("/renacer/offline.html"));
    })
  );
});