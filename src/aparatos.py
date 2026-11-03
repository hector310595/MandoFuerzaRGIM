"""Ilustraciones de los APARATOS REALES (vista frontal) para unir símbolo ↔ aparato.

Dibujos técnicos propios (sin marcas comerciales), en milímetros aproximados:
módulo DIN de 18 mm, contactor de 45 mm, pulsadores de Ø22 mm. Los bornes llevan
la MISMA numeración que el símbolo IEC 60617 que se usa en los esquemas.
Uso: python3 src/aparatos.py  →  figuras/a_*.png / .svg
"""
import math
import os

import matplotlib

matplotlib.use("Agg")
matplotlib.rcParams["svg.hashsalt"] = "rgim-aparatos"
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import (Arc, Circle, FancyBboxPatch, Polygon, Rectangle,  # noqa: E402
                                Wedge)

FIG = os.path.join(os.path.dirname(__file__), "..", "figuras")

BODY = "#e4e6e9"
FACE = "#f5f6f7"
EDGE = "#5f646b"
DARK = "#33373d"
SCREW = "#b9bdc3"
RAIL = "#a9adb3"
COPPER = "#c98a3d"
TXT = "#1a1a1a"
MAIN_C = "#1a1a1a"     # bornes de fuerza
AUX_C = "#1f4e9c"      # contactos auxiliares
COIL_C = "#c0392b"     # bobina
GREEN = "#13a35a"
RED = "#d0342c"
YELLOW = "#f2c200"
BLUE = "#2f6db5"
CALL = "#c0392b"       # etiquetas de designación


class Canvas:
    def __init__(self, x0, y0, w, h, k=0.06):
        self.fig = plt.figure(figsize=(w * k, h * k))
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set_xlim(x0, x0 + w)
        self.ax.set_ylim(y0, y0 + h)
        self.ax.set_aspect("equal")
        self.ax.axis("off")
        self.k = k

    def save(self, name):
        os.makedirs(FIG, exist_ok=True)
        self.fig.savefig(os.path.join(FIG, name + ".png"), dpi=220, transparent=False,
                         facecolor="white")
        self.fig.savefig(os.path.join(FIG, name + ".svg"), metadata={"Date": None},
                         facecolor="white")
        plt.close(self.fig)


# ------------------------------------------------------------------ primitivas
def rbox(ax, x, y, w, h, fc=BODY, ec=EDGE, r=1.5, lw=0.9, z=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=%g" % r,
                                fc=fc, ec=ec, lw=lw, zorder=z))


def rect(ax, x, y, w, h, fc, ec=EDGE, lw=0.8, z=2):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=lw, zorder=z))


def t(ax, x, y, s, fs=7, color=TXT, weight="normal", ha="center", va="center", z=8, rot=0):
    ax.text(x, y, s, fontsize=fs, color=color, fontweight=weight, ha=ha, va=va, zorder=z,
            rotation=rot)


def screw(ax, cx, cy, r=2.6, z=5):
    """Borne de tornillo: abertura del cable + cabeza del tornillo."""
    ax.add_patch(Circle((cx, cy), r, fc=SCREW, ec=EDGE, lw=0.8, zorder=z))
    d = r * 0.6
    ax.plot([cx - d, cx + d], [cy, cy], color=EDGE, lw=0.9, zorder=z + 1)
    ax.plot([cx, cx], [cy - d, cy + d], color=EDGE, lw=0.9, zorder=z + 1)


def rail(ax, x0, x1, yc):
    """Riel DIN de 35 mm (detrás de los aparatos)."""
    rect(ax, x0, yc - 17.5, x1 - x0, 35, RAIL, ec="#8a8f96", lw=0.8, z=0)
    for x in range(int(x0) + 6, int(x1) - 4, 25):
        rbox(ax, x, yc - 3, 12, 6, fc="#8f949a", ec="#8f949a", r=2.5, z=1)


def tag(ax, x, y, s, fs=11, color=CALL):
    """Etiqueta de designación (como la placa del tablero)."""
    ax.text(x, y, s, fontsize=fs, color="white", fontweight="bold", ha="center", va="center",
            zorder=20, bbox=dict(boxstyle="round,pad=0.25", fc=color, ec="none"))


