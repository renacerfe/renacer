#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compositor.py — Lanzador de escritorio de «Renacer · Atlas Bíblico» para Linux.

No necesita ninguna dependencia externa: solo la biblioteca estándar de Python 3
y un navegador instalado en el sistema (Firefox, Chrome, Chromium, Brave,
Edge, Vivaldi, Epiphany, Falkon, Midori u otro navegador registrado con
xdg-open).

Órdenes disponibles
-------------------
  abrir [--seccion=mapas]   Abre la aplicación (como aplicación de escritorio).
  servir [--puerto=8765]    Sirve la aplicación en red local y la abre.
  instalar [--dir=...]      Instala accesos directos, iconos y asociaciones.
  desinstalar               Quita los accesos directos y la copia instalada.
  accesos                   Reinstala solo los accesos del menú y el escritorio.
  autoprueba                Comprueba que todos los datos están en su sitio.
  version                   Muestra la versión y las fuentes de datos.

Ejemplos
--------
  python3 compositor.py abrir
  python3 compositor.py abrir --seccion=diccionarios
  python3 compositor.py servir --puerto=8765 --host=0.0.0.0
  python3 compositor.py instalar
"""

import argparse
import http.server
import json
import mimetypes
import os
import shutil
import signal
import socket
import socketserver
import subprocess
import sys
import threading
import time
import urllib.parse
import webbrowser
from pathlib import Path

NOMBRE = "Renacer · Atlas Bíblico"
VERSION = "1.0.0"
ESQUEMA = "renacer"
IDENTIFICADOR = "renacer-atlas-biblico"

AQUI = Path(__file__).resolve().parent          # /ruta/atlas-biblico
APP = AQUI / "app"
DESTINO = Path(os.environ.get("RENACER_DESTINO", Path.home() / ".local/share/renacer-atlas"))
BIN = Path.home() / ".local/bin"
APPS = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share")) / "applications"
ICONOS = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share")) / "icons/hicolor"
ESTADO = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "renacer-atlas"
PUERTO_FIJO = 8790                     # puerto del servidor en segundo plano
REGISTRO = ESTADO / "servidor.log"
FICHERO_PID = ESTADO / "servidor.pid"

NAVEGADORES = [
    ("firefox", "Mozilla Firefox"), ("firefox-esr", "Mozilla Firefox ESR"),
    ("google-chrome", "Google Chrome"), ("google-chrome-stable", "Google Chrome"),
    ("chromium", "Chromium"), ("chromium-browser", "Chromium"),
    ("brave-browser", "Brave"), ("microsoft-edge", "Microsoft Edge"),
    ("vivaldi", "Vivaldi"), ("opera", "Opera"), ("epiphany", "GNOME Web"),
    ("falkon", "Falkon"), ("midori", "Midori"), ("qutebrowser", "qutebrowser"),
    ("waterfox", "Waterfox"), ("palemoon", "Pale Moon"),
]

SECCIONES = {
    "inicio": "", "mapas": "mapas", "lugares": "lugares", "diccionarios": "diccionarios",
    "temas": "temas", "biblia": "biblia", "arte": "arte", "cartografia": "cartografia",
    "biblioteca": "biblioteca", "ayuda": "ayuda", "acerca": "acerca",
}


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------
def color(texto, codigo):
    if not sys.stdout.isatty():
        return texto
    return f"\033[{codigo}m{texto}\033[0m"


def info(msg):
    print(f"  {color('·', '33')} {msg}")


def bien(msg):
    print(f"  {color('✔', '32')} {msg}")


def aviso(msg):
    print(f"  {color('!', '33')} {msg}")


def error(msg):
    print(f"  {color('✘', '31')} {msg}", file=sys.stderr)


def ruta_datos():
    """Directorio con los datos de la aplicación (instalado o en el repositorio)."""
    return APP if (APP / "index.html").exists() else DESTINO / "app"


def hay_entorno_grafico():
    if sys.platform.startswith("win") or sys.platform == "darwin":
        return True
    return bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))


def buscar_ejecutable(nombres):
    for nombre in nombres:
        ruta = shutil.which(nombre)
        if ruta:
            return ruta
    return None


def navegador_del_sistema():
    return (buscar_ejecutable(["xdg-open", "gio", "gnome-open", "kde-open5", "kde-open",
                               "exo-open", "sensible-browser"]) or
            (sys.executable if sys.platform == "darwin" else None))


def localizar_navegador():
    """Devuelve (comando, etiqueta) del navegador preferido."""
    del_entorno = os.environ.get("BROWSER")
    if del_entorno:
        primero = del_entorno.split(os.pathsep)[0].split(" ")[0]
        ruta = shutil.which(primero)
        if ruta:
            return ruta, Path(ruta).name
    for ejecutable, etiqueta in NAVEGADORES:
        ruta = shutil.which(ejecutable)
        if ruta:
            return ruta, etiqueta
    return None, None


NAVEGADOR = localizar_navegador()


# ---------------------------------------------------------------------------
# Perfil propio de navegador (para que se abra como aplicación, no como pestaña)
# ---------------------------------------------------------------------------
def preparar_perfil(puerto):
    """Crea (o reutiliza) un perfil de navegador exclusivo de la aplicación."""
    perfil = Path.home() / f".config/{IDENTIFICADOR}/perfil-navegador"
    perfil.mkdir(parents=True, exist_ok=True)
    marca = perfil / "renacer-marca.txt"
    if not marca.exists():
        marca.write_text(f"{NOMBRE} {VERSION}\n", encoding="utf-8")
    # Preferencias que hacen que se comporte como una ventana de aplicación
    prefs = perfil / "user.js"
    prefs.write_text(
        'user_pref("browser.shell.checkDefaultBrowser", false);\n'
        'user_pref("browser.startup.homepage_override.mstone", "ignore");\n'
        'user_pref("browser.aboutwelcome.enabled", false);\n'
        'user_pref("datareporting.policy.dataSubmissionEnabled", false);\n'
        'user_pref("toolkit.telemetry.enabled", false);\n'
        'user_pref("browser.tabs.warnOnClose", false);\n'
        'user_pref("browser.tabs.warnOnCloseOtherTabs", false);\n'
        'user_pref("browser.bookmarks.restore_default_bookmarks", false);\n'
        'user_pref("browser.sessionstore.resume_from_crash", false);\n'
        'user_pref("browser.fullscreen.autohide", true);\n'
        'user_pref("browser.uidensity", 1);\n', encoding="utf-8")
    (perfil / "First Run").touch(exist_ok=True)
    local_state = perfil / "Local State"
    if not local_state.exists():
        local_state.write_text('{"browser": {"check_default_browser": false}}\n', encoding="utf-8")
    return perfil


def argumentos_navegador(ruta_ejecutable, url, perfil, ancho=1500, alto=950):
    """Argumentos para abrir el navegador en modo aplicación."""
    nombre = Path(ruta_ejecutable).name.lower()
    args = [ruta_ejecutable, "--app=" + url, f"--window-size={ancho},{alto}",
            f"--user-data-dir={perfil}", "--no-first-run", "--no-default-browser-check"]
    if "epiphany" in nombre:
        args = [ruta_ejecutable, "--application-mode", "--profile=" + str(perfil)]
    elif nombre in ("qutebrowser",):
        args = [ruta_ejecutable, str(perfil), url]
    elif nombre in ("falkon", "midori", "palemoon"):
        args = [ruta_ejecutable, "--profile=" + str(perfil), url]
    elif "firefox" in nombre or "waterfox" in nombre:
        args = [ruta_ejecutable, "--new-window", url, "--profile", str(perfil),
                "--no-remote"]
    return args


def lanzar_navegador(url, perfil=None, esperar=False):
    """Abre la URL en un navegador. Devuelve True si se pudo lanzar."""
    if NAVEGADOR[0]:
        ruta, etiqueta = NAVEGADOR
        perfil = perfil or preparar_perfil(url)
        args = argumentos_navegador(ruta, url, perfil)
        try:
            if esperar:
                return subprocess.call(args) == 0
            subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                             start_new_session=True)
            return True
        except OSError:
            pass
    otro = navegador_del_sistema()
    if otro:
        try:
            subprocess.Popen([otro, url], stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL, start_new_session=True)
            return True
        except OSError:
            pass
    try:
        return webbrowser.open_new(url)
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Servidor local
# ---------------------------------------------------------------------------
class Manejador(http.server.SimpleHTTPRequestHandler):
    """Sirve la aplicación con los tipos MIME correctos y sin caché.

    Si hay una carpeta de descargas (junto al programa o en app/descargas), sus
    archivos se ofrecen también en /descargas/<archivo>, para poder descargar el
    paquete de la aplicación desde ella misma.
    """

    descargas = None

    def translate_path(self, ruta):
        limpia = urllib.parse.urlparse(ruta).path
        if self.descargas and limpia.startswith("/descargas/"):
            nombre = Path(urllib.parse.unquote(limpia[len("/descargas/"):])).name
            if nombre:
                archivo = Path(self.descargas) / nombre
                if archivo.is_file():
                    return str(archivo)
        return super().translate_path(ruta)

    extensiones = {".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8",
                   ".json": "application/json; charset=utf-8", ".svg": "image/svg+xml",
                   ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                   ".webp": "image/webp", ".css": "text/css; charset=utf-8",
                   ".txt": "text/plain; charset=utf-8", ".md": "text/plain; charset=utf-8",
                   ".ico": "image/x-icon", ".woff2": "font/woff2",
                   ".zip": "application/zip", ".gz": "application/gzip", ".xz": "application/x-xz"}

    def guess_type(self, ruta):
        ext = Path(urllib.parse.urlparse(ruta).path).suffix.lower()
        return self.extensiones.get(ext, mimetypes.guess_type(ruta)[0] or "application/octet-stream")

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.send_header("Service-Worker-Allowed", "/")
        super().end_headers()

    def log_message(self, formato, *args):      # silencio: no ensuciar la terminal
        pass


class Servidor(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def puerto_libre(preferido):
    for puerto in range(preferido, preferido + 40):
        with socket.socket() as s:
            try:
                s.bind(("127.0.0.1", puerto))
                return puerto
            except OSError:
                continue
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def carpeta_descargas():
    """Carpeta desde la que se ofrecen los paquetes de descarga (puede no existir).

    Se busca, en este orden, la carpeta indicada en la variable de entorno
    RENACER_DESCARGAS, la que está junto a este programa (descargas/) y la de
    dentro de la aplicación (app/descargas/).
    """
    candidatas = [Path(os.environ["RENACER_DESCARGAS"])] if os.environ.get("RENACER_DESCARGAS") else []
    candidatas += [AQUI / "descargas", APP / "descargas"]
    for ruta in candidatas:
        if ruta.is_dir() and any(ruta.glob("*.zip")):
            return ruta
    return None


def levantar_servidor(puerto, host="127.0.0.1", directorio=None):
    directorio = Path(directorio or ruta_datos())

    class ManejadorLocal(Manejador):
        pass

    ManejadorLocal.descargas = carpeta_descargas()
    manejador = lambda *a, **k: ManejadorLocal(*a, directory=str(directorio), **k)  # noqa: E731
    servidor = Servidor((host, puerto), manejador)
    hilo = threading.Thread(target=servidor.serve_forever, daemon=True)
    hilo.start()
    return servidor


def url_de(seccion="", puerto=None, ruta_local=None):
    ancla = SECCIONES.get(seccion, seccion)
    if puerto:
        return f"http://127.0.0.1:{puerto}/index.html" + (f"#{ancla}" if ancla else "")
    base = (ruta_local or ruta_datos() / "index.html").resolve()
    return base.as_uri() + (f"#{ancla}" if ancla else "")


# ---------------------------------------------------------------------------
# Órdenes
# ---------------------------------------------------------------------------
def directorio_escritorio():
    """Localiza la carpeta de escritorio del usuario (respeta el idioma del sistema)."""
    if os.environ.get("XDG_DESKTOP_DIR") and Path(os.environ["XDG_DESKTOP_DIR"]).is_dir():
        return Path(os.environ["XDG_DESKTOP_DIR"])
    try:
        salida = subprocess.run(["xdg-user-dir", "DESKTOP"], capture_output=True, text=True,
                                check=False).stdout.strip()
        if salida and Path(salida).is_dir():
            return Path(salida)
    except (OSError, subprocess.SubprocessError):
        pass
    for nombre in ("Escritorio", "Desktop", "Escritorio", "Bureau", "Schreibtisch", "Área de trabalho"):
        ruta = Path.home() / nombre
        if ruta.is_dir():
            return ruta
    ruta = Path.home() / "Escritorio"
    return ruta if ruta.exists() else None


def marcar_confiable(acceso):
    """En GNOME hay que marcar el acceso del escritorio como «de confianza»."""
    try:
        acceso.chmod(0o755)
    except OSError:
        pass
    for orden in (["gio", "set", str(acceso), "metadata::trusted", "true"],
                  ["gio", "set", str(acceso), "metadata::xfce-exe-checksum", ""]):
        try:
            subprocess.run(orden, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except (OSError, subprocess.SubprocessError):
            break


def puerto_escuchando(puerto, host="127.0.0.1"):
    with socket.socket() as s:
        s.settimeout(0.4)
        return s.connect_ex((host, puerto)) == 0


def leer_pid():
    try:
        return int(FICHERO_PID.read_text(encoding="utf-8").strip())
    except (OSError, ValueError):
        return None


def servidor_de_fondo(puerto=PUERTO_FIJO):
    """Arranca (o reutiliza) un servidor en segundo plano y devuelve el puerto."""
    if puerto_escuchando(puerto):
        return puerto
    ESTADO.mkdir(parents=True, exist_ok=True)
    orden = [sys.executable, str(Path(__file__).resolve()), "servir",
             "--puerto", str(puerto), "--host", "127.0.0.1", "--sin-abrir", "--exacto"]
    with open(REGISTRO, "ab") as registro:
        proceso = subprocess.Popen(orden, stdout=registro, stderr=registro, stdin=subprocess.DEVNULL,
                                   start_new_session=True)
    FICHERO_PID.write_text(str(proceso.pid), encoding="utf-8")
    for _ in range(40):                     # hasta 8 segundos
        if puerto_escuchando(puerto):
            return puerto
        time.sleep(0.2)
    return None


def orden_detener():
    """Detiene el servidor que quedó trabajando en segundo plano."""
    pid = leer_pid()
    if pid is None and not puerto_escuchando(PUERTO_FIJO):
        info("No hay ningún servidor en segundo plano.")
        return 0
    detenido = False
    if pid:
        try:
            os.kill(pid, signal.SIGTERM)
            detenido = True
        except OSError:
            pass
    try:
        subprocess.run(["pkill", "-f", "compositor.py servir"], check=False,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (OSError, subprocess.SubprocessError):
        pass
    try:
        FICHERO_PID.unlink()
    except OSError:
        pass
    bien("Servidor detenido." if detenido or pid else "Servidor detenido.")
    return 0


def orden_abrir(seccion="inicio", puerto=None, host="127.0.0.1", esperar=False, fondo=False):
    """Abre la aplicación. Si hay navegador, usa un servidor local (recomendado)."""
    if fondo:
        # modo «doble clic»: se levanta el servidor y se suelta el proceso
        puerto = servidor_de_fondo(puerto or PUERTO_FIJO)
        if puerto is None:
            error("No se pudo poner en marcha el servidor local.")
            return 1
        url = url_de(seccion, puerto)
        bien(f"{NOMBRE} en {url}")
        if lanzar_navegador(url):
            return 0
        aviso("No se ha podido abrir el navegador automáticamente.")
        print(f"   Abre esta dirección en tu navegador: {url}")
        return 0
    uso_servidor = puerto is not None or True     # siempre por servidor: mejor rendimiento
    servidor = None
    if uso_servidor:
        puerto = puerto_libre(puerto or 8790)
        try:
            servidor = levantar_servidor(puerto, host=host)
            url = url_de(seccion, puerto)
        except OSError as exc:
            aviso(f"No se pudo abrir el servidor local ({exc}); se abre desde el archivo.")
            url = url_de(seccion)
            servidor = None
    else:
        url = url_de(seccion)
    if not hay_entorno_grafico() and not esperar:
        aviso("No se detecta entorno gráfico (DISPLAY/WAYLAND_DISPLAY).")
        print(f"   Abre esta dirección en el navegador: {url}")
        if servidor:
            print("   El servidor seguirá activo hasta que pulses Ctrl+C.")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                pass
        return 0
    info(f"Dirección local: {color(url, '36')}")
    if NAVEGADOR[0]:
        info(f"Navegador: {NAVEGADOR[1]}")
        lanzar_navegador(url, esperar=esperar)
    else:
        aviso("No se ha encontrado un navegador conocido; se intenta con xdg-open.")
        lanzar_navegador(url, esperar=esperar)
    print()
    print(f"  {NOMBRE} está abierto en tu navegador.")
    print("  Deja esta ventana abierta mientras la usas; ciérrala para detener la aplicación.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n  Aplicación detenida.")
    finally:
        if servidor:
            servidor.shutdown()
    return 0


def orden_servir(puerto=8765, host="127.0.0.1", seccion="inicio", abrir=True, exacto=False):
    puerto = puerto if exacto else puerto_libre(puerto)
    servidor = levantar_servidor(puerto, host=host)
    ip = "127.0.0.1"
    if host not in ("127.0.0.1", "localhost"):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
        except OSError:
            ip = host
    url = f"http://{ip}:{puerto}/index.html" + (f"#{SECCIONES.get(seccion, '')}" if SECCIONES.get(seccion, '') else "")
    bien(f"Sirviendo {NOMBRE} en {color(url, '36')}")
    print("   Pulsa Ctrl+C para detener el servidor.")
    if abrir:
        lanzar_navegador(url)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n  Servidor detenido.")
    finally:
        servidor.shutdown()
    return 0


def escribir_desktop(destino, ejecutable, icono, seccion="", servidor=False):
    if servidor:
        exec_linea = f'"{ejecutable}" servir --puerto=8765 --host=0.0.0.0'
        nombre = f"{NOMBRE} (servidor en la red local)"
    else:
        # --fondo: el servidor queda trabajando y el navegador se abre enseguida
        exec_linea = f'"{ejecutable}" abrir --fondo'
        if seccion:
            exec_linea += f" --seccion={seccion}"
        nombre = NOMBRE if not seccion else f"{NOMBRE}: {seccion.capitalize()}"
    contenido = f"""[Desktop Entry]
