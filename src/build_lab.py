"""Sesión 2 (laboratorio CADe_SIMU, 3 h).  Uso: python3 src/build_lab.py

Las diapositivas de SOLUCIÓN se generan ocultas (clic derecho → Mostrar diapositiva)."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from ejercicios import EJ, TENSION  # noqa: E402
from pptx.enum.text import MSO_ANCHOR  # noqa: E402
from pptx_utils import (DGREEN, GTINT, INK, NAVY, RED, ROOT, TINT, Deck, box, card,  # noqa: E402
                        circle_num, image, table, text)

OUT = os.path.join(ROOT, "sesion2_laboratorio", "RGIM_S2_Laboratorio_CADeSIMU.pptx")
d = Deck("Seguridad eléctrica · Mando y fuerza · RGIM")

d.cover()
d.title_slide("Laboratorio: esquemas de mando y fuerza",
              "Armar y simular en CADe_SIMU\nSesión de laboratorio · 3 h",
              notes="Las diapositivas de solución están OCULTAS. Para mostrarlas: clic derecho en la "
                    "miniatura → Mostrar diapositiva.")

s = d.content("Plan del laboratorio (180 min)",
              notes="Si el grupo va lento, L5 queda como tarea.")
filas = [["Tiempo", "Actividad"], ["0:00 – 0:15", "CADe_SIMU en 15 minutos"]]
t = 15
for e in EJ:
    if e["key"] == "L4":
        filas.append(["%d:%02d – %d:%02d" % (t // 60, t % 60, (t + 10) // 60, (t + 10) % 60), "Pausa"])
        t += 10
    filas.append(["%d:%02d – %d:%02d" % (t // 60, t % 60, (t + e["minutos"]) // 60,
                                          (t + e["minutos"]) % 60), e["titulo"]])
    t += e["minutos"]
filas.append(["%d:%02d – 3:00" % (t // 60, t % 60), "Errores frecuentes y cierre"])
table(s, 0.6, 1.5, 7.9, filas, [1.9, 6.0], size=13, row_h=0.42)
card(s, 8.8, 1.6, 3.95, 4.3, "Entregable por ejercicio", [
    "Esquema de fuerza y de mando en CADe_SIMU",
    "Captura de la simulación funcionando",
    "Respuestas a las preguntas guía"], fill=GTINT, head_color=DGREEN, size=15)

d.section("0", "CADe_SIMU en 15 minutos", "Dibujar, nombrar y simular",
          notes="Demostración en vivo con L0 mientras los alumnos replican. CADe_SIMU es gratuito "
                "(Windows). Los nombres de menús pueden variar entre versiones (usamos la 4.x).")

s = d.content("Flujo de trabajo en CADe_SIMU",
              notes="Puntos donde se traban: (1) el contacto no actúa porque no tiene EXACTAMENTE el "
                    "mismo nombre que su bobina; (2) se olvida la alimentación; (3) se intenta "
                    "editar con la simulación en marcha.")
pasos = [("Alimentación", "Coloca L1-L2-L3 (fuerza) y L1-N (mando) desde la biblioteca de alimentaciones."),
         ("Componentes", "Arrastra protecciones, contactores, térmico, motor, pulsadores y pilotos."),
         ("Cablear", "Une los bornes con la herramienta de cable. Revisa cada unión."),
         ("Nombrar", "Doble clic en cada aparato: bobina KM1 y sus contactos también KM1."),
         ("Ajustar", "Temporizador: tiempo (p. ej. 5 s). Térmico: su nombre F1."),
         ("Simular", "Botón de simulación. Clic en los pulsadores; clic en el térmico = sobrecarga."),
         ("Verificar", "Compara con la tabla de estados del enunciado.")]
for i, (h, b) in enumerate(pasos):
    col = 0 if i < 4 else 1
    row = i if i < 4 else i - 4
    x, y = 0.6 + col * 6.15, 1.55 + row * 1.12
    circle_num(s, x, y + 0.08, 0.5, str(i + 1), size=14)
    text(s, x + 0.65, y, 5.3, 0.4, [h], size=16, bold=True, color=NAVY)
    text(s, x + 0.65, y + 0.38, 5.3, 0.7, [b], size=13, color=INK)
box(s, 6.75, 4.95, 6.0, 1.0, fill=GTINT)
text(s, 6.9, 5.0, 5.75, 0.9, [[("Regla de oro de CADe_SIMU: ", {"bold": True, "color": DGREEN}),
                               ("un contacto pertenece al aparato que tiene su MISMO nombre.", {})]],
     size=13, anchor=MSO_ANCHOR.MIDDLE)

s = d.content("Convenciones del laboratorio",
              notes="Fijar las convenciones antes de empezar evita la mitad de los errores.")
card(s, 0.6, 1.6, 5.95, 4.3, "Tensiones y nombres", [
    TENSION,
    "Q interruptor, KM contactor, KT temporizador, F protecciones, S pulsadores, H pilotos, M motor",
    "Paro S0; marchas S1, S2…"], size=15)
card(s, 6.8, 1.6, 5.95, 4.3, "Bornes", [
    "Bobina A1-A2; principales 1-2, 3-4, 5-6",
    "Auxiliar NA 13-14 / 43-44; NC 21-22",
    "Térmico 95-96 (NC) y 97-98 (NA)",
    "Temporizador 55-56 (NC) y 67-68 (NA)"], fill=GTINT, head_color=DGREEN, size=15)

s = d.content("Lo que dibujas en CADe_SIMU existe en el tablero",
              notes="Mostrar antes de L1: cada aparato del esquema tiene una ubicación física y la "
                    "misma etiqueta. Si el laboratorio tiene un tablero didáctico, señalar en él Q1, "
                    "KM1, F1, la bornera y la puerta.")
image(s, "a_tablero", 0.6, 1.4, 6.3, 4.75)
card(s, 7.15, 1.6, 5.6, 4.3, "Esquema L1 → tablero", [
    "Q1 y F2 arriba, en el riel DIN",
    "KM1 con F1 enchufado debajo",
    "Bornera X1: motor y puerta; PE verde-amarillo",
    "Puerta: S0, S1, H1, H2"], fill=GTINT, head_color=DGREEN, size=15)

for e in EJ:
    s = d.content(e["titulo"],
                  notes="Tiempo sugerido: %d min. Dejar trabajar en parejas; mostrar la solución "
                        "(diapositiva oculta siguiente) solo al cierre del ejercicio." % e["minutos"])
    box(s, 0.6, 1.55, 5.6, 4.4, fill=TINT)
    text(s, 0.8, 1.65, 5.2, 0.4, ["Enunciado"], size=16, bold=True, color=NAVY)
    text(s, 0.8, 2.15, 5.2, 3.7, [e["enunciado"]], size=15)
    text(s, 6.55, 1.5, 6.2, 0.4, ["Preguntas guía"], size=17, bold=True, color=DGREEN)
    n = len(e["preguntas"])
    for i, q in enumerate(e["preguntas"]):
        y = 2.0 + i * (3.95 / n)
        circle_num(s, 6.55, y + 0.02, 0.42, str(i + 1), size=13)
        text(s, 7.1, y - 0.03, 5.65, 3.95 / n, [q], size=14)

    s = d.content("Solución · " + e["titulo"], hidden=True,
                  notes="Explicar el funcionamiento siguiendo la corriente en el mando.")
    if e["fuerza"]:
        image(s, e["fuerza"], 0.4, 1.4, 3.6, 4.7)
        image(s, e["mando"], 4.1, 1.4, 5.2, 4.7)
        x = 9.45
    else:
        image(s, e["mando"], 0.6, 1.4, 4.0, 4.7)
        x = 5.0
    box(s, x, 1.55, 12.75 - x, 4.45, fill=GTINT)
    text(s, x + 0.12, 1.62, 12.75 - x - 0.24, 4.3, e["funcionamiento"], size=12, bullets=True,
         space_after=3)

s = d.content("Errores frecuentes",
              notes="Repasar con los casos reales vistos durante el laboratorio.")
errs = [("Nombres distintos", "KM1 y Km1 son aparatos distintos: el contacto no actúa."),
        ("Autorretención en serie", "KM1 13-14 va en PARALELO con S1, no en serie."),
        ("Térmico fuera del mando", "Sin 95-96 en serie, el disparo no detiene el motor."),
        ("Sin enclavamiento", "KM1 y KM2 juntos (o KM2 y KM3): cortocircuito."),
        ("Temporizador equivocado", "Debe ser a la conexión (retardo al energizar)."),
        ("Editar simulando", "Detén la simulación antes de modificar el esquema.")]
for i, (h, b) in enumerate(errs):
    col, row = i % 2, i // 2
    x, y = 0.6 + col * 6.15, 1.6 + row * 1.45
    box(s, x, y, 5.95, 1.3, fill=TINT if col == 0 else GTINT)
    text(s, x + 0.2, y + 0.1, 5.6, 0.45, [h], size=16, bold=True, color=RED)
    text(s, x + 0.2, y + 0.55, 5.6, 0.7, [b], size=14, color=INK)

s = d.content("Lista de verificación",
              notes="Puede usarse como rúbrica (1 punto por ítem).")
chk = ["Fuerza y mando dibujados por separado",
       "Todo en reposo; NA abiertos y NC cerrados",
       "Mismo nombre en bobina y contactos",
       "Bornes numerados (A1-A2, 13-14, 95-96…)",
       "Protecciones: Q1, F1 (95-96 en serie), F2",
       "Autorretención y enclavamientos correctos",
       "Simulación verificada estado por estado",
       "Sobrecarga simulada: el motor se detiene"]
for i, c in enumerate(chk):
    col, row = i // 4, i % 4
    x, y = 0.6 + col * 6.15, 1.6 + row * 1.05
    box(s, x, y + 0.12, 0.45, 0.45, fill=GTINT, radius=False)
    text(s, x + 0.65, y, 5.4, 0.75, [c], size=16, anchor=MSO_ANCHOR.MIDDLE)

d.cover()
os.makedirs(os.path.dirname(OUT), exist_ok=True)
d.save(OUT)
print("ok", OUT, len(d.prs.slides))
