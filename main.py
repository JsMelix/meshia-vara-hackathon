import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
import random
from datetime import date

load_dotenv()

# --- Configuración de Gemini ---
gemini_api_key = os.getenv("GOOGLE_API_KEY")
if not gemini_api_key:
    st.error("La clave de API de Gemini no se encontró. Asegúrate de haberla configurado en el archivo .env.")
    st.stop()

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=gemini_api_key)

# --- Configuración de Langchain PromptTemplate ---
prompt_template = PromptTemplate(
    input_variables=["topic"],
    template="""Crea una pregunta concisa y desafiante sobre el tema de {topic} para un mini-juego vocacional de IA. """,
)

python_duolingo_exercise_prompt = PromptTemplate(
    input_variables=["python_concept"],
    template="""Crea un ejercicio de programación en Python estilo Duolingo sobre el concepto de {python_concept}. El ejercicio debe ser un pequeño fragmento de código para completar o corregir. Proporciona el código con espacios en blanco o errores y pide al usuario que lo complete o corrija para que funcione correctamente. Incluye la solución correcta y una breve explicación de la solución y el concepto involucrado. Separa la solución correcta y la explicación con '#### Explicación:'. """,
)

rust_duolingo_exercise_prompt = PromptTemplate(
    input_variables=["rust_concept"],
    template="""Crea un ejercicio de programación en Rust estilo Duolingo sobre el concepto de {rust_concept}. El ejercicio debe ser un pequeño fragmento de código para completar o corregir. Proporciona el código con espacios en blanco o errores y pide al usuario que lo complete o corrija para que funcione correctamente. Incluye la solución correcta y una breve explicación de la solución y el concepto involucrado. Separa la solución correcta y la explicación con '#### Explicación:'. """,
)

# --- Variables de estado de la sesión ---
if 'wallet_address' not in st.session_state:
    st.session_state['wallet_address'] = None
if 'token_balance' not in st.session_state:
    st.session_state['token_balance'] = 0
if 'current_prompt' not in st.session_state:
    st.session_state['current_prompt'] = None
if 'challenge_submitted' not in st.session_state:
    st.session_state['challenge_submitted'] = False
if 'feedback' not in st.session_state:
    st.session_state['feedback'] = None
if 'python_duo_exercise_content' not in st.session_state:
    st.session_state['python_duo_exercise_content'] = None
if 'rust_duo_exercise_content' not in st.session_state:
    st.session_state['rust_duo_exercise_content'] = None
if 'python_duo_solution' not in st.session_state:
    st.session_state['python_duo_solution'] = None
if 'python_duo_explanation' not in st.session_state:
    st.session_state['python_duo_explanation'] = None
if 'rust_duo_solution' not in st.session_state:
    st.session_state['rust_duo_solution'] = None
if 'rust_duo_explanation' not in st.session_state:
    st.session_state['rust_duo_explanation'] = None
if 'knowledge_challenge_completed' not in st.session_state:
    st.session_state['knowledge_challenge_completed'] = False
if 'python_exercise_completed_today' not in st.session_state:
    st.session_state['python_exercise_completed_today'] = False
if 'rust_exercise_completed_today' not in st.session_state:
    st.session_state['rust_exercise_completed_today'] = False

# --- Funciones del Agente de IA ---
def generate_prompt(topic):
    prompt = prompt_template.format(topic=topic)
    response = llm.invoke(prompt)
    return response.content

def verify_answer(prompt, user_answer):
    verification_prompt_template = PromptTemplate(
        input_variables=["prompt", "user_answer"],
        template="""Evalúa la siguiente respuesta a la pregunta dada.
        Pregunta: {prompt}
        Respuesta del usuario: {user_answer}
        Indica si la respuesta del usuario es correcta y relevante a la pregunta.
        Responde con 'Sí' o 'No'.
        """,
    )
    verification_prompt = verification_prompt_template.format(prompt=prompt, user_answer=user_answer)
    response = llm.invoke(verification_prompt)
    return "sí" in response.content.lower()

def generate_hackathon_idea():
    prompt_idea = "Genera una idea innovadora para un proyecto de hackathon que utilice inteligencia artificial y blockchain."
    response = llm.invoke(prompt_idea)
    return response.content

