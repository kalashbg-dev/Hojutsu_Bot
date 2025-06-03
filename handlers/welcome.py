from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters, CallbackQueryHandler

async def send_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for user in update.message.new_chat_members:
        keyboard = InlineKeyboardMarkup.from_button(
            InlineKeyboardButton("✅ Confirmar", callback_data=f"verify_{user.id}")
        )
        await update.message.reply_text(
            f"¡Bienvenido {user.first_name}! Pulsa el botón para confirmar tu ingreso.",
            reply_markup=keyboard
        )

async def confirm_verification(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("✅ ¡Gracias por confirmar tu ingreso!")

def register_handlers(app):
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, send_welcome))
    app.add_handler(CallbackQueryHandler(confirm_verification, pattern="^verify_"))
