import os
import re
from difflib import get_close_matches
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Permitir conexiones desde Google Sites
CORS(app, resources={r"/*": {"origins": "*"}})

# =========================================================
#            SUPER IA ADMISIONES UPB BOLIVIA
# =========================================================

CONTACTO_HUMANO = """
No tengo información exacta sobre eso todavía 😅  
Por favor contacta a Jazmín Burton al 76764364 para una atención personalizada.
"""

# =========================================================
# BASE DE CONOCIMIENTO MASIVA
# =========================================================

UPB_DATA = {

    "saludo": """
¡Hola! 👋
Soy el Asistente Inteligente de Admisiones UPB Bolivia 🤖🎓

Puedo ayudarte con:
✅ Carreras
✅ Ingeniería en IA
✅ Examen PAA
✅ Becas
✅ Costos
✅ Campus
✅ Intercambios internacionales
✅ Inglés
✅ Preuniversitario
✅ Modalidad de estudio
✅ Requisitos de admisión
✅ Inscripciones
✅ Doble titulación
✅ Vida universitaria
✅ Tecnología y laboratorios

Hazme cualquier pregunta 😎
""",

    "carreras": """
📚 La UPB Bolivia ofrece carreras en:

🏛️ NEGOCIOS Y DERECHO
• Administración de Empresas
• Analítica Gerencial de Datos
• Comunicación
• Derecho
• Diseño Gráfico
• Economía
• Gerencia en Turismo
• Ingeniería Comercial
• Ingeniería Financiera
• Marketing y Logística
• Psicología Organizacional
• Relaciones Internacionales

⚙️ INGENIERÍAS
• Arquitectura
• Bioingeniería
• Ingeniería Civil
• Ingeniería de Inteligencia Artificial
• Ingeniería de Sistemas Computacionales
• Ingeniería Industrial
• Ingeniería Electrónica
• Ingeniería Electromecánica
• Ingeniería Ambiental
• Ingeniería de Producción
""",

    "ia": """
🤖 Ingeniería de Inteligencia Artificial (IA)

⏳ Duración:
4 años y medio

📚 Aprenderás:
• Machine Learning
• Deep Learning
• Redes Neuronales
• Robótica
• Ciencia de Datos
• Visión Computacional
• Programación avanzada
• Automatización inteligente

💼 Salidas laborales:
• Científico de Datos
• Ingeniero IA
• Desarrollador de IA
• Especialista en automatización
• Analista de datos
• Investigador tecnológico

🔥 Es una de las carreras con mayor demanda del futuro.
""",

    "paa": """
📝 PAA - Prueba de Aptitud Académica

💰 Costo:
200 Bs.

📚 Evalúa:
• Razonamiento Matemático
• Razonamiento Verbal
• Redacción indirecta

🎯 Puntaje mínimo:
1100/1600

💡 Consejo:
Practica matemáticas básicas, comprensión lectora y lógica.
""",

    "admision": """
🎓 PROCESO DE ADMISIÓN UPB

1️⃣ Registro de postulación
2️⃣ Presentar:
   • Libreta de 5to
   • Carnet/Pasaporte
   • Ensayo personal
   • Curriculum Vitae

3️⃣ Programar examen PAA
4️⃣ Dar el examen
5️⃣ Revisar resultados
6️⃣ Inscribirse oficialmente
""",

    "becas": """
🏆 BECAS UPB

La UPB cuenta con:
✅ Becas académicas
✅ Becas por excelencia
✅ Becas deportivas
✅ Convenios institucionales
✅ Ayuda financiera

🔥 Algunas becas dependen del resultado obtenido en la PAA.
""",

    "prepa": """
📘 PREPA UPB

Es un programa preuniversitario de nivelación.

Dependiendo de tu carrera puedes pasar:
• Matemáticas
• Física
• Química
• Expresión creativa
• Comunicación
• Nivelación académica

💡 Ayuda muchísimo para adaptarse al sistema modular UPB.
""",

    "ingles": """
🇺🇸 Programa de Inglés UPB

Niveles:
• Beginners
• Elementary
• Intermediate
• Advanced

✅ Puedes convalidar con:
• TOEFL
• IELTS
• Duolingo English Test

🔥 La UPB impulsa mucho el inglés internacional.
""",

    "internacional": """
🌎 INTERNACIONALIZACIÓN UPB

La UPB tiene convenios con más de 300 universidades.

🔥 Doble titulación con:
• University of London
• LSE
• PPA Business School (Francia)

✈️ También existen intercambios internacionales.
""",

    "sedes": """
🏫 CAMPUS UPB

📍 Cochabamba
Campus Julio León Prado

📍 La Paz
Campus Fernando Illanes

📍 Santa Cruz
Campus UPB Santa Cruz
""",

    "costos": """
💰 Para información actualizada sobre:
• Pensiones
• Costos
• Becas
• Descuentos
• Inscripciones

📲 Contacta a Jazmín Burton:
76764364
""",

    "modalidad": """
💻 Modalidad de estudio UPB

✅ Presencial
✅ Sistema modular
✅ Enfoque práctico
✅ Proyectos reales
✅ Tecnología avanzada

🔥 La universidad se enfoca mucho en innovación y liderazgo.
""",

    "vida": """
🎉 VIDA UNIVERSITARIA

La UPB tiene:
• Actividades estudiantiles
• Deportes
• Networking
• Ferias
• Hackathons
• Laboratorios modernos
• Eventos tecnológicos
• Clubes estudiantiles
""",

    "laboratorios": """
🖥️ LABORATORIOS Y TECNOLOGÍA

La UPB cuenta con:
✅ Laboratorios modernos
✅ Equipos especializados
✅ Software profesional
✅ Simuladores
✅ Tecnología aplicada
✅ Espacios de innovación
""",
}