# -------------------------------------------------------------------- aparatos
def mcb(ax, x0, y0, top, bot, rating, sub="", rcd=False, fs=6.5):
    """Interruptor modular (termomagnético o diferencial). Módulos de 18 mm × 90 mm."""
    n = len(top)
    W = 18 * n
    rbox(ax, x0, y0, W, 90, BODY)
    rbox(ax, x0 + 1.5, y0 + 22, W - 3, 46, FACE, lw=0.7)
    for i in range(1, n):
        ax.plot([x0 + 18 * i] * 2, [y0 + 22, y0 + 68], color="#c2c5ca", lw=0.7, zorder=3)
    for i in range(n):
        cx = x0 + 9 + 18 * i
        rect(ax, cx - 4.5, y0 + 85, 9, 4, DARK, ec=DARK, z=3)
        rect(ax, cx - 4.5, y0 + 1, 9, 4, DARK, ec=DARK, z=3)
        screw(ax, cx, y0 + 78)
        screw(ax, cx, y0 + 12)
        t(ax, cx, y0 + 71.5, top[i], fs=fs, weight="bold")
        t(ax, cx, y0 + 18.5, bot[i], fs=fs, weight="bold")
    # palanca (en posición I = ON)
    rect(ax, x0 + 4, y0 + 46, W - 8, 8, "#4a4f56", ec="#4a4f56", z=4)   # ranura
    for i in range(n):
        cx = x0 + 9 + 18 * i
        rbox(ax, cx - 4, y0 + 50, 8, 12, DARK, ec=DARK, r=1.2, z=6)        # palanca arriba = I
    if n > 1:
        rect(ax, x0 + 9, y0 + 55, 18 * (n - 1), 3, DARK, ec=DARK, z=5)     # barra de unión
    t(ax, x0 + W - 3, y0 + 64.5, "I-ON", fs=fs - 2, ha="right", color="#555")
    t(ax, x0 + 9, y0 + 36, rating, fs=fs + 1.5, weight="bold")
    if sub:
        t(ax, x0 + W / 2 + (9 if rcd else 0), y0 + 28.5, sub, fs=fs - 0.5)
    if rcd:
        rbox(ax, x0 + W - 13, y0 + 31, 8, 8, YELLOW, ec=EDGE, r=1, z=6)
        t(ax, x0 + W - 9, y0 + 35, "T", fs=fs, weight="bold")
    return W


def portafusible(ax, x0, y0, top="1", bot="2", fs=6.5):
    rbox(ax, x0, y0, 18, 82, BODY)
    for cy, lab, ly in ((y0 + 73, top, y0 + 66), (y0 + 9, bot, y0 + 16)):
        screw(ax, x0 + 9, cy)
        t(ax, x0 + 9, ly, lab, fs=fs, weight="bold")
    rbox(ax, x0 + 2, y0 + 22, 14, 38, DARK, ec=DARK, r=1.5, z=4)
    rbox(ax, x0 + 5, y0 + 33, 8, 16, "#e9e3c9", ec="#e9e3c9", r=0.8, z=5)   # visor
    t(ax, x0 + 9, y0 + 41, "gG", fs=fs - 1, z=9)
    t(ax, x0 + 9, y0 + 27, "10×38", fs=fs - 2, color="white")
    return 18


def cartucho(ax, x0, y0, txt="2 A", fs=7):
    """Fusible cilíndrico 10×38 visto de lado (horizontal)."""
    rbox(ax, x0, y0, 38, 10, "#f3efe2", ec=EDGE, r=1, z=3)
    rbox(ax, x0, y0, 6, 10, SCREW, ec=EDGE, r=1, z=4)
    rbox(ax, x0 + 32, y0, 6, 10, SCREW, ec=EDGE, r=1, z=4)
    t(ax, x0 + 19, y0 + 5, "gG " + txt, fs=fs)


