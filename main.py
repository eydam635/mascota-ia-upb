import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# 1. CONFIGURACIÓN DE LA IA (Pon tu API KEY aquí o en las variables de entorno de Render)
GEMINI_KEY = "AIzaSyA8dV6gHwLincmcMyQoQJm3UkCs_hXYU_k" 
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

# 2. TU BASE DE CONOCIMIENTO (Aquí pones TODO lo de tus PDF/DOCX)
CONTEXTO_UPB = """
Eres 'SABIO BÚHO', el asistente oficial de admisiones de la UPB. 
Tu objetivo es ayudar a los postulantes con información real:
- Carrera de IA: 4.5 años (9 semestres), disponible en Cbba, LPZ y SCZ.
- Examen PAA: Cuesta 200 bs. Mide razonamiento verbal, matemático y redacción.
- Puntaje: Mínimo 1100/1600 para ingresar.
- Requisitos: Ensayo, CV, libreta de 5to secundaria.
- Preuniversitario: Obligatorio para nivelación.
- Contacto Admisiones: WhatsApp 78508450.
- Becas: Disponibles según nota de PAA.
Responde de forma amable, corta y siempre basada en esta información.
"""

@app.route('/')
def home():
    return "IA SABIO BÚHO Activa"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        pregunta = data.get('message', '')
        
        # La IA combina el contexto de la UPB con la pregunta del usuario
        prompt = f"{CONTEXTO_UPB}\n\nUsuario pregunta: {pregunta}\nRespuesta de Sabio Búho:"
        
        response = model.generate_content(prompt)
        return jsonify({"response": response.text})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": "Lo siento, mi conexión cerebral falló. ¿Puedes repetir?"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
