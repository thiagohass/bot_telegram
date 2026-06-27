import os
import asyncio
from telegram.ext import ApplicationBuilder

TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

async def enviar_mensagem(context):
    await context.bot.send_message(chat_id=CHAT_ID, text="Oi! Esta é a sua mensagem automática de 30 minutos.")

async def main():
    # A mudança principal está aqui: usar build() sem chamar job_queue diretamente
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Criar o job com o job_queue do application
    application.job_queue.run_repeating(enviar_mensagem, interval=1800, first=10)
    
    print("Bot rodando...")
    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())