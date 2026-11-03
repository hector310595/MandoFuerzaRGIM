"""Genera guía del alumno, solucionario, guía paso a paso de CADe_SIMU y plan de sesiones.
Uso: python3 src/build_docs.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from catalogo_elec import CATALOGO, ORDEN  # noqa: E402
from docx_utils import (MUTED, NAVY, RED, ROOT, answer_box, bullets, callout, figure,  # noqa: E402
                        image_table, new_doc, numbered, page_break, para, table)
from ejercicios import EJ, TENSION  # noqa: E402

KICK = "REPRESENTACIÓN GRÁFICA PARA INGENIERÍA MECATRÓNICA"
KICK_D = KICK + " · USO DOCENTE"
D_LAB = os.path.join(ROOT, "sesion2_laboratorio")
D_DOC = os.path.join(ROOT, "docente")
for p in (D_LAB, D_DOC):
    os.makedirs(p, exist_ok=True)

DESIGNACIONES = [["Letra", "Aparato", "Ejemplo"],
                 ["Q", "Interruptor, seccionador, diferencial", "Q1"],
                 ["KM", "Contactor", "KM1"], ["KA / KT", "Relé auxiliar / temporizador", "KT"],
                 ["F", "Fusible, relé térmico", "F1, F2"], ["S", "Pulsador", "S0, S1"],
                 ["H", "Piloto", "H1"], ["M", "Motor", "M1"]]
BORNES = [["Bornes", "Significado"], ["A1 – A2", "Bobina"],
          ["1-2, 3-4, 5-6", "Contactos principales"], ["13-14, 43-44", "Auxiliar NA"],
          ["11-12, 21-22", "Auxiliar NC"], ["95-96 / 97-98", "Térmico NC / NA"],
          ["55-56 / 67-68", "Temporizado NC / NA"], ["U1 V1 W1 / U2 V2 W2", "Motor"]]

CADESIMU_BASE = [
    ("Instalar y abrir", "CADe_SIMU es gratuito para Windows. Abre un archivo nuevo."),
    ("Alimentación", "Desde la biblioteca de alimentaciones coloca la trifásica (L1, L2, L3) para la "
                     "fuerza y una monofásica (L1, N) para el mando."),
    ("Colocar componentes", "Arrastra protecciones, contactores, relé térmico, motor, pulsadores, "
                            "temporizador y pilotos desde sus bibliotecas. Dibuja la fuerza a la "
                            "izquierda y el mando a la derecha."),
    ("Cablear", "Usa la herramienta de cable para unir bornes. Revisa que cada unión quede hecha; un "
                "cable que solo «pasa por encima» no conecta."),
    ("Nombrar", "Doble clic en cada aparato y escribe su nombre. La bobina KM1 y TODOS sus contactos "
                "(principales y auxiliares) deben llamarse exactamente KM1. Lo mismo F1 (térmico) "
                "y KT (temporizador)."),
    ("Ajustar", "En el temporizador escribe el tiempo (p. ej. 5 s) en su diálogo."),
    ("Simular", "Activa la simulación. Haz clic sobre los pulsadores para accionarlos. Para simular "
                "una sobrecarga, haz clic sobre el relé térmico durante la simulación."),
    ("Detener y editar", "Para modificar el esquema, detén primero la simulación."),
    ("Guardar", "Guarda con el nombre del ejercicio (p. ej. L1_marcha_paro) en la carpeta cadesimu/."),
]
PROBLEMAS = [["Síntoma", "Causa probable", "Solución"],
             ["Un contacto nunca cambia", "Nombre distinto al de su bobina", "Mismo nombre exacto"],
             ["El motor se para al soltar S1", "Falta la autorretención o está en serie",
              "KM1 13-14 en paralelo con S1"],
             ["El térmico dispara y el motor sigue", "95-96 no está en el mando", "95-96 en serie"],
             ["Aviso de cortocircuito", "Dos contactores que no deben cerrar juntos",
              "Enclavamiento con NC cruzados"],
             ["Nada funciona", "Falta alimentación o fusible abierto", "Revisa L1/N y F2"],
             ["No puedo editar", "Simulación en marcha", "Detén la simulación"]]


def catalogo(doc, titulo="Catálogo de símbolos (IEC 60617)"):
    doc.add_heading(titulo, 1)
    para(doc, "Todo se dibuja en REPOSO: sin tensión y sin accionar. Por eso un contacto NA aparece "
              "abierto y uno NC cerrado.")
    rows = []
    for k in ORDEN:
        c = CATALOGO[k]
        rows.append([c["img"], [(c["nombre"], {"bold": True, "color": NAVY}),
                                ("\n" + c["designacion"], {})], c["reconocer"], c["funcion"]])
    image_table(doc, ["Símbolo", "Nombre y designación", "Cómo reconocerlo", "Para qué sirve"], rows,
                [3.0, 4.2, 5.6, 4.2], img_w_cm=2.6)


# =================================================================== guía del alumno
def guia():
    doc = new_doc("Guía de laboratorio", "Esquemas de mando y fuerza en CADe_SIMU · 3 h", kicker=KICK)
    doc.add_heading("1. Objetivos y entregables", 1)
    bullets(doc, ["Dibujar esquemas de fuerza y de mando con símbolos IEC 60617.",
                  "Usar designaciones y numeración de bornes correctas.",
                  "Construir autorretenciones, enclavamientos y temporizaciones.",
                  "Simular y diagnosticar fallas en CADe_SIMU."])
    para(doc, [("Entregable por ejercicio: ", {"bold": True, "color": NAVY}),
               ("archivo de CADe_SIMU, captura de la simulación y respuestas a las preguntas guía.", {})])
    callout(doc, "Seguridad:", "aunque hoy trabajamos en simulador, en un tablero real se aplican las "
                               "cinco reglas de oro: cortar, bloquear, verificar ausencia de tensión, "
                               "poner a tierra y señalizar.", fill="FFF4E5", color=RED)
    doc.add_heading("2. Repaso express", 1)
    para(doc, TENSION)
    doc.add_heading("Designaciones", 3)
    table(doc, DESIGNACIONES, [2.0, 10.0, 5.0])
    doc.add_heading("Numeración de bornes", 3)
    table(doc, BORNES, [5.0, 12.0])
    catalogo(doc, "3. Símbolos que usarás")
    doc.add_heading("4. CADe_SIMU en 15 minutos", 1)
    para(doc, [("Los nombres de menús pueden variar levemente entre versiones.",
                {"italic": True, "color": MUTED})], size=9)
    numbered(doc, ["%s: %s" % (h, b) for h, b in CADESIMU_BASE])
    page_break(doc)
    doc.add_heading("5. Ejercicios", 1)
    for e in EJ:
        doc.add_heading(e["titulo"] + "  (%d min)" % e["minutos"], 2)
        para(doc, e["enunciado"])
        doc.add_heading("Preguntas guía", 3)
        numbered(doc, e["preguntas"])
        answer_box(doc, "Esquema de fuerza / mando (borrador) y respuestas", 6)
    doc.add_heading("6. Lista de verificación", 1)
    table(doc, [["✓", "Criterio"]] + [["☐", c] for c in [
        "Fuerza y mando dibujados por separado",
        "Todo en reposo: NA abiertos, NC cerrados",
        "Mismo nombre en la bobina y en todos sus contactos",
        "Bornes numerados (A1-A2, 13-14, 95-96…)",
        "Protecciones: Q1, F1 (95-96 en serie con el mando), F2",
        "Autorretención y enclavamientos correctos",
        "Simulación verificada estado por estado",
        "Sobrecarga simulada: el motor se detiene"]], [1.2, 15.8])
    path = os.path.join(D_LAB, "RGIM_Guia_Laboratorio_Alumno.docx")
    doc.save(path)
    return path


# =================================================================== solucionario
def solucionario():
    doc = new_doc("Solucionario docente", "Laboratorio de mando y fuerza en CADe_SIMU", kicker=KICK_D)
    para(doc, "Para cada ejercicio: esquemas de fuerza y mando, funcionamiento, tabla de estados, "
              "componentes a colocar en CADe_SIMU y errores típicos. " + TENSION)
    catalogo(doc, "0. Catálogo de símbolos (IEC 60617)")
    for e in EJ:
        page_break(doc)
        doc.add_heading(e["titulo"], 1)
        para(doc, [("Enunciado: ", {"bold": True, "color": NAVY}), (e["enunciado"], {})])
        if e["fuerza"]:
            t = doc.add_table(rows=1, cols=2)
            for i, (fig, w) in enumerate(((e["fuerza"], 6.4), (e["mando"], 9.6))):
                c = t.cell(0, i)
                c.paragraphs[0].add_run().add_picture(os.path.join(ROOT, "figuras", fig + ".png"),
                                                      width=__import__("docx").shared.Cm(w))
            para(doc, [("Izquierda: fuerza. Derecha: mando.", {"italic": True, "color": MUTED})], size=9)
        else:
            figure(doc, e["mando"], 6.0, "Esquema de mando")
        doc.add_heading("Funcionamiento", 3)
        bullets(doc, e["funcionamiento"])
        if e["estados"]:
            doc.add_heading("Tabla de estados (● = energizado)", 3)
            n = len(e["estados"][0])
            table(doc, e["estados"], [5.0] + [12.0 / (n - 1)] * (n - 1))
        doc.add_heading("Componentes en CADe_SIMU", 3)
        table(doc, [["Componente", "Nombre / bornes"]] + [list(c) for c in e["componentes"]], [8.0, 9.0])
        doc.add_heading("Errores típicos", 3)
        bullets(doc, e["errores"])
    path = os.path.join(D_DOC, "RGIM_Solucionario_Laboratorio.docx")
    doc.save(path)
    return path


# =================================================================== guía CADe_SIMU
TIPS = {
    "L0": ["Usa un pulsador NA; el piloto H1 es una lámpara de señalización."],
    "L1": ["Arma y prueba primero la FUERZA con el contactor forzado (o con la simulación del "
           "mando completo); luego el mando de arriba hacia abajo: F2 → F1 95-96 → S0 → (S1 ∥ KM1 13-14) "
           "→ bobina KM1.",
           "Los pilotos van en ramas aparte, entre L1 (después de F2) y N."],
    "L2": ["Parte del archivo de L1 (guárdalo con otro nombre) y agrega S01 en serie con S0 y S11 "
           "en paralelo con S1."],
    "L3": ["En la fuerza, KM2 recibe L1-L2-L3 y entrega L3-L2-L1: intercambia solo la primera y la "
           "tercera fase.",
           "Prueba a propósito quitar un enclavamiento para ver el aviso de cortocircuito; luego "
           "repónlo."],
    "L4": ["Usa un motor de 6 bornes. KM2 une W2-U2-V2; KM3 une U1-W2, V1-U2, W1-V2.",
           "Ajusta KT a 5 s. Observa que KM2 suelta antes de que entre KM3."],
    "L5": ["Copia la fuerza de L1 dos veces (Q1 común). Los dos contactos 95-96 van en serie al "
           "inicio del mando."],
}


def guia_cadesimu():
    doc = new_doc("Guía paso a paso en CADe_SIMU", "Cómo armar y simular cada ejercicio",
                  kicker=KICK_D)
    callout(doc, "Versión:", "pasos pensados para CADe_SIMU 4.x en Windows. Los nombres exactos de "
                             "bibliotecas y menús pueden variar levemente entre versiones.",
            fill="FFF4E5", color=RED)
    doc.add_heading("1. Procedimiento base", 1)
    numbered(doc, ["%s: %s" % (h, b) for h, b in CADESIMU_BASE])
    doc.add_heading("2. Problemas frecuentes", 1)
    table(doc, PROBLEMAS, [5.0, 6.0, 6.0])
    for e in EJ:
        page_break(doc)
        doc.add_heading(e["titulo"], 1)
        doc.add_heading("Paso 1 · Coloca y nombra", 2)
        table(doc, [["Componente", "Nombre / bornes"]] + [list(c) for c in e["componentes"]], [8.0, 9.0])
        doc.add_heading("Paso 2 · Arma y cablea", 2)
        bullets(doc, TIPS[e["key"]])
        if e["fuerza"]:
            figure(doc, e["fuerza"], 6.0, "Fuerza")
        figure(doc, e["mando"], 9.0 if e["fuerza"] else 5.5, "Mando")
        doc.add_heading("Paso 3 · Simula y comprueba", 2)
        if e["estados"]:
            table(doc, e["estados"], [5.0] + [12.0 / (len(e["estados"][0]) - 1)] * (len(e["estados"][0]) - 1))
        bullets(doc, e["funcionamiento"])
    path = os.path.join(D_DOC, "RGIM_Guia_CADeSIMU_Paso_a_Paso.docx")
    doc.save(path)
    return path


# =================================================================== plan
def plan():
    doc = new_doc("Plan de sesiones", "Seguridad eléctrica y esquemas de mando y fuerza · 2 h + 3 h",
                  kicker=KICK_D)
    doc.add_heading("Sesión 1 · Teoría (120 min)", 1)
    para(doc, "Archivo: sesion1_teoria/RGIM_S1_Seguridad_Mando_Fuerza_Teoria.pptx (27 diapositivas, "
              "notas del orador con tiempos).")
    table(doc, [["Min.", "Bloque", "Diapos.", "Contenido"],
                ["0–5", "Apertura", "1–3", "Objetivos y agenda"],
                ["5–45", "1 · Seguridad eléctrica", "4–11", "Corriente y tiempo, efectos (IEC 60479-1), "
                                                           "contacto directo/indirecto, protecciones, "
                                                           "reglas de oro, buenas prácticas"],
                ["45–70", "2 · Representación", "12–16", "Fuerza y mando, designaciones, bornes, símbolos"],
                ["70–115", "3 · Circuitos", "17–24", "Marcha-paro, dos puntos, inversión, estrella-triángulo"],
                ["115–120", "Cierre", "25–27", "Metodología y resumen"]], [1.7, 4.0, 1.8, 9.5])
    doc.add_heading("Sesión 2 · Laboratorio CADe_SIMU (180 min)", 1)
    para(doc, "Archivos: sesion2_laboratorio/RGIM_S2_Laboratorio_CADeSIMU.pptx (soluciones ocultas) y "
              "RGIM_Guia_Laboratorio_Alumno.docx.")
    rows = [["Min.", "Actividad"], ["0–15", "CADe_SIMU en 15 minutos (demo con L0)"]]
    t = 15
    for e in EJ:
        if e["key"] == "L4":
            rows.append(["%d–%d" % (t, t + 10), "Pausa"])
            t += 10
        rows.append(["%d–%d" % (t, t + e["minutos"]), e["titulo"]])
        t += e["minutos"]
    rows.append(["%d–180" % t, "Errores frecuentes y cierre"])
    table(doc, rows, [2.5, 14.5])
    doc.add_heading("Si falta tiempo", 3)
    bullets(doc, ["L5 queda como tarea.", "En L4, entregar el esquema de fuerza ya armado y que "
                                         "armen solo el mando."])
    doc.add_heading("Preparación previa", 1)
    bullets(doc, ["Verificar que CADe_SIMU esté instalado en las PC del laboratorio (Windows).",
                  "Probar los seis ejercicios con la guía paso a paso.",
                  "Comprobar que las diapositivas de solución sigan ocultas."])
    doc.add_heading("Evaluación sugerida", 1)
    para(doc, "Lista de verificación de la guía (8 criterios, 1 punto c/u) sobre L3 o L4, más 2 "
              "puntos por la simulación funcionando con sobrecarga simulada.")
    path = os.path.join(D_DOC, "RGIM_Plan_de_Sesiones.docx")
    doc.save(path)
    return path


if __name__ == "__main__":
    for f in (guia(), solucionario(), guia_cadesimu(), plan()):
        print("ok", f)
