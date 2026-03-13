import os
import sys
import argparse
from concurrent.futures import ThreadPoolExecutor
from pyrogram import Client, filters
from pyrogram.types import Message
from flask import Flask
import threading

class TelegramBaseBot:
    def __init__(self, api_id, api_hash, bot_token):
        self.api_id = api_id
        self.api_hash = api_hash
        self.bot_token = bot_token
        self.app = Client("nekobot", api_id=int(api_id), api_hash=api_hash, bot_token=bot_token)
        self.flask_thread = None
        self.download_pool = ThreadPoolExecutor(max_workers=20)
        self.flask_app = Flask(__name__)
        self.setup_handlers()
    
    def setup_handlers(self):
        @self.app.on_message(filters.command("start"))
        async def start_command(client: Client, message: Message):
            await message.reply("Ejemplo base de bot")
        
        @self.flask_app.route('/')
        def home():
            return "Bot de Telegram funcionando"
    
    def start_flask(self):
        def run_flask():
            self.flask_app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
        
        self.flask_thread = threading.Thread(target=run_flask, daemon=True)
        self.flask_thread.start()
        print("[INFO] Servidor Flask iniciado en puerto 5000")
    
    def run(self):
        try:
            self.app.run()
        except KeyboardInterrupt:
            print("\n[INFO] Bot detenido por el usuario")
        except Exception as e:
            print(f"[ERROR] Error al ejecutar el bot: {e}")
        finally:
            self.download_pool.shutdown(wait=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-A", "--api", help="API ID de Telegram")
    parser.add_argument("-H", "--hash", help="API Hash de Telegram")
    parser.add_argument("-T", "--token", help="Token del Bot")
    parser.add_argument("-F", "--flask", action="store_true", 
                       help="Incluir servidor Flask junto con el bot")
    args = parser.parse_args()

    api_id = args.api or os.environ.get("API_ID")
    api_hash = args.hash or os.environ.get("API_HASH")
    bot_token = args.token or os.environ.get("BOT_TOKEN")
    
    if not all([api_id, api_hash, bot_token]):
        print("Error: Faltan credenciales. Usa -A -H -T o variables de entorno.")
        sys.exit(1)
    
    bot = TelegramBaseBot(api_id, api_hash, bot_token)

    if args.flask:
        bot.start_flask()
    
    print("[INFO] Iniciando bot de Telegram...")
    bot.run()

if __name__ == "__main__":
    main()
