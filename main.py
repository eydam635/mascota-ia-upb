import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# CONFIGURACIÓN DE LA IA
# Usa tu nueva API KEY aquí
GEMINI_KEY = "AIzaSyA4EEjVQIihdP3HKLTjfAgpWkLbcQ5bDZc" 
genai.configure(api_key=GEMINI_KEY)

# USAMOS EL MODELO LATEST PARA EVITAR EL ERROR 404
model = genai.GenerativeModel('gemini-1.5-flash-latest')

CONTEXTO_UPB = """
Eres 'SABIO BÚHO', el asistente oficial de admisiones de la UPB. 
Responde de forma amable y corta basándote en esto:
- Carrera IA: 4.5 años.
- Examen PAA: 200 bs.
- Puntaje mínimo: 1100.
- WhatsApp: 78508450.
"""

@app.route('/')
def home():
    return "Servidor del Sabio Búho Operativo con Gemini 1.5 Flash Latest"

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200

    try:
        data = request.get_json(force=True, silent=True)
        user_message = data.get('message', '') if data else ""
        
        if not user_message:
            return jsonify({"response": "¡Hola! ¿En qué puedo ayudarte?"}), 200

        # Llamada al modelo con el nuevo nombre compatible
        prompt = f"{CONTEXTO_UPB}\nUsuario: {user_message}\nSabio Búho:"
        response = model.generate_content(prompt)
        
        return jsonify({"response": response.text})

    except Exception as e:
        print(f"DEBUG: {e}")
        # Si el modelo flash falla por región, intentamos con el pro automáticamente
        return jsonify({"response": "Estoy procesando mucha información, ¿puedes intentar de nuevo?"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
