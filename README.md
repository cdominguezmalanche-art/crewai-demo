# MILPA - Prototipo multiagente con CrewAI

Proyecto Agentes, Fase 3. Materia de Inteligencia Artificial.

MILPA es un sistema de apoyo para la orientación financiera y la preparación
para el retiro de trabajadores informales. El prototipo usa CrewAI con cuatro
agentes especializados que trabajan en orden: perfilamiento, dictamen
normativo, escenarios financieros y síntesis educativa.

## Contenido

- `MILPA_Agentes.ipynb`: notebook con los agentes, las tareas y el Crew.
  Incluye las salidas de la corrida de demostración.
- `requirements.txt`: librerías necesarias.
- `.env.example`: plantilla para la llave del modelo.

## Cómo correrlo

1. Crea el entorno virtual e instala las librerías:

       python -m venv .venv
       .venv\Scripts\python.exe -m pip install -r requirements.txt

   En Mac o Linux: `.venv/bin/python -m pip install -r requirements.txt`

2. Elige el modelo de lenguaje.

   **Con Claude.** Copia `.env.example` como `.env` y escribe la llave.

   **Con un modelo local.** Instala Ollama, descarga el modelo con
   `ollama pull llama3.1` y en la segunda celda del notebook cambia la línea
   del modelo por la que está comentada abajo.

3. Abre `MILPA_Agentes.ipynb`, selecciona el entorno `.venv` como kernel y
   ejecuta todas las celdas.

## Notas

- Los datos del caso de prueba son ficticios.
- Todas las cifras las calculan funciones de Python. Los agentes solo las
  interpretan y explican.
- El archivo `.env` no se sube al repositorio.
