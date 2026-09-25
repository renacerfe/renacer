# Renacer

Sitio web estático para estudio bíblico, lectura de la Biblia y juegos educativos.

## Ejecutar en Debian/Linux

Desde esta carpeta:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Luego abrir <http://127.0.0.1:8000/index.html>.

Es necesario usar un servidor local porque el lector bíblico y los juegos cargan archivos JSON mediante `fetch`.

## Páginas principales

- `index.html`: bienvenida.
- `menu-index.html`: menú principal.
- `menu-clases.html`: clases bíblicas.
- `historia-menu.html`: libros de la Biblia.
- `reina.html`: lector Reina-Valera 1960.
- `menu-juegos.html`: zona de juegos.
- `juego.html`: cuestionario de Números 11.
- `index-juego1.html`: juego Valentía.

## Estructura sencilla

- Los estilos compartidos están en `site.css`.
- Los estilos del lector están dentro de `reina.html` y usan las reglas responsive de `site.css`.
- La lógica del cuestionario está en `quiz.js`.
- `juego-style.css` contiene los estilos del juego Valentía.
- Los libros bíblicos están en archivos JSON con sus nombres originales.

## Comprobaciones rápidas

```bash
# Ver el estado del repositorio
git status

# Revisar enlaces y archivos referenciados
grep -RIn 'href="#"\|numeros11.json\|style.css\|estilos.css' --include='*.html' --include='*.htm' .
```
