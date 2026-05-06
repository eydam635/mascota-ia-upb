from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app) # Esto es vital para que Google Sites no bloquee la conexión

# AQUÍ PONES LA INFO DE TUS PDF Y DOCX
CONTEXTO_UPB = """
Eres la mascota oficial de IA de la UPB. Tu objetivo es ayudar en admisiones.
Información clave:
- Carreras: Ing. de Inteligencia Artificial (4.5 años), Civil, Sistemas, etc.
- PAA (Examen): Cuesta 200 bs. Puntaje mínimo: 1100/1600.
- Requisitos: Ensayo, CV, Libreta de 5to secundaria.
- Contacto WhatsApp: 78508450.
- Prepa UPB: Obligatorio para nivelación.
"""

@app.route('/preguntar', methods=['POST'])
def preguntar():
    datos = request.json
    pregunta_usuario = datos.get("mensaje")
    
    # Aquí es donde conectarías con la API de OpenAI o Gemini
    # Por ahora, simulamos una respuesta usando el contexto
    respuesta = f"Soy la mascota UPB: Sobre '{pregunta_usuario}', te cuento que el examen PAA cuesta 200 bs y la carrera de IA dura 4.5 años."
    
    return jsonify({"respuesta": respuesta})

if __name__ == "__main__":
    # Render usa el puerto que le asigne el sistema
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)