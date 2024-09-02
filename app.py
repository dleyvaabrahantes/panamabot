import requests
import time
import urllib3

# Suprimir las advertencias de seguridad
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuración del bot de Telegram
token = '7258309648:AAFfsxkBnk7FHkwmJZpK3QeDh6HjxdzG2r8'
chat_id = '722567297'
telegram_url = f'https://api.telegram.org/bot{token}/sendMessage'

# URL que vamos a monitorear
url_to_monitor = 'https://visas.migracion.gob.pa/SIVA/verif_citas/'

# Variable para almacenar el contenido anterior
previous_content = None

def send_telegram_message(message):
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(telegram_url, data=payload)
    if response.status_code == 200:
        print('Mensaje enviado exitosamente!')
    else:
        print('Error al enviar el mensaje:', response.status_code)

while True:
    try:
        # Realizar la solicitud a la URL sin verificar SSL
        print("Realizando la solicitud a la URL...")
        response = requests.get(url_to_monitor, verify=False)
        print(f'Status code de la respuesta: {response.status_code}')
        
        if response.status_code == 200:
            current_content = response.text
            print('Contenido actual (primeros 100 caracteres):', current_content[:100])

            # Comparar con el contenido anterior
            if previous_content is not None:
                print('Comparando el contenido...')
                if current_content != previous_content:
                    print('Cambio detectado. Enviando notificaciones...')
                    for _ in range(5):  # Enviar el mensaje 5 veces
                        send_telegram_message('¡Cambio detectado en la URL monitoreada!')
                        time.sleep(2)  # Esperar 2 segundos entre mensajes

            # Actualizar el contenido anterior
            previous_content = current_content
        else:
            print(f'Error al acceder a la URL: {response.status_code}')
        
    except Exception as e:
        print(f'Error durante la solicitud: {e}')
    
    # Esperar un minuto antes de la siguiente revisión
    print("Esperando un minuto antes de la siguiente revisión...")
    time.sleep(60)
