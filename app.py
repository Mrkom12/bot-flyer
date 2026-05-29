import os
import asyncio
import logging
from telegram import Bot
from telegram.error import TelegramError
import glob
import json

# Configuration
BOT_TOKEN = "8444990656:AAGeAF1AflD4UvnB9qXwv5M23VAECpn-8sQ"
CHANNEL_ID = -1002106421814
FOLDER_PATH = "images"
SENT_LOG = "sent.json"

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
        logging.info("Plus d'images à poster !")
        return None
    
    return unsent[0]

async def post_image():
    bot = Bot(token=BOT_TOKEN)
    image_path = get_next_image()
    
    if image_path is None:
        return False
    
    try:
        with open(image_path, 'rb') as photo:
            await bot.send_photo(chat_id=CHANNEL_ID, photo=photo)
        
        save_sent_image(image_path)
        logging.info(f"Image postée avec succès : {image_path}")
        return True
    except TelegramError as e:
        logging.error(f"Erreur Telegram : {e}")
        return False

async def main():
    logging.info("Bot démarré !")
    
    while True:
        await post_image()
        logging.info("Attente de 45 minutes...")
        await asyncio.sleep(2000)  # 45 minutes

if __name__ == "__main__":
    asyncio.run(main())