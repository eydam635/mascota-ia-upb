import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# SOLUCIÓN AL ERROR DE CONEXIÓN: Permite que Google Sites entre sin bloqueos
CORS(app, resources={r"/*": {"origins": "*"}})

# Base de datos extraída de tus documentos
INFO_UPB = {
    "ia": "La carrera de Ingeniería de Inteligencia Artificial dura 4.5 años (9 semestres). Se enfoca en crear sistemas que aprenden y razonan.",
    "paa": "El examen PAA cuesta 200 bs. Mide Razonamiento Verbal, Matemático y Redacción Indirecta.",
    "puntaje": "El puntaje mínimo para ser admitido es de 1100/1600 puntos.",
    "requisitos": "Necesitas cargar tu ensayo, CV, libreta de 5to de secundaria y certificado de inglés (si tienes).",
    "prepa": "El preuniversitario es obligatorio para nivelación. Para ingeniería llevas Matemáticas, Física y Química.",
    "contacto": "Para costos exactos de mensualidades, comunícate al WhatsApp 78508450.",
    "becas": "Existen varios programas de becas basados en tu nota del examen de admisión."
}

@app.route('/')
def home():
    return "Servidor de Yupi Bot funcionando y listo para Google Sites."

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"response": "No recibí mensaje."}), 400
        
        user_msg = data['message'].lower()
        
        # Lógica de respuestas inteligentes
        if "ia" in user_msg or "inteligencia" in user_msg:
            reply = INFO_UPB["ia"]
        elif "examen" in user_msg or "paa" in user_msg or "costo" in user_msg:
            reply = INFO_UPB["paa"]
        elif "punto" in user_msg or "puntaje" in user_msg:
            reply = INFO_UPB["puntaje"]
        elif "precio" in user_msg or "mensualidad" in user_msg or "pagar" in user_msg:
            reply = INFO_UPB["contacto"]
        elif "beca" in user_msg:
            reply = INFO_UPB["becas"]
        elif "prepa" in user_msg or "nivelacion" in user_msg:
            reply = INFO_UPB["prepa"]
        elif "requisito" in user_msg or "papeles" in user_msg:
            reply = INFO_UPB["requisitos"]
        else:
            reply = "¡Hola! Soy Yupi. Pregúntame sobre la carrera de IA, el examen PAA (200 bs), puntajes mínimos o la Prepa UPB."

        return jsonify({"response": reply})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": "Lo siento, tuve un error interno. Intenta de nuevo."}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
