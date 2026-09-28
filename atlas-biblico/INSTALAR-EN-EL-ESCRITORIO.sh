#!/bin/bash
# ==========================================================================
#  Instalador de «Renacer · Atlas Bíblico y Biblioteca»
#
#  Deja la aplicación instalada en tu equipo y crea sus iconos en el
#  escritorio, para que se abra con un doble clic. No necesita permisos de
#  administrador: todo se guarda en tu carpeta personal.
#
#  Cómo usarlo:  doble clic en este archivo y elegir «Ejecutar».
#  Si tu gestor de archivos no lo ejecuta, abre una terminal en esta carpeta
#  y escribe:   bash INSTALAR-EN-EL-ESCRITORIO.sh
# ==========================================================================

set -u
CARPETA="$(cd "$(dirname "$0")" && pwd)"
cd "$CARPETA" || exit 1

azul='\033[36m'; verde='\033[32m'; amarillo='\033[33m'; rojo='\033[31m'; normal='\033[0m'

echo
echo -e "${azul}  ══════════════════════════════════════════════════════════${normal}"
echo -e "${azul}    Renacer · Atlas Bíblico y Biblioteca — instalación${normal}"
echo -e "${azul}  ══════════════════════════════════════════════════════════${normal}"
echo
echo "  Carpeta: $CARPETA"
echo

# --- 1. ¿Está Python 3? ----------------------------------------------------
if ! command -v python3 >/dev/null 2>&1; then
  echo -e "${rojo}  ✘ No se ha encontrado Python 3.${normal}"
  echo "     En Ubuntu, Debian o Linux Mint se instala con:"
  echo "         sudo apt install python3"
  echo "     En Fedora: sudo dnf install python3"
  echo "     En Arch:   sudo pacman -S python"
  echo
  read -r -p "  Pulsa Intro para cerrar…" _ || true
  exit 1
fi
echo -e "${verde}  ✔ Python 3 disponible:${normal} $(python3 --version 2>&1 | cut -d' ' -f2)"

# --- 2. ¿Hay navegador? ----------------------------------------------------
navegador=""
for n in firefox chromium chromium-browser google-chrome google-chrome-stable brave-browser microsoft-edge vivaldi opera epiphany; do
  if command -v "$n" >/dev/null 2>&1; then navegador="$n"; break; fi
done
if [ -n "$navegador" ]; then
  echo -e "${verde}  ✔ Navegador encontrado:${normal} $navegador"
else
  echo -e "${amarillo}  ! No se ha encontrado un navegador conocido.${normal}"
  echo "     Se intentará abrir con el navegador predeterminado del sistema."
fi
echo

# --- 3. Instalación en el escritorio ---------------------------------------
python3 "$CARPETA/compositor.py" escritorio
resultado=$?

echo
if [ $resultado -eq 0 ]; then
  echo -e "${verde}  ✔ Listo. Ya tienes tres iconos en el escritorio:${normal}"
  echo "       · Atlas Bíblico ....... la aplicación completa"
  echo "       · Mapas bíblicos ...... los 71 mapas y planos"
  echo "       · Galería de arte ..... los 241 grabados de Gustave Doré"
  echo
  echo "  Haz doble clic en el que quieras. Si el sistema pregunta si confías en"
  echo "  el archivo, elige «Permitir lanzar» o «Ejecutar»."
  echo
  echo "  La aplicación también está en el menú de aplicaciones del sistema,"
  echo "  dentro de «Educación», y en la terminal con la orden:  renacer-atlas abrir"
else
  echo -e "${rojo}  ✘ La instalación no ha terminado bien.${normal}"
  echo "     Copia este mensaje y lo revisamos."
fi
echo
echo "  Puedes cerrar esta ventana."
read -r -p "  Pulsa Intro para cerrar…" _ || true
