from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Configuración de Telegram
TELEGRAM_BOT_TOKEN = '7250099290:AAES0s4Ixl6XjMRgPKoh4IjpsAocIFBScBQ'
TELEGRAM_CHAT_ID = '7115083048'

# Ruta para manejar el webhook de monday.com
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Datos recibidos del webhook:", data)

    # Verifica si el evento es un cambio en el estado
    if data.get('event', {}).get('type') == 'change_column_value':
        item_id = data['event']['pulseId']
        new_status = data['event']['value']['label']  # Asume que el estado es un label

        # Mensaje para Telegram
        message = f"El estado del elemento {item_id} ha cambiado a: {new_status}"

        # Envía la notificación a Telegram
        send_telegram_message(message)

    return jsonify({"status": "success"}), 200

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