import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from web3 import Web3
from tronpy import Tron
import logging
from config import VIP_GROUP_ID

load_dotenv()
logger = logging.getLogger(__name__)

# Configurar conexiones a las redes
tron_client = Tron(network='mainnet')
tron_private_key = os.getenv('WALLET_PRIVATE_KEY')
tron_client.private_key = tron_private_key
tron_client.default_address = tron_client.address.from_private_key(tron_private_key)

w3 = Web3(Web3.HTTPProvider(os.getenv('ETHEREUM_NODE_URL')))

USDC_CONTRACT_ADDRESS_TRON = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
USDC_CONTRACT_ADDRESS_ETH = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"

async def handle_crypto_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando para iniciar pago en cripto (USDC Tron/Ethereum)"""
    try:
        args = context.args if hasattr(context, 'args') else []
        if not args or args[0].lower() not in ('tron', 'ethereum'):
            await update.message.reply_text("Uso: /pagar_crypto <tron|ethereum>")
            return
        network = args[0].lower()
        address = get_payment_address(network)
        await update.message.reply_text(
            f"Dirección de pago USDC ({network.title()}): {address}\nPor favor, envía tu pago y contacta a un admin para verificación.")
        logger.info(f"Dirección de pago {network} enviada a usuario {update.message.from_user.id}")
    except Exception as e:
        logger.error(f"Error generando dirección de pago cripto: {e}")
        await update.message.reply_text(f"Error generando dirección de pago: {str(e)}")

def get_payment_address(network: str) -> str:
    """Devuelve la dirección de pago para la red solicitada (no genera nuevas claves por seguridad)"""
    if network == 'tron':
        return tron_client.default_address.base58
    elif network == 'ethereum':
        return w3.eth.account.from_key(os.getenv('WALLET_PRIVATE_KEY')).address
    else:
        raise ValueError("Red no soportada")

# Nota: La verificación automática de pagos requiere integración con un servicio externo o polling.
# Aquí solo se muestra el flujo de inicio de pago y entrega de dirección.

def register_handlers(app):
    app.add_handler(CommandHandler("pagar_crypto", handle_crypto_payment))