Type=Application
Version=1.0
Name={nombre}
Name[en]={NOMBRE if not seccion else NOMBRE + ': ' + seccion.capitalize()}
GenericName=Atlas bíblico y biblioteca de estudio
GenericName[en]=Bible atlas and study library
Comment=Mapas bíblicos, diccionarios enciclopédicos, temas, Biblia RVR1960 y arte
Comment[en]=Bible maps, encyclopedic dictionaries, topics, Bible text and art
Exec={exec_linea}
Icon={icono}
Terminal=false
Categories=Education;Literature;Geography;Science;
Keywords=Biblia;Bible;mapas;maps;atlas;diccionario;dictionary;teología;theology;
StartupNotify=true
StartupWMClass={IDENTIFICADOR}
X-GNOME-UsesNotifications=false
"""
    if not seccion and not servidor:
        contenido += (f"MimeType=x-scheme-handler/{ESQUEMA};\n"
                      f"X-Renacer-SchemeHosts=app;\n")
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(contenido, encoding="utf-8")
    destino.chmod(0o755)
    return destino


def orden_instalar(directorio_destino=DESTINO, accesos=True):
    print(color(f"\n  Instalando {NOMBRE} {VERSION}\n", "1"))
    # 1. Copia de la aplicación
    directorio_destino = Path(directorio_destino)
    if directorio_destino.exists():
        info(f"Actualizando la copia instalada en {directorio_destino}")
    (directorio_destino / "app").mkdir(parents=True, exist_ok=True)
    # se copia la aplicación (web + datos + mapas + imágenes) manteniendo el árbol
    for entrada in APP.iterdir():
        destino = directorio_destino / "app" / entrada.name
        if entrada.is_dir():
            shutil.copytree(entrada, destino, dirs_exist_ok=True)
        else:
            shutil.copy2(entrada, destino)
    # se copia el propio lanzador y los materiales de escritorio del paquete
    shutil.copy2(AQUI / "compositor.py", directorio_destino / "compositor.py")
    if (AQUI / "bin/renacer-atlas").exists():
        (directorio_destino / "bin").mkdir(exist_ok=True)
        shutil.copy2(AQUI / "bin/renacer-atlas", directorio_destino / "bin/renacer-atlas")
    for nombre in ("LEEME.md", "CREDITOS.md"):
        if (AQUI / nombre).exists():
            shutil.copy2(AQUI / nombre, directorio_destino / nombre)
    lanzador = directorio_destino / "compositor.py"
    lanzador.chmod(0o755)
    bien(f"Aplicación copiada en {directorio_destino}")
    total = sum(f.stat().st_size for f in (directorio_destino / "app").rglob("*") if f.is_file())
    info(f"Tamaño instalado: {total / 1024 / 1024:.1f} MB")

    # 2. Iconos
    icono_principal = APP / "imagenes/icono.png"
    if icono_principal.exists():
        for tam in (48, 64, 128, 256, 512):
            destino = ICONOS / f"{tam}x{tam}/apps/{IDENTIFICADOR}.png"
            destino.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(icono_principal, destino)
        bien(f"Iconos instalados en {ICONOS}")

    # 3. Lanzador de terminal
    BIN.mkdir(parents=True, exist_ok=True)
    script = BIN / "renacer-atlas"
    script.write_text(f"""#!/bin/sh