# =========================================================
# RESPUESTAS INTELIGENTES
# =========================================================

KEYWORDS = {

    "carreras": [
        "carrera", "carreras", "oferta", "estudiar",
        "facultad", "ingenieria", "ingeniería"
    ],

    "ia": [
        "ia", "inteligencia artificial",
        "machine learning", "deep learning",
        "robotica", "robótica"
    ],

    "paa": [
        "paa", "examen", "prueba",
        "puntaje", "admisión", "admision"
    ],

    "admision": [
        "entrar", "inscribirme",
        "postular", "requisitos",
        "documentos", "admisión"
    ],

    "becas": [
        "beca", "becas",
        "descuento", "ayuda"
    ],

    "prepa": [
        "prepa", "nivelacion",
        "nivelación", "preuniversitario"
    ],

    "ingles": [
        "ingles", "inglés",
        "toefl", "ielts", "duolingo"
    ],

    "internacional": [
        "intercambio", "francia",
        "londres", "internacional",
        "doble titulacion"
    ],

    "sedes": [
        "campus", "donde",
        "ubicacion", "ubicación",
        "sede", "cochabamba",
        "santa cruz", "la paz"
    ],

    "costos": [
        "precio", "costo",
        "mensualidad", "pension",
        "pensión", "cuanto vale"
    ],

    "modalidad": [
        "virtual", "presencial",
        "modular", "clases"
    ],

    "vida": [
        "vida universitaria",
        "actividades",
        "deportes", "eventos"
    ],

    "laboratorios": [
        "laboratorios",
        "tecnologia",
        "tecnología",
        "equipos"
    ]
}

# =========================================================
# MOTOR IA
# =========================================================

def limpiar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r'[^\w\s]', '', texto)
    return texto

def detectar_intencion(mensaje):

    mensaje = limpiar_texto(mensaje)

    puntuaciones = {}

    for categoria, palabras in KEYWORDS.items():

        score = 0

        for palabra in palabras:

            if palabra in mensaje:
                score += 2

            similares = get_close_matches(
                palabra,
                mensaje.split(),
                n=1,
                cutoff=0.8
            )

            if similares:
                score += 1

        puntuaciones[categoria] = score

    mejor_categoria = max(puntuaciones, key=puntuaciones.get)

    if puntuaciones[mejor_categoria] > 0:
        return mejor_categoria

    return None

# =========================================================
# CHATBOT PRINCIPAL
# =========================================================

def respuesta_bot(mensaje):

    if not mensaje.strip():
        return "Escríbeme una pregunta 😊"

    mensaje_lower = mensaje.lower()

    # SALUDOS
    saludos = [
        "hola", "buenas",
        "hello", "hi",
        "que tal", "qué tal"
    ]

    if any(s in mensaje_lower for s in saludos):
        return UPB_DATA["saludo"]

    # DETECTAR INTENCIÓN
    intencion = detectar_intencion(mensaje)

    if intencion and intencion in UPB_DATA:
        return UPB_DATA[intencion]

    # RESPUESTA MÁS INTELIGENTE
    if "mejor universidad" in mensaje_lower:
        return """
🔥 La UPB es considerada una de las universidades privadas más prestigiosas de Bolivia.

Destaca por:
✅ Nivel académico alto
✅ Enfoque internacional
✅ Tecnología moderna
✅ Convenios internacionales
✅ Empleabilidad
✅ Innovación
"""

    if "trabajo" in mensaje_lower:
        return """
💼 La UPB tiene gran reconocimiento laboral.

Muchas empresas buscan graduados UPB por:
✅ Nivel académico
✅ Inglés
✅ Liderazgo
✅ Tecnología
✅ Formación práctica
"""

    if "dificil" in mensaje_lower:
        return """
📚 La UPB tiene un nivel académico exigente, pero con esfuerzo y organización puedes adaptarte perfectamente 🚀
"""

    # FALLBACK INTELIGENTE
    return CONTACTO_HUMANO

# =========================================================
# RUTAS FLASK
# =========================================================

@app.route('/')
def home():
    return "🤖 SUPER IA UPB ACTIVA"

@app.route('/chat', methods=['POST'])
def chat():

    try:

        data = request.get_json()

        user_message = data.get('message', '')

        response = respuesta_bot(user_message)

        return jsonify({
            "status": "success",
            "response": response
        })

    except Exception as e:

        print("ERROR:", e)

        return jsonify({
            "status": "error",
            "response": "⚠️ Ocurrió un error técnico."
        }), 500

# =========================================================
# INICIAR SERVIDOR
# =========================================================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host='0.0.0.0',
        port=port,
        debug=True
    )
