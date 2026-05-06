import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
# CORS total para evitar bloqueos de Google Sites
CORS(app)

# 1. CONFIGURACIÓN DE LA IA
# Asegúrate de que esta sea tu API KEY real de Google AI Studio
GEMINI_KEY = "AIzaSyA4EEjVQIihdP3HKLTjfAgpWkLbcQ5bDZc" 
genai.configure(api_key=GEMINI_KEY)

# Usamos el modelo más estable y rápido
model = genai.GenerativeModel('gemini-1.5-flash')

CONTEXTO_UPB = """
Eres 'SABIO BÚHO', el asistente oficial de admisiones de la UPB. 
Responde de forma amable y corta basándote en esto:
- Carrera IA: 4.5 años.
- Examen PAA: 200 bs.
- Puntaje mínimo: 1100.
- WhatsApp: 78508450.
Si no sabes algo, pide que escriban al WhatsApp.
"""

@app.route('/')
def home():
    return "Servidor del Sabio Búho Operativo"

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    # Manejo de la petición pre-vuelo de CORS
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200

    try:
        # Forzamos la lectura del JSON
        data = request.get_json(force=True, silent=True)
        if not data:
            return jsonify({"response": "Error: No se recibió JSON"}), 400
            
        user_message = data.get('message', '')
        
        # Llamada a Gemini con manejo de errores interno
        prompt = f"{CONTEXTO_UPB}\nUsuario: {user_message}\nSabio Búho:"
        response = model.generate_content(prompt)
        
        return jsonify({"response": response.text})

    except Exception as e:
        # Este print aparecerá en tus logs de Render para que sepas qué falló
        print(f"DEBUG ERROR: {str(e)}")
        return jsonify({"response": "Lo siento, mi conexión cerebral falló. Intenta de nuevo en un momento."}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
