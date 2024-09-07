import axios from 'axios';

// Configuración del bot de Telegram
const token = '7258309648:AAFfsxkBnk7FHkwmJZpK3QeDh6HjxdzG2r8';
const chat_id = '722567297';
const telegram_url = `https://api.telegram.org/bot${token}/sendMessage`;

// URL que vamos a monitorear
const url_to_monitor = 'https://visas.migracion.gob.pa/SIVA/verif_citas/';

let previous_content = null;

async function sendTelegramMessage(message) {
  try {
    const response = await axios.post(telegram_url, {
      chat_id: chat_id,
      text: message,
    });

    if (response.status === 200) {
      console.log('Mensaje enviado exitosamente!');
    } else {
      console.error('Error al enviar el mensaje:', response.status);
    }
  } catch (error) {
    console.error('Error durante el envío del mensaje:', error);
  }
}

export default async function handler(req, res) {
  try {
    const response = await axios.get(url_to_monitor);
    const current_content = response.data;

    console.log('Contenido actual (primeros 100 caracteres):', current_content.slice(0, 100));

    if (previous_content !== null && current_content !== previous_content) {
      console.log('Cambio detectado. Enviando notificaciones...');
      for (let i = 0; i < 5; i++) {
        await sendTelegramMessage('¡Cambio detectado en la URL monitoreada!');
        await new Promise(resolve => setTimeout(resolve, 2000)); // Esperar 2 segundos entre mensajes
      }
    }

    previous_content = current_content;

    res.status(200).json({ message: 'Monitoreo completado' });
  } catch (error) {
    console.error('Error durante la solicitud:', error);
    res.status(500).json({ error: 'Error durante la solicitud' });
  }
}
