# meshia-vara-hackathon

```markdown
# Vocational AI Mini-Game

Este es un mini-juego vocacional interactivo desarrollado con Streamlit que te permite aprender sobre nuevas tecnologías como Inteligencia Artificial, blockchain y programación (Python y Rust) de una manera divertida y gamificada. ¡Completa desafíos, gana tokens y expande tus conocimientos!

## Características Principales

*   **Conexión de Wallet (Simulada):** Conecta una wallet simulada para participar en el juego y llevar un registro de tus tokens ganados.
*   **Desafío de Conocimiento:** Responde preguntas desafiantes sobre Inteligencia Artificial para poner a prueba tus conocimientos.
*   **Ejercicios de Programación Estilo Duolingo:** Aprende y practica Python y Rust resolviendo pequeños fragmentos de código para completar o corregir. Recibe retroalimentación y explicaciones para mejorar tu comprensión.
*   **Chatbot de IA:** Interactúa con un chatbot impulsado por IA para obtener respuestas a tus preguntas sobre el proyecto o las tecnologías involucradas.
*   **Inspiración para Hackathon:** Obtén ideas creativas para proyectos de hackathon que combinen inteligencia artificial y blockchain.
*   **Sistema de Recompensas:** Gana tokens virtuales al completar correctamente los desafíos y ejercicios.

## Tecnologías Utilizadas

*   **Streamlit:** Para crear la interfaz web interactiva.
*   **Langchain:** Para facilitar la interacción con modelos de lenguaje (Gemini).
*   **Google Gemini:** Como modelo de lenguaje para generar preguntas, ejercicios y respuestas del chatbot.
*   **Python:** El lenguaje principal del backend y para los ejercicios de programación.
*   **Rust:** Para los ejercicios de programación.
*   **dotenv:** Para gestionar las variables de entorno de forma segura.

## Requisitos Previos

Antes de ejecutar el proyecto, asegúrate de tener instalado lo siguiente:

*   **Python 3.7 o superior:** Puedes descargarlo desde [python.org](https://www.python.org/).
*   **pip:** El gestor de paquetes de Python, generalmente incluido con la instalación de Python.

## Configuración

1. **Clona el repositorio:**
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd <nombre_del_repositorio>
    ```

2. **Crea un entorno virtual (recomendado):**
    ```bash
    python -m venv venv
    # Activa el entorno virtual (dependiendo de tu sistema operativo)
    # En Linux/macOS:
    source venv/bin/activate
    # En Windows:
    .\venv\Scripts\activate
    ```

3. **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configura la clave de API de Google Gemini:**
    *   Crea un archivo llamado `.env` en el directorio raíz del proyecto.
    *   Agrega tu clave de API de Google Gemini al archivo `.env`:
        ```
        GOOGLE_API_KEY="TU_CLAVE_DE_API_AQUI"
        ```
        **Nota:** Si no tienes una clave de API de Google Gemini, puedes obtener una siguiendo las instrucciones en la [documentación de Google AI Studio](https://makersuite.google.com/).

## Ejecución

Para ejecutar la aplicación Streamlit, navega hasta el directorio del proyecto en tu terminal y ejecuta el siguiente comando:

```bash
streamlit run tu_archivo_principal.py
```

Reemplaza `tu_archivo_principal.py` con el nombre del archivo principal de tu aplicación Streamlit (en este caso, el nombre del archivo que contiene el código que proporcionaste).

La aplicación se abrirá automáticamente en tu navegador web.

## Uso

1. **Conectar Wallet:** Haz clic en el botón "Conectar Wallet" para simular la conexión de una wallet. Esto te permitirá participar en el sistema de recompensas.
2. **Desafío de Conocimiento:** Haz clic en "Obtener Pregunta" para recibir una pregunta sobre Inteligencia Artificial. Escribe tu respuesta en el área de texto y haz clic en "Enviar Respuesta" para verificarla. Si es correcta, ganarás tokens.
3. **Ejercicios de Programación Estilo Duolingo:**
    *   **Python:** Haz clic en "Generar Ejercicio de Python" para obtener un ejercicio de programación en Python. Completa o corrige el código en el área de texto y haz clic en "Comprobar Python". Recibirás retroalimentación y una explicación si te equivocas.
    *   **Rust:** Haz clic en "Generar Ejercicio de Rust" para obtener un ejercicio de programación en Rust. Completa o corrige el código y haz clic en "Comprobar Rust".
4. **Chat con la IA:** Utiliza la barra lateral para interactuar con el chatbot de IA. Escribe tu pregunta en el cuadro de texto y recibe una respuesta.
5. **Inspiración para Hackathon:** Haz clic en "Obtener Idea para Hackathon" para generar una idea de proyecto que involucre IA y blockchain.

## Contribución

¡Las contribuciones son bienvenidas! Si deseas contribuir a este proyecto, por favor considera lo siguiente:

*   Reporta errores o sugiere nuevas funcionalidades a través de las Issues de GitHub.
*   Envía Pull Requests con mejoras o correcciones.

## Licencia

Este proyecto está bajo la Licencia [MIT](https://opensource.org/licenses/MIT) (o la licencia que prefieras). Consulta el archivo `LICENSE` para obtener más detalles.
```