def chatbot_response(query):
    response = llm.invoke(query)
    return response.content

def generate_duolingo_exercise(concept, is_rust=False):
    if is_rust:
        prompt = rust_duolingo_exercise_prompt.format(rust_concept=concept)
    else:
        prompt = python_duolingo_exercise_prompt.format(python_concept=concept)
    response = llm.invoke(prompt)
    parts = response.content.split("#### Explicación:")
    exercise = parts[0].strip()
    solution_explanation_part = parts[1].split("\n") if len(parts) > 1 else [""]
    solution = solution_explanation_part[0].strip()
    explanation = "\n".join(solution_explanation_part[1:]).strip() if len(solution_explanation_part) > 1 else None
    return exercise, solution, explanation

# --- Funciones de Blockchain (Simuladas por ahora) ---
def connect_wallet():
    st.session_state['wallet_address'] = "0x" + os.urandom(20).hex()
    st.session_state['token_balance'] = 10
    st.success(f"Wallet conectada: {st.session_state['wallet_address']}")

def award_tokens(amount=1):
    if st.session_state['wallet_address']:
        st.session_state['token_balance'] += amount
        st.success(f"¡Ejercicio completado correctamente! +{amount} tokens. Saldo actual: {st.session_state['token_balance']}")
    else:
        st.warning("Conecta tu wallet para recibir tokens.")

# --- Interfaz de Streamlit ---
st.title("Vocational AI Mini-Game")
st.write("¡Aprende sobre nuevas tecnologías y gana tokens!")

# --- Barra lateral para documentación y chatbot ---
with st.sidebar:
    st.header("Vara Network Documentation")
    st.markdown("[Enlace a la documentación de Vara Network](https://vara.network/)")

    st.header("Chat con la IA")
    chatbot_query = st.text_input("Escribe tu pregunta:", key="chatbot_input")
    if chatbot_query:
        with st.spinner("Pensando..."):
            chatbot_answer = chatbot_response(chatbot_query)
            st.write(chatbot_answer)

    st.header("Progreso")
    today = date.today()
    st.write(f"**Hoy:** {today.strftime('%Y-%m-%d')}")
    st.write("**Retos Completados:**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Conocimiento", "✅" if st.session_state['knowledge_challenge_completed'] else "❌")
    with col2:
        st.metric("Python", "✅" if st.session_state['python_exercise_completed_today'] else "❌")
    with col3:
        st.metric("Rust", "✅" if st.session_state['rust_exercise_completed_today'] else "❌")

# --- Botón para conectar la wallet ---
if st.button("Conectar Wallet"):
    connect_wallet()

# --- Mostrar la dirección de la wallet y el saldo de tokens ---
if st.session_state['wallet_address']:
    st.write(f"**Wallet:** {st.session_state['wallet_address']}")
    st.write(f"**Tokens:** {st.session_state['token_balance']}")

# --- Desafío de Conocimiento ---
st.header("Desafío de Conocimiento")
if st.button("Obtener Pregunta", disabled=st.session_state['knowledge_challenge_completed']):
    with st.spinner('Generando pregunta...'):
        st.session_state['current_prompt'] = generate_prompt(topic="Inteligencia Artificial")
        st.session_state['challenge_submitted'] = False
        st.session_state['feedback'] = None

if st.session_state['current_prompt']:
    st.info(st.session_state['current_prompt'])

    user_answer = st.text_area("Tu respuesta:", key="answer_input")

    if st.button("Enviar Respuesta", disabled=st.session_state['challenge_submitted']):
        if user_answer:
            with st.spinner('Verificando respuesta...'):
                is_correct = verify_answer(st.session_state['current_prompt'], user_answer)
                if is_correct:
                    st.session_state['feedback'] = "¡Correcto!"
                    award_tokens()
                    st.session_state['challenge_submitted'] = True
                    st.session_state['knowledge_challenge_completed'] = True
                else:
                    st.session_state['feedback'] = "Incorrecto. Inténtalo de nuevo."
        else:
            st.warning("Por favor, ingresa tu respuesta.")

    if st.session_state['feedback']:
        st.write(f"**Retroalimentación:** {st.session_state['feedback']}")

# --- Ejercicios de Programación Estilo Duolingo ---
st.header("Ejercicios de Programación Estilo Duolingo")