def contactor(ax, x0, y0, coil="220 V 60 Hz", fs=6.5, show_bottom=True):
    """Contactor tripolar con 1 NA auxiliar (45 × 80 mm)."""
    rbox(ax, x0, y0, 45, 80, BODY)
    rbox(ax, x0 + 3, y0 + 21, 39, 38, FACE, lw=0.7)
    tops = [(5.5, "A1", COIL_C), (14.5, "1/L1", MAIN_C), (23.5, "3/L2", MAIN_C),
            (32.5, "5/L3", MAIN_C), (40.5, "13\nNO", AUX_C)]
    bots = [(14.5, "2/T1", MAIN_C), (23.5, "4/T2", MAIN_C), (32.5, "6/T3", MAIN_C),
            (40.5, "14\nNO", AUX_C), (5.5, "A2", COIL_C)]
    for dx, lab, col in tops:
        screw(ax, x0 + dx, y0 + 73, r=2.4)
        t(ax, x0 + dx, y0 + 65 if "\n" not in lab else y0 + 64.2, lab, fs=fs - (1 if "\n" in lab else 0),
          color=col, weight="bold")
    if show_bottom:
        for dx, lab, col in bots:
            screw(ax, x0 + dx, y0 + 7, r=2.4)
            t(ax, x0 + dx, y0 + 15 if "\n" not in lab else y0 + 15.8, lab,
              fs=fs - (1 if "\n" in lab else 0), color=col, weight="bold")
    # ventana indicadora y portaetiquetas
    rect(ax, x0 + 17, y0 + 43, 11, 8, DARK, ec=DARK, z=4)
    rect(ax, x0 + 19.5, y0 + 45, 6, 4, "#9aa0a6", ec="#9aa0a6", z=5)
    t(ax, x0 + 22.5, y0 + 37, "Contactor", fs=fs - 0.5)
    t(ax, x0 + 22.5, y0 + 31.5, "Ie 9 A  AC-3", fs=fs - 1.5, color="#555")
    t(ax, x0 + 22.5, y0 + 26, "Bobina " + coil, fs=fs - 1.5, color=COIL_C)
    return 45


def termico(ax, x0, y0, fs=6.5, pins=True):
    """Relé térmico que se enchufa debajo del contactor (45 × 50 mm)."""
    if pins:
        for dx in (14.5, 23.5, 32.5):
            rect(ax, x0 + dx - 1.4, y0 + 48, 2.8, 10, COPPER, ec="#8a5a22", z=1)
    rbox(ax, x0, y0, 45, 50, BODY)
    for dx, lab in ((14.5, "2/T1"), (23.5, "4/T2"), (32.5, "6/T3")):
        screw(ax, x0 + dx, y0 + 7, r=2.4)
        t(ax, x0 + dx, y0 + 14.5, lab, fs=fs, weight="bold")
    # contactos auxiliares a la derecha
    for cy, lab, col in ((y0 + 43, "97", AUX_C), (y0 + 35.5, "98", AUX_C),
                         (y0 + 26.5, "95", COIL_C), (y0 + 19, "96", COIL_C)):
        screw(ax, x0 + 40.5, cy, r=2.1)
        t(ax, x0 + 35.3, cy, lab, fs=fs - 0.5, color=col, weight="bold")
    # dial de ajuste de corriente
    cx, cy = x0 + 20, y0 + 32
    ax.add_patch(Circle((cx, cy), 6.5, fc="#d7dade", ec=EDGE, lw=0.8, zorder=5))
    ax.add_patch(Wedge((cx, cy), 6.5, 200, 340, fc="#c4c8cd", ec="none", zorder=5))
    ax.plot([cx, cx + 4.5 * math.cos(math.radians(60))], [cy, cy + 4.5 * math.sin(math.radians(60))],
            color=DARK, lw=1.4, zorder=6)
    t(ax, cx, cy - 10, "7 – 10 A", fs=fs - 1.5, color="#555")
    # botón de rearme (azul) y prueba (rojo)
    ax.add_patch(Circle((x0 + 6.5, y0 + 39), 3.2, fc=BLUE, ec=EDGE, lw=0.8, zorder=5))
    t(ax, x0 + 6.5, y0 + 39, "R", fs=fs - 1, color="white", weight="bold")
    rbox(ax, x0 + 4, y0 + 27, 5, 4, RED, ec=EDGE, r=0.6, z=5)
    t(ax, x0 + 6.5, y0 + 24, "Test", fs=fs - 2.5, color="#555")
    return 45


