from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Obtener variables de entorno
TELEGRAM_BOT_TOKEN = os.getenv('7250099290:AAES0s4Ixl6XjMRgPKoh4IjpsAocIFBScBQ')
TELEGRAM_CHAT_ID = os.getenv('7115083048')

# Ruta para manejar solicitudes GET (verificación de monday.com)
@app.route('/webhook', methods=['GET'])
def verify_webhook():
    # Obtén el parámetro "challenge" de la solicitud
    challenge = request.args.get('challenge')
    if challenge:
        # Devuelve el valor del challenge para verificar la URL
        return challenge, 200
    else:
        return "Falta el parámetro 'challenge'.", 400

# Ruta para manejar solicitudes POST (webhook de monday.com)
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Obtén los datos JSON de la solicitud
        data = request.json
        if not data:
            return jsonify({"status": "error", "message": "No se recibieron datos JSON"}), 400

        print("Datos recibidos del webhook:", data)

        # Verifica si el evento es un cambio en el estado
        if data.get('event', {}).get('type') == 'change_column_value':
            item_id = data['event']['pulseId']
            new_status = data['event']['value']['label']  # Asume que el estado es un label

            # Mensaje para Telegram
            message = f"El estado del elemento {item_id} ha cambiado a: {new_status}"
            print(message)  # Imprime el mensaje en los logs

            # Envía la notificación a Telegram
            send_telegram_message(message)

        return jsonify({"status": "success"}), 200
    except Exception as e:
        print("Error en el webhook:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

# Función para enviar mensajes a Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot7250099290:AAES0s4Ixl6XjMRgPKoh4IjpsAocIFBScBQ/sendMessage"
    payload = {
        "chat_id": 7115083048,
        "text": message
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print("Error enviando mensaje a Telegram:", response.text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)