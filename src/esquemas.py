"""Genera todos los esquemas eléctricos (PNG + SVG) en ../figuras/.

Uso:  python3 src/esquemas.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from simbolos_elec import GREEN, RED, Sheet  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..", "figuras")
os.makedirs(OUT, exist_ok=True)
NA, NC = "NO", "NC"
LAMP_G = "#bfe8cf"
LAMP_R = "#f5c6c0"
LAMP_Y = "#fbe7a8"


def out(name):
    return os.path.join(OUT, name)


# ================================================================= símbolos sueltos
def simbolos():
    def one(name, fn, w=3.4, h=2.0, x0=-2.0, y0=-1.5):
        s = Sheet(w, h, x0, y0)
        fn(s)
        s.save(out(name))

    one("sym_na", lambda s: s.contact(0.3, 0.25, NA, terms=("13", "14")))
    one("sym_nc", lambda s: s.contact(0.3, 0.25, NC, terms=("21", "22")))
    one("sym_pulsador_na", lambda s: s.contact(0.6, 0.25, NA, act="push", terms=("13", "14")))
    one("sym_pulsador_nc", lambda s: s.contact(0.6, 0.25, NC, act="push", terms=("11", "12")))
    one("sym_contacto_principal", lambda s: s.contact(0.3, 0.25, NA, main=True, terms=("1", "2")))
    one("sym_termico_95", lambda s: s.contact(0.7, 0.25, NC, act="thermal", terms=("95", "96")))
    one("sym_termico_97", lambda s: s.contact(0.7, 0.25, NA, act="thermal", terms=("97", "98")))
    one("sym_temp_na", lambda s: s.contact(0.6, 0.25, NA, act="timer", terms=("67", "68")))
    one("sym_temp_nc", lambda s: s.contact(0.6, 0.25, NC, act="timer", terms=("55", "56")))
    one("sym_bobina", lambda s: s.coil(0.3, 0.25))
    one("sym_bobina_temp", lambda s: s.coil(0.5, 0.25, timer=True))
    one("sym_piloto", lambda s: s.lamp(0.3, 0.25, terms=("X1", "X2")))
    one("sym_fusible", lambda s: s.fuse(0.3, 0.25))

    s = Sheet(4.4, 2.0, -1.6, -1.5)
    s.multipole([0.0, 0.9, 1.8], 0.25, "", [("1", "2"), ("3", "4"), ("5", "6")], breaker=True)
    s.save(out("sym_interruptor_3p"))
    s = Sheet(4.4, 2.0, -1.6, -1.5)
    s.multipole([0.0, 0.9, 1.8], 0.25, "", [("1", "2"), ("3", "4"), ("5", "6")], main=True)
    s.save(out("sym_contactor_3p"))
    s = Sheet(4.4, 2.0, -1.6, -1.5)
    s.thermal3([0.0, 0.9, 1.8], 0.25, "")
    s.save(out("sym_termico_3p"))
    s = Sheet(4.0, 3.6, -1.3, -3.3)
    s.motor([0.0, 0.8, 1.6], 0.25, "")
    s.save(out("sym_motor"))
    s = Sheet(1.6, 1.4, -0.8, -1.0)
    s.earth((0, 0.2))
    s.save(out("sym_tierra"))


# ================================================================= fuerza
def fuerza_directo(name="f_arranque_directo", label_motor="M1"):
    s = Sheet(7.0, 9.4, -1.8, -3.2)
    xs = [1.0, 2.0, 3.0]
    top = 5.6
    for x, n in zip(xs, ["L1", "L2", "L3"]):
        s.text((x, top + 0.3), n, fs=9, weight="bold")
    s.text((2.0, -2.9), "3 × 380 V, 60 Hz", fs=8, color="#555")
    s.multipole(xs, top, "Q1", [("1", "2"), ("3", "4"), ("5", "6")], breaker=True)
    for x in xs:
        s.seg((x, top - 1), (x, top - 1.6))
    s.multipole(xs, top - 1.6, "KM1", [("1", "2"), ("3", "4"), ("5", "6")], main=True)
    for x in xs:
        s.seg((x, top - 2.6), (x, top - 3.2))
    s.thermal3(xs, top - 3.2, "F1")
    s.motor(xs, top - 4.2, label_motor)
    s.save(out(name))


def fuerza_inversion():
    s = Sheet(10.6, 10.6, -1.8, -4.2)
    xs = [1.0, 2.0, 3.0]
    xs2 = [5.0, 6.0, 7.0]
    top = 5.6
    for x, n in zip(xs, ["L1", "L2", "L3"]):
        s.text((x, top + 0.3), n, fs=9, weight="bold")
    s.multipole(xs, top, "Q1", [("1", "2"), ("3", "4"), ("5", "6")], breaker=True)
    for x in xs:
        s.seg((x, top - 1), (x, top - 1.6))
    # entradas de KM2: cada fase en su propia altura (sin unir fases)
    for i, (x, x2) in enumerate(zip(xs, xs2)):
        y = top - 1.15 - 0.15 * i
        s.dot((x, y))
        s.wire([(x, y), (x2, y), (x2, top - 1.6)])
    s.multipole(xs, top - 1.6, "KM1", [("1", "2"), ("3", "4"), ("5", "6")], main=True)
    s.multipole(xs2, top - 1.6, "KM2", [("1", "2"), ("3", "4"), ("5", "6")], main=True)
    yj = top - 3.4
    for x in xs:
        s.seg((x, top - 2.6), (x, yj - 0.4))
    # salidas de KM2 cruzadas: L1 -> W1 (x=3), L2 -> V1 (x=2), L3 -> U1 (x=1)
    for i, (x2, xd) in enumerate(zip(xs2, [xs[2], xs[1], xs[0]])):
        y = yj + 0.3 - 0.15 * i
        s.wire([(x2, top - 2.6), (x2, y), (xd, y)])
        s.dot((xd, y))
    s.text((7.5, yj + 0.15), "L1 ↔ L3", fs=9, ha="left", color=RED, weight="bold")
    s.thermal3(xs, yj - 0.4, "F1")
    s.motor(xs, yj - 1.4, "M1")
    s.save(out("f_inversion"))


def fuerza_estrella_triangulo():
    s = Sheet(11.6, 14.2, -1.8, -7.6)
    xs = [1.0, 2.0, 3.0]
    xs3 = [5.6, 6.6, 7.6]
    top = 6.0
    for x, n in zip(xs, ["L1", "L2", "L3"]):
        s.text((x, top + 0.3), n, fs=9, weight="bold")
    s.multipole(xs, top, "Q1", [("1", "2"), ("3", "4"), ("5", "6")], breaker=True)
    for x in xs:
        s.seg((x, top - 1), (x, top - 1.4))
    s.multipole(xs, top - 1.4, "KM1", [("1", "2"), ("3", "4"), ("5", "6")], main=True)
    for x in xs:
        s.seg((x, top - 2.4), (x, top - 2.8))
    s.thermal3(xs, top - 2.8, "F1")
    yj = top - 3.8
    for x in xs:
        s.seg((x, yj), (x, yj - 0.9))
    # derivaciones hacia KM3, cada fase a su altura
    for i, (x, x3) in enumerate(zip(xs, xs3)):
        y = yj - 0.15 - 0.2 * i
        s.dot((x, y))
        s.wire([(x, y), (x3, y), (x3, yj - 0.9)])
    s.multipole(xs3, yj - 0.9, "KM3", [("1", "2"), ("3", "4"), ("5", "6")], main=True)
    xc, cy = s.motor(xs, yj - 0.9, "M1", six=True)
    ylow = cy - 0.75 - 1.0          # bornes W2, U2, V2 (x = 1, 2, 3)
    # salidas de KM3 a W2, U2, V2 (U1-W2, V1-U2, W1-V2), cada una a su altura
    for i, (x3, x) in enumerate(zip(xs3, xs)):
        y = ylow - 0.3 - 0.25 * i
        s.wire([(x3, yj - 1.9), (x3, y), (x, y)])
        s.dot((x, y))
    for x in xs:
        s.seg((x, ylow), (x, ylow - 1.2))
    yk = ylow - 1.2
    s.multipole(xs, yk, "KM2", [("1", "2"), ("3", "4"), ("5", "6")], main=True)
    s.wire([(xs[0], yk - 1), (xs[0], yk - 1.3), (xs[2], yk - 1.3), (xs[2], yk - 1)])
    s.seg((xs[1], yk - 1), (xs[1], yk - 1.3))
    s.dot((xs[1], yk - 1.3))
    s.text((3.6, yk - 1.3), "punto estrella", fs=8, ha="left", color="#555", style="italic")
    s.text((8.2, yj - 1.4), "U1–W2\nV1–U2\nW1–V2", fs=8, ha="left", color=RED, weight="bold")
    s.save(out("f_estrella_triangulo"))


# ================================================================= mando
def _mando_base(s, x0, x1, ytop, ybot):
    s.rail(x0, x1, ytop, "L1")
    s.rail(x0, x1, ybot, "N")


def mando_lampara():
    s = Sheet(6.0, 6.8, -1.6, -0.6)
    _mando_base(s, 0.0, 3.2, 5.6, 0.0)
    x = 1.6
    s.fuse(x, 5.6, "F2")
    s.seg((x, 4.6), (x, 4.2))
    s.contact(x, 4.2, NA, act="push", label="S1", terms=("13", "14"))
    s.seg((x, 3.2), (x, 2.6))
    s.lamp(x, 2.6, "H1", color=LAMP_Y)
    s.seg((x, 1.6), (x, 0.0))
    s.save(out("m_lampara"))


def mando_marcha_paro(name="m_marcha_paro", dos_puntos=False):
    w = 13.4 if dos_puntos else 11.0
    s = Sheet(w, 10.6, -1.6, -0.9)
    xr = w - 2.6
    ytop, ybot = 9.4, 0.0
    _mando_base(s, 0.0, xr, ytop, ybot)
    x = 1.6
    s.fuse(x, ytop, "F2")
    s.seg((x, ytop - 1), (x, ytop - 1.4))
    s.contact(x, ytop - 1.4, NC, act="thermal", label="F1", terms=("95", "96"))
    y = ytop - 2.4
    yh = y - 0.4  # nodo para pilotos
    s.seg((x, y), (x, yh))
    s.dot((x, yh))
    s.seg((x, yh), (x, yh - 0.4))
    y = yh - 0.4
    if not dos_puntos:
        s.contact(x, y, NC, act="push", label="S0", terms=("11", "12"))
        y -= 1.0
    else:
        s.contact(x, y, NC, act="push", label="S0", terms=("11", "12"))
        y -= 1.0
        s.seg((x, y), (x, y - 0.3))
        y -= 0.3
        s.contact(x, y, NC, act="push", label="S01", terms=("11", "12"))
        y -= 1.0
    s.seg((x, y), (x, y - 0.4))
    yn = y - 0.4
    xk = x + 1.6 if not dos_puntos else x + 4.0
    s.dot((x, yn))
    s.wire([(x, yn), (xk, yn), (xk, yn - 0.3)])
    s.seg((x, yn), (x, yn - 0.3))
    s.contact(x, yn - 0.3, NA, act="push", label="S1", terms=("13", "14"))
    if dos_puntos:
        xs11 = x + 2.3
        s.dot((xs11, yn))
        s.seg((xs11, yn), (xs11, yn - 0.3))
        s.contact(xs11, yn - 0.3, NA, act="push", label="S11", terms=("13", "14"))
    s.contact(xk, yn - 0.3, NA, label="KM1", terms=("13", "14"), label_dx=0.45)
    yj = yn - 1.6
    s.seg((x, yn - 1.3), (x, yj))
    if dos_puntos:
        s.wire([(xs11, yn - 1.3), (xs11, yj)])
        s.dot((xs11, yj))
    s.wire([(xk, yn - 1.3), (xk, yj), (x, yj)])
    s.dot((x, yj))
    s.seg((x, yj), (x, yj - 0.4))
    s.coil(x, yj - 0.4, "KM1")
    s.seg((x, yj - 1.4), (x, ybot))
    # pilotos
    xm = xr - 2.4
    s.wire([(x, yh), (xm, yh), (xm, yh - 0.4)])
    s.contact(xm, yh - 0.4, NA, label="KM1", terms=("43", "44"), label_dx=0.45)
    s.seg((xm, yh - 1.4), (xm, yh - 2.0))
    s.lamp(xm, yh - 2.0, "H1", color=LAMP_G)
    s.seg((xm, yh - 3.0), (xm, ybot))
    s.text((xm, ybot - 0.4), "marcha", fs=8, color=GREEN)
    xf = xr - 0.6
    yf = ytop - 1.4
    s.dot((x, yf))
    s.wire([(x, yf), (xf, yf), (xf, yf - 0.3)])
    s.contact(xf, yf - 0.3, NA, act="thermal", label="F1", terms=("97", "98"), label_dx=1.3)
    s.seg((xf, yf - 1.3), (xf, yh - 2.0))
    s.lamp(xf, yh - 2.0, "H2", color=LAMP_R)
    s.seg((xf, yh - 3.0), (xf, ybot))
    s.text((xf, ybot - 0.4), "disparo térmico", fs=8, color=RED)
    for xx in (x, xm, xf):
        s.dot((xx, ybot))
    s.save(out(name))


def mando_inversion():
    s = Sheet(10.4, 13.2, -1.6, -0.6)
    ytop, ybot = 12.0, 0.0
    _mando_base(s, 0.0, 7.6, ytop, ybot)
    x = 1.6
    s.fuse(x, ytop, "F2")
    s.seg((x, ytop - 1), (x, ytop - 1.4))
    s.contact(x, ytop - 1.4, NC, act="thermal", label="F1", terms=("95", "96"))
    s.seg((x, ytop - 2.4), (x, ytop - 2.8))
    s.contact(x, ytop - 2.8, NC, act="push", label="S0", terms=("11", "12"))
    yn = ytop - 4.2
    s.seg((x, ytop - 3.8), (x, yn))
    xa, xb = 1.6, 5.6
    s.dot((x, yn))
    s.wire([(x, yn), (xb, yn)])
    for xx, km, sb, other in ((xa, "KM1", "S1", "KM2"), (xb, "KM2", "S2", "KM1")):
        xk = xx + 1.6
        s.dot((xx, yn)) if xx != x else None
        s.wire([(xx, yn), (xk, yn), (xk, yn - 0.3)])
        s.seg((xx, yn), (xx, yn - 0.3))
        s.contact(xx, yn - 0.3, NA, act="push", label=sb, terms=("13", "14"))
        s.contact(xk, yn - 0.3, NA, label=km, terms=("13", "14"), label_dx=0.45)
        yj = yn - 1.6
        s.seg((xx, yn - 1.3), (xx, yj))
        s.wire([(xk, yn - 1.3), (xk, yj), (xx, yj)])
        s.dot((xx, yj))
        s.seg((xx, yj), (xx, yj - 0.4))
        s.contact(xx, yj - 0.4, NC, label=other, terms=("21", "22"))
        s.seg((xx, yj - 1.4), (xx, yj - 1.8))
        s.coil(xx, yj - 1.8, km)
        s.seg((xx, yj - 2.8), (xx, ybot))
        s.dot((xx, ybot))
        s.text((xx + 0.55, yj - 0.9), "enclavamiento", fs=7.5, ha="left", color=RED, style="italic")
    s.text((xa, ybot - 0.35), "giro horario", fs=8, color="#555")
    s.text((xb, ybot - 0.35), "giro antihorario", fs=8, color="#555")
    s.save(out("m_inversion"))


def mando_estrella_triangulo():
    s = Sheet(13.4, 13.6, -1.6, -0.9)
    ytop, ybot = 12.4, 0.0
    _mando_base(s, 0.0, 10.6, ytop, ybot)
    x = 1.6
    s.fuse(x, ytop, "F2")
    s.seg((x, ytop - 1), (x, ytop - 1.4))
    s.contact(x, ytop - 1.4, NC, act="thermal", label="F1", terms=("95", "96"))
    s.seg((x, ytop - 2.4), (x, ytop - 2.8))
    s.contact(x, ytop - 2.8, NC, act="push", label="S0", terms=("11", "12"))
    yn = ytop - 4.2
    s.seg((x, ytop - 3.8), (x, yn))
    # marcha con autorretención de KM1
    xk = x + 1.6
    s.dot((x, yn))
    s.wire([(x, yn), (xk, yn), (xk, yn - 0.3)])
    s.seg((x, yn), (x, yn - 0.3))
    s.contact(x, yn - 0.3, NA, act="push", label="S1", terms=("13", "14"))
    s.contact(xk, yn - 0.3, NA, label="KM1", terms=("13", "14"), label_dx=0.45)
    yj = yn - 1.6
    s.seg((x, yn - 1.3), (x, yj))
    s.wire([(xk, yn - 1.3), (xk, yj), (x, yj)])
    s.dot((x, yj))
    # columnas: KM1 (x), KT (x2), KM2 (x3), KM3 (x4)
    x2, x3, x4 = 4.6, 7.0, 9.4
    s.wire([(x, yj), (x4, yj)])
    for xx in (x2, x3, x4):
        s.dot((xx, yj)) if xx != x4 else None
    s.seg((x, yj), (x, yj - 2.6))
    s.coil(x, yj - 2.6, "KM1")
    s.seg((x, yj - 3.6), (x, ybot))
    # KT
    s.seg((x2, yj), (x2, yj - 2.6))
    s.coil(x2, yj - 2.6, "KT", timer=True)
    s.seg((x2, yj - 3.6), (x2, ybot))
    # KM2 estrella: KT 55-56 (NC temporizado) + KM3 21-22
    s.seg((x3, yj), (x3, yj - 0.3))
    s.contact(x3, yj - 0.3, NC, act="timer", label="KT", terms=("55", "56"), label_dx=1.05)
    s.seg((x3, yj - 1.3), (x3, yj - 1.6))
    s.contact(x3, yj - 1.6, NC, label="KM3", terms=("21", "22"))
    s.seg((x3, yj - 2.6), (x3, yj - 2.9))
    s.coil(x3, yj - 2.9, "KM2")
    s.seg((x3, yj - 3.9), (x3, ybot))
    # KM3 triángulo: KT 67-68 (NA temporizado) + KM2 21-22
    s.seg((x4, yj), (x4, yj - 0.3))
    s.contact(x4, yj - 0.3, NA, act="timer", label="KT", terms=("67", "68"), label_dx=1.05)
    s.seg((x4, yj - 1.3), (x4, yj - 1.6))
    s.contact(x4, yj - 1.6, NC, label="KM2", terms=("21", "22"))
    s.seg((x4, yj - 2.6), (x4, yj - 2.9))
    s.coil(x4, yj - 2.9, "KM3")
    s.seg((x4, yj - 3.9), (x4, ybot))
    for xx in (x, x2, x3, x4):
        s.dot((xx, ybot))
    s.text((x, ybot - 0.4), "línea", fs=8, color="#555")
    s.text((x2, ybot - 0.4), "temporizador", fs=8, color="#555")
    s.text((x3, ybot - 0.4), "estrella", fs=8, color="#555")
    s.text((x4, ybot - 0.4), "triángulo", fs=8, color="#555")
    s.save(out("m_estrella_triangulo"))


def mando_secuencial():
    """Reto: M2 arranca t s después de M1; S0 o cualquier térmico paran ambos."""
    s = Sheet(11.6, 13.0, -1.6, -0.9)
    ytop, ybot = 11.8, 0.0
    _mando_base(s, 0.0, 8.8, ytop, ybot)
    x = 1.6
    s.fuse(x, ytop, "F3")
    s.seg((x, ytop - 1), (x, ytop - 1.4))
    s.contact(x, ytop - 1.4, NC, act="thermal", label="F1", terms=("95", "96"))
    s.seg((x, ytop - 2.4), (x, ytop - 2.7))
    s.contact(x, ytop - 2.7, NC, act="thermal", label="F2", terms=("95", "96"))
    s.seg((x, ytop - 3.7), (x, ytop - 4.0))
    s.contact(x, ytop - 4.0, NC, act="push", label="S0", terms=("11", "12"))
    yn = ytop - 5.4
    s.seg((x, ytop - 5.0), (x, yn))
    xk = x + 1.6
    s.dot((x, yn))
    s.wire([(x, yn), (xk, yn), (xk, yn - 0.3)])
    s.seg((x, yn), (x, yn - 0.3))
    s.contact(x, yn - 0.3, NA, act="push", label="S1", terms=("13", "14"))
    s.contact(xk, yn - 0.3, NA, label="KM1", terms=("13", "14"), label_dx=0.45)
    yj = yn - 1.6
    s.seg((x, yn - 1.3), (x, yj))
    s.wire([(xk, yn - 1.3), (xk, yj), (x, yj)])
    s.dot((x, yj))
    x2, x3 = 5.0, 7.6
    s.wire([(x, yj), (x3, yj)])
    s.dot((x2, yj))
    s.seg((x, yj), (x, yj - 1.6))
    s.coil(x, yj - 1.6, "KM1")
    s.seg((x, yj - 2.6), (x, ybot))
    s.seg((x2, yj), (x2, yj - 1.6))
    s.coil(x2, yj - 1.6, "KT", timer=True)
    s.seg((x2, yj - 2.6), (x2, ybot))
    s.seg((x3, yj), (x3, yj - 0.3))
    s.contact(x3, yj - 0.3, NA, act="timer", label="KT", terms=("67", "68"), label_dx=1.05)
    s.seg((x3, yj - 1.3), (x3, yj - 1.6))
    s.coil(x3, yj - 1.6, "KM2")
    s.seg((x3, yj - 2.6), (x3, ybot))
    for xx in (x, x2, x3):
        s.dot((xx, ybot))
    s.text((x, ybot - 0.4), "M1", fs=8, color="#555")
    s.text((x2, ybot - 0.4), "retardo t", fs=8, color="#555")
    s.text((x3, ybot - 0.4), "M2", fs=8, color="#555")
    s.save(out("m_secuencial"))


def fuerza_dos_motores():
    s = Sheet(11.0, 10.6, -1.8, -4.4)
    top = 5.6
    xsA, xsB = [1.0, 2.0, 3.0], [6.0, 7.0, 8.0]
    for x, n in zip(xsA, ["L1", "L2", "L3"]):
        s.text((x, top + 0.3), n, fs=9, weight="bold")
    s.multipole(xsA, top, "Q1", [("1", "2"), ("3", "4"), ("5", "6")], breaker=True)
    yb = top - 1.3
    for x, xb in zip(xsA, xsB):
        s.seg((x, top - 1), (x, top - 1.6))
        s.dot((x, yb - (x - 1.0) * 0.15))
        s.wire([(x, yb - (x - 1.0) * 0.15), (xb, yb - (x - 1.0) * 0.15), (xb, top - 1.6)])
    for xs, km, f, m in ((xsA, "KM1", "F1", "M1"), (xsB, "KM2", "F2", "M2")):
        s.multipole(xs, top - 1.6, km, [("1", "2"), ("3", "4"), ("5", "6")], main=True)
        for x in xs:
            s.seg((x, top - 2.6), (x, top - 3.2))
        s.thermal3(xs, top - 3.2, f)
        s.motor(xs, top - 4.2, m)
    s.save(out("f_dos_motores"))


# ================================================================= teoría: bornes del motor
def placa_bornes():
    from matplotlib.patches import Circle as C
    s = Sheet(13.0, 5.6, -0.6, -0.6)
    for k, (title, bridges) in enumerate((("Estrella (Y)", "Y"), ("Triángulo (Δ)", "D"))):
        ox = k * 6.6
        s.text((ox + 2.6, 4.5), title, fs=12, weight="bold")
        top = ["U1", "V1", "W1"]
        bot = ["W2", "U2", "V2"]
        for i in range(3):
            for j, (row, y) in enumerate(((top, 3.0), (bot, 1.2))):
                c = (ox + 1.0 + i * 1.6, y)
                s.ax.add_patch(C(c, 0.32, fill=False, ec="#1a1a1a", lw=1.5, zorder=3))
                s.text(c, row[i], fs=8)
        if bridges == "Y":
            s.seg((ox + 1.0 + 0.32, 1.2), (ox + 2.6 - 0.32, 1.2), lw=4, color=RED)
            s.seg((ox + 2.6 + 0.32, 1.2), (ox + 4.2 - 0.32, 1.2), lw=4, color=RED)
        else:
            for i in range(3):
                s.seg((ox + 1.0 + i * 1.6, 3.0 - 0.32), (ox + 1.0 + i * 1.6, 1.2 + 0.32), lw=4,
                      color=RED)
        for i, n in enumerate(("L1", "L2", "L3")):
            s.seg((ox + 1.0 + i * 1.6, 3.32), (ox + 1.0 + i * 1.6, 3.9))
            s.text((ox + 1.0 + i * 1.6 + 0.3, 3.75), n, fs=8, ha="left")
        s.text((ox + 2.6, 0.2), "U fase = U línea / √3" if bridges == "Y" else "U fase = U línea",
               fs=9, color="#555")
    s.save(out("t_placa_bornes"))


if __name__ == "__main__":
    simbolos()
    fuerza_directo()
    fuerza_inversion()
    fuerza_estrella_triangulo()
    fuerza_dos_motores()
    mando_lampara()
    mando_marcha_paro()
    mando_marcha_paro("m_dos_puntos", dos_puntos=True)
    mando_inversion()
    mando_estrella_triangulo()
    mando_secuencial()
    placa_bornes()
    print("ok")