# --- Python Exercise ---
st.subheader("Python")
if st.button("Generar Ejercicio de Python", key="python_duo_button", disabled=st.session_state['python_exercise_completed_today']):
    with st.spinner("Generando ejercicio de Python..."):
        python_concepts = ["Listas", "Funciones", "Clases", "Bucles", "Condicionales"]
        chosen_concept = random.choice(python_concepts)
        exercise, solution, explanation = generate_duolingo_exercise(chosen_concept)
        st.session_state['python_duo_exercise_content'] = exercise
        st.session_state['python_duo_solution'] = solution
        st.session_state['python_duo_explanation'] = explanation
        st.session_state['python_duo_submitted'] = False

if st.session_state.get('python_duo_exercise_content'):
    st.write(st.session_state['python_duo_exercise_content'])
    python_duo_answer = st.text_area("Completa o corrige el código:", key="python_duo_input")
    check_python_disabled = st.session_state.get('python_duo_submitted', False)
    if st.button("Comprobar Python", key="check_python_duo", disabled=check_python_disabled):
        if python_duo_answer:
            if python_duo_answer.strip() == st.session_state['python_duo_solution'].strip():
                st.success("¡Correcto!")
                award_tokens()
                if st.session_state['python_duo_explanation']:
                    st.info(f"Explicación: {st.session_state['python_duo_explanation']}")
                st.session_state['python_exercise_completed_today'] = True
                st.session_state['python_duo_exercise_content'] = None
                st.session_state['python_duo_submitted'] = True
            else:
                st.error("Incorrecto. Inténtalo de nuevo.")
                with st.expander("Mostrar solución"):
                    st.info(f"Solución correcta: \n```python\n{st.session_state['python_duo_solution']}\n```\n")
                    if st.session_state['python_duo_explanation']:
                        st.info(f"Explicación: {st.session_state['python_duo_explanation']}")
        else:
            st.warning("Por favor, ingresa tu respuesta.")

# --- Rust Exercise ---
st.subheader("Rust")
if st.button("Generar Ejercicio de Rust", key="rust_duo_button", disabled=st.session_state['rust_exercise_completed_today']):
    with st.spinner("Generando ejercicio de Rust..."):
        rust_concepts = ["Ownership", "Borrowing", "Structs", "Enums", "Traits"]
        chosen_concept = random.choice(rust_concepts)
        exercise, solution, explanation = generate_duolingo_exercise(chosen_concept, is_rust=True)
        st.session_state['rust_duo_exercise_content'] = exercise
        st.session_state['rust_duo_solution'] = solution
        st.session_state['rust_duo_explanation'] = explanation
        st.session_state['rust_duo_submitted'] = False

if st.session_state.get('rust_duo_exercise_content'):
    st.write(st.session_state['rust_duo_exercise_content'])
    rust_duo_answer = st.text_area("Completa o corrige el código:", key="rust_duo_input")
    check_rust_disabled = st.session_state.get('rust_duo_submitted', False)
    if st.button("Comprobar Rust", key="check_rust_duo", disabled=check_rust_disabled):
        if rust_duo_answer:
            if rust_duo_answer.strip() == st.session_state['rust_duo_solution'].strip():
                st.success("¡Correcto!")
                award_tokens()
                if st.session_state['rust_duo_explanation']:
                    st.info(f"Explicación: {st.session_state['rust_duo_explanation']}")
                st.session_state['rust_exercise_completed_today'] = True
                st.session_state['rust_duo_exercise_content'] = None
                st.session_state['rust_duo_submitted'] = True
            else:
                st.error("Incorrecto. Inténtalo de nuevo.")
                with st.expander("Mostrar solución"):
                    st.info(f"Solución correcta: \n```rust\n{st.session_state['rust_duo_solution']}\n```\n")
                    if st.session_state['rust_duo_explanation']:
                        st.info(f"Explicación: {st.session_state['rust_duo_explanation']}")
        else:
            st.warning("Por favor, ingresa tu respuesta.")

# --- Generar ideas para hackathon ---
st.header("Inspiración para Hackathon")
if st.button("Obtener Idea para Hackathon"):
    with st.spinner('Generando ideas...'):
        hackathon_idea = generate_hackathon_idea()
        st.success(hackathon_idea)