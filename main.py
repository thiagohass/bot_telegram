import os
import threading
from flask import Flask
from telegram.ext import ApplicationBuilder

app = Flask(__name__)

# Rota simples para manter o bot ativo em serviços como Render/Railway
@app.route("/")
def home():
    return "Bot está rodando!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# Configurações
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Lista de mensagens
mensagens = [
    {
        "texto": "🍛 NÃO ESQUECE DE GRAVAR A LOUÇA DO ALMOÇO! 🧼",
        "foto": "imagens/foto1.png"
    },
    {
        "texto": "👯‍♀️ CHAMA AS AMIGAS! 👯‍♀️",
        "foto": "imagens/foto2.png"
    },
    {
        "texto": "Mensagem 4",
        "foto": "https://exemplo.com/foto4.jpg"
    }
]

indice = 0

async def enviar_mensagem(context):
    global indice
    msg = mensagens[indice]
    
    try:
        # Verifica se o arquivo é local ou URL
        photo_path = msg["foto"]
        
        if photo_path.startswith("http"):
            photo_input = photo_path
        else:
            # Verifica se o arquivo existe para evitar crash
            if not os.path.exists(photo_path):
                print(f"Erro: Arquivo {photo_path} não encontrado.")
                return
            photo_input = open(photo_path, 'rb')

        # Envia como foto com legenda
        await context.bot.send_photo(
            chat_id=CHAT_ID,
            photo=photo_input,
            caption=msg["texto"]
        )
        
        # Fecha o arquivo se foi aberto localmente
        if hasattr(photo_input, 'close'):
            photo_input.close()

    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")
    
    # Atualiza o índice para a próxima vez
    indice = (indice + 1) % len(mensagens)

def main():
    if not TOKEN or not CHAT_ID:
        raise ValueError("TOKEN ou CHAT_ID não definidos nas variáveis de ambiente.")

    # Inicia o Flask em uma thread separada
    threading.Thread(target=run_flask, daemon=True).start()

    # Configuração do bot
    application = ApplicationBuilder().token(TOKEN).build()

    # Job que roda a cada 60 segundos
    application.job_queue.run_repeating(
        enviar_mensagem,
        interval=60,
        first=10
    )

    print("Bot iniciado com sucesso...")
    application.run_polling()

if __name__ == "__main__":
    main()