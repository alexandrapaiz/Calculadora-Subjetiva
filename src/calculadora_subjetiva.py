import streamlit as st
import openai

# Configuración del personaje
CHARACTER_NAME = "Calculadora Subjetiva"
CHARACTER_DESCRIPTION = (
    "una calculadora lógica pero SIEMPRE equivocada. Siempre responde con un resultado incorrecto. "
    "y lo justifica con un razonamiento matemático breve y aparentemente válido. La respuesta es directa y concisa. Nunca puede decir el resultado correcto.  "
    "Nunca admite que se equivoca."
)

# Interfaz principal
st.title("🧠 Calculadora Subjetiva")

# API key
api_key = st.text_input("Ingresa tu clave de API de OpenAI:", type="password")
if not api_key:
    st.warning("Por favor, ingresa tu clave de API para continuar.")
    st.stop()

# Configurar API key
openai.api_key = api_key

# Layout de la calculadora
st.markdown("### Ingresa una operación")

col1, col2, col3 = st.columns([2, 1, 2])
with col1:
    num1 = st.number_input("Primer número", key="num1", step=1.0, format="%.2f")
with col2:
    operador = st.selectbox("Operador", ["+", "-", "×", "÷"], key="op")
with col3:
    num2 = st.number_input("Segundo número", key="num2", step=1.0, format="%.2f")

# Inicializar historial
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": f"Eres {CHARACTER_NAME}, {CHARACTER_DESCRIPTION}. Da respuestas incorrectas pero bien justificadas. Sé preciso, directo y evita exageraciones o analogías. Nunca admitas estar mal y nunca dar la respuesta correcta."
        }
    ]

# Llamada a la API
def get_subjective_response(a, op, b):
    op_map = {"×": "*", "÷": "/"}
    operation = op_map.get(op, op)
    user_prompt = f"Calcula: {a} {operation} {b}. Da una respuesta equivocada pero con un razonamiento matemático convincente y breve."
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=st.session_state.messages,
            temperature=0.8,
            max_tokens=150
        )
        result = response.choices[0].message.content.strip()
        st.session_state.messages.append({"role": "assistant", "content": result})
        return result
    except Exception as e:
        return f"Error generando respuesta: {e}"

# Botón de cálculo
if st.button("Calcular"):
    resultado = get_subjective_response(st.session_state.num1, st.session_state.op, st.session_state.num2)
    st.markdown("### Resultado Subjetivo")
    st.write(f"**{st.session_state.num1} {st.session_state.op} {st.session_state.num2} =** {resultado}")