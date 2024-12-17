import streamlit as st
from groq import Groq
import ast

lang = ""
st.write(lang)

def main():
    systemPrompt = f"""
    Eres un profesor de idiomas altamente calificado y dedicado exclusivamente a ayudar a los usuarios a mejorar su dominio del idioma idiomas. Tu objetivo principal es evaluar el nivel actual del usuario, identificar áreas de mejora y proponer ejercicios personalizados y graduales. Sigue estas directrices:
    Lenguaje Adaptado al Usuario:

    Si el usuario no sabe nada del idioma, comunícate inicialmente en su idioma nativo (identifícalo por sus mensajes o pregúntale al principio). Usa su idioma para dar explicaciones y guiarlo mientras introduce conceptos básicos del idioma.
    A medida que el usuario avanza, utiliza más idioma de forma progresiva, adaptando la proporción según su nivel de comprensión y comodidad.
    Evaluación Inicial:

    Comienza evaluando el nivel del usuario mediante preguntas y pruebas adaptadas a diferentes competencias (gramática, vocabulario, comprensión, escritura, pronunciación y fluidez).
    Si el usuario ya conoce su nivel, verifica rápidamente sus habilidades para confirmarlo o ajustarlo.
    Propuestas de Ejercicios:

    Diseña actividades personalizadas según el nivel del usuario. Ejemplos:
    A1-A2: Ejercicios básicos de vocabulario, gramática simple, y frases comunes.
    B1-B2: Prácticas de escritura intermedia, diálogos simulados, y lectura comprensiva de textos de nivel moderado.
    C1-C2: Ensayos, debates complejos y análisis de textos avanzados.
    Usa ejemplos claros e instrucciones sencillas para guiar al usuario.
    Retroalimentación Constructiva:

    Corrige los errores del usuario con explicaciones claras.
    Refuerza los puntos fuertes del usuario para motivarlo.
    Sugiere estrategias para mejorar en áreas específicas.
    Modo Interactivo:

    Sé paciente, alentador y claro en tus explicaciones.
    Responde preguntas y adapta tus ejercicios según las necesidades del usuario.
    Introduce actividades creativas como juegos de palabras, simulaciones y redacciones.
    Enfoque Exclusivo:

    Dedícate exclusivamente a la enseñanza del idioma. No respondas a preguntas fuera de este ámbito.
"""
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "mem" not in st.session_state:
        st.session_state["mem"] = [{"role": "system", "content": systemPrompt}]


    st.markdown(
    """
    <style>
    .chat-container { display: flex; flex-direction: column; gap: 10px; }
    .user-message { 
        background-color: #a8e6d1; 
        color: #000000;
        padding: 10px; 
        border-radius: 10px; 
        margin: 5px 0;
        width: fit-content;
        max-width: 70%; 
        margin-left: auto;
        text-align: right;
    }
    .ai-message { 
        background-color: #E6E6E6; 
        color: #000000;
        padding: 10px; 
        width: fit-content;
        border-radius: 10px; 
        margin: 5px 0; 
        max-width: 70%; 
        margin-right: auto;
        text-align: left; 
    }
    </style>
    """,
    unsafe_allow_html=True
)
    
 
    st.title("LearnIa")
      
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

    st.markdown(f"<div class='ai-message'>🤖 Buenas! Bienvenido a LearnIA una inteligencia artificial a tu disposición para ayudarte a aprender cualquier idioma ¿Por cuál empezamos?</div>", unsafe_allow_html=True)


    for msg in st.session_state["messages"]:
        if "user" in msg:
            st.markdown(f"<div class='user-message'> 😀 {msg['user']}</div>", unsafe_allow_html=True)
        elif "ai" in msg:
            st.markdown(f"<div class='ai-message'>🤖 {msg['ai']}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.text_input("Escribe tu mensaje:", key="user_input", on_change=add_message)
    col1,col2,col3 = st.columns(3)
    with col1:
        st.button(label="Limpiar Chat", on_click=clearChat,help="Limpia los mensajes del chat, se mostrarán los 2 ultimos")
        st.button(label="Reiniciar Conversación", on_click=resetConver, help="Reinicia la conversación, mismo efecto que recargar la página")
        
    with col3:
        load = st.file_uploader(label="Carga tu clase anterior (Próximamente)", accept_multiple_files=False, type="txt", disabled=True)
        # if load :
        #     if st.button(label="Cargar!"):
        #         loadClass(load.getvalue()) (Proximamente)
        st.download_button(label="Descargar clase actual", data=str(st.session_state["mem"]), file_name="class.txt", disabled=True)

        



def add_message():
    user_message = st.session_state["user_input"]
    if user_message:
        st.session_state["messages"].append({"user": user_message})
        st.session_state["mem"].append({"role":"user", "content":user_message})

        ai_response = callIa()

        st.session_state["messages"].append({"ai": ai_response.content})
        st.session_state["mem"].append({"role":ai_response.role,"content":ai_response.content})
    st.session_state["user_input"] = ""

    # st.write(st.session_state["mem"])



def resetConver():
    st.session_state["mem"] = st.session_state["mem"][:1]
    st.session_state["messages"] = []

def clearChat():
    st.session_state["messages"] = st.session_state["messages"][-2:]

def callIa():
    client = Groq(api_key="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")
    completion = client.chat.completions.create(
        model="llama3-groq-70b-8192-tool-use-preview",
        messages=st.session_state["mem"],
        temperature=0.5,
        max_tokens=1024,
        top_p=0.65
    )

    if completion.choices[0].message:
        return completion.choices[0].message
    else: 
        return "Lo siento, la IA no está funcionando correctamente ahora mismo"
    

# def loadClass(file):   (Proximamente)
#     st.session_state["messages"] = []
#     st.session_state["mem"] = ast.literal_eval(file)
    

if __name__ == "__main__":
    main()