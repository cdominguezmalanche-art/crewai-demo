"""
Demo de CrewAI con Gemini: equipo de 3 agentes que investiga, redacta y revisa un informe.
La clave se lee de la variable de entorno GEMINI_API_KEY (nunca se escribe en el código).
"""

import os
import sys
from crewai import Agent, Task, Crew, Process, LLM

# ---------------------------------------------------------------------------
# 0. MODELO DE LENGUAJE
# ---------------------------------------------------------------------------
mi_llave = os.getenv("GEMINI_API_KEY")
if not mi_llave:
    sys.exit("Falta la variable de entorno GEMINI_API_KEY.")

llm = LLM(
    model="gemini/gemini-3.8-flash",  # prefijo "gemini/" = proveedor Google
    api_key=mi_llave,
    temperature=0.3,                  # baja = respuestas más estables
)

# ---------------------------------------------------------------------------
# 1. AGENTES (Agent): rol, objetivo y backstory definen su comportamiento.
# {tema} se rellena con las entradas del kickoff.
# ---------------------------------------------------------------------------
investigador = Agent(
    role="Investigador Senior sobre {tema}",
    goal="Reunir los datos y puntos clave más relevantes sobre {tema}.",
    backstory="Eres un analista meticuloso. Siempre distingues hechos de opiniones y señalas cuando algo es incierto.",
    llm=llm,
    verbose=True,            # imprime el razonamiento paso a paso (el "log")
    allow_delegation=False,  # no delega trabajo en otros agentes
)

redactor = Agent(
    role="Redactor Técnico",
    goal="Convertir la investigación sobre {tema} en un informe claro y breve.",
    backstory="Eres un redactor que explica temas complejos con lenguaje sencillo, estructura lógica y ejemplos concretos.",
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

revisor = Agent(
    role="Revisor de Calidad",
    goal="Verificar coherencia, claridad y ausencia de afirmaciones sin sustento.",
    backstory="Eres un editor exigente. Corriges errores, eliminas redundancias y entregas la versión final lista para publicar.",
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

# ---------------------------------------------------------------------------
# 2. TAREAS (Task): qué hacer, qué producir y quién lo hace.
# context=[...] pasa el resultado de tareas previas como insumo.
# ---------------------------------------------------------------------------
tarea_investigar = Task(
    description="Investiga el tema '{tema}' para el público '{audiencia}'. Identifica 5 puntos clave, con una breve justificación de cada uno.",
    expected_output="Lista de 5 puntos clave con su justificación.",
    agent=investigador,
)

tarea_redactar = Task(
    description="Con la investigación disponible, redacta un informe de máximo 300 palabras sobre '{tema}' dirigido a '{audiencia}'. Incluye introducción, desarrollo y conclusión.",
    expected_output="Informe de máximo 300 palabras con introducción, desarrollo y conclusión.",
    agent=redactor,
    context=[tarea_investigar],  # recibe la salida de la tarea 1
)

tarea_revisar = Task(
    description="Revisa el informe: corrige redacción, elimina redundancias y verifica que sea coherente con la investigación. Entrega la versión final consolidada.",
    expected_output="Informe final revisado, en formato Markdown.",
    agent=revisor,
    context=[tarea_investigar, tarea_redactar],
)

# ---------------------------------------------------------------------------
# 3. TRIPULACIÓN (Crew): agrupa agentes y tareas; Process.sequential las
# ejecuta en orden. output_log_file guarda el log en un archivo.
# ---------------------------------------------------------------------------
crew = Crew(
    agents=[investigador, redactor, revisor],
    tasks=[tarea_investigar, tarea_redactar, tarea_revisar],
    process=Process.sequential,
    verbose=True,
    output_log_file="log_crew.txt",
)

# ---------------------------------------------------------------------------
# 4. CORRIDA DE DEMOSTRACIÓN
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    entradas = {
        "tema": "El impacto de la inteligencia artificial en la educación superior",
        "audiencia": "directivos universitarios",
    }

    print("=== ENTRADAS PROPORCIONADAS ===")
    for k, v in entradas.items():
        print(f"- {k}: {v}")
    print("\n=== INICIO DE EJECUCIÓN (log de razonamiento) ===\n")

    resultado = crew.kickoff(inputs=entradas)

    print("\n=== RESPUESTA FINAL CONSOLIDADA ===\n")
    print(resultado.raw)

    with open("respuesta_final.md", "w", encoding="utf-8") as f:
        f.write(resultado.raw)
