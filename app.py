import os
import asyncio
import logging
import random
from datetime import datetime
from telegram import Bot
from telegram.error import TelegramError
import glob
import json

# Configuration
BOT_TOKEN = "8444990656:AAGeAF1AflD4UvnB9qXwv5M23VAECpn-8sQ"
CHANNEL_ID = -1002106421814
FOLDER_PATH = "images"
SENT_LOG = "sent.json"
INTERVAL_MINUTES = 25  # ← CHANGE ICI : 25 minutes

# Messages aléatoires pour accompagner les images
CAPTIONS = [
    "🚀 Nouveau flyer !",
    "📊 À ne pas rater !",
    "💡 Une info pour vous",
    "🔥 Offre spéciale",
    "💰 Opportunité à saisir",
    "📈 Les marchés bougent",
    "🎯 Stratégie du jour",
    "⚡ Action rapide",
    "🏆 Nos experts recommandent",
    "💎 Contenu exclusif"
]

# Hashtags automatiques
HASHTAGS = ["#Trading", "#Crypto", "#Forex", "#Investissement", "#MrKom"]

logging.basicConfig(level=logging.INFO)

def load_sent_images():
    if os.path.exists(SENT_LOG):
        with open(SENT_LOG, 'r') as f:
            return set(json.load(f))
    return set()

def save_sent_image(filename):
    sent = load_sent_images()
    sent.add(filename)
    with open(SENT_LOG, 'w') as f:
        json.dump(list(sent), f)

def get_next_image():
    sent = load_sent_images()
    extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.webp']
    all_images = []
    for ext in extensions:
        all_images.extend(glob.glob(os.path.join(FOLDER_PATH, ext)))
    
    unsent = [img for img in all_images if img not in sent]
    
    if not unsent:
        logging.info("✅ Plus d'images à poster ! En attente de nouvelles images...")
        return None
    
    return unsent[0]

def get_random_caption():
    """Génère une légende aléatoire avec hashtags"""
    caption = random.choice(CAPTIONS)
    hashtags = random.sample(HASHTAGS, k=random.randint(1, 3))
    return f"{caption}\n\n{' '.join(hashtags)}"

async def post_image():
    bot = Bot(token=BOT_TOKEN)
    image_path = get_next_image()
    
    if image_path is None:
        return False
    
    try:
        # Récupère le nom du fichier sans le chemin
        filename = os.path.basename(image_path)
        
        with open(image_path, 'rb') as photo:
            # Envoie avec une légende aléatoire
            caption = get_random_caption()
            await bot.send_photo(
                chat_id=CHANNEL_ID, 
                photo=photo,
                caption=caption
            )
        
        save_sent_image(image_path)
        
        # Statistiques
        sent_count = len(load_sent_images())
        total_images = len(glob.glob(os.path.join(FOLDER_PATH, "*.*")))
        remaining = total_images - sent_count
        
        logging.info(f"✅ Image postée : {filename}")
        logging.info(f"📊 Statistiques : {sent_count}/{total_images} postées | Reste : {remaining}")
        return True
        
    except TelegramError as e:
        logging.error(f"❌ Erreur Telegram : {e}")
        return False

async def health_check():
    """Vérification périodique de l'état du bot"""
    while True:
        await asyncio.sleep(3600)  # Toutes les heures
        sent_count = len(load_sent_images())
        total_images = len(glob.glob(os.path.join(FOLDER_PATH, "*.*")))
        logging.info(f"💚 BOT EN VIE - {datetime.now().strftime('%H:%M:%S')} - {sent_count}/{total_images} images postées")

async def main():
    logging.info("🤖 BOT INTELLIGENT DÉMARRÉ !")
    logging.info(f"⏱️  Intervalle : {INTERVAL_MINUTES} minutes")
    logging.info(f"📁 Dossier images : {FOLDER_PATH}")
    logging.info(f"🎯 Channel : {CHANNEL_ID}")
    
    # Lance la vérification de santé en arrière-plan
    asyncio.create_task(health_check())
    
    while True:
        try:
            await post_image()
            logging.info(f"⏰ Prochaine publication dans {INTERVAL_MINUTES} minutes...")
            await asyncio.sleep(INTERVAL_MINUTES * 60)  # Conversion en secondes
            
        except Exception as e:
            logging.error(f"⚠️ Erreur inattendue : {e}")
            await asyncio.sleep(60)  # Attendre 1 minute avant de réessayer

if __name__ == "__main__":
    asyncio.run(main())