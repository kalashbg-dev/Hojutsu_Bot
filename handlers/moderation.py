from telegram.ext import CommandHandler, ContextTypes
from telegram import Update, ChatPermissions
import logging
from datetime import datetime, timedelta

MUTE_DURATION = 300  # segundos (5 minutos)
logger = logging.getLogger(__name__)

async def restrict_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("Debes responder al mensaje del usuario que quieres silenciar.")
        return

    admin_member = await context.bot.get_chat_member(update.message.chat_id, update.message.from_user.id)
    if not (admin_member.status in ("administrator", "creator")):
        await update.message.reply_text("Solo los administradores pueden usar este comando.")
        return

    user_id = update.message.reply_to_message.from_user.id
    until_date = datetime.utcnow() + timedelta(seconds=MUTE_DURATION)
    try:
        await context.bot.restrict_chat_member(
            update.message.chat_id,
            user_id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=until_date
        )
        logger.info(f"Usuario {user_id} silenciado por {update.message.from_user.id} en chat {update.message.chat_id}")
        await update.message.reply_text(f"🔇 Usuario silenciado por {MUTE_DURATION//60} minutos.")
        # Intentar notificar al usuario silenciado por privado (opcional)
        try:
            await context.bot.send_message(user_id, f"Has sido silenciado en el grupo {update.message.chat.title} por {MUTE_DURATION//60} minutos.")
        except Exception:
            pass  # Puede fallar si el usuario no tiene chat abierto con el bot
    except Exception as e:
        logger.error(f"Error al silenciar usuario {user_id}: {e}")
        await update.message.reply_text("No se pudo silenciar al usuario. ¿Tengo permisos suficientes?")

def register_handlers(app):
    app.add_handler(CommandHandler("silenciar", restrict_user))
