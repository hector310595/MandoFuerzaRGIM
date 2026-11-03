"""Sesión 1 (teoría, 2 h): Seguridad eléctrica y esquemas de mando y fuerza.
Uso: python3 src/build_teoria.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import fotos  # noqa: E402
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN  # noqa: E402
from pptx_utils import (DGREEN, GREEN, GTINT, INK, MUTED, NAVY, RED, ROOT, TINT, WHITE, Deck, box,  # noqa: E402
                        caption, card, circle_num, image, table, text)

OUT = os.path.join(ROOT, "sesion1_teoria", "RGIM_S1_Seguridad_Mando_Fuerza_Teoria.pptx")
d = Deck("Seguridad eléctrica · Mando y fuerza · RGIM")

def foto(slide, clave, x, y, w, h, cap=None):
    """Foto real con su crédito (obligatorio por la licencia) debajo."""
    image(slide, fotos.ruta(clave), x, y, w, h - 0.62)
    if cap:
        caption(slide, x, y + h - 0.6, w, cap, size=12, color=INK)
    caption(slide, x, y + h - 0.3, w, fotos.credito(clave), size=8, color=MUTED)


# ------------------------------------------------------------------ apertura
d.cover()
d.title_slide("Seguridad eléctrica y esquemas de mando y fuerza",
              "Representación Gráfica para Ingeniería Mecatrónica\nSesión teórica · 2 h",
              notes="Esta semana pasamos del aire a la electricidad. Hoy: (1) cómo protegerse y "
                    "proteger la instalación, y (2) cómo se DIBUJA y se LEE un esquema eléctrico "
                    "industrial. En el laboratorio lo armaremos y simularemos en CADe_SIMU.")

s = d.content("Al terminar la semana podrás…",
              notes="(3 min) Alcance. No veremos: cálculo de secciones de cable, selectividad, "
                    "esquemas TT/TN/IT en detalle, variadores ni PLC.")
items = [("1", "Explicar el riesgo eléctrico", "Qué daña al cuerpo y cómo protegen el diferencial, "
                                                 "la puesta a tierra y las protecciones."),
         ("2", "Leer un esquema", "Distinguir fuerza y mando, reconocer símbolos IEC 60617 y la "
                                  "numeración de bornes."),
         ("3", "Dibujar un esquema", "Marcha-paro, inversión de giro y estrella-triángulo, en "
                                     "reposo y con designaciones correctas."),
         ("4", "Simular en CADe_SIMU", "Armar, verificar y diagnosticar fallas de un circuito.")]
for i, (n, h, b) in enumerate(items):
    y = 1.6 + i * 1.08
    circle_num(s, 0.8, y + 0.08, 0.62, n)
    text(s, 1.65, y, 5.3, 0.45, [h], size=19, bold=True, color=NAVY)
    text(s, 1.65, y + 0.45, 5.6, 0.6, [b], size=14, color=MUTED)
box(s, 7.6, 1.6, 5.1, 4.3, fill=TINT)
text(s, 7.85, 1.75, 4.7, 0.45, ["Agenda de hoy (120 min)"], size=18, bold=True, color=NAVY)
for i, (t, a) in enumerate([("40'", "Seguridad eléctrica aplicada al tablero"),
                            ("25'", "Cómo se representa: fuerza, mando, símbolos y bornes"),
                            ("45'", "Circuitos: marcha-paro, dos puntos, inversión, Y-Δ"),
                            ("10'", "Metodología y cierre")]):
    y = 2.35 + i * 0.8
    text(s, 7.85, y, 0.8, 0.5, [t], size=16, bold=True, color=DGREEN)
    text(s, 8.65, y, 3.9, 0.7, [a], size=15, color=INK)

# --------------------------------------------------------- 1 · seguridad
d.section("1", "Seguridad eléctrica", "Riesgo, contactos, puesta a tierra y protecciones",
          notes="Bloque de 40 min. Mensaje: lo que daña es la CORRIENTE que atraviesa el cuerpo y el "
                "TIEMPO que dura; las protecciones existen para limitar una de las dos.")

s = d.content("Lo peligroso es la corriente… y el tiempo",
              notes="(5 min) La tensión 'empuja', pero el daño depende de la corriente que pasa por el "
                    "cuerpo (I = U / R del cuerpo) y de cuánto dura. Factores: magnitud, tiempo, "
                    "trayectoria (mano-mano, mano-pie: cruza el corazón), frecuencia (50/60 Hz es la "
                    "más peligrosa para el corazón) y la resistencia del cuerpo (piel húmeda la baja "
                    "mucho). Por eso las protecciones de personas actúan sobre el TIEMPO de corte.")
for i, (h, b) in enumerate([("Intensidad", "A más mA, efectos más graves."),
                            ("Tiempo", "La misma corriente es más grave cuanto más dura."),
                            ("Trayectoria", "Si cruza el pecho (mano-pie, mano-mano), afecta al corazón."),
                            ("Frecuencia", "50/60 Hz es la zona más peligrosa para el corazón."),
                            ("Resistencia del cuerpo", "Piel húmeda o herida → mucha más corriente.")]):
    col, row = i % 3, i // 3
    x, y = 0.6 + col * 4.1, 1.6 + row * 2.2
    box(s, x, y, 3.85, 2.0, fill=TINT if row == 0 else GTINT)
    text(s, x + 0.2, y + 0.2, 3.45, 0.45, [h], size=18, bold=True, color=NAVY)
    text(s, x + 0.2, y + 0.8, 3.45, 1.1, [b], size=15)
box(s, 8.8, 3.8, 3.95, 2.0, fill=NAVY)
text(s, 9.0, 3.95, 3.6, 1.7, [[("I = U / R", {"bold": True, "color": GREEN, "size": 26})],
                              [("El daño depende de I y t, no solo de la tensión.", {"color": WHITE})]],
     size=15)

s = d.content("Efectos de la corriente alterna en el cuerpo",
              notes="(6 min) Zonas de IEC 60479-1 para CA de 15 a 100 Hz. Los valores en mA son "
                    "ORIENTATIVOS (trayectoria mano-pie, exposición de varios segundos); la norma "
                    "las define como curvas tiempo-corriente. El mensaje para el alumno: unos pocos "
                    "mA durante segundos ya pueden impedir soltar el conductor; por eso el "
                    "diferencial de protección de personas es de 30 mA y corta en milisegundos.")
table(s, 0.6, 1.6, 8.0, [
    ["Zona (IEC 60479-1)", "Efecto", "Orden de magnitud*"],
    ["AC-1", "Percepción, sin reacción", "≈ 0,5 mA"],
    ["AC-2", "Percepción y contracciones involuntarias, sin daño", "≈ 0,5 – 10 mA"],
    ["AC-3", "Contracción fuerte, dificultad para soltar y para respirar", "≈ 10 mA a decenas de mA"],
    ["AC-4", "Riesgo de fibrilación ventricular (aumenta con I y t)", "decenas–cientos de mA"],
], [2.2, 4.0, 1.8], size=14, row_h=0.62)
text(s, 0.6, 4.85, 8.0, 0.9, ["* Valores orientativos para CA 50/60 Hz y varios segundos de "
                              "exposición. La norma usa curvas tiempo-corriente: a menor tiempo, "
                              "se tolera más corriente."], size=12, color=MUTED)
card(s, 8.9, 1.6, 3.85, 4.3, "Consecuencia práctica", [
    "Diferencial de 30 mA para proteger personas",
    "Corte automático rápido (ms)",
    "Nunca trabajar con tensión: reglas de oro"], fill=GTINT, head_color=DGREEN)

s = d.content("Contacto directo y contacto indirecto",
              notes="(6 min) Directo: la persona toca una parte que NORMALMENTE está en tensión "
                    "(un borne, un cable pelado). Indirecto: toca una masa metálica que NO debería "
                    "tener tensión pero la tiene por una falla de aislamiento (carcasa del motor). "
                    "Contra el indirecto: puesta a tierra de las masas + corte automático (el "
                    "diferencial detecta la fuga y abre). El diferencial de 30 mA es además "
                    "protección ADICIONAL contra contacto directo, no la principal.")
card(s, 0.6, 1.6, 5.95, 4.3, "Contacto directo", [
    "Con una parte activa: borne, cable pelado, barra",
    [("Protección: ", {"bold": True}), ("aislamiento, envolventes, tapas, distancia", {})],
    [("Adicional: ", {"bold": True}), ("diferencial ≤ 30 mA", {})],
    "En el laboratorio: no abrir el tablero energizado"], fill=TINT)
card(s, 6.8, 1.6, 5.95, 4.3, "Contacto indirecto", [
    "Con una masa que quedó en tensión por una falla (carcasa del motor)",
    [("Protección: ", {"bold": True}), ("puesta a tierra de las masas + corte automático", {})],
    "El diferencial detecta la corriente que se fuga a tierra y abre",
    "Conductor de protección PE: verde-amarillo"], fill=GTINT, head_color=DGREEN)

s = d.content("Protecciones del tablero: qué protege cada una",
              notes="(8 min) Pasar por cada fila mostrando el símbolo. Clave para el esquema: el "
                    "relé térmico protege al MOTOR contra sobrecarga pero NO corta cortocircuitos; "
                    "por eso siempre va acompañado de fusibles o de un interruptor magnético aguas "
                    "arriba. El guardamotor reúne térmico + magnético en un solo aparato.")
rows = [("sym_fusible", "Fusible (F)", "Cortocircuito (y sobrecarga según tipo)", "Se funde: hay que reponerlo"),
        ("sym_interruptor_3p", "Interruptor termomagnético (Q)", "Sobrecarga + cortocircuito",
         "Curvas B, C, D según la carga"),
        ("sym_termico_3p", "Relé térmico (F)", "Sobrecarga del motor",
         "No corta cortocircuitos; abre el mando con 95-96"),
        ("sym_nc", "Interruptor diferencial (Q)", "Fuga a tierra / personas",
         "30 mA: protección de personas")]
for i, (img, h, prot, nota) in enumerate(rows):
    y = 1.55 + i * 1.12
    box(s, 0.6, y, 12.15, 1.0, fill=TINT if i % 2 == 0 else GTINT)
    if i < 3:
        image(s, img, 0.7, y + 0.05, 1.9, 0.9)
    else:
        text(s, 0.7, y + 0.15, 1.9, 0.7, ["IΔn"], size=22, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
    text(s, 2.8, y + 0.1, 3.3, 0.8, [h], size=16, bold=True, color=NAVY, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 6.2, y + 0.1, 3.3, 0.8, [prot], size=15, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 9.5, y + 0.1, 3.2, 0.8, [nota], size=13, color=MUTED, anchor=MSO_ANCHOR.MIDDLE)

s = d.content("Así se ven en el tablero",
              notes="(2 min) Si es posible, llevar los aparatos reales del laboratorio y pasarlos de "
                    "mano en mano. Señalar: (1) todos se montan a presión en el riel DIN de 35 mm; "
                    "(2) la numeración impresa junto a cada tornillo es la MISMA del símbolo "
                    "(1-2, 3-4, 5-6); (3) el diferencial se reconoce por el botón de prueba T, que "
                    "debe probarse periódicamente; (4) el fusible es un cartucho que se cambia "
                    "abriendo el portafusible SIN tensión.")
image(s, "a_protecciones", 0.6, 1.45, 8.3, 4.6)
card(s, 9.15, 1.6, 3.6, 4.3, "Cómo reconocerlos", [
    "Termomagnético: palanca y curva/corriente (C16)",
    "Diferencial: botón T y IΔn 30 mA",
    "Portafusible: tapa abatible con el cartucho gG",
    "Bornes numerados igual que el símbolo"], fill=GTINT, head_color=DGREEN, size=13)

s = d.content("¿Dónde está cada protección en un arranque directo?",
              notes="(5 min) Recorrer el esquema de fuerza de arriba hacia abajo: Q1 protege la línea "
                    "y permite seccionar; KM1 es el que maniobra (no protege); F1 protege el motor "
                    "contra sobrecarga y, a través de su contacto 95-96, corta el MANDO; F2 protege "
                    "el circuito de mando. El diferencial suele estar aguas arriba, en el tablero "
                    "general.")
image(s, "f_arranque_directo", 0.6, 1.45, 4.6, 4.6)
for i, (tag, h, b) in enumerate([("Q1", "Interruptor", "Protege la línea (cortocircuito) y secciona"),
                                 ("KM1", "Contactor", "Maniobra el motor; no protege"),
                                 ("F1", "Relé térmico", "Sobrecarga del motor → abre 95-96 en el mando"),
                                 ("F2", "Fusible de mando", "Protege el circuito de mando"),
                                 ("IΔn", "Diferencial", "Aguas arriba: protege a las personas")]):
    y = 1.55 + i * 0.88
    box(s, 5.6, y, 7.15, 0.78, fill=TINT if i % 2 == 0 else GTINT)
    text(s, 5.75, y + 0.08, 1.0, 0.6, [tag], size=17, bold=True, color=RED, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 6.8, y + 0.08, 2.2, 0.6, [h], size=15, bold=True, color=NAVY, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 9.0, y + 0.08, 3.7, 0.65, [b], size=13, anchor=MSO_ANCHOR.MIDDLE)

s = d.content("Las cinco reglas de oro",
              notes="(5 min) Antes de intervenir un tablero o un motor, SIEMPRE en este orden. En el "
                    "laboratorio físico se aplican; en CADe_SIMU no hay riesgo, pero conviene "
                    "nombrarlas al detener la simulación.")
for i, (h, b) in enumerate([("Cortar", "Abrir todas las fuentes de tensión (visible)."),
                            ("Bloquear", "Candado y tarjeta: que nadie reconecte."),
                            ("Verificar", "Comprobar ausencia de tensión con el instrumento adecuado."),
                            ("Poner a tierra", "Puesta a tierra y en cortocircuito de los conductores."),
                            ("Señalizar", "Delimitar y señalizar la zona de trabajo.")]):
    x = 0.6 + i * 2.45
    box(s, x, 1.7, 2.25, 3.6, fill=TINT if i % 2 == 0 else GTINT)
    circle_num(s, x + 0.82, 1.9, 0.62, str(i + 1))
    text(s, x + 0.1, 2.7, 2.05, 0.5, [h], size=17, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
    text(s, x + 0.15, 3.3, 1.95, 1.9, [b], size=14, align=PP_ALIGN.CENTER)

s = d.content("Bloquear y verificar: lo que se usa",
              notes="(2 min) Reglas 2 y 3 en concreto. Cada persona que interviene pone SU candado "
                    "(con un pasador múltiple si son varias) y su tarjeta con nombre y fecha; nadie "
                    "retira el candado de otro. Antes de tocar, verificar ausencia de tensión con "
                    "un detector bipolar, probándolo antes y después en una fuente conocida.")
image(s, "a_consignacion", 0.6, 1.45, 7.6, 4.6)
card(s, 8.45, 1.6, 4.3, 4.3, "Consignación", [
    "Un candado por persona; la llave la guarda quien trabaja",
    "Tarjeta con nombre, fecha y motivo",
    "Detector: probarlo antes y después en una fuente conocida",
    "Medir entre fases y entre fase y tierra"], size=14)

s = d.content("En la realidad: protecciones y bloqueo",
              notes="(2 min) Fotos reales. Diferencial: se ven el botón TEST, la palanca azul, la "
                    "sensibilidad 0,03 A (30 mA) y el pequeño esquema impreso en el frente. "
                    "Termomagnético: palanca y la curva/corriente impresa (C10). Bloqueo: dispositivo "
                    "rojo de consignación con varios candados personales colgando — uno por cada "
                    "persona que trabaja en la máquina.")
ph = [k for k in ("diferencial", "termomagnetico", "bloqueo") if k in fotos.FOTOS]
caps = {"diferencial": "Diferencial 2P, 30 mA", "termomagnetico": "Termomagnético en riel DIN",
        "bloqueo": "Bloqueo con candados personales"}
wcol = 12.15 / len(ph)
for i, k in enumerate(ph):
    foto(s, k, 0.6 + i * wcol, 1.45, wcol - 0.15, 4.75, caps[k])

s = d.content("Buenas prácticas en el tablero",
              notes="(5 min) Colores según IEC 60204-1 (seguridad de máquinas) y colores de "
                    "conductores según IEC 60445. Tensión de mando reducida: 24 V es más segura; en "
                    "el laboratorio usaremos 220 V de mando (fase-neutro) porque es lo común en "
                    "tableros sencillos y así se ve en CADe_SIMU.")
table(s, 0.6, 1.6, 6.3, [
    ["Elemento", "Color"],
    ["Pulsador de marcha", "Blanco (preferido), gris, negro o verde"],
    ["Pulsador de paro", "Negro (preferido), gris, blanco o rojo"],
    ["Parada de emergencia", "Rojo sobre fondo amarillo"],
    ["Piloto de falla", "Rojo"],
    ["Piloto de funcionamiento normal", "Verde"],
], [2.9, 3.4], size=13, row_h=0.55)
caption(s, 0.6, 5.0, 6.3, "IEC 60204-1 (equipamiento eléctrico de máquinas)", size=11)
card(s, 7.2, 1.6, 5.55, 4.3, "En el tablero", [
    "PE verde-amarillo; neutro azul (IEC 60445)",
    "Mando a tensión reducida (24 V) o protegido con fusible propio (F2)",
    "Contacto del térmico (95-96) siempre en serie con el mando",
    "Paros en serie, marchas en paralelo"], fill=GTINT, head_color=DGREEN, size=15)

# ----------------------------------------------------- 2 · representación
d.section("2", "Cómo se representa", "Fuerza y mando, símbolos, designaciones y bornes",
          notes="Bloque de 25 min. Puente con la semana anterior: igual que en neumática, primero "
                "aprendemos a LEER el símbolo y luego a armar el circuito.")

s = d.content("Dos esquemas para una misma máquina",
              notes="(5 min) El esquema de FUERZA lleva la energía al motor (380 V, corrientes "
                    "altas, trazo grueso). El de MANDO decide cuándo se energiza la bobina del "
                    "contactor (220 V o 24 V, corrientes pequeñas). Se unen a través del contactor: "
                    "su bobina está en el mando y sus contactos principales en la fuerza. En el "
                    "esquema desarrollado cada aparato aparece 'desarmado' en los dos esquemas con el "
                    "mismo nombre (KM1).")
image(s, "f_arranque_directo", 0.6, 1.45, 3.9, 4.0)
caption(s, 0.6, 5.5, 3.9, "Fuerza: lleva la energía al motor", size=13, color=INK)
image(s, "m_marcha_paro", 4.7, 1.45, 4.5, 4.0)
caption(s, 4.7, 5.5, 4.5, "Mando: decide cuándo se energiza KM1", size=13, color=INK)
card(s, 9.45, 1.6, 3.3, 4.3, "Esquema desarrollado", [
    "Cada aparato se reparte entre los dos esquemas",
    "Se reconoce por su nombre: KM1",
    "Todo se dibuja en reposo"], size=14)

s = d.content("El mismo arranque, en un tablero real",
              notes="(3 min) Este es el tablero del ejercicio L1 (arranque directo). Arriba Q1 y el "
                    "fusible de mando F2; al centro el contactor KM1 con el térmico F1 enchufado "
                    "debajo; abajo la bornera X1 (salidas al motor y a la puerta, con bornes PE "
                    "verde-amarillo). Los pulsadores y pilotos van en la PUERTA y llegan con una "
                    "manguera flexible. La etiqueta del aparato en el tablero es la misma que en "
                    "el esquema: así se encuentra un aparato al revisar una falla.")
image(s, "a_tablero", 0.6, 1.4, 6.3, 4.75)
card(s, 7.15, 1.6, 5.6, 4.3, "Del esquema al tablero", [
    [("Placa de montaje: ", {"bold": True}), ("Q1, F2, KM1, F1 y bornera X1 sobre riel DIN", {})],
    [("Canaletas: ", {"bold": True}), ("ocultan y ordenan los cables", {})],
    [("Puerta: ", {"bold": True}), ("S0, S1, H1, H2 (mando y señalización)", {})],
    [("Etiquetas: ", {"bold": True}), ("las mismas designaciones que el esquema", {})]],
     fill=GTINT, head_color=DGREEN, size=14)

s = d.content("Designación de los aparatos",
              notes="(4 min) Usamos la designación clásica que emplean CADe_SIMU y la mayoría de "
                    "catálogos en la región. Mencionar que la norma vigente (IEC 81346-2) agrupa por "
                    "función: el contactor de potencia también se designa Q y los pulsadores S, por "
                    "ejemplo. Lo importante es ser consistente en todo el esquema.")
table(s, 0.6, 1.6, 7.6, [
    ["Letra", "Aparato", "Ejemplo"],
    ["Q", "Interruptor, seccionador, diferencial", "Q1"],
    ["KM", "Contactor (potencia)", "KM1, KM2"],
    ["KA / KT", "Relé auxiliar / temporizador", "KA1, KT"],
    ["F", "Fusible, relé térmico", "F1, F2"],
    ["S", "Pulsador, interruptor, final de carrera", "S0, S1"],
    ["H", "Señalización (piloto)", "H1, H2"],
    ["M", "Motor", "M1"],
], [1.3, 4.3, 2.0], size=14, row_h=0.52)
card(s, 8.5, 1.6, 4.25, 4.3, "Regla", [
    "Mismo nombre en fuerza y en mando",
    "Numerar en orden: S0 paro, S1, S2 marchas",
    "IEC 81346-2 (vigente) agrupa por función; se ve en catálogos nuevos"], fill=GTINT,
     head_color=DGREEN, size=14)

s = d.content("Numeración de bornes: el número dice qué contacto es",
              notes="(5 min) Ejercicio rápido: mostrar un contacto 23-24 y preguntar qué es "
                    "(2.º contacto, normalmente abierto). Primer dígito = número de orden; segundo "
                    "dígito: 1-2 NC, 3-4 NA. Funciones especiales: 5-6 NC y 7-8 NA "
                    "(temporizados, térmico). La numeración de temporizadores varía algo entre "
                    "fabricantes; en este curso usamos 55-56 (NC temporizado) y 67-68 (NA "
                    "temporizado).")
table(s, 0.6, 1.6, 7.7, [
    ["Bornes", "Significado"],
    ["A1 – A2", "Bobina"],
    ["1-2, 3-4, 5-6", "Contactos principales (fuerza)"],
    ["13-14, 43-44", "Auxiliar NA (2.º dígito 3-4)"],
    ["11-12, 21-22", "Auxiliar NC (2.º dígito 1-2)"],
    ["95-96 / 97-98", "Relé térmico: NC / NA"],
    ["55-56 / 67-68", "Temporizado: NC / NA"],
    ["U1 V1 W1 / U2 V2 W2", "Bornes del motor"],
], [2.6, 5.1], size=14, row_h=0.52)
for i, (img, cap) in enumerate([("sym_na", "NA 13-14"), ("sym_nc", "NC 21-22"),
                                ("sym_termico_95", "Térmico 95-96"), ("sym_temp_na", "Temporizado 67-68")]):
    x = 8.6 + (i % 2) * 2.1
    y = 1.6 + (i // 2) * 2.2
    image(s, img, x, y, 2.0, 1.6)
    caption(s, x, y + 1.6, 2.0, cap, size=12, color=INK)

s = d.content("Los números están impresos en el aparato",
              notes="(3 min) El contactor muestra arriba A1 y las entradas 1/L1, 3/L2, 5/L3; abajo "
                    "A2 y las salidas 2/T1, 4/T2, 6/T3. Su contacto auxiliar NA trae 13-14. El relé "
                    "térmico se enchufa directamente en 2/T1, 4/T2, 6/T3 y repite esas salidas para "
                    "el motor; a un costado tiene 95-96 (NC, va al mando) y 97-98 (NA, piloto de "
                    "falla), el dial para ajustar la corriente del motor y el botón azul de rearme. "
                    "Pedir a los alumnos que señalen en el esquema de L1 dónde va cada borne.")
image(s, "a_contactor_termico", 0.6, 1.4, 5.6, 4.75)
for i, (img, cap) in enumerate([("sym_bobina", "Bobina A1-A2"), ("sym_contactor_3p", "Principales 1-2, 3-4, 5-6"),
                                ("sym_na", "Auxiliar NA 13-14"), ("sym_termico_3p", "Térmico (fuerza)"),
                                ("sym_termico_95", "Térmico 95-96"), ("sym_termico_97", "Térmico 97-98")]):
    x = 6.55 + (i % 3) * 2.1
    y = 1.5 + (i // 3) * 2.3
    box(s, x, y, 1.95, 2.15, fill=TINT)
    image(s, img, x + 0.1, y + 0.1, 1.75, 1.5)
    caption(s, x, y + 1.65, 1.95, cap, size=11, color=INK)

s = d.content("El contactor real, por fuera y por dentro",
              notes="(3 min) Izquierda: un contactor comercial; se leen A1 y A2 arriba, 1 L1, 3 L2, "
                    "5 L3 y 13 en la entrada; 2 T1, 4 T2, 6 T3 y 14 en la salida. Derecha: el mismo "
                    "tipo de aparato desarmado. Al energizar la BOBINA, la culata se imanta y atrae la "
                    "ARMADURA MÓVIL, que arrastra a todos los contactos móviles a la vez: los NA cierran "
                    "y los NC abren. Al cortar la corriente, el MUELLE DE RETORNO los devuelve al "
                    "reposo. Por eso en el esquema todos los contactos de KM1 se mueven juntos.")
foto(s, "contactor", 0.6, 1.4, 4.0, 4.8, "Bornes impresos: A1-A2, 1-2, 3-4, 5-6, 13-14")
foto(s, "despiece", 4.8, 1.4, 7.95, 3.95, "Despiece: bobina, culata, armadura móvil, muelle y contactos")
box(s, 4.8, 5.4, 7.95, 0.8, fill=GTINT)
text(s, 4.95, 5.42, 7.7, 0.75, [[("Bobina energizada → ", {"bold": True, "color": DGREEN}),
                                 ("la armadura cierra y mueve TODOS los contactos a la vez; el muelle los "
                                  "devuelve al reposo.", {})]], size=13, anchor=MSO_ANCHOR.MIDDLE)

s = d.content("Símbolos que usaremos (IEC 60617)",
              notes="(2 min) Repasar rápido; el catálogo completo está en la guía del alumno y en el "
                    "solucionario. Énfasis: el contacto NA se dibuja abierto y el NC cerrado porque "
                    "el esquema está en REPOSO.")
syms = [("sym_na", "Contacto NA"), ("sym_nc", "Contacto NC"), ("sym_pulsador_na", "Pulsador NA"),
        ("sym_pulsador_nc", "Pulsador NC"), ("sym_bobina", "Bobina"), ("sym_bobina_temp", "Bobina temporizada"),
        ("sym_contactor_3p", "Contactor 3P"), ("sym_interruptor_3p", "Interruptor 3P"),
        ("sym_termico_3p", "Relé térmico"), ("sym_piloto", "Piloto"), ("sym_fusible", "Fusible"),
        ("sym_motor", "Motor 3~")]
for i, (img, cap) in enumerate(syms):
    col, row = i % 6, i // 6
    x, y = 0.6 + col * 2.03, 1.55 + row * 2.25
    box(s, x, y, 1.9, 2.1, fill=TINT)
    image(s, img, x + 0.1, y + 0.1, 1.7, 1.45)
    caption(s, x, y + 1.6, 1.9, cap, size=12, color=INK)

s = d.content("Mando en la puerta: pulsadores, pilotos y temporizador",
              notes="(2 min) Cada pulsador es un cabezal de 22 mm más un BLOQUE de contactos que se "
                    "monta detrás: el bloque define si es NA (13-14) o NC (11-12), no el color. La "
                    "parada de emergencia es una seta roja sobre fondo amarillo con bloque NC y "
                    "enclavamiento. El piloto lleva un portalámpara X1-X2. El temporizador se monta "
                    "en el riel y se ajusta con su dial; la numeración de sus contactos varía según "
                    "el fabricante (en el curso: 55-56 y 67-68).")
image(s, "a_mando", 0.6, 1.5, 12.15, 3.75)
for i, (h, b) in enumerate([("Pulsador", "Cabezal + bloque NA o NC"),
                            ("Emergencia", "Seta roja, fondo amarillo, NC"),
                            ("Piloto", "Lámpara X1-X2: verde marcha, rojo falla"),
                            ("Temporizador", "Dial de tiempo; bobina A1-A2")]):
    x = 0.6 + i * 3.06
    box(s, x, 5.4, 2.9, 0.75, fill=TINT if i % 2 == 0 else GTINT)
    text(s, x + 0.1, 5.42, 2.7, 0.7, [[(h + ": ", {"bold": True, "color": NAVY}), (b, {})]], size=12,
         anchor=MSO_ANCHOR.MIDDLE)

s = d.content("En la realidad: puerta de mando y motor",
              notes="(2 min) Izquierda: panel de mando de una máquina con la parada de emergencia "
                    "(seta roja sobre fondo amarillo), pulsadores, un piloto y un selector. Derecha: "
                    "motor asíncrono trifásico; arriba se ve la caja de bornes, donde están U1 V1 W1 / "
                    "U2 V2 W2 y los puentes estrella o triángulo.")
foto(s, "emergencia", 0.6, 1.45, 6.0, 4.75, "Parada de emergencia, pulsadores y piloto")
foto(s, "motor", 6.75, 1.45, 6.0, 4.75, "Motor trifásico con su caja de bornes")

# --------------------------------------------------------- 3 · circuitos
d.section("3", "Circuitos de mando y fuerza", "Marcha-paro, dos puntos, inversión y estrella-triángulo",
          notes="Bloque de 45 min. Cada circuito es la base de un ejercicio del laboratorio.")

s = d.content("Marcha-paro con autorretención",
              notes="(8 min) Seguir la corriente: S1 cierra → bobina KM1 → KM1 cierra 13-14 en "
                    "paralelo con S1 → al soltar S1 la bobina sigue alimentada (autorretención). S0 "
                    "(NC) corta y todo vuelve a reposo. Si el térmico dispara, 95-96 abre (para) y "
                    "97-98 cierra (enciende H2). Paralelo con la neumática: la autorretención es la "
                    "'memoria', como la 5/2 biestable.")
image(s, "m_marcha_paro", 0.6, 1.45, 5.6, 4.6)
for i, (h, b) in enumerate([("1  Marcha", "Pulso en S1 → KM1 se energiza"),
                            ("2  Autorretención", "KM1 13-14 mantiene la bobina aunque sueltes S1"),
                            ("3  Paro", "S0 (NC) abre el circuito"),
                            ("4  Sobrecarga", "F1 95-96 abre; 97-98 enciende H2")]):
    y = 1.55 + i * 1.12
    box(s, 6.5, y, 6.25, 1.0, fill=TINT if i % 2 == 0 else GTINT)
    text(s, 6.7, y + 0.08, 2.5, 0.85, [h], size=16, bold=True, color=NAVY, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 9.2, y + 0.08, 3.5, 0.85, [b], size=14, anchor=MSO_ANCHOR.MIDDLE)

s = d.content("Mando desde dos puntos",
              notes="(5 min) Misma lógica que la O y la Y de neumática: cualquier marcha arranca "
                    "(paralelo = O); cualquier paro detiene (serie = Y de condiciones para seguir "
                    "funcionando). Pregunta: ¿qué pasaría si pongo los paros en paralelo?")
image(s, "m_dos_puntos", 0.6, 1.45, 7.2, 4.6)
card(s, 8.1, 1.6, 4.65, 4.3, "Regla", [
    "Paros (NC) en SERIE: cualquiera detiene",
    "Marchas (NA) en PARALELO: cualquiera arranca",
    "Es la O y la Y de la neumática, ahora con contactos"], fill=GTINT, head_color=DGREEN, size=15)

s = d.content("Inversión de giro: fuerza",
              notes="(5 min) Para invertir el giro de un motor trifásico se intercambian dos fases. "
                    "KM1 entrega L1-L2-L3; KM2 entrega L3-L2-L1. Si KM1 y KM2 cierran a la vez → "
                    "CORTOCIRCUITO entre L1 y L3. Por eso el enclavamiento es obligatorio.")
image(s, "f_inversion", 0.6, 1.45, 6.0, 4.6)
card(s, 6.9, 1.6, 5.85, 4.3, "Idea clave", [
    "Invertir dos fases invierte el giro",
    "KM1: L1-L2-L3 → giro horario",
    "KM2: L3-L2-L1 → giro antihorario",
    [("KM1 y KM2 juntos = cortocircuito", {"bold": True, "color": RED})]], size=15)

s = d.content("Inversión de giro: mando con enclavamiento",
              notes="(6 min) Enclavamiento eléctrico: el NC de KM2 (21-22) en serie con la bobina de "
                    "KM1, y viceversa. Si KM1 está energizado, su 21-22 abre y KM2 no puede entrar. "
                    "Mencionar también el enclavamiento por pulsadores (pulsadores dobles) y el "
                    "mecánico entre contactores en la práctica real. Para cambiar de sentido: pasar "
                    "por S0.")
image(s, "m_inversion", 0.6, 1.45, 6.0, 4.6)
card(s, 6.9, 1.6, 5.85, 4.3, "Enclavamiento eléctrico", [
    "NC de KM2 en serie con la bobina KM1",
    "NC de KM1 en serie con la bobina KM2",
    "Nunca pueden estar los dos energizados",
    "Para invertir: S0 y luego la otra marcha"], fill=GTINT, head_color=DGREEN, size=15)

s = d.content("Estrella-triángulo: por qué y cómo se conecta",
              notes="(5 min) En arranque directo la corriente de arranque es varias veces la "
                    "nominal. En estrella cada bobina recibe U/√3: la corriente y el par de arranque "
                    "bajan a aproximadamente 1/3. Luego se pasa a triángulo (tensión plena). "
                    "Requisito: el motor debe estar diseñado para trabajar en triángulo a la tensión "
                    "de la red (p. ej. 380 V Δ).")
image(s, "t_placa_bornes", 0.6, 1.6, 7.2, 3.2)
card(s, 8.1, 1.6, 4.65, 4.3, "Idea clave", [
    "Estrella: U fase = U línea/√3 → ~1/3 de la corriente de arranque",
    "Luego triángulo: tensión plena",
    "Motor apto para Δ a la tensión de red"], size=15)
text(s, 0.6, 5.0, 7.2, 0.9, ["Seis bornes: U1 V1 W1 (inicio) y U2 V2 W2 (final de cada bobina). "
                             "Los puentes definen la conexión."], size=14, color=MUTED)

s = d.content("La caja de bornes del motor",
              notes="(2 min) Al abrir la caja de bornes se ven los seis espárragos y unas plaquitas "
                    "metálicas (puentes). Con dos puentes horizontales el motor queda en estrella; "
                    "con tres verticales, en triángulo. En el arranque estrella-triángulo se QUITAN "
                    "los puentes: los contactores KM2 y KM3 hacen ese trabajo, por eso llegan seis "
                    "cables al motor. Leer la placa de características: p. ej. 380 V Δ / 660 V Y "
                    "indica que en una red de 380 V el motor trabaja en triángulo.")
image(s, "a_motor_bornes", 0.6, 1.45, 12.15, 3.9)
text(s, 0.6, 5.45, 12.15, 0.7, [[("Arranque Y-Δ: ", {"bold": True, "color": NAVY}),
                                ("se retiran los puentes y llegan 6 cables; KM2 hace la estrella y KM3 "
                                 "el triángulo.", {})]], size=14, align=PP_ALIGN.CENTER)

s = d.content("Estrella-triángulo: fuerza",
              notes="(5 min) KM1 (línea) alimenta U1 V1 W1. KM2 une W2-U2-V2 (punto estrella). KM3 "
                    "une U1-W2, V1-U2, W1-V2 (triángulo). KM2 y KM3 nunca juntos: sería un "
                    "cortocircuito.")
image(s, "f_estrella_triangulo", 0.6, 1.4, 5.2, 4.7)
table(s, 6.2, 1.7, 6.55, [["Etapa", "KM1", "KM2 (Y)", "KM3 (Δ)"],
                          ["Arranque", "●", "●", "—"],
                          ["Tras el tiempo t", "●", "—", "●"],
                          ["Paro / térmico", "—", "—", "—"]], [2.45, 1.3, 1.4, 1.4], size=15,
      row_h=0.6)
text(s, 6.2, 4.4, 6.55, 1.4, [[("KM2 y KM3 nunca a la vez: ", {"bold": True, "color": RED}),
                               ("enclavamiento eléctrico entre ellos.", {})]], size=15)

s = d.content("Estrella-triángulo: mando temporizado",
              notes="(6 min) S1 energiza KM1, KT y (a través de KT 55-56 y KM3 21-22) KM2: arranque "
                    "en estrella. Al cumplirse t, KT 55-56 abre (sale KM2) y KT 67-68 cierra (entra "
                    "KM3 si KM2 ya soltó, por su 21-22). Resultado: triángulo. S0 o F1 paran todo.")
image(s, "m_estrella_triangulo", 0.6, 1.4, 6.6, 4.7)
for i, (h, b) in enumerate([("S1", "KM1 + KT + KM2 → estrella"),
                            ("t cumplido", "KT 55-56 abre → sale KM2"),
                            ("", "KT 67-68 cierra → entra KM3 → triángulo"),
                            ("S0 / F1", "Todo vuelve a reposo")]):
    y = 1.55 + i * 1.12
    box(s, 7.5, y, 5.25, 1.0, fill=TINT if i % 2 == 0 else GTINT)
    text(s, 7.65, y + 0.08, 1.6, 0.85, [h], size=15, bold=True, color=NAVY, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 9.25, y + 0.08, 3.45, 0.85, [b], size=14, anchor=MSO_ANCHOR.MIDDLE)

# -------------------------------------------------------------- cierre
s = d.content("Del enunciado al esquema: metodología",
              notes="(5 min) Receta para el laboratorio. Es la misma lógica que en neumática: "
                    "primero qué debe pasar, luego qué aparato lo hace, luego dibujar en reposo y "
                    "simular.")
for i, (h, b) in enumerate([("Leer", "Qué debe hacer la máquina, condiciones de seguridad."),
                            ("Fuerza", "Protección, contactores, térmico, motor."),
                            ("Mando", "Protecciones en serie, paros, marchas, bobinas."),
                            ("Memorias y enclavamientos", "Autorretenciones, NC cruzados, temporizadores."),
                            ("Designar y numerar", "Mismo nombre en fuerza y mando; bornes."),
                            ("Simular", "Verificar cada estado y provocar fallas (térmico).")]):
    col, row = i % 3, i // 3
    x, y = 0.6 + col * 4.1, 1.6 + row * 2.2
    box(s, x, y, 3.85, 2.0, fill=TINT if row == 0 else GTINT)
    circle_num(s, x + 0.2, y + 0.2, 0.5, str(i + 1), size=14)
    text(s, x + 0.85, y + 0.2, 2.9, 0.5, [h], size=16, bold=True, color=NAVY)
    text(s, x + 0.2, y + 0.85, 3.5, 1.1, [b], size=15)

s = d.content("Resumen y laboratorio",
              notes="(3 min) Cierre y presentación del laboratorio.")
card(s, 0.6, 1.6, 5.9, 4.3, "Hoy aprendimos", [
    "El daño depende de la corriente y del tiempo",
    "Directo / indirecto; diferencial y puesta a tierra",
    "Fuerza y mando; designaciones y bornes",
    "Autorretención, enclavamiento y temporizador"])
card(s, 6.8, 1.6, 5.95, 4.3, "Laboratorio CADe_SIMU (3 h)", [
    "Interfaz y primer circuito",
    "Marcha-paro con pilotos y térmico",
    "Dos puntos de mando e inversión de giro",
    "Estrella-triángulo y reto secuencial"], fill=GTINT, head_color=DGREEN)

s = d.content("Créditos de las fotografías",
              notes="Las fotos tienen licencias libres de Wikimedia Commons; las CC BY-SA exigen "
                    "citar autor y licencia. Las ilustraciones y esquemas son propios del curso.")
rows = [["Foto", "Autor", "Licencia", "Fuente (Wikimedia Commons)"]]
for k, (f, t, a, lic) in fotos.FOTOS.items():
    rows.append([t, a, lic, fotos.url(k).replace("https://", "")])
table(s, 0.6, 1.5, 12.15, rows, [3.3, 1.9, 1.4, 5.55], size=10, row_h=0.42)

d.cover()
os.makedirs(os.path.dirname(OUT), exist_ok=True)
d.save(OUT)
print("ok", OUT, len(d.prs.slides))