def temporizador(ax, x0, y0, fs=6.5):
    """Relé temporizado modular (2 módulos)."""
    W = 36
    rbox(ax, x0, y0, W, 90, BODY)
    rbox(ax, x0 + 1.5, y0 + 22, W - 3, 46, FACE, lw=0.7)
    for (dx, lab, col) in ((7, "A1", COIL_C), (18, "55", AUX_C), (29, "67", AUX_C)):
        screw(ax, x0 + dx, y0 + 78, r=2.4)
        t(ax, x0 + dx, y0 + 71.5, lab, fs=fs, color=col, weight="bold")
    for (dx, lab, col) in ((7, "A2", COIL_C), (18, "56", AUX_C), (29, "68", AUX_C)):
        screw(ax, x0 + dx, y0 + 12, r=2.4)
        t(ax, x0 + dx, y0 + 18.5, lab, fs=fs, color=col, weight="bold")
    cx, cy = x0 + W / 2, y0 + 44
    ax.add_patch(Circle((cx, cy), 9, fc="white", ec=EDGE, lw=0.8, zorder=4))
    for k in range(11):
        a = math.radians(225 - k * 27)
        r0 = 7.3 if k % 5 else 6.4
        ax.plot([cx + r0 * math.cos(a), cx + 8.6 * math.cos(a)],
                [cy + r0 * math.sin(a), cy + 8.6 * math.sin(a)], color=EDGE, lw=0.6, zorder=5)
    ax.add_patch(Circle((cx, cy), 4.5, fc=DARK, ec=DARK, zorder=6))
    a = math.radians(225 - 5 * 27)
    ax.plot([cx, cx + 6.2 * math.cos(a)], [cy, cy + 6.2 * math.sin(a)], color="white", lw=1.6,
            zorder=7)
    t(ax, cx - 7.5, cy - 9.5, "0", fs=fs - 1.5)
    t(ax, cx + 7.5, cy - 9.5, "10 s", fs=fs - 1.5)
    for dx, col, lab in ((-9, GREEN, "U"), (9, YELLOW, "R")):
        ax.add_patch(Circle((cx + dx, y0 + 61.5), 1.6, fc=col, ec=EDGE, lw=0.6, zorder=5))
        t(ax, cx + dx + 3.2, y0 + 61.5, lab, fs=fs - 2)
    t(ax, cx, y0 + 28, "Retardo a la\nconexión", fs=fs - 2, color="#555")
    return W


def pulsador(ax, cx, cy, color, mark, plate, block, fs=7, mushroom=False):
    """Pulsador de Ø22 mm visto de frente, con su placa y su bloque de contactos."""
    if mushroom:
        ax.add_patch(Circle((cx, cy), 21, fc=YELLOW, ec=EDGE, lw=0.8, zorder=2))
        ax.add_patch(Circle((cx, cy), 15, fc="#9b1d17", ec="#6e120e", lw=0.8, zorder=3))
        ax.add_patch(Circle((cx, cy), 13, fc=color, ec="none", zorder=4))
        ax.add_patch(Circle((cx - 3.5, cy + 3.5), 5, fc="white", ec="none", alpha=0.18, zorder=5))
    else:
        ax.add_patch(Circle((cx, cy), 15, fc="#cfd2d6", ec=EDGE, lw=0.8, zorder=2))
        ax.add_patch(Circle((cx, cy), 12.5, fc="#a7abb1", ec="none", zorder=3))
        ax.add_patch(Circle((cx, cy), 11, fc=color, ec="none", zorder=4))
        ax.add_patch(Circle((cx - 3, cy + 3), 4.5, fc="white", ec="none", alpha=0.2, zorder=5))
        t(ax, cx, cy, mark, fs=fs + 5, color="white", weight="bold")
    py = cy - (27 if mushroom else 23)
    rbox(ax, cx - 16, py - 4, 32, 8, "white", ec=EDGE, r=1, z=3)
    t(ax, cx, py, plate, fs=fs - 1, weight="bold")
    # bloque de contactos (se monta detrás)
    by = py - 22
    rbox(ax, cx - 11, by - 7, 22, 14, BODY, r=1, z=3)
    a, b, kind = block
    screw(ax, cx - 5.5, by + 1.5, r=2.2)
    screw(ax, cx + 5.5, by + 1.5, r=2.2)
    t(ax, cx - 5.5, by - 4.5, a, fs=fs - 1.5, color=AUX_C if kind == "NA" else COIL_C, weight="bold")
    t(ax, cx + 5.5, by - 4.5, b, fs=fs - 1.5, color=AUX_C if kind == "NA" else COIL_C, weight="bold")
    t(ax, cx, by - 11.5, "bloque " + kind, fs=fs - 1.5, color="#555")
    ax.plot([cx, cx], [py - 4, by + 7], color="#9aa0a6", lw=0.8, ls=(0, (2, 1.5)), zorder=1)


def piloto(ax, cx, cy, color, glow, plate, fs=7):
    ax.add_patch(Circle((cx, cy), 15, fc="#cfd2d6", ec=EDGE, lw=0.8, zorder=2))
    ax.add_patch(Circle((cx, cy), 12.5, fc="#a7abb1", ec="none", zorder=3))
    ax.add_patch(Circle((cx, cy), 11, fc=color, ec="none", zorder=4))
    for r_, a in ((8, 0.35), (5, 0.55), (2.5, 0.8)):
        ax.add_patch(Circle((cx, cy), r_, fc=glow, ec="none", alpha=a, zorder=5))
    py = cy - 23
    rbox(ax, cx - 16, py - 4, 32, 8, "white", ec=EDGE, r=1, z=3)
    t(ax, cx, py, plate, fs=fs - 1, weight="bold")
    by = py - 22
    rbox(ax, cx - 11, by - 7, 22, 14, BODY, r=1, z=3)
    screw(ax, cx - 5.5, by + 1.5, r=2.2)
    screw(ax, cx + 5.5, by + 1.5, r=2.2)
    t(ax, cx - 5.5, by - 4.5, "X1", fs=fs - 1.5, weight="bold")
    t(ax, cx + 5.5, by - 4.5, "X2", fs=fs - 1.5, weight="bold")
    t(ax, cx, by - 11.5, "portalámpara", fs=fs - 1.5, color="#555")
    ax.plot([cx, cx], [py - 4, by + 7], color="#9aa0a6", lw=0.8, ls=(0, (2, 1.5)), zorder=1)


def motor(ax, x0, y0, fs=7, body="#3d6d99"):
    """Motor de inducción trifásico visto de lado (≈ 135 × 95)."""
    dark = "#2b5070"
    # patas
    for px in (34, 84):
        ax.add_patch(Polygon([(x0 + px, y0 + 16), (x0 + px + 22, y0 + 16), (x0 + px + 26, y0 + 4),
                              (x0 + px - 4, y0 + 4)], closed=True, fc=dark, ec=EDGE, lw=0.8, zorder=2))
    # eje con chaveta
    rect(ax, x0, y0 + 41, 18, 10, "#c3c7cc", z=2)
    rect(ax, x0 + 3, y0 + 49, 9, 2, "#8f949a", ec="#8f949a", lw=0.5, z=3)
    # brida delantera
    rbox(ax, x0 + 16, y0 + 20, 8, 52, dark, r=1.5, z=3)
    # carcasa con aletas
    rbox(ax, x0 + 22, y0 + 16, 88, 60, body, r=3, z=3)
    for k in range(9):
        y = y0 + 21 + k * 6.2
        ax.plot([x0 + 26, x0 + 106], [y, y], color=dark, lw=1.1, zorder=4)
    # tapa del ventilador con rejilla
    ax.add_patch(FancyBboxPatch((x0 + 110, y0 + 19), 22, 54, boxstyle="round,pad=0,rounding_size=8",
                                fc=dark, ec=EDGE, lw=0.8, zorder=3))
    for k in range(5):
        x = x0 + 114 + k * 3.6
        ax.plot([x, x], [y0 + 25, y0 + 67], color="#1d3a52", lw=1.2, zorder=4)
    # placa de características
    rect(ax, x0 + 74, y0 + 36, 26, 18, "#e8e8e8", ec=EDGE, z=5)
    for k in range(4):
        ax.plot([x0 + 77, x0 + 97 - (k % 2) * 6], [y0 + 50 - k * 3.6] * 2, color="#888", lw=0.7, zorder=6)
    # caja de bornes
    rbox(ax, x0 + 44, y0 + 76, 30, 17, body, r=1.5, z=3)
    rect(ax, x0 + 42, y0 + 91, 34, 3, dark, z=4)
    ax.add_patch(Circle((x0 + 74 + 3, y0 + 83), 3.2, fc="#22262b", ec=EDGE, lw=0.6, zorder=4))
    t(ax, x0 + 50, y0 + 46, "M\n3~", fs=fs + 2, color="white", weight="bold", z=9)


def caja_bornes(ax, x0, y0, kind, fs=7.5):
    """Caja de bornes abierta, vista desde arriba: 6 espárragos y puentes."""
    rbox(ax, x0, y0, 70, 64, "#3d6d99", ec=EDGE, r=4, z=1)
    rbox(ax, x0 + 5, y0 + 5, 60, 54, "#e9dcc0", ec="#9b8a66", r=2, z=2)   # placa aislante
    top = ["U1", "V1", "W1"]
    bot = ["W2", "U2", "V2"]
    xs = [x0 + 17, x0 + 35, x0 + 53]
    yt, yb = y0 + 40, y0 + 18
    if kind == "Y":
        rbox(ax, xs[0] - 4, yb - 4, xs[2] - xs[0] + 8, 8, COPPER, ec="#8a5a22", r=2, z=3)
    else:
        for x in xs:
            rbox(ax, x - 4, yb - 4, 8, yt - yb + 8, COPPER, ec="#8a5a22", r=2, z=3)
    for row, y in ((top, yt), (bot, yb)):
        for x, lab in zip(xs, row):
            ax.add_patch(Circle((x, y), 3.2, fc="#d9b45a", ec="#8a6a1e", lw=0.8, zorder=4))
            ax.add_patch(Circle((x, y), 1.3, fc="#8a6a1e", ec="none", zorder=5))
            t(ax, x + 6.3, y + (5.3 if row is top else -5.3), lab, fs=fs, weight="bold")
    # cables de la red L1 L2 L3
    for x, col, lab in zip(xs, ("#7b4a1e", "#222222", "#8c8c8c"), ("L1", "L2", "L3")):
        ax.plot([x, x], [yt + 3, y0 + 76], color=col, lw=3.2, solid_capstyle="butt", zorder=6)
        t(ax, x, y0 + 80, lab, fs=fs, weight="bold")


# ----------------------------------------------------------------- figuras
def fig_protecciones():
    c = Canvas(-6, -16, 196, 120, k=0.05)
    ax = c.ax
    rail(ax, -4, 188, 45)
    mcb(ax, 0, 0, ["1", "3", "5"], ["2", "4", "6"], "C16", sub="400 V~")
    mcb(ax, 66, 0, ["1", "N"], ["2", "N"], "25 A", sub="IΔn 30 mA", rcd=True)
    portafusible(ax, 114, 4)
    cartucho(ax, 140, 30)
    t(ax, 159, 22, "cartucho 10×38", fs=6, color="#555")
    for x, s in ((27, "Termomagnético 3P"), (84, "Diferencial 2P"), (123, "Portafusible"),
                 (159, "Fusible")):
        t(ax, x, -9, s, fs=7.5, weight="bold")
    c.save("a_protecciones")


def fig_contactor_termico():
    c = Canvas(-4, -20, 114, 120, k=0.065)
    ax = c.ax
    contactor(ax, 0, 6)
    termico(ax, 62, 6)
    t(ax, 22.5, 93, "Contactor KM", fs=8.5, weight="bold")
    t(ax, 84.5, 93, "Relé térmico F", fs=8.5, weight="bold")
    t(ax, 84.5, 81, "se enchufa DEBAJO del contactor,\nen 2/T1 4/T2 6/T3", fs=6.3, color="#555")
    # leyenda de colores
    for i, (col, s_) in enumerate(((MAIN_C, "Fuerza\n1-2, 3-4, 5-6"), (COIL_C, "Bobina A1-A2\nTérmico 95-96"),
                                   (AUX_C, "Auxiliar NA\n13-14 · 97-98"))):
        x = 0 + i * 37
        rect(ax, x, -12, 5, 5, col, ec=col, z=3)
        t(ax, x + 7, -9.5, s_, fs=6.5, ha="left")
    c.save("a_contactor_termico")


def fig_mando():
    c = Canvas(-4, -46, 300, 92, k=0.05)
    ax = c.ax
    pulsador(ax, 20, 22, GREEN, "I", "MARCHA S1", ("13", "14", "NA"))
    pulsador(ax, 62, 22, "#1f1f1f", "O", "PARO S0", ("11", "12", "NC"))
    pulsador(ax, 110, 22, RED, "", "EMERGENCIA", ("11", "12", "NC"), mushroom=True)
    piloto(ax, 160, 22, "#0d7a40", "#7dffb5", "MARCHA H1")
    piloto(ax, 202, 22, "#9b1d17", "#ffb0a8", "FALLA H2")
    temporizador(ax, 236, -44)
    c.save("a_mando")


def fig_motor():
    c = Canvas(-4, -4, 310, 104, k=0.045)
    ax = c.ax
    motor(ax, 0, 0)
    caja_bornes(ax, 150, 4, "Y")
    caja_bornes(ax, 232, 4, "D")
    t(ax, 185, -0.5, "Estrella (Y)", fs=8, weight="bold")
    t(ax, 267, -0.5, "Triángulo (Δ)", fs=8, weight="bold")
    c.save("a_motor_bornes")


