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

mensagens = [
    "Mensagem 1",
    "Mensagem 2",
    "Mensagem 3",
    "Mensagem 4",
    "Mensagem 5"
]

indice = 0

async def enviar_mensagem(context):
    global indice

    await context.bot.send_message(
        chat_id=CHAT_ID,
        text=mensagens[indice]
    )

    indice = (indice + 1) % len(mensagens)

def main():
    if not TOKEN:
        raise ValueError("TOKEN não encontrada.")

    if not CHAT_ID:
        raise ValueError("CHAT_ID não encontrado.")

    threading.Thread(
        target=run_flask,
        daemon=True
    ).start()

    application = ApplicationBuilder().token(TOKEN).build()

    application.job_queue.run_repeating(
        enviar_mensagem,
        interval=60,  # teste: 1 minuto
        first=10
    )

    print("Bot rodando...")
    application.run_polling()

if __name__ == "__main__":
    main()