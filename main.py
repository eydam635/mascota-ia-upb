import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
# CORS habilitado para que Google Sites no bloquee la conexión
CORS(app, resources={r"/*": {"origins": "*"}})

# 1. CONFIGURACIÓN DE LA IA
# REEMPLAZA ESTO CON TU CLAVE REAL DE GOOGLE AI STUDIO
GEMINI_KEY = "AIzaSyA8dV6gHwLincmcMyQoQJm3UkCs_hXYU_k" 
genai.configure(api_key=GEMINI_KEY)

# Usamos gemini-1.5-flash para evitar el error 404 y tener respuestas rápidas
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. BASE DE CONOCIMIENTO (Personaliza esto con toda la info de tus documentos)
CONTEXTO_UPB = """
Eres 'SABIO BÚHO', el asistente inteligente de admisiones de la carrera de Inteligencia Artificial en la UPB.
Tu tono es sabio, amable y muy servicial. 

INFORMACIÓN CRUCIAL QUE DEBES USAR PARA RESPONDER:
- Carrera: Ingeniería de Inteligencia Artificial (duración 4.5 años / 9 semestres).
- Sedes: Cochabamba, La Paz y Santa Cruz.
- Examen PAA: Es la Prueba de Aptitud Académica. Cuesta 200 bs. 
- Contenido PAA: Razonamiento Verbal, Razonamiento Matemático y Redacción Indirecta.
- Puntaje de ingreso: Mínimo 1100 sobre 1600 puntos.
- Requisitos de Admisión: Ensayo personal, CV actualizado y libreta de calificaciones de 5to de secundaria.
- Preuniversitario (Prepa): Es obligatorio para nivelación académica.
- Becas: Se otorgan según el puntaje obtenido en el examen PAA.
- Contacto Directo: Para dudas de costos o pagos, escribir al WhatsApp 78508450.

REGLAS:
1. Si no sabes algo, pide que contacten al número de WhatsApp mencionado.
2. Mantén tus respuestas concisas pero completas.
3. Siempre actúa como un asistente de admisiones, no respondas cosas que no tengan que ver con la universidad.
"""

@app.route('/')
def home():
    return "Servidor de SABIO BÚHO (Gemini 1.5 Flash) está ONLINE"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        pregunta_usuario = data.get('message', '')
        
        if not pregunta_usuario:
            return jsonify({"response": "No me has enviado ninguna pregunta."}), 400

        # Construimos el prompt uniendo el conocimiento con la pregunta
        prompt_completo = f"{CONTEXTO_UPB}\n\nPregunta del usuario: {pregunta_usuario}\nRespuesta del Sabio Búho:"
        
        # Generar respuesta con la IA
        response = model.generate_content(prompt_completo)
        
        return jsonify({"response": response.text})

    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"response": "Lo siento, mi conexión cerebral tuvo un pequeño parpadeo. ¿Podrías repetirme tu duda?"}), 500

if __name__ == "__main__":
    # Render asigna el puerto automáticamente
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