def fig_consignacion():
    c = Canvas(-4, -6, 196, 112, k=0.05)
    ax = c.ax
    # candado de seguridad
    ax.add_patch(Arc((26, 66), 30, 36, theta1=0, theta2=180, lw=5, color="#9aa0a6", zorder=2))
    ax.plot([11, 11], [50, 66], color="#9aa0a6", lw=5, zorder=2)
    ax.plot([41, 41], [50, 66], color="#9aa0a6", lw=5, zorder=2)
    rbox(ax, 6, 14, 40, 42, RED, ec="#8e1f19", r=4, z=3)
    ax.add_patch(Circle((26, 38), 3.5, fc="#3a0c09", ec="none", zorder=4))
    ax.add_patch(Polygon([(24.5, 37), (27.5, 37), (28.5, 28), (23.5, 28)], fc="#3a0c09", ec="none",
                         zorder=4))
    t(ax, 26, 20, "personal", fs=6.5, color="white")
    t(ax, 26, 4, "Candado (uno por persona)", fs=7, weight="bold")
    # tarjeta
    rbox(ax, 62, 14, 46, 76, "white", ec=EDGE, r=2, z=2)
    rect(ax, 62, 66, 46, 24, RED, ec=EDGE, z=3)
    ax.add_patch(Circle((85, 84), 3, fc="white", ec=EDGE, lw=0.8, zorder=4))
    t(ax, 85, 73, "PELIGRO", fs=9, color="white", weight="bold")
    t(ax, 85, 52, "NO OPERAR", fs=7.5, weight="bold")
    t(ax, 85, 38, "Personal\ntrabajando", fs=6.5)
    t(ax, 85, 23, "Nombre: ______\nFecha: ______", fs=5.5, color="#555")
    ax.plot([85, 41], [87, 60], color="#555", lw=0.8, zorder=1)
    t(ax, 85, 4, "Tarjeta", fs=7, weight="bold")
    # detector de tensión bipolar
    rbox(ax, 128, 20, 22, 72, "#f0b400", ec=EDGE, r=4, z=2)
    rbox(ax, 132, 42, 14, 44, "#2b2b2b", ec="#2b2b2b", r=1.5, z=3)
    for k, v in enumerate(("400", "230", "120", "50", "24", "12")):
        y = 81 - k * 7
        ax.add_patch(Circle((136, y), 1.6, fc="#ff5a4f" if k > 1 else "#ffd3cf", ec="none", zorder=4))
        t(ax, 142.5, y, v, fs=5, color="white")
    rect(ax, 137.5, 8, 3, 12, "#d6d9dd", z=2)
    t(ax, 139, 33, "V", fs=8, weight="bold")
    ax.plot([139, 139, 165, 170], [92, 98, 98, 86], color="#2b2b2b", lw=1.8, zorder=1)
    rbox(ax, 164, 40, 12, 46, "#f0b400", ec=EDGE, r=3, z=2)
    rect(ax, 168.5, 28, 3, 12, "#d6d9dd", z=2)
    t(ax, 152, 4, "Detector de tensión", fs=7, weight="bold")
    c.save("a_consignacion")


