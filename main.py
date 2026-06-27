import os
import asyncio
import threading
from flask import Flask
from telegram.ext import ApplicationBuilder

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot está rodando!"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

async def enviar_mensagem(context):
    await context.bot.send_message(chat_id=CHAT_ID, text="Oi! Esta é a sua mensagem automática de 30 minutos.")

async def main():
    application = ApplicationBuilder().token(TOKEN).job_queue(True).build()
    application.job_queue.run_repeating(enviar_mensagem, interval=1800, first=10)

    # Inicia o Flask em uma thread separada para não travar o bot
    threading.Thread(target=run_flask).start()

    print("Bot rodando...")
    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())