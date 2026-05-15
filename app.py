from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from transformers import pipeline

app = Flask(__name__)
CORS(app)

# =====================================
# MODELO IA
# =====================================

chatbot = pipeline(
    "text-generation",
    model="distilgpt2"
)

# =====================================
# CONTEXTO EMPRESA
# =====================================

contexto_empresa = """
Eres el asistente virtual oficial de REPUESTOS GUTIERREZ SRL.

La empresa vende:
- Filtros
- Frenos
- Baterías
- Lubricantes
- Suspensión
- Accesorios automotrices

Debes responder únicamente temas relacionados con:
- Repuestos automotrices
- Atención al cliente
- Compatibilidad
- Horarios
- Ventas
- Servicios automotrices
"""


# =====================================
# PAGINA PRINCIPAL
# =====================================

@app.route('/')
def home():
    return render_template('index.html')

# =====================================
# CHATBOT API
# =====================================

@app.route('/chat', methods=['POST'])
def chat():

    data = request.get_json()
    pregunta = data['mensaje']

    # =====================================
    # RESPUESTAS RAPIDAS EMPRESARIALES
    # =====================================

    respuestas_fijas = {
        "filtro": "Sí, contamos con filtros de aceite, aire y combustible para diferentes marcas y modelos de vehículos.",
        "filtros": "Disponemos de filtros originales y alternativos para vehículos livianos y pesados.",
        "bateria": "Disponemos de baterías de diferentes amperajes para automóviles, camionetas y camiones.",
        "baterias": "Contamos con baterías selladas y de alto rendimiento para diferentes vehículos.",
        "horario": "Atendemos de lunes a sábado Horario Comercial.",
        "lubricante": "Sí, ofrecemos lubricantes sintéticos, semisintéticos y minerales.",
        "lubricantes": "Contamos con lubricantes para motores diésel y gasolina.",
        "freno": "Tenemos frenos, pastillas y discos para diferentes vehículos.",
        "frenos": "Disponemos de sistemas de frenos y accesorios automotrices.",
        "toyota": "Contamos con repuestos para Toyota. Indique el modelo y año del vehículo.",
        "nissan": "Disponemos de repuestos para Nissan, incluyendo suspensión, filtros y frenos.",
        "suzuki": "Sí, contamos con repuestos originales y alternativos para Suzuki.",
        "mazda": "Tenemos filtros, amortiguadores y repuestos para Mazda.",
        "hyundai": "Disponemos de repuestos Hyundai para diferentes modelos.",
        "kia": "Sí, contamos con accesorios y repuestos para Kia.",
        "precio": "Puede solicitar una cotización indicando marca, modelo y año del vehículo.",
        "precios": "Los precios varían según el tipo de repuesto y la marca.",
        "cotizacion": "Podemos realizar cotizaciones rápidas para repuestos y accesorios.",
        "ubicacion": "Estamos ubicados en Cochabamba, Bolivia.",
        "direccion": "Nuestra tienda principal se encuentra en Cochabamba, Bolivia.",
        "envio": "Realizamos envíos a diferentes ciudades del país.",
        "delivery": "Contamos con servicio de entrega para pedidos seleccionados.",
        "pago": "Aceptamos pagos en efectivo, transferencia y QR.",
        "pagos": "Puede realizar pagos mediante QR, transferencia bancaria o efectivo.",
        "garantia": "Los productos cuentan con garantía según la marca y el fabricante.",
        "garantía": "Ofrecemos garantía en productos seleccionados.",
        "aceite": "Tenemos aceites sintéticos y minerales para diferentes motores.",
        "motor": "Disponemos de repuestos y accesorios para motores diésel y gasolina.",
        "suspension": "Contamos con amortiguadores, resortes y piezas de suspensión.",
        "suspensión": "Disponemos de sistemas de suspensión para vehículos livianos y pesados.",
        "camioneta": "Sí, tenemos repuestos para camionetas y vehículos 4x4.",
        "camion": "Contamos con repuestos para camiones y transporte pesado.",
        "accesorios": "Disponemos de accesorios automotrices modernos y de alta calidad.",
        "llantas": "Podemos orientarlo sobre llantas y accesorios relacionados.",
        "radiador": "Sí, contamos con radiadores y sistemas de refrigeración.",
        "embrague": "Disponemos de kits de embrague y accesorios relacionados.",
        "amortiguador": "Tenemos amortiguadores delanteros y traseros.",
        "faros": "Contamos con faros, luces y accesorios eléctricos.",
        "electrico": "Disponemos de repuestos eléctricos automotrices.",
        "electricos": "Sí, contamos con sensores, luces y accesorios eléctricos.",
        "consulta": "Gracias por comunicarse con REPUESTOS GUTIÉRREZ SRL. ¿Qué repuesto necesita?",
        "hola": "¡Hola! Bienvenido a REPUESTOS GUTIÉRREZ SRL. ¿Cómo podemos ayudarle?",
        "buenos dias": "¡Buenos días! Estamos listos para ayudarle con sus consultas automotrices.",
        "gracias": "Gracias por confiar en REPUESTOS GUTIÉRREZ SRL.",
        "adios": "Gracias por visitarnos. ¡Lo esperamos nuevamente!"
    }

    pregunta_lower = pregunta.lower()

    for clave, respuesta in respuestas_fijas.items():
        if clave in pregunta_lower:
            return jsonify({
                'respuesta': respuesta
            })


    # =====================================
    # PROMPT IA MEJORADO
    # =====================================

    prompt = f'''
{contexto_empresa}

Cliente: {pregunta}
Asistente:
'''

    respuesta = chatbot(
        prompt,
        max_new_tokens=60,
        temperature=0.3,
        top_k=40,
        top_p=0.9,
        repetition_penalty=1.2,
        do_sample=True,
        truncation=True,
        pad_token_id=50256
    )

    texto = respuesta[0]['generated_text']

    resultado = texto.split('Asistente:')[-1].strip()
    # =====================================
    # VALIDAR RESPUESTA
    # =====================================

    if len(resultado) < 5:
        resultado = 'Puede visitar nuestra tienda para mayor información sobre repuestos automotrices.'

    if 'Cliente:' in resultado:
        resultado = resultado.split('Cliente:')[0]

    return jsonify({
        'respuesta': resultado.strip()
    })

# =====================================
# EJECUTAR
# =====================================

if __name__ == '__main__':
    app.run(debug=True)