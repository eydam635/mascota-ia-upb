import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests # Usamos requests para que sea ultra simple

app = Flask(__name__)
CORS(app)

# 1. CONFIGURACIÓN
HF_TOKEN = "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"
# Usamos Llama 3 de Meta, es increíblemente bueno
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

CONTEXTO_UPB = """
Eres 'SABIO BÚHO', el asistente de admisiones de la carrera de IA en la UPB.
Información: Carrera 4.5 años, Examen PAA 200 bs, Puntaje min 1100, WhatsApp 78508450.
Responde de forma corta y amable.
"""

@app.route('/')
def home():
    return "Servidor del Sabio Búho (Llama 3) Online"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json(force=True)
        user_message = data.get('message', '')

        # Preparamos la consulta para Llama 3
        payload = {
            "inputs": f"<|system|>\n{CONTEXTO_UPB}\n<|user|>\n{user_message}\n<|assistant|>\n",
            "parameters": {"max_new_tokens": 250, "temperature": 0.7}
        }

        response = requests.post(API_URL, headers=headers, json=payload)
        resultado = response.json()

        # Limpiamos la respuesta para que solo salga lo que dijo el Búho
        bot_text = resultado[0]['generated_text'].split("<|assistant|>\n")[-1]
        
        return jsonify({"response": bot_text})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": "Lo siento, mi conexión cerebral está lenta. ¿Repetimos?"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
