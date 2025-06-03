from config import VIP_GROUP_ID
from telegram.ext import CommandHandler, ContextTypes
from telegram import Update

# Simulación básica (en producción usar base de datos)
vip_users = set()

async def acceso_vip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in vip_users:
        invite_link = await context.bot.create_chat_invite_link(VIP_GROUP_ID, member_limit=1)
        await update.message.reply_text(f"🎟️ Aquí tienes acceso VIP: {invite_link.invite_link}")
    else:
        await update.message.reply_text("❌ No tienes acceso VIP. Realiza el pago para continuar.")

def register_handlers(app):
    app.add_handler(CommandHandler("vip", acceso_vip))
