"""Fotos reales (Wikimedia Commons, licencias libres) usadas en las presentaciones.

Las fotos ya están reducidas en figuras/fotos/ (máx. 1200 px). Este módulo guarda los
créditos que exige cada licencia y genera figuras/fotos/CREDITOS.md.
Uso: python3 src/fotos.py
"""
import os

DIR = os.path.join(os.path.dirname(__file__), "..", "figuras", "fotos")

# clave: (archivo, título en Commons, autor, licencia)
FOTOS = {
    "contactor": ("f_contactor.jpg", "JLC1-D09-10.jpg", "Редактор1511", "CC BY-SA 4.0"),
    "despiece": ("f_contactor_despiece.jpg", "Despiece contactor.jpg", "Saguzar1", "CC0"),
    "diferencial": ("f_diferencial.jpg", "Residual Current Device F202.jpg", "ABB ltd", "CC BY-SA 3.0"),
    "emergencia": ("f_emergencia.jpg", "Emergency stop button.jpg", "Cjp24", "CC BY-SA 3.0"),
    "motor": ("f_motor.jpg", "Induction motor.JPG", "ZngZng", "CC BY-SA 3.0"),
    "bloqueo": ("f_bloqueo.jpg", "Lockout on hoist brake.JPG", "Wtshymanski", "CC BY-SA 4.0"),
}


def ruta(clave):
    return os.path.join("fotos", FOTOS[clave][0])


def url(clave):
    return "https://commons.wikimedia.org/wiki/File:" + FOTOS[clave][1].replace(" ", "_")


def credito(clave):
    _, _, autor, lic = FOTOS[clave]
    return "Foto: %s · %s · Wikimedia Commons" % (autor, lic)


def creditos_md():
    lines = ["# Créditos de las fotografías", "",
             "Fotos de Wikimedia Commons, reducidas de tamaño (sin otras modificaciones).", "",
             "| Archivo | Original | Autor | Licencia |", "|---|---|---|---|"]
    for k, (f, t, a, lic) in FOTOS.items():
        lines.append("| `%s` | [%s](%s) | %s | %s |" % (f, t, url(k), a, lic))
    lines += ["", "Licencias: CC BY-SA 3.0 https://creativecommons.org/licenses/by-sa/3.0/ · "
              "CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0/ · "
              "CC0 https://creativecommons.org/publicdomain/zero/1.0/", ""]
    with open(os.path.join(DIR, "CREDITOS.md"), "w") as fh:
        fh.write("\n".join(lines))


if __name__ == "__main__":
    creditos_md()
    print("ok")
