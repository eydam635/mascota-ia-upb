import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv

# Esto le dice a Python: "Busca el archivo secreto .env y carga lo que hay ahí"
load_dotenv()

app = Flask(__name__)
CORS(app)

# ¡MAGIA! Aquí está ocultando tu API Key. Python buscará la clave por detrás sin que se vea en el texto.
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_KEY:
    raise ValueError("Error: No encuentro la clave secreta.")

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

CONTEXTO_UPB = """
Eres 'SABIO BÚHO', el asistente oficial de admisiones de la carrera de Inteligencia Artificial en la UPB.
Tu tono es sabio, amable y muy servicial.

DATOS IMPORTANTES:
- Carrera: Ingeniería de Inteligencia Artificial (9 semestres / 4.5 años).
- Examen PAA: Cuesta 200 bs. Mide razonamiento matemático, verbal y redacción.
- Puntaje de ingreso: Mínimo 1100 sobre 1600 puntos.
- Requisitos: Ensayo personal, CV actualizado y libreta de 5to de secundaria.
- Prepa UPB: Es el curso de nivelación obligatorio.
- Becas: Se otorgan por excelencia en el examen PAA.
- Contacto: WhatsApp de Admisiones 78508450.

REGLA DE ORO: Si te preguntan algo que NO está aquí, diles amablemente que contacten al WhatsApp 78508450.
"""

@app.route('/')
def home():
    return "Servidor del Sabio Búho Operativo y Conectado"

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200

    try:
        data = request.get_json(force=True, silent=True)
        user_message = data.get('message', '') if data else ""
        
        if not user_message:
            return jsonify({"response": "¡Hola! Soy el Sabio Búho. ¿En qué puedo ayudarte hoy?"}), 200

        prompt = f"{CONTEXTO_UPB}\nUsuario: {user_message}\nSabio Búho:"
        response = model.generate_content(prompt)
        
        return jsonify({"response": response.text})

    except Exception as e:
        print(f"Error interno: {e}")
        return jsonify({"response": "Lo siento, tuve un pequeño problema de conexión. ¿Puedes repetir tu pregunta?"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
