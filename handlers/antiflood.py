import asyncio
from collections import defaultdict, deque
from datetime import datetime, timedelta
from telegram.ext import MessageHandler, filters, ContextTypes
from telegram import Update, ChatPermissions
import logging

# Configuración de anti-flood
FLOOD_LIMIT = 5  # mensajes
FLOOD_WINDOW = 10  # segundos
MUTE_DURATION = 60  # segundos

# Estructura: user_id -> deque de timestamps
user_message_times = defaultdict(lambda: deque(maxlen=FLOOD_LIMIT))

logger = logging.getLogger(__name__)

async def check_flood(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    now = datetime.utcnow()
    times = user_message_times[user_id]
    times.append(now)

    # Verificar si el usuario excede el límite en la ventana de tiempo
    if len(times) == FLOOD_LIMIT and (now - times[0]).total_seconds() <= FLOOD_WINDOW:
        logger.info(f"Usuario {user_id} silenciado por flood en chat {update.message.chat_id}")
        await update.message.reply_text("⚠️ Estás enviando demasiados mensajes. Silenciado temporalmente.")
        try:
            await context.bot.restrict_chat_member(
                update.message.chat_id,
                user_id,
                permissions=ChatPermissions(can_send_messages=False),
                until_date=now + timedelta(seconds=MUTE_DURATION)
            )
        except Exception as e:
            logger.error(f"Error al silenciar usuario {user_id}: {e}")
        # Limpiar el historial para evitar silenciar repetidamente
        user_message_times[user_id].clear()


def register_handlers(app):
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_flood))
