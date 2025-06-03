import logging
from telegram.ext import ApplicationBuilder
from config import BOT_TOKEN
from handlers import welcome, antiflood, moderation, payments, payments_paypal, payments_crypto, vip_access
from logging_config import setup_logging

# Configurar logging
logger = setup_logging()

def main():
    try:
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        logger.info("Bot iniciado correctamente")
    except Exception as e:
        logger.error(f"Error iniciando el bot: {str(e)}")
        raise

    # Registrar handlers
    welcome.register_handlers(app)
    antiflood.register_handlers(app)
    moderation.register_handlers(app)
    payments.register_handlers(app)
    vip_access.register_handlers(app)

    print("Bot iniciado...")
    app.run_polling()

if __name__ == "__main__":
    main()
