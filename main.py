import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Permitir que tu Google Sites se conecte al servidor sin bloqueos de seguridad
CORS(app, resources={r"/*": {"origins": "*"}})

# BASE DE CONOCIMIENTOS EXTRAÍDA DE TUS DOCUMENTOS (UPB)
CONOCIMIENTO_UPB = {
    "carreras": {
        "negocios": "Administración de Empresas, Analítica Gerencial de Datos, Comunicación, Derecho, Diseño Gráfico, Economía, Gerencia en Turismo, Ing. Comercial, Ing. Financiera, Marketing y Logística, Psicología Organizacional y Relaciones Internacionales[cite: 1, 2].",
        "ingenieria": "Arquitectura, Bioingeniería, Ing. Civil, Ing. de Inteligencia Artificial, Ing. de Sistemas Computacionales, Ing. de la Producción, Ing. del Medio Ambiente, Ing. Electromecánica, Ing. Electrónica e Ing. Industrial[cite: 1, 2]."
    },
    "ia": "La carrera de Ing. de Inteligencia Artificial dura 4.5 años y forma profesionales en sistemas que aprenden y razonan, cubriendo áreas como Machine Learning, Deep Learning y Robótica[cite: 1, 25].",
    "admision": {
        "pasos": "1. Iniciar postulación (ensayo, CV, libreta 5to secundaria). 2. Programar el examen PAA. 3. Consultar resultados[cite: 22, 23].",
        "paa": "La PAA (Prueba de Aptitud Académica) mide Razonamiento Verbal, Matemático y Redacción Indirecta. Tiene un costo de 200 bs.",
        "puntaje": "El puntaje mínimo para ser admitido es de 1100 sobre 1600 puntos."
    },
    "prepa": "El preuniversitario (Prepa UPB) es obligatorio para nivelación y adaptación al sistema modular. Según tu carrera, llevas materias como Matemáticas, Física, Química o talleres de Creatividad y Expresión.",
    "internacional": "La UPB tiene convenios con más de 300 universidades y programas de doble titulación con la University of London (LSE) y PPA Business School en Francia.",
    "ingles": "El programa de inglés tiene niveles desde Beginners hasta Advanced. Puedes convalidarlo sin costo con certificados como TOEFL (72+), IELTS (6.0+) o Duolingo (115+).",
    "sedes": "Contamos con campus en el eje central: Cochabamba (Campus Julio León Prado), La Paz (Campus Fernando Illanes) y Santa Cruz[cite: 9, 642].",
    "contacto": "Para costos detallados y pensiones, escribe al WhatsApp de admisiones: 78508450[cite: 642]."
}

def respuesta_bot(mensaje):
    m = mensaje.lower()
    
    # Lógica de respuesta por palabras clave
    if any(x in m for x in ["carrera", "estudiar", "oferta"]):
        return f"La UPB ofrece licenciaturas en Negocios y Derecho: {CONOCIMIENTO_UPB['carreras']['negocios']} Y en Ingenierías: {CONOCIMIENTO_UPB['carreras']['ingenieria']}"
    
    if "ia" in m or "inteligencia artificial" in m:
        return CONOCIMIENTO_UPB["ia"]
    
    if any(x in m for x in ["entrar", "examen", "paa", "admision"]):
        return f"{CONOCIMIENTO_UPB['admision']['pasos']} {CONOCIMIENTO_UPB['admision']['paa']}"
    
    if "punto" in m or "puntaje" in m:
        return f"Para ingresar necesitas un puntaje mínimo de {CONOCIMIENTO_UPB['admision']['puntaje']}"
    
    if "prepa" in m or "nivelacion" in m:
        return CONOCIMIENTO_UPB["prepa"]
    
    if any(x in m for x in ["beca", "descuento", "ayuda"]):
        return "Sí, existen programas de becas basados en tu desempeño en el examen de admisión PAA[cite: 642]."
    
    if any(x in m for x in ["costo", "precio", "cuanto vale", "mensualidad", "pension"]):
        return CONOCIMIENTO_UPB["contacto"]
    
    if any(x in m for x in ["intercambio", "londres", "francia", "viajar"]):
        return CONOCIMIENTO_UPB["internacional"]
    
    if "ingles" in m or "toefl" in m:
        return CONOCIMIENTO_UPB["ingles"]
    
    if "donde" in m or "campus" in m or "ubicacion" in m:
        return CONOCIMIENTO_UPB["sedes"]
    
    # Respuesta por defecto si no entiende
    return "¡Hola! Soy el asistente virtual de la UPB. Puedo darte info sobre carreras (como IA), requisitos de admisión, el examen PAA (200 bs), la Prepa o becas. ¿En qué puedo ayudarte?"

@app.route('/')
def index():
    return "Servidor UPB Bot activo."

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        response = respuesta_bot(user_message)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"response": "Ups, tuve un problema técnico. Intenta de nuevo."}), 500

if __name__ == "__main__":
    # Importante: El puerto debe ser dinámico para servicios como Render o Heroku
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