# Lanzador de {NOMBRE}
exec python3 "{lanzador}" "$@"
""", encoding="utf-8")
    script.chmod(0o755)
    bien(f"Orden de terminal instalada: {script} (escríbela como «renacer-atlas»)")

    # 4. Accesos directos del menú de aplicaciones y del escritorio
    escritorio = directorio_escritorio()
    if accesos:
        principal = escribir_desktop(APPS / f"{IDENTIFICADOR}.desktop", lanzador, IDENTIFICADOR)
        bien(f"Acceso en el menú de aplicaciones: {principal}")
        if escritorio:
            # tres accesos bien ordenados en el escritorio del usuario
            for sufijo, seccion, etiqueta in (("", "", "Atlas Bíblico"),
                                              ("-mapas", "mapas", "Mapas bíblicos"),
                                              ("-arte", "arte", "Galería de arte")):
                copia = escribir_desktop(escritorio / f"{IDENTIFICADOR}{sufijo}.desktop",
                                         lanzador, IDENTIFICADOR, seccion=seccion)
                marcar_confiable(copia)
                bien(f"Acceso en el escritorio: {copia.name}  ({etiqueta})")
        else:
            aviso("No se encontró la carpeta Escritorio/Desktop; se omite el acceso del escritorio.")
        # accesos a cada sección principal
        for seccion, etiqueta in (("mapas", "Mapas"), ("diccionarios", "Diccionarios"),
                                  ("biblia", "Biblia"), ("arte", "Arte"),
                                  ("temas", "Temas")):
            escribir_desktop(APPS / f"{IDENTIFICADOR}-{seccion}.desktop", lanzador,
                             IDENTIFICADOR, seccion=seccion)
        bien("Accesos directos por secciones añadidos al menú")
        escribir_desktop(APPS / f"{IDENTIFICADOR}-servidor.desktop", lanzador,
                         IDENTIFICADOR, servidor=True)
        # 5. Registro de la aplicación y del esquema renacer://
        try:
            subprocess.run(["update-desktop-database", str(APPS)], check=False,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except (OSError, subprocess.SubprocessError):
            pass
        try:
            subprocess.run(["xdg-mime", "default", f"{IDENTIFICADOR}.desktop",
                            f"x-scheme-handler/{ESQUEMA}"], check=False,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except (OSError, subprocess.SubprocessError):
            pass
        try:
            subprocess.run(["gtk-update-icon-cache", "-q", "-t", "-f",
                            str(ICONOS.parent)], check=False,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except (OSError, subprocess.SubprocessError):
            pass
        bien(f"Esquema «{ESQUEMA}://» registrado (se puede llamar desde otras aplicaciones)")

    print()
    bien("Instalación terminada.")
    print(f"   · Menú de aplicaciones → «{NOMBRE}»")
    print("   · Terminal → renacer-atlas abrir")
    print("   · Desinstalar → renacer-atlas desinstalar")
    return 0


def orden_escritorio(directorio_destino=DESTINO):
    """Instala la aplicación con su icono en el escritorio y la abre al terminar."""
    orden_instalar(directorio_destino, accesos=True)
    escritorio = directorio_escritorio()
    if escritorio:
        try:
            for acceso in escritorio.glob(f"{IDENTIFICADOR}*.desktop"):
                marcar_confiable(acceso)
            # algunos entornos exigen permiso de ejecución en la propia carpeta
            escritorio.chmod(escritorio.stat().st_mode | 0o755)
        except OSError:
            pass
    print()
    info("Abriendo la aplicación…")
    orden_abrir("inicio", PUERTO_FIJO, "127.0.0.1", esperar=False, fondo=True)
    print()
    if escritorio:
        print(f"   En el escritorio ({escritorio}) tienes tres iconos:")
        print("     · «Atlas Bíblico» ......... la aplicación completa")
        print("     · «Mapas bíblicos» ........ los 71 mapas y planos")
        print("     · «Galería de arte» ....... los 241 grabados de Doré")
        print("   Haz doble clic en cualquiera de ellos para volver a abrirla.")
    print("   Para detener el servidor:  python3 compositor.py detener")
    return 0


def orden_desinstalar(conservar_datos=False):
    print(color(f"\n  Desinstalando {NOMBRE}\n", "1"))
    borrados = 0
    if APPS.exists():
        for f in APPS.glob(f"{IDENTIFICADOR}*.desktop"):
            f.unlink()
            borrados += 1
    escritorios = [directorio_escritorio(), Path.home() / "Escritorio", Path.home() / "Desktop"]
    for escritorio in escritorios:
        if escritorio.exists():
            for f in escritorio.glob(f"{IDENTIFICADOR}*.desktop"):
                f.unlink()
                borrados += 1
    bien(f"Accesos directos eliminados: {borrados}")
    for tam in (48, 64, 128, 256, 512):
        icono = ICONOS / f"{tam}x{tam}/apps/{IDENTIFICADOR}.png"
        if icono.exists():
            icono.unlink()
    bien("Iconos eliminados")
    script = BIN / "renacer-atlas"
    if script.exists():
        script.unlink()
        bien("Orden de terminal eliminada")
    if DESTINO.exists() and not conservar_datos:
        shutil.rmtree(DESTINO)
        bien(f"Copia instalada eliminada ({DESTINO})")
    print()
    print("  Nota: tus descargas de mapas o imágenes se guardan en ~/Imágenes/Renacer-Atlas"
          " y no se tocan.")
    return 0


def orden_accesos(directorio_destino=DESTINO):
    lanzador = Path(directorio_destino) / "compositor.py"
    if not lanzador.exists():
        aviso("No hay instalación previa; ejecutando la instalación completa.")
        return orden_instalar(directorio_destino)
    principal = escribir_desktop(APPS / f"{IDENTIFICADOR}.desktop", lanzador, IDENTIFICADOR)
    bien(f"Acceso del menú reinstalado: {principal}")
    return 0


def orden_paquete():
    """Genera el paquete ZIP que el usuario descarga y descomprime."""
    script = AQUI / "herramientas" / "empaquetar_zip.py"
    if not script.exists():
        error(f"No se encuentra {script}")
        return 1
    resultado = subprocess.call([sys.executable, str(script)])
    if resultado == 0:
        print(f"   Envíalo a donde quieras: se puede descargar desde {PAQUETE_URL}")
    return resultado


PAQUETE_URL = "la propia aplicación (pestaña «Ayuda») o el archivo descargas/atlas-biblico.zip"


def orden_autoprueba():
    print(color(f"\n  Autoprueba de {NOMBRE} {VERSION}\n", "1"))
    fallos = 0
    datos = ruta_datos()
    print(f"  Directorio de datos: {datos}")
    obligatorios = ["index.html", "app.js", "estilo.css", "sw.js", "manifest.webmanifest",
                    "datos/indice.json", "datos/lugares.json",
                    "datos/temas.json", "datos/mapas.json", "datos/base.json", "datos/regiones.json",
                    "datos/arte.json", "datos/lugares_indice.json", "datos/temas_indice.json",
                    "datos/diccionarios_indice.json", "datos/biblia_busqueda.json",
                    "datos/biblia/libros.json", "datos/diccionarios/easton.json",
                    "datos/fotos.json", "imagenes/icono.png", "imagenes/portada.jpg"]
    for relativo in obligatorios:
        ruta = datos / relativo
        if ruta.exists():
            bien(f"{relativo} ({ruta.stat().st_size / 1024:.0f} KB)")
        else:
            error(f"FALTA {relativo}")
            fallos += 1
    try:
        indice = json.loads((datos / "datos/indice.json").read_text(encoding="utf-8"))
        print()
        print(f"  Lugares bíblicos ...... {indice.get('lugares', '?')}")
        print(f"  Regiones .............. {indice.get('regiones', '?')}")
        print(f"  Temas ................. {indice.get('temas', '?')}")
        print(f"  Referencias temáticas . {indice.get('referencias_tematicas', '?')}")
        total_voces = sum(d.get("entradas", 0) for d in indice.get("diccionarios", []))
        print(f"  Voces de diccionario .. {total_voces}")
        print(f"  Libros de la Biblia ... {indice.get('libros_biblia', '?')}")
        print(f"  Versículos ............ {indice.get('versiculos_biblia', '?')}")
        print(f"  Fotografías ........... {indice.get('fotos', '?')}")
        mapas = json.loads((datos / "datos/mapas.json").read_text(encoding="utf-8"))
        print(f"  Mapas y planos ........ {len(mapas)}")
        faltan = [m["id"] for m in mapas if not (datos / m["archivo"]).exists()]
        if faltan:
            error(f"Faltan archivos de mapa: {', '.join(faltan[:8])}")
            fallos += len(faltan)
        else:
            bien("Todos los archivos de mapas están presentes")
        arte = json.loads((datos / "datos/arte.json").read_text(encoding="utf-8"))
        print(f"  Obras de arte ......... {arte.get('total', 0)}")
        sin_imagen = [o["id"] for o in arte.get("obras", []) if not (datos / o["archivo"]).exists()]
        if sin_imagen:
            error(f"Faltan ilustraciones: {', '.join(sin_imagen[:8])}")
            fallos += len(sin_imagen)
        else:
            bien("Todas las ilustraciones están presentes")
        faltan_libros = indice.get("libros_faltantes") or []
        if faltan_libros:
            aviso(f"Libros de la Biblia sin texto en el repositorio: {', '.join(faltan_libros)}")
    except (OSError, json.JSONDecodeError, KeyError) as exc:
        error(f"No se pudieron leer los datos: {exc}")
        fallos += 1
    print()
    print(f"  Navegador detectado: {NAVEGADOR[1] if NAVEGADOR[0] else 'ninguno conocido'}")
    print(f"  Entorno gráfico: {'sí' if hay_entorno_grafico() else 'no'}")
    print(f"  Python: {sys.version.split()[0]} ({sys.executable})")
    if fallos:
        error(f"Autoprueba terminada con {fallos} problema(s)")
        return 1
    bien("Autoprueba superada: la aplicación está completa.")
    return 0


def orden_version():
    print(f"{NOMBRE} {VERSION}")
    indice = ruta_datos() / "datos/indice.json"
    if indice.exists():
        d = json.loads(indice.read_text(encoding="utf-8"))
        print(f"  Datos construidos el {d.get('construido', '?')}")
        for fuente in d.get("fuentes", []):
            print(f"  · {fuente['nombre']} — {fuente['licencia']}")
            print(f"      {fuente['url']}")
    return 0


# ---------------------------------------------------------------------------
# Línea de órdenes
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(prog="renacer-atlas",
                                 description=f"{NOMBRE} {VERSION}: lanzador de escritorio")
    sub = ap.add_subparsers(dest="orden")

    p = sub.add_parser("abrir", help="Abre la aplicación")
    p.add_argument("--seccion", default="inicio", choices=sorted(SECCIONES))
    p.add_argument("--puerto", type=int, default=None)
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--esperar", action="store_true", help="Espera a que se cierre el navegador")
    p.add_argument("--fondo", action="store_true",
                   help="Deja el servidor funcionando en segundo plano (para el doble clic)")

    p = sub.add_parser("servir", help="Sirve la aplicación en la red local")
    p.add_argument("--puerto", type=int, default=8765)
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--seccion", default="inicio", choices=sorted(SECCIONES))
    p.add_argument("--sin-abrir", action="store_true")
    p.add_argument("--exacto", action="store_true", help="Usa el puerto indicado aunque esté ocupado")

    p = sub.add_parser("instalar", help="Instala accesos directos e integración de escritorio")
    p.add_argument("--dir", default=str(DESTINO))
    p.add_argument("--sin-accesos", action="store_true")

    p = sub.add_parser("desinstalar", help="Quita accesos directos y la copia instalada")
    p.add_argument("--conservar-datos", action="store_true")

    p = sub.add_parser("accesos", help="Reinstala los accesos del menú")
    p.add_argument("--dir", default=str(DESTINO))

    sub.add_parser("escritorio", help="Instala la aplicación y su icono en el escritorio")
    sub.add_parser("detener", help="Detiene el servidor que trabaja en segundo plano")
    sub.add_parser("autoprueba", help="Comprueba que los datos están completos")
    sub.add_parser("version", help="Muestra la versión y las fuentes")

    args = ap.parse_args()
    orden = args.orden or "abrir"
    if orden == "abrir":
        return orden_abrir(args.seccion, args.puerto, args.host, args.esperar, args.fondo)
    if orden == "servir":
        return orden_servir(args.puerto, args.host, args.seccion, not args.sin_abrir, args.exacto)
    if orden == "escritorio":
        return orden_escritorio()
    if orden == "detener":
        return orden_detener()
    if orden == "instalar":
        return orden_instalar(args.dir, accesos=not args.sin_accesos)
    if orden == "desinstalar":
        return orden_desinstalar(args.conservar_datos)
    if orden == "accesos":
        return orden_accesos(args.dir)
    if orden == "paquete":
        return orden_paquete()
    if orden == "autoprueba":
        return orden_autoprueba()
    if orden == "version":
        return orden_version()
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
