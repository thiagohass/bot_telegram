import os
import asyncio
from telegram.ext import ApplicationBuilder

# Pega os dados das Variáveis de Ambiente que vamos configurar na nuvem
TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

async def enviar_mensagem(context):
    await context.bot.send_message(chat_id=CHAT_ID, text="Oi! Esta é a sua mensagem automática de 30 minutos.")

async def main():
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Configura o loop: 1800 segundos = 30 minutos
    job_queue = application.job_queue
    job_queue.run_repeating(enviar_mensagem, interval=1800, first=10)
    
    print("Bot rodando...")
    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())