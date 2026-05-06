import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# BASE DE CONOCIMIENTO EXTENDIDA (Basada en Documentación UPB)
INFO_UPB = {
    "oferta_academica": {
        "negocios": "Administración de Empresas, Analítica Gerencial de Datos, Comunicación, Derecho, Diseño Gráfico, Economía, Gerencia en Turismo, Ing. Comercial, Ing. Financiera, Marketing y Logística, Psicología Organizacional y Relaciones Internacionales.",
        "ingenieria": "Arquitectura, Bioingeniería, Ing. Civil, Ing. de Inteligencia Artificial, Ing. de Sistemas Computacionales, Ing. de la Producción, Ing. del Medio Ambiente, Ing. Electromecánica, Ing. Electrónica e Ing. Industrial."
    },
    "admision": {
        "pasos": "1. Iniciar postulación online (ensayo, CV, libreta 5to secundaria). 2. Programar examen PAA. 3. Consultar resultados.",
        "paa": "La Prueba de Aptitud Académica (PAA) cuesta 200 bs y mide: Razonamiento Verbal, Razonamiento Matemático y Redacción Indirecta.",
        "puntaje": "El puntaje mínimo de ingreso es de 1100 sobre 1600 puntos.",
        "fechas": "Admisión temprana (Mayo-Julio), Regular (Agosto-Octubre) y Tardía (Noviembre-Enero)."
    },
    "prepa": "La Prepa UPB es obligatoria para nivelación académica y conocer el sistema modular. Según tu carrera llevas: Matemáticas, Física, Química, o talleres de Creatividad y Expresión Escrita.",
    "internacional": {
        "programas": "La UPB tiene convenios con más de 300 universidades. Destacan la Doble Titulación con la University of London (LSE) y programas con PPA Business School (Francia).",
        "ingles": "Se requiere dominar el inglés. Puedes convalidar niveles con TOEFL (72+), IELTS (6.0+), Duolingo (115+) o el Diploma IB."
    },
    "sedes": {
        "cochabamba": "Campus Julio León Prado (Av. Capitán Ustariz Km 6.5). Tel: 78508450.",
        "la_paz": "Campus Fernando Illanes de la Riva (Achocalla). Tel: 62625361.",
        "santa_cruz": "Campus Santa Cruz (Zona Urubó). Tel: 67195952."
    },
    "diferenciadores": "Es la universidad #1 de Bolivia según rankings internacionales. Única con 4 estrellas QS Stars. Destaca por su sistema modular (una materia a la vez) y su enfoque en investigación.",
    "costos": "Las mensualidades varían por carrera y sede. Para un presupuesto personalizado, contacta al WhatsApp oficial: 78508450.",
    "becas": "Existen becas de excelencia basadas en el puntaje de tu examen PAA. A mayor puntaje, mayor porcentaje de beca."
}

def respuesta_inteligente(mensaje):
    msg = mensaje.lower()
    
    # 1. Carreras e Ingenierías
    if any(x in msg for x in ["carrera", "qué hay", "estudiar", "oferta"]):
        return f"La UPB ofrece carreras en Negocios ({INFO_UPB['oferta_academica']['negocios']}) e Ingenierías ({INFO_UPB['oferta_academica']['ingenieria']})."
    
    # 2. IA (Tu carrera específica)
    if "ia" in msg or "inteligencia" in msg:
        return "La carrera de Ing. de Inteligencia Artificial dura 4.5 años (9 semestres). Es líder en el país con enfoque en Machine Learning y Ciencia de Datos."

    # 3. Examen y Admisión
    if any(x in msg for x in ["examen", "paa", "entrar", "ingresar", "admitido"]):
        return f"{INFO_UPB['admision']['pasos']} {INFO_UPB['admision']['paa']}"
    
    if "punto" in msg or "puntaje" in msg or "cuanto necesito" in msg:
        return INFO_UPB['admision']['puntaje']

    # 4. Dinero y Becas
    if "beca" in msg:
        return INFO_UPB["becas"]
    
    if any(x in msg for x in ["costo", "precio", "cuanto vale", "mensualidad", "pagar", "pension"]):
        return f"{INFO_UPB['costos']} El examen de admisión PAA tiene un costo de 200 bs."

    # 5. Preuniversitario
    if any(x in msg for x in ["prepa", "nivelacion", "curso pre"]):
        return INFO_UPB["prepa"]

    # 6. Ubicación y Contacto
    if "donde queda" in msg or "campus" in msg or "ubicacion" in msg:
        return f"Estamos en el eje central. Cochabamba: {INFO_UPB['sedes']['cochabamba']} | La Paz: {INFO_UPB['sedes']['la_paz']} | Santa Cruz: {INFO_UPB['sedes']['santa_cruz']}"

    # 7. Internacional e Inglés
    if any(x in msg for x in ["intercambio", "londres", "lse", "viajar", "extranjero", "doble titulacion"]):
        return INFO_UPB["internacional"]["programas"]
    
    if "ingles" in msg or "toefl" in msg or "idioma" in msg:
        return f"El inglés es clave en la UPB. {INFO_UPB['internacional']['ingles']}"

    # 8. Requisitos y documentos
    if any(x in msg for x in ["requisito", "papel", "documento", "ensayo", "cv"]):
        return "Para postular necesitas cargar a la plataforma: Tu ensayo personal, CV actualizado, libreta de 5to de secundaria y certificado de inglés si lo tienes."

    # 9. Por qué la UPB?
    if any(x in msg for x in ["mejor", "ranking", "porque", "beneficio", "modular"]):
        return INFO_UPB["diferenciadores"]

    return "¡Hola! Soy Yupi, la IA de la UPB. Puedo ayudarte con info sobre carreras (IA, Comercial, etc.), el examen PAA, becas, convenios internacionales o requisitos de ingreso. ¿Qué te gustaría saber?"

@app.route('/')
def home():
    return "Servidor Yupi Bot v2.0 - UPB"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"response": "No recibí mensaje."}), 400
        
        reply = respuesta_inteligente(data['message'])
        return jsonify({"response": reply})

    except Exception as e:
        return jsonify({"response": "Ocurrió un error en mi sistema. Intenta preguntar de otra forma."}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
