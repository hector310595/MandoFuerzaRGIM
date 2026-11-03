"""Mini-librería para dibujar esquemas eléctricos de mando y fuerza (IEC 60617 simplificado).

Convenciones (las mismas que se piden en CADe_SIMU):
  * Esquema desarrollado: los aparatos se dibujan vertical, en estado de reposo
    (sin tensión, sin accionar).
  * Mando: entre una línea superior (L1, fase de mando) y una inferior (N).
  * Fuerza: tres líneas verticales L1, L2, L3 que bajan hasta el motor.
  * Cada contacto lleva su designación (KM1, S1…) y la numeración de bornes.

Unidad de dibujo: 1 u = altura de un contacto.
"""
import matplotlib

matplotlib.use("Agg")
matplotlib.rcParams["svg.hashsalt"] = "rgim-mando"
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Arc, Circle, Rectangle  # noqa: E402

INK = "#1a1a1a"
LINK = "#1f4e9c"      # enlaces mecánicos (discontinuos)
RED = "#c0392b"
GREEN = "#0b7a53"
SCALE = 0.42
TERM_FS = 7
LABEL_FS = 10
LW = 1.5


class Sheet:
    def __init__(self, w, h, x0=0.0, y0=0.0):
        self.fig = plt.figure(figsize=(w * SCALE, h * SCALE))
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set_xlim(x0, x0 + w)
        self.ax.set_ylim(y0, y0 + h)
        self.ax.set_aspect("equal")
        self.ax.axis("off")

    # -------------------------------------------------------------- básicos
    def seg(self, a, b, lw=LW, color=INK, ls="-", z=3):
        self.ax.plot([a[0], b[0]], [a[1], b[1]], color=color, lw=lw, ls=ls,
                     solid_capstyle="butt", zorder=z)

    def wire(self, pts, lw=LW, color=INK):
        self.ax.plot([p[0] for p in pts], [p[1] for p in pts], color=color, lw=lw,
                     solid_capstyle="butt", solid_joinstyle="miter", zorder=2)

    def dot(self, p):
        self.ax.add_patch(Circle(p, 0.07, color=INK, zorder=5))

    def text(self, p, s, fs=LABEL_FS, ha="center", va="center", color=INK, weight="normal",
             style="normal"):
        self.ax.text(p[0], p[1], s, fontsize=fs, ha=ha, va=va, color=color, fontweight=weight,
                     fontstyle=style, zorder=6)

    def link(self, a, b):
        """Enlace mecánico (línea discontinua)."""
        self.seg(a, b, lw=1.0, color=LINK, ls=(0, (3, 2)), z=2)

    def _terms(self, x, ytop, terms, side=1, h=1.0):
        if not terms:
            return
        self.text((x + side * 0.12, ytop - 0.1), terms[0], fs=TERM_FS, ha="left" if side > 0 else "right",
                  color="#444")
        self.text((x + side * 0.12, ytop - h + 0.1), terms[1], fs=TERM_FS,
                  ha="left" if side > 0 else "right", color="#444")

    # -------------------------------------------------------------- contactos
    def contact(self, x, ytop, kind="NO", label=None, terms=None, act=None, main=False,
                breaker=False, label_dx=None):
        """Contacto vertical entre (x, ytop) y (x, ytop-1). Devuelve (top, bottom, mid_blade).
        kind: 'NO' (normalmente abierto) | 'NC' (normalmente cerrado)
        act: None | 'push' | 'thermal' | 'timer' | 'mech'"""
        yt, yb = ytop - 0.33, ytop - 0.67
        self.seg((x, ytop), (x, yt))
        self.seg((x, ytop - 1), (x, yb))
        if kind == "NO":
            tip = (x - 0.3, yt + 0.02)
            self.seg((x, yb), tip)
        else:
            self.seg((x, yt), (x + 0.22, yt))
            tip = (x + 0.3, yt + 0.05)
            self.seg((x, yb), tip)
        m = ((x + tip[0]) / 2, (yb + tip[1]) / 2)
        if main:  # función contactor: semicírculo en el contacto fijo
            self.ax.add_patch(Arc((x, yt - 0.0), 0.2, 0.2, theta1=0, theta2=180, ec=INK, lw=1.1,
                                  zorder=3))
        if breaker:  # función interruptor: aspa
            d = 0.08
            self.seg((x - d, yt - d), (x + d, yt + d), lw=1.2)
            self.seg((x - d, yt + d), (x + d, yt - d), lw=1.2)
        ax_ = x - 0.75
        if act == "push":
            self.link(m, (ax_, m[1]))
            self.seg((ax_, m[1] - 0.15), (ax_, m[1] + 0.15), lw=1.3)
            self.seg((ax_, m[1] - 0.15), (ax_ - 0.12, m[1] - 0.15), lw=1.3)
            self.seg((ax_, m[1] + 0.15), (ax_ - 0.12, m[1] + 0.15), lw=1.3)
        elif act == "thermal":
            self.link(m, (ax_, m[1]))
            s = 0.12
            pts = [(ax_, m[1]), (ax_ - s, m[1]), (ax_ - s, m[1] + s), (ax_ - 2 * s, m[1] + s),
                   (ax_ - 2 * s, m[1]), (ax_ - 3 * s, m[1])]
            self.wire(pts, lw=1.2)
        elif act == "timer":
            self.link(m, (ax_ + 0.2, m[1]))
            self.ax.add_patch(Arc((ax_ + 0.05, m[1]), 0.3, 0.36, theta1=90, theta2=270, ec=INK,
                                  lw=1.2, zorder=3))
            self.seg((ax_ - 0.1, m[1] + 0.18), (ax_ - 0.1, m[1] - 0.18), lw=1.2)
        elif act == "mech":
            self.link(m, (ax_, m[1]))
        self._terms(x, ytop, terms)
        if label:
            dx = label_dx if label_dx is not None else {"push": 1.05, "timer": 1.05, "thermal": 1.3}.get(act, 0.45)
            self.text((x - dx, ytop - 0.5), label, ha="right", weight="bold")
        return (x, ytop), (x, ytop - 1), m

    def coil(self, x, ytop, label=None, timer=False, terms=("A1", "A2")):
        """Bobina (contactor / relé). Ocupa ytop .. ytop-1."""
        self.seg((x, ytop), (x, ytop - 0.3))
        self.seg((x, ytop - 0.7), (x, ytop - 1))
        self.ax.add_patch(Rectangle((x - 0.3, ytop - 0.7), 0.6, 0.4, fill=False, ec=INK, lw=LW,
                                    zorder=3))
        if timer:  # bobina con retardo a la conexión
            self.ax.add_patch(Rectangle((x - 0.62, ytop - 0.7), 0.32, 0.4, fill=False, ec=INK,
                                        lw=LW, zorder=3))
            self.seg((x - 0.62, ytop - 0.7), (x - 0.3, ytop - 0.3), lw=1.0)
            self.seg((x - 0.62, ytop - 0.3), (x - 0.3, ytop - 0.7), lw=1.0)
        self._terms(x, ytop, terms)
        if label:
            self.text((x - (0.75 if timer else 0.45), ytop - 0.5), label, ha="right", weight="bold")
        return (x, ytop), (x, ytop - 1)

    def lamp(self, x, ytop, label=None, color=None, terms=("X1", "X2")):
        self.seg((x, ytop), (x, ytop - 0.28))
        self.seg((x, ytop - 0.72), (x, ytop - 1))
        c = (x, ytop - 0.5)
        self.ax.add_patch(Circle(c, 0.22, fill=bool(color), fc=color or "none", ec=INK, lw=LW,
                                 alpha=1, zorder=3))
        d = 0.155
        self.seg((c[0] - d, c[1] - d), (c[0] + d, c[1] + d), lw=1.1)
        self.seg((c[0] - d, c[1] + d), (c[0] + d, c[1] - d), lw=1.1)
        self._terms(x, ytop, terms)
        if label:
            self.text((x - 0.45, ytop - 0.5), label, ha="right", weight="bold")
        return (x, ytop), (x, ytop - 1)

    def fuse(self, x, ytop, label=None, terms=None):
        self.ax.add_patch(Rectangle((x - 0.1, ytop - 0.75), 0.2, 0.5, fill=False, ec=INK, lw=LW,
                                    zorder=3))
        self.seg((x, ytop), (x, ytop - 1))
        self._terms(x, ytop, terms)
        if label:
            self.text((x - 0.4, ytop - 0.5), label, ha="right", weight="bold")
        return (x, ytop), (x, ytop - 1)

    # ---------------------------------------------------------------- fuerza
    def multipole(self, xs, ytop, label, terms, main=False, breaker=False):
        mids = []
        for x, t in zip(xs, terms):
            _, _, m = self.contact(x, ytop, "NO", terms=t, main=main, breaker=breaker)
            mids.append(m)
        self.link((mids[0][0] - 0.25, mids[0][1]), mids[-1])
        self.text((xs[0] - 0.75, ytop - 0.5), label, ha="right", weight="bold")
        return [(x, ytop - 1) for x in xs]

    def thermal3(self, xs, ytop, label, terms=(("1", "2"), ("3", "4"), ("5", "6"))):
        for x, t in zip(xs, terms):
            self.seg((x, ytop), (x, ytop - 0.25))
            self.seg((x, ytop - 0.75), (x, ytop - 1))
            self.ax.add_patch(Rectangle((x - 0.18, ytop - 0.75), 0.36, 0.5, fill=False, ec=INK,
                                        lw=LW, zorder=3))
            s = 0.1
            y0 = ytop - 0.5
            self.wire([(x, ytop - 0.25), (x, y0 + s), (x - s, y0 + s), (x - s, y0 - s), (x, y0 - s),
                       (x, ytop - 0.75)], lw=1.1)
            self._terms(x + 0.15, ytop, t)
        self.link((xs[0] + 0.18, ytop - 0.5), (xs[-1] - 0.18, ytop - 0.5))
        self.text((xs[0] - 0.4, ytop - 0.5), label, ha="right", weight="bold")
        return [(x, ytop - 1) for x in xs]

    def motor(self, xs, ytop, label="M1", six=False, r=0.75):
        """Motor trifásico bajo las líneas xs (3). Devuelve centro."""
        xc = sum(xs) / len(xs)
        cy = ytop - 1.4 - r
        self.ax.add_patch(Circle((xc, cy), r, fill=False, ec=INK, lw=LW, zorder=3))
        self.text((xc, cy + 0.12), "M", fs=13, weight="bold")
        self.text((xc, cy - 0.3), "3~", fs=10)
        names = ["U1", "V1", "W1"]
        for x, n in zip(xs, names):
            # bajar y converger al círculo
            tx = xc + (x - xc) * 0.55
            self.wire([(x, ytop), (x, ytop - 0.6), (tx, cy + r * 0.92)])
            self.text((x + 0.12, ytop - 0.3), n, fs=TERM_FS, ha="left", color="#444")
        if six:
            for x, n in zip(xs, ["W2", "U2", "V2"]):
                bx = xc + (x - xc) * 0.55
                self.wire([(bx, cy - r * 0.92), (x, cy - r - 0.6), (x, cy - r - 1.0)])
                self.text((x + 0.12, cy - r - 0.75), n, fs=TERM_FS, ha="left", color="#444")
        self.text((xc - r - 0.25, cy), label, ha="right", weight="bold")
        return (xc, cy)

    def earth(self, p):
        x, y = p
        self.seg((x, y), (x, y - 0.25))
        for i, w in enumerate((0.3, 0.2, 0.1)):
            self.seg((x - w, y - 0.25 - i * 0.09), (x + w, y - 0.25 - i * 0.09), lw=1.2)

    def rail(self, x0, x1, y, name, color=INK):
        self.seg((x0, y), (x1, y), lw=1.8, color=color)
        self.text((x0 - 0.15, y), name, ha="right", fs=9, weight="bold", color=color)

    def save(self, path_noext):
        self.fig.savefig(path_noext + ".png", dpi=220, facecolor="white")
        self.fig.savefig(path_noext + ".svg", facecolor="white", metadata={"Date": None})
        plt.close(self.fig)
