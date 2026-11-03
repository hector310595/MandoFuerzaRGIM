# Seguridad eléctrica y esquemas de mando y fuerza · RGIM (PUCP)

Material de la semana de **seguridad eléctrica y esquemas de mando y fuerza** del curso
*Representación Gráfica para Ingeniería Mecatrónica*: 2 h de teoría y 3 h de laboratorio en
CADe_SIMU.

## Contenido

| Carpeta / archivo | Para quién | Qué es |
|---|---|---|
| `sesion1_teoria/RGIM_S1_Seguridad_Mando_Fuerza_Teoria.pptx` | Docente (proyectar) | 33 diapositivas con plantilla PUCP (incluye ilustraciones de los aparatos reales); notas del orador con tiempos |
| `sesion2_laboratorio/RGIM_S2_Laboratorio_CADeSIMU.pptx` | Docente (proyectar) | Enunciados y preguntas guía; **las soluciones son diapositivas ocultas** |
| `sesion2_laboratorio/RGIM_Guia_Laboratorio_Alumno.docx` | Alumnos | Repaso, catálogo de símbolos, CADe_SIMU, ejercicios L0–L5 y lista de verificación |
| `docente/RGIM_Solucionario_Laboratorio.docx` | Docente | Catálogo de símbolos y, por ejercicio: fuerza, mando, funcionamiento, tabla de estados, componentes y errores típicos |
| `docente/RGIM_Guia_CADeSIMU_Paso_a_Paso.docx` | Docente | Procedimiento base en CADe_SIMU, problemas frecuentes y armado paso a paso de cada ejercicio |
| `docente/RGIM_Plan_de_Sesiones.docx` | Docente | Cronograma de ambas sesiones, preparación y evaluación |
| `figuras/` | — | Símbolos, esquemas e ilustraciones de aparatos reales (`a_*`, generadas con `src/aparatos.py`) en PNG y SVG |
| `cadesimu/` | Docente | Lugar para guardar los archivos de CADe_SIMU probados |
| `src/` | — | Generadores (Python) de todo el material |

## Ejercicios del laboratorio

| Ejercicio | Tema |
|---|---|
| L0 | Lámpara con pulsador (primer circuito) |
| L1 | Arranque directo con marcha-paro, térmico y pilotos |
| L2 | Mando desde dos puntos |
| L3 | Inversión de giro con enclavamiento |
| L4 | Arranque estrella-triángulo temporizado |
| L5 | Reto: arranque secuencial de dos motores |

## Convenciones

- **Tensiones:** fuerza 3 × 380 V, 60 Hz; mando 220 V (L1-N) con fusible propio.
- **Designaciones clásicas:** Q, KM, KT, F, S, H, M. La teoría menciona la IEC 81346-2 vigente.
- **Bornes:** A1-A2; 1-2/3-4/5-6; 13-14 NA; 21-22 NC; 95-96 / 97-98; 55-56 / 67-68 (temporizado).

## Regenerar el material

```bash
./build_all.sh
```
