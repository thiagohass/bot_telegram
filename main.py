import os
import threading
from flask import Flask
from telegram.ext import ApplicationBuilder

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot está rodando!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

async def enviar_mensagem(context):
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text="Oi! Esta é a sua mensagem automática de 30 minutos."
    )

def main():
    if not TOKEN:
        raise ValueError("TOKEN não encontrada nas variáveis de ambiente.")

    if not CHAT_ID:
        raise ValueError("CHAT_ID não encontrado nas variáveis de ambiente.")

    threading.Thread(
        target=run_flask,
        daemon=True
    ).start()

    application = ApplicationBuilder().token(TOKEN).build()

    application.job_queue.run_repeating(
        enviar_mensagem,
        interval=1800,  # 30 minutos
        first=10        # primeira mensagem após 10 segundos
    )

    print("Bot rodando...")
    application.run_polling()

if __name__ == "__main__":
    main()