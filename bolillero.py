import random
import time
import os

# --- CONFIGURACIÓN DE ALUMNOS ---
# Lista de diccionarios con nombre y significado.
# Puedes agregar más alumnos copiando el formato: {"nombre": "X", "significado": "Y"},
ALUMNOS_DB = [
    {"nombre": "Valentina", "significado": "Valiente, fuerte, saludable (Latín)."},
    {"nombre": "Gisella", "significado": "Flecha poderosa, rayo de luz o prenda de felicidad (Germánico)."},
    {"nombre": "Josefa", "significado": "Dios añadirá o Dios multiplica (Hebreo)."},
    {"nombre": "Carolina", "significado": "Mujer fuerte, libre y audaz (Germánico)."},
    {"nombre": "Noelia", "significado": "La que nació en Navidad o Natividad (Francés/Latín)."},
    {"nombre": "Sofia", "significado": "Sabiduría (Griego)."},
    {"nombre": "Claudia", "significado": "Perteneciente a la ilustre familia Claudia (Latín)."},
    {"nombre": "Ezequiel", "significado": "Dios es mi fortaleza (Hebreo)."},
    {"nombre": "Gerardo", "significado": "Guerrero valiente con la lanza (Germánico)."},
    {"nombre": "Cristian", "significado": "Seguidor de Cristo o ungido (Griego/Latín)."},
    {"nombre": "Santino", "significado": "Santo, sagrado (Latín/Italiano)."},
    {"nombre": "Dardo", "significado": "Hombre hábil, audaz o amigo querido (Germánico)."},
    {"nombre": "Orlando", "significado": "Fama de la tierra o gloria del país (Germánico)."}
]

def limpiar_pantalla():
    """Limpia la consola para una visualización más limpia en el proyector/pantalla."""
    os.system('cls' if os.name == 'nt' else 'clear')

def animacion_suspenso():
    """Genera un pequeño efecto de espera antes de mostrar el nombre."""
    print("\n🎲 Girando el bolillero...", end="", flush=True)
    for _ in range(3):
        time.sleep(0.6) # Tiempo de espera entre puntos
        print(".", end="", flush=True)
    print("\n")

def main():
    # Hacemos una copia de la lista original para ir sacando nombres sin borrar la base de datos
    bolillas = ALUMNOS_DB.copy()
    random.shuffle(bolillas) # Mezclamos las bolillas al inicio

    limpiar_pantalla()
    print("╔════════════════════════════════════════╗")
    print("║         🎓 BOLILLERO DIGITAL 🎓        ║")
    print("╚════════════════════════════════════════╝")
    print(f"  Total de alumnos en lista: {len(ALUMNOS_DB)}")
    print("\nInstrucciones:")
    print("👉 Presiona [ENTER] para sacar un alumno.")
    print("👉 Escribe 'salir' para terminar el programa.")

    while True:
        print(f"\n(Quedan {len(bolillas)} alumnos por salir)")
        entrada = input("¿Listo? Presiona ENTER >> ")

        if entrada.lower() == 'salir':
            print("\n¡Clase finalizada! Hasta luego. 👋")
            break

        if not bolillas:
            print("\n⚠️  ¡ATENCIÓN: Ya han salido todos los alumnos!")
            reiniciar = input("¿Quieres reiniciar el bolillero y mezclar de nuevo? (s/n): ")
            if reiniciar.lower() == 's':
                bolillas = ALUMNOS_DB.copy()
                random.shuffle(bolillas)
                limpiar_pantalla()
                print("🔄 ¡Bolillero recargado y mezclado nuevamente!")
                continue
            else:
                print("Fin del sorteo.")
                break

        animacion_suspenso()
        
        # Sacamos (pop) el último elemento de la lista mezclada
        elegido = bolillas.pop()
        
        print(f"🎉  ALUMNO SELECCIONADO:  {elegido['nombre'].upper()}  🎉")
        print(f"📖  Significado: {elegido['significado']}")
        print("──────────────────────────────────────────")

if __name__ == "__main__":
    main()