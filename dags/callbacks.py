"""
Module de callbacks pour les DAGs Airflow.
Contient la logique d'envoi d'alertes vers WhatsApp via TextMeBot.
"""
import logging
import requests
from urllib.parse import quote

logger = logging.getLogger(__name__)

# ==============================================================================
# ⚠️ CONFIGURATION : Remplacez ces valeurs par les vôtres
# ==============================================================================
TEXTMEBOT_API_KEY = "5eVkFXyMp6SV"          # La clé reçue par email
WHATSAPP_PHONE = "+21624989255"              # Votre numéro au format international
# ==============================================================================

def task_failure_whatsapp_alert(context):
    """
    Callback appelé automatiquement lorsqu'une tâche échoue.
    Envoie une alerte WhatsApp via l'API TextMeBot.
    """
    try:
        # 1. Extraction des informations depuis le contexte Airflow
        task_instance = context.get("task_instance")
        dag_id = task_instance.dag_id
        task_id = task_instance.task_id
        log_url = task_instance.log_url
        exception = context.get("exception")
        
        # 2. Construction du message (avec formatage Markdown pour WhatsApp)
        message = (
            f"🚨 *Échec d'une tâche Airflow*\n\n"
            f"*DAG :* {dag_id}\n"
            f"*Tâche :* {task_id}\n"
            f"*Erreur :* {str(exception)[:200]}\n\n"
            f"*Logs :* {log_url}"
        )
        
        # 3. Encodage du message pour qu'il soit valide dans l'URL
        encoded_message = quote(message)
        
        # 4. Construction de l'URL de l'API TextMeBot
        url = (
            f"https://api.textmebot.com/send.php?"
            f"recipient={quote(WHATSAPP_PHONE)}"
            f"&apikey={TEXTMEBOT_API_KEY}"
            f"&text={encoded_message}"
            f"&json=yes"
        )
        
        # 5. Envoi de la requête HTTP
        response = requests.get(url, timeout=10)
        
        # 6. Vérification de la réponse
        if response.status_code == 200:
            logger.info("Alerte WhatsApp envoyée avec succès via TextMeBot.")
        else:
            logger.error(f"Échec de l'envoi. Statut: {response.status_code}, Réponse: {response.text}")

    except Exception as e:
        # On ne veut jamais qu'une erreur dans le callback ne masque l'erreur originale d'Airflow
        logger.error(f"Impossible d'envoyer l'alerte WhatsApp : {e}")