from config import STRIPE_PROVIDER_TOKEN, VIP_GROUP_ID
from telegram.ext import CommandHandler, ContextTypes, PreCheckoutQueryHandler, filters
from telegram import Update, LabeledPrice
import logging

logger = logging.getLogger(__name__)

async def pagar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    title = "Acceso VIP a Hojutsu Labs"
    description = "Pago único para obtener acceso al grupo exclusivo Hojutsu Labs VIP."
    payload = "vip_payment"
    currency = "USD"
    prices = [LabeledPrice("Acceso VIP", 1000)]  # 1000 = $10.00
    try:
        await context.bot.send_invoice(
            chat_id,
            title,
            description,
            payload,
            STRIPE_PROVIDER_TOKEN,
            currency,
            prices
        )
        logger.info(f"Factura enviada a {chat_id}")
    except Exception as e:
        logger.error(f"Error al enviar factura: {e}")
        await update.message.reply_text("No se pudo procesar el pago. Intenta más tarde.")

async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.pre_checkout_query
    if query.invoice_payload != "vip_payment":
        await query.answer(ok=False, error_message="Error en el payload de pago.")
        logger.warning(f"Payload inválido: {query.invoice_payload}")
    else:
        await query.answer(ok=True)
        logger.info(f"Pre-checkout aprobado para usuario {query.from_user.id}")

async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    logger.info(f"Pago exitoso de usuario {user_id}")
    await update.message.reply_text("¡Pago recibido! Ahora tienes acceso al grupo VIP.")
    try:
        await context.bot.invite_chat_member(VIP_GROUP_ID, user_id)
    except Exception as e:
        logger.error(f"Error al invitar al grupo VIP: {e}")
        await update.message.reply_text("No se pudo añadir al grupo VIP automáticamente. Contacta a un admin.")

def register_handlers(app):
    app.add_handler(CommandHandler("pagar", pagar))
    app.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    app.add_handler(filters.SUCCESSFUL_PAYMENT, successful_payment)
