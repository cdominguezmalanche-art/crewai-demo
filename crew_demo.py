"""
Demo de CrewAI: equipo de 3 agentes que investiga, redacta y revisa un informe.

Requisitos:
    pip install crewai
    export OPENAI_API_KEY="tu_clave"      # Windows: set OPENAI_API_KEY=tu_clave

Ejecución (guarda además la salida de consola como evidencia):
    python crew_demo.py | tee salida_consola.txt
"""

from crewai import Agent, Task, Crew, Process, LLM

# ---------------------------------------------------------------------------
# 0. MODELO DE LENGUAJE
# Se define una sola vez y se comparte entre los agentes.
# temperature baja = respuestas más estables y reproducibles.
# ---------------------------------------------------------------------------
llm = LLM(model="gpt-4o-mini", temperature=0.3)

# ---------------------------------------------------------------------------
# 1. AGENTES (Agent)
# Cada agente tiene: rol (qué es), objetivo (qué busca) y backstory
# (contexto que moldea su estilo de razonamiento).
# {tema} es un placeholder que se rellena con las entradas del kickoff.
# ---------------------------------------------------------------------------
investigador = Agent(
    role="Investigador Senior sobre {tema}",
    goal="Reunir los datos y puntos clave más relevantes sobre {tema}.",
    backstory=(
        "Eres un analista meticuloso. Siempre distingues hechos de opiniones "
        "y señalas cuando algo es incierto."
    ),
    llm=llm,
    verbose=True,            # imprime el razonamiento paso a paso (el "log")
    allow_delegation=False,  # este agente no delega en otros
)

redactor = Agent(
    role="Redactor Técnico",
    goal="Convertir la investigación sobre {tema} en un informe claro y breve.",
    backstory=(
        "Eres un redactor que explica temas complejos con lenguaje sencillo, "
        "estructura lógica y ejemplos concretos."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

revisor = Agent(
    role="Revisor de Calidad",
    goal="Verificar coherencia, claridad y ausencia de afirmaciones sin sustento.",
    backstory=(
        "Eres un editor exigente. Corriges errores, eliminas redundancias y "
        "entregas la versión final lista para publicar."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

# ---------------------------------------------------------------------------
# 2. TAREAS (Task)
# Cada tarea indica: qué hacer (description), qué debe producir
# (expected_output) y quién la hace (agent).
# context=[...] pasa el resultado de tareas previas como insumo.
# ---------------------------------------------------------------------------
tarea_investigar = Task(
    description=(
        "Investiga el tema '{tema}' para el público '{audiencia}'. "
        "Identifica 5 puntos clave, con una breve justificación de cada uno."
    ),
    expected_output="Lista de 5 puntos clave con su justificación.",
    agent=investigador,
)

tarea_redactar = Task(
    description=(
        "Con la investigación disponible, redacta un informe de máximo "
        "300 palabras sobre '{tema}' dirigido a '{audiencia}'. "
        "Incluye introducción, desarrollo y conclusión."
    ),
    expected_output="Informe de máximo 300 palabras con introducción, desarrollo y conclusión.",
    agent=redactor,
    context=[tarea_investigar],  # recibe la salida de la tarea 1
)

tarea_revisar = Task(
    description=(
        "Revisa el informe: corrige redacción, elimina redundancias y "
        "verifica que sea coherente con la investigación. "
        "Entrega la versión final consolidada."
    ),
    expected_output="Informe final revisado, en formato Markdown.",
    agent=revisor,
    context=[tarea_investigar, tarea_redactar],
)

# ---------------------------------------------------------------------------
# 3. TRIPULACIÓN (Crew)
# Agrupa agentes y tareas. Process.sequential ejecuta las tareas en orden.
# output_log_file guarda automáticamente el log de ejecución en un archivo.
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
# inputs: valores que sustituyen los {placeholders} de agentes y tareas.
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

    # Guarda también la respuesta final en un archivo
    with open("respuesta_final.md", "w", encoding="utf-8") as f:
        f.write(resultado.raw)
