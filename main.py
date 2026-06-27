import os
import threading
from flask import Flask
from telegram.ext import ApplicationBuilder

# Configurações iniciais
app = Flask(__name__)
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

@app.route("/")
def home():
    return "Bot está rodando!"

def run_flask():
    # O Render define a porta automaticamente, o código pega essa porta
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# Lista de mensagens
mensagens = [
    {
        "texto": "🍛 NÃO ESQUECE DE GRAVAR A LOUÇA DO ALMOÇO! 🧼",
        "foto": "imagens/foto1.png"
    },
    {
        "texto": "👯‍♀️ CHAMA AS AMIGAS! 👯‍♀️",
        "foto": "imagens/foto2.png"
    }
]

indice = 0

async def enviar_mensagem(context):
    global indice
    msg = mensagens[indice]
    
    try:
        photo_path = msg["foto"]
        
        # Lógica para tratar URL ou arquivo local
        if photo_path.startswith("http"):
            photo_input = photo_path
        else:
            if not os.path.exists(photo_path):
                print(f"Erro: Arquivo {photo_path} não encontrado.")
                return
            photo_input = open(photo_path, 'rb')

        await context.bot.send_photo(
            chat_id=CHAT_ID,
            photo=photo_input,
            caption=msg["texto"]
        )
        
        if hasattr(photo_input, 'close'):
            photo_input.close()

    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")
    
    indice = (indice + 1) % len(mensagens)

def main():
    if not TOKEN or not CHAT_ID:
        raise ValueError("TOKEN ou CHAT_ID não definidos.")

    # 1. Inicia o Flask
    threading.Thread(target=run_flask, daemon=True).start()

    # 2. Constrói a aplicação com o JobQueue habilitado automaticamente
    # A biblioteca 20+ inicializa o JobQueue ao chamar o builder
    application = ApplicationBuilder().token(TOKEN).build()

    # 3. Agenda o job
    if application.job_queue:
        application.job_queue.run_repeating(
            enviar_mensagem,
            interval=60,
            first=10
        )
        print("JobQueue configurado com sucesso.")
    else:
        print("Erro: JobQueue não foi carregado. Verifique o requirements.txt")
        return

    print("Bot rodando...")
    application.run_polling()

if __name__ == "__main__":
    main()