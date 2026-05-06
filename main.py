import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
# Solución definitiva al error de CORS para Google Sites
CORS(app, resources={r"/*": {"origins": "*"}})

# CONFIGURACIÓN DE LA IA
GEMINI_KEY = "AIzaSyA8dV6gHwLincmcMyQoQJm3UkCs_hXYU_k" # Pon aquí tu clave de Google AI Studio
genai.configure(api_key=GEMINI_KEY)

# Cambio vital para evitar el error 404 de tus logs
model = genai.GenerativeModel('gemini-1.5-flash')

CONTEXTO_UPB = """
Eres 'SABIO BÚHO', asistente de admisiones de IA en la UPB. 
Responde sobre: Carrera (4.5 años), PAA (200 bs), Puntaje (1100/1600), 
Requisitos (Ensayo, CV, libreta) y WhatsApp (78508450).
"""

@app.route('/')
def home():
    return "Servidor de SABIO BÚHO Online"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        pregunta = data.get('message', '')
        if not pregunta:
            return jsonify({"response": "No recibí pregunta"}), 400
            
        prompt = f"{CONTEXTO_UPB}\nUsuario: {pregunta}\nSabio Búho:"
        response = model.generate_content(prompt)
        return jsonify({"response": response.text})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": "Tuve un parpadeo cerebral. ¿Repites?"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