def fig_tablero():
    """Tablero de un arranque directo (ejercicio L1) con la puerta abierta al lado."""
    c = Canvas(-6, -10, 560, 440, k=0.022)
    ax = c.ax
    # placa de montaje
    rect(ax, 0, 0, 330, 420, "#f0ebe1", ec="#9b9384", lw=1.2, z=0)
    duct = "#9da2a8"

    def canaleta(x, y, w, h):
        rect(ax, x, y, w, h, duct, ec="#7f848a", lw=0.8, z=1)
        if w > h:
            for xx in range(int(x) + 4, int(x + w) - 3, 9):
                ax.plot([xx, xx], [y + 2, y + h - 2], color="#b9bdc2", lw=1.2, zorder=1)
        else:
            for yy in range(int(y) + 4, int(y + h) - 3, 9):
                ax.plot([x + 2, x + w - 2], [yy, yy], color="#b9bdc2", lw=1.2, zorder=1)

    canaleta(14, 388, 302, 20)
    canaleta(14, 252, 302, 20)
    canaleta(14, 82, 302, 20)
    canaleta(14, 102, 20, 150)
    canaleta(296, 102, 20, 150)
    canaleta(14, 272, 20, 116)
    canaleta(296, 272, 20, 116)
    # riel 1: Q1 y F2
    rail(ax, 40, 290, 330)
    mcb(ax, 70, 285, ["1", "3", "5"], ["2", "4", "6"], "C16", fs=3.6)
    portafusible(ax, 150, 289, fs=3.6)
    # riel 2: KM1 + F1
    rail(ax, 40, 290, 210)
    contactor(ax, 120, 168, fs=3.6, show_bottom=False)
    termico(ax, 120, 114, fs=3.6, pins=False)
    # riel 3: bornera X1
    rail(ax, 40, 290, 42)
    for i in range(12):
        x = 60 + i * 9
        pe = i in (3, 11)
        rect(ax, x, 18, 8, 48, "#e8d24a" if pe else "#a9b0b8", ec=EDGE, lw=0.6, z=3)
        if pe:
            for yy in range(20, 64, 6):
                ax.plot([x + 0.5, x + 7.5], [yy, yy + 4], color=GREEN, lw=1.2, zorder=4)
        ax.add_patch(Circle((x + 4, 58), 2.2, fc=SCREW, ec=EDGE, lw=0.5, zorder=5))
        ax.add_patch(Circle((x + 4, 26), 2.2, fc=SCREW, ec=EDGE, lw=0.5, zorder=5))
    # cables (cortos, del borne a la canaleta)
    pwr = ("#7b4a1e", "#222222", "#8c8c8c")
    for i in range(3):
        x = 79 + 18 * i
        ax.plot([x, x], [370, 388], color=pwr[i], lw=1.6, zorder=6)
        ax.plot([x, x], [290, 272], color=pwr[i], lw=1.6, zorder=6)
        xc = 134.5 + 9 * i
        ax.plot([xc, xc], [244, 252], color=pwr[i], lw=1.6, zorder=6)
        ax.plot([xc, xc], [118, 102], color=pwr[i], lw=1.6, zorder=6)
        xb = 64 + 9 * i
        ax.plot([xb, xb], [64, 82], color=pwr[i], lw=1.6, zorder=6)
    for x0_, y0_, y1_ in ((159, 289 + 73, 388), (159, 298, 272), (125.5, 244, 252)):
        ax.plot([x0_, x0_], [y0_, y1_], color="#d0342c", lw=1.2, zorder=6)
    for i in range(4, 11):
        ax.plot([64 + 9 * i] * 2, [64, 82], color="#d0342c" if i < 9 else "#2f6db5", lw=1.2, zorder=6)
    # etiquetas
    tag(ax, 136, 340, "Q1", fs=9)
    tag(ax, 182, 340, "F2", fs=9)
    tag(ax, 182, 228, "KM1", fs=9)
    tag(ax, 182, 145, "F1", fs=9)
    tag(ax, 230, 42, "X1", fs=9)
    t(ax, 252, 352, "Riel DIN", fs=6.5, color="#555")
    t(ax, 252, 260, "Canaleta", fs=6.5, color="#555")
    t(ax, 236, 26, "PE verde-amarillo", fs=5.5, color="#555")
    t(ax, 165, -6, "Placa de montaje", fs=8, weight="bold")
    # puerta (vista interior desde el frente)
    rect(ax, 360, 130, 190, 290, "#e2e4e7", ec="#80858b", lw=1.2, z=0)
    for k, (cx, cy, col, glow, mark, tg) in enumerate((
            (410, 360, GREEN, None, "I", "S1"), (500, 360, "#1f1f1f", None, "O", "S0"),
            (410, 250, "#0d7a40", "#7dffb5", "", "H1"), (500, 250, "#9b1d17", "#ffb0a8", "", "H2"))):
        ax.add_patch(Circle((cx, cy), 20, fc="#cfd2d6", ec=EDGE, lw=0.8, zorder=2))
        ax.add_patch(Circle((cx, cy), 15, fc=col, ec="none", zorder=4))
        if glow:
            for r_, a in ((10, 0.35), (6, 0.6)):
                ax.add_patch(Circle((cx, cy), r_, fc=glow, ec="none", alpha=a, zorder=5))
        else:
            t(ax, cx, cy, mark, fs=9, color="white", weight="bold")
        tag(ax, cx, cy - 34, tg, fs=9)
    t(ax, 455, 146, "Puerta: mando y señalización", fs=7.5, weight="bold")
    # manguera flexible placa ↔ puerta
    xs = [316, 330, 345, 360]
    ax.plot(xs, [200, 214, 196, 210], color="#555", lw=3, zorder=1)
    # motor
    motor(ax, 400, 0, fs=5)
    tag(ax, 500, 108, "M1", fs=9)
    ax.plot([330, 360, 380], [40, 40, 50], color="#555", lw=3, zorder=1)
    c.save("a_tablero")


if __name__ == "__main__":
    fig_protecciones()
    fig_contactor_termico()
    fig_mando()
    fig_motor()
    fig_consignacion()
    fig_tablero()
    print("ok")
