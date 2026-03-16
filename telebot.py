import os
import sys
import argparse
import threading
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import Message

app = Flask(__name__)

@app.route("/")
def base_flask():
    return "Bot is running!"

def run_flask():
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)

class NekoTelegram:
    def __init__(self, api_id, api_hash, bot_token):
        self.api_id = api_id
        self.api_hash = api_hash
        self.bot_token = bot_token
        self.app = Client("nekobot", api_id=int(api_id), api_hash=api_hash, bot_token=bot_token)
        self.flask_thread = None
        
        @self.app.on_message(filters.private)
        async def handle_message(client: Client, message: Message):
            await self._handle_message(client, message)
    
    async def _handle_message(self, client: Client, message: Message):
        if not message.text:
            return
        
        text = message.text.strip()

        if text.startswith("/start"):
            await client.send_photo(
                chat_id=message.chat.id,
                photo="https://cdn.imgchest.com/files/93cb097b575e.webp",
                protect_content=True,
                caption="Nyaa, Hello, I'm Alice. The cute pet of @nakigeplayer"
            )
    
    def start_flask(self):
        if self.flask_thread and self.flask_thread.is_alive():
            return
            
        self.flask_thread = threading.Thread(target=run_flask, daemon=True)
        self.flask_thread.start()
    
    def run(self):
        self.app.run()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-A", "--api", help="API ID")
    parser.add_argument("-H", "--hash", help="API Hash")
    parser.add_argument("-T", "--token", help="Bot Token")
    parser.add_argument("-F", "--flask", action="store_true", help="Incluir Flask")
    args = parser.parse_args()

    api_id = args.api or os.environ.get("API_ID")
    api_hash = args.hash or os.environ.get("API_HASH")
    bot_token = args.token or os.environ.get("BOT_TOKEN")
    
    if not all([api_id, api_hash, bot_token]):
        print("Error: Faltan credenciales")
        sys.exit(1)
    
    bot = NekoTelegram(api_id, api_hash, bot_token)

    if args.flask:
        bot.start_flask()
    
    bot.run()

if __name__ == "__main__":
    main()
