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

# lista de mensagens com texto + foto
mensagens = [
    {"texto": "_*🍛 NÃO ESQUECE DE GRAVAR A LOUÇA DO ALMOÇO! 🧼*_

Garanta aqueles minutos valiosos para suas horas diárias.", "foto": "imagens/foto1.png"},
    {"texto": "_*👯‍♀️ CHAMA AS AMIGAS! 👯‍♀️*_
`Coisa boa precisa ser dividida com quem você gosta!` 

Traga suas amigas para a campanha de Tarefas Domésticas e *ganhem juntas*!", "foto": "imagens/foto2.png"},
    {"texto": "Mensagem 4", "foto": "https://exemplo.com/foto4.jpg"},
    {"texto": "Mensagem 4", "foto": "https://exemplo.com/foto4.jpg"},
    {"texto": "Mensagem 5", "foto": "https://exemplo.com/foto5.jpg"},
]

indice = 0

async def enviar_mensagem(context):
    global indice
    msg = mensagens[indice]

    # envia texto
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text=msg["texto"]
    )

    # envia foto
    await context.bot.send_photo(
        chat_id=CHAT_ID,
        photo=msg["foto"],
        caption=f"Imagem da {msg['texto']}"
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
