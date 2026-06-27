import os
import threading
from flask import Flask
from telegram.ext import ApplicationBuilder

app = Flask(__name__)

# Configurações
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# --- LÓGICA DE PERSISTÊNCIA DO ÍNDICE ---
def carregar_indice():
    if os.path.exists("indice.txt"):
        with open("indice.txt", "r") as f:
            try:
                return int(f.read())
            except ValueError:
                return 0
    return 0

def salvar_indice(idx):
    with open("indice.txt", "w") as f:
        f.write(str(idx))

# Lista de mensagens
mensagens = [
    {
        "texto": "🍛 NÃO ESQUECE DE GRAVAR A LOUÇA DO ALMOÇO! 🧼
Garanta aqueles minutos valiosos para suas horas diárias. ",
        "foto": "imagens/foto1.png"
    },
    {
        "texto": "_*👯‍♀️ CHAMA AS AMIGAS! 👯‍♀️*_
`Coisa boa precisa ser dividida com quem você gosta!` 

Traga suas amigas para a campanha de Tarefas Domésticas e *ganhem juntas*!",
        "foto": "imagens/foto2.png"
    }
]

@app.route("/")
def home():
    return "Bot está rodando!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

async def enviar_mensagem(context):
    indice = carregar_indice()
    msg = mensagens[indice]
    
    try:
        photo_path = msg["foto"]
        
        # Verifica se é URL ou arquivo local
        if photo_path.startswith("http"):
            photo_input = photo_path
        else:
            if not os.path.exists(photo_path):
                print(f"Erro: Arquivo {photo_path} não encontrado.")
                return
            photo_input = open(photo_path, 'rb')

        # Envia a foto com legenda
        await context.bot.send_photo(
            chat_id=CHAT_ID,
            photo=photo_input,
            caption=msg["texto"]
        )
        
        if hasattr(photo_input, 'close'):
            photo_input.close()
            
        # Atualiza e salva o próximo índice
        novo_indice = (indice + 1) % len(mensagens)
        salvar_indice(novo_indice)
        
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")

def main():
    if not TOKEN or not CHAT_ID:
        raise ValueError("TOKEN ou CHAT_ID não definidos.")

    threading.Thread(target=run_flask, daemon=True).start()

    application = ApplicationBuilder().token(TOKEN).build()

    if application.job_queue:
        application.job_queue.run_repeating(
            enviar_mensagem,
            interval=60,
            first=10
        )

    application.run_polling()

if __name__ == "__main__":
    main()