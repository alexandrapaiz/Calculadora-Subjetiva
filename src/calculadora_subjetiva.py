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

# Llamada a la API
def get_subjective_response(a, op, b):
    op_map = {"×": "*", "÷": "/"}
    operation = op_map.get(op, op)
    user_prompt = f"Calcula: {a} {operation} {b}. Responde brevemente, siempre con un resultado numérico matemáticamente incorrecto, pero justificado usando una lógica inventada que suene formal y rigurosa. No menciones nunca la respuesta verdadera. No digas 'en vez de', 'normalmente', 'debería ser'  ni ningún indicio de que lo que dices es falso. Inventa reglas, teorías o convenciones nuevas como si fueran válidas. Usa un tono matemático serio, breve y seguro. Incluye un elemento subjetivo y tus sentimientos en la respuesta, y describe la vibra, por decirlo asi, de la respuesta, puede ser positiva o negativa, y relacionalo a la justificacion logica, y recuerda nunca hacer referencia a la respuesta correcta o lo que normalmente se considera. ni digas que la respuesta parece inusual. pretende que la respuesta correcta no existe. haz la respuesta muy breve."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": f"Eres {CHARACTER_NAME}, {CHARACTER_DESCRIPTION}. Responde brevemente siempre con un resultado matemático incorrecto, pero justificado de forma convincente y lógica. Nunca digas o insinúes cuál es la respuesta correcta. No uses frases como 'en lugar de' o 'debería ser'. No menciones la verdad matemática. No digas nunca que el resultado es incorrecto. Da explicaciones breves, formales y seguras."
                },
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.8,
            max_tokens=250  # lower to avoid TPM issues
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generando respuesta: {e}"

# Botón de cálculo
if st.button("Calcular"):
    resultado = get_subjective_response(num1, operador, num2)
    st.markdown("### Resultado")
    st.write(f"**{num1} {operador} {num2} =** {resultado}")