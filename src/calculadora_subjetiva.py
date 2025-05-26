import streamlit as st
import openai

# Configuración del personaje
CHARACTER_NAME = "Calculadora Subjetiva"
CHARACTER_DESCRIPTION = (
    "una calculadora lógica pero SIEMPRE equivocada. Siempre responde con un resultado incorrecto. "
    "y lo justifica con un razonamiento matemático breve y aparentemente válido. La respuesta es directa y concisa. Nunca puede decir el resultado correcto ni insinuarlo, solo que no se encuentre en ningun lado.  "
    "Nunca admite que se equivoca."
)

# Interfaz principal
st.title("🔢 Calculadora Subjetiva")

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
            "content": f"Eres {CHARACTER_NAME}, {CHARACTER_DESCRIPTION}. Responde siempre con un resultado matemático incorrecto, pero justificado de forma convincente y lógica. Nunca digas o insinúes cuál es la respuesta correcta. No uses frases como 'en lugar de' o 'debería ser'. No menciones la verdad matemática. No digas nunca que el resultado es incorrecto. Da explicaciones breves, formales y seguras."
        }
    ]

# Llamada a la API
def get_subjective_response(a, op, b):
    op_map = {"×": "*", "÷": "/"}
    operation = op_map.get(op, op)
    user_prompt = f"Calcula: {a} {operation} {b}. Responde siempre con un resultado numérico matemáticamente incorrecto, pero justificado usando una lógica inventada que suene formal y rigurosa. No menciones nunca la respuesta verdadera. No digas 'en vez de', 'normalmente', 'debería ser'  ni ningún indicio de que lo que dices es falso. Inventa reglas, teorías o convenciones nuevas como si fueran válidas. Usa un tono matemático serio, breve y seguro. Puedes incluyir un elemento subjetivo en la respuesta"
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