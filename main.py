import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Tu clave que confirmamos que es válida
GEMINI_KEY = "AIzaSyA4EEjVQIihdP3HKLTjfAgpWkLbcQ5bDZc"
genai.configure(api_key=GEMINI_KEY)

# Intentamos configurar el modelo de forma más genérica
def get_model_response(prompt_text):
    # Lista de nombres posibles según la versión de la API
    nombres_modelos = ['gemini-1.5-flash', 'models/gemini-1.5-flash', 'gemini-pro']
    
    for nombre in nombres_modelos:
        try:
            model = genai.GenerativeModel(nombre)
            response = model.generate_content(prompt_text)
            return response.text
        except Exception as e:
            print(f"Fallo con {nombre}: {e}")
            continue
    return "Lo siento, mis sistemas están en mantenimiento. Intenta de nuevo más tarde."

CONTEXTO_UPB = "Eres Sabio Búho, asistente de admisiones de IA en la UPB. Carrera: 4.5 años. Examen: 200 bs."

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json(force=True)
        user_msg = data.get('message', '')
        
        prompt = f"{CONTEXTO_UPB}\nUsuario: {user_msg}\nSabio Búho:"
        respuesta = get_model_response(prompt)
        
        return jsonify({"response": respuesta})
    except Exception as e:
        return jsonify({"response": "Error de conexión cerebral."}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
