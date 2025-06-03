import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración del bot
BOT_TOKEN = os.getenv('BOT_TOKEN')
FREE_GROUP_ID = int(os.getenv('FREE_GROUP_ID'))
VIP_GROUP_ID = int(os.getenv('VIP_GROUP_ID'))

# Configuración de pagos
STRIPE_PROVIDER_TOKEN = os.getenv('STRIPE_PROVIDER_TOKEN')
PAYPAL_CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID')
PAYPAL_CLIENT_SECRET = os.getenv('PAYPAL_CLIENT_SECRET')
TRON_NODE_URL = os.getenv('TRON_NODE_URL')
ETHEREUM_NODE_URL = os.getenv('ETHEREUM_NODE_URL')
WALLET_PRIVATE_KEY = os.getenv('WALLET_PRIVATE_KEY')

# Validaciones de configuración crítica
required_vars = {
    'BOT_TOKEN': BOT_TOKEN,
    'FREE_GROUP_ID': FREE_GROUP_ID,
    'VIP_GROUP_ID': VIP_GROUP_ID,
    'STRIPE_PROVIDER_TOKEN': STRIPE_PROVIDER_TOKEN,
    'PAYPAL_CLIENT_ID': PAYPAL_CLIENT_ID,
    'PAYPAL_CLIENT_SECRET': PAYPAL_CLIENT_SECRET,
    'TRON_NODE_URL': TRON_NODE_URL,
    'ETHEREUM_NODE_URL': ETHEREUM_NODE_URL,
    'WALLET_PRIVATE_KEY': WALLET_PRIVATE_KEY,
}

missing = [k for k, v in required_vars.items() if v in (None, '', 0)]
if missing:
    raise EnvironmentError(f"Faltan variables de entorno requeridas: {', '.join(missing)}")
