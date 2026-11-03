#!/usr/bin/env bash
# Regenera figuras, presentaciones y documentos.
# Requisitos: python3 con matplotlib, python-pptx, python-docx, Pillow.
set -euo pipefail
cd "$(dirname "$0")"
python3 src/esquemas.py
python3 src/aparatos.py
python3 src/build_teoria.py
python3 src/build_lab.py
python3 src/build_docs.py
