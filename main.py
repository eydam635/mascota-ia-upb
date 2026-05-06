import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
# Permitimos que Google Sites se conecte sin restricciones de seguridad
CORS(app)

# 1. CONFIGURACIÓN DE LA IA CON TU API KEY
GEMINI_KEY = "AIzaSyA4EEjVQIihdP3HKLTjfAgpWkLbcQ5bDZc" 
genai.configure(api_key=GEMINI_KEY)

# Usamos el modelo más rápido y actualizado
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. EL "CEREBRO" DEL BÚHO (Aquí está toda la info de la UPB)
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
    # Manejo de la "pre-consulta" de los navegadores
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200

    try:
        # Leemos la pregunta del usuario
        data = request.get_json(force=True, silent=True)
        user_message = data.get('message', '') if data else ""
        
        if not user_message:
            return jsonify({"response": "¡Hola! Soy el Sabio Búho. ¿En qué puedo ayudarte hoy?"}), 200

        # La IA procesa la respuesta usando el contexto
        prompt = f"{CONTEXTO_UPB}\nUsuario: {user_message}\nSabio Búho:"
        response = model.generate_content(prompt)
        
        return jsonify({"response": response.text})

    except Exception as e:
        print(f"Error interno: {e}")
        return jsonify({"response": "Lo siento, tuve un pequeño problema de conexión. ¿Puedes repetir tu pregunta?"}), 200

if __name__ == "__main__":
    # Render asigna el puerto automáticamente
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
