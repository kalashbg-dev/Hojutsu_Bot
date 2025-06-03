import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from paypalrestsdk import Api, Payment
import logging
from config import VIP_GROUP_ID

load_dotenv()
logger = logging.getLogger(__name__)

# Configurar PayPal API
api = Api({
    'mode': 'sandbox' if os.getenv('ENVIRONMENT', 'development') == 'development' else 'live',
    'client_id': os.getenv('PAYPAL_CLIENT_ID'),
    'client_secret': os.getenv('PAYPAL_CLIENT_SECRET')
})

def create_payment(amount: float, description: str):
    """Crear un pago de PayPal y devolver el objeto Payment o None"""
    try:
        payment = Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "transactions": [{
                "amount": {"total": str(amount), "currency": "USD"},
                "description": description
            }],
            "redirect_urls": {
                "return_url": "https://your-website.com/success",
                "cancel_url": "https://your-website.com/cancel"
            }
        })
        if payment.create():
            logger.info(f"Pago PayPal creado: {payment.id}")
            return payment
        else:
            logger.error(f"Error creando pago PayPal: {payment.error}")
            return None
    except Exception as e:
        logger.error(f"Excepción creando pago PayPal: {e}")
        return None

async def handle_paypal_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para procesar pagos de PayPal"""
    amount = 10.00  # Ejemplo: $10
    description = "Acceso VIP a Hojutsu Labs"
    payment = create_payment(amount, description)
    if payment:
        approval_url = next((str(link.href) for link in payment.links if link.rel == "approval_url"), None)
        if approval_url:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Por favor, completa el pago en: {approval_url}"
            )
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="No se pudo obtener el enlace de aprobación de PayPal."
            )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Error al crear el pago de PayPal. Intenta más tarde."
        )

# Nota: El manejo de la notificación de pago exitoso debe implementarse mediante webhook o polling externo.
# Aquí solo se muestra el flujo de inicio de pago.

def register_handlers(app):
    app.add_handler(CommandHandler("pagar_paypal", handle_paypal_payment))
