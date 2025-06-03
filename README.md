# 🤖 Hojutsu Labs Bot

Modelo para Bot de gestión de grupos de Telegram.

---

## 📋 Tabla de Contenidos
- [Requisitos previos](#requisitos-previos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Funciones incluidas](#funciones-incluidas)
- [Comandos disponibles](#comandos-disponibles)
- [Notas sobre pagos](#notas-sobre-pagos)
- [Seguridad](#seguridad)
- [Contribución](#contribución)

---

## 🛠️ Requisitos previos
- Python 3.8 o superior
- pip
- Cuenta en Telegram y acceso a BotFather
- Cuentas y credenciales para Stripe, PayPal, Tron/Ethereum (opcional según métodos de pago)

---

## 🚀 Instalación
1. Clona el repositorio:
   ```bash
   git clone <url-del-repo>
   cd hojutsu_bot
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:
   ```env
   BOT_TOKEN=tu_token_de_botfather
   PAYPAL_CLIENT_ID=tu_id_cliente_paypal
   PAYPAL_CLIENT_SECRET=tu_secreto_paypal
   STRIPE_PROVIDER_TOKEN=tu_token_stripe
   TRON_NODE_URL=https://api.trongrid.io
   ETHEREUM_NODE_URL=https://mainnet.infura.io/v3/tu_id_proyecto
   WALLET_PRIVATE_KEY=tu_clave_privada
   VIP_GROUP_ID=-1009876543210
   FREE_GROUP_ID=-1001234567890
   ```
4. Ejecuta el bot:
   ```bash
   python bot.py
   ```

---

## ⚙️ Configuración
- Todas las credenciales y tokens se manejan a través de variables de entorno.
- El archivo `.env` debe estar en `.gitignore` para evitar exposición de credenciales.
- Puedes personalizar la configuración en `config.py` y el logging en `logging_config.py`.

---

## 📁 Estructura del proyecto
```
hojutsu_bot/
├── assets/                # Recursos gráficos (favicon, logo)
├── handlers/              # Módulos de lógica del bot
│   ├── antiflood.py
│   ├── moderation.py
│   ├── payments.py
│   ├── payments_crypto.py
│   ├── payments_paypal.py
│   ├── vip_access.py
│   ├── welcome.py
│   └── __init__.py
├── bot.py                 # Script principal del bot
├── config.py              # Configuración general
├── logging_config.py      # Configuración de logs
├── requirements.txt       # Dependencias
└── README.md              # Documentación
```

---

## ✅ Funciones incluidas
- Verificación manual de nuevos usuarios
- Mensajes de bienvenida
- Moderación y antiflood
- Pago mediante múltiples métodos:
  - Stripe (Telegram Payments)
  - PayPal
  - USDC (Tron y Ethereum)
- Acceso al grupo VIP tras pago
- Logging y monitoreo detallado
- Listo para desplegar en [Render](https://render.com)

---

## 📌 Comandos disponibles
- `/pagar` → Envía el formulario de pago
- `/vip` → Verifica si el usuario puede entrar al VIP
- `/silenciar` (responder a mensaje) → Silencia un usuario
- `nuevo usuario` → Envía bienvenida y botón de verificación

### Ejemplo de uso
- Un usuario nuevo entra al grupo: el bot envía un mensaje de bienvenida y solicita verificación.
- Un usuario ejecuta `/pagar`: el bot muestra las opciones de pago disponibles.
- Un admin responde con `/silenciar` a un mensaje: el usuario es silenciado temporalmente.

---

## 📝 Notas sobre pagos
El bot soporta múltiples métodos de pago:
- **Stripe**: Integración nativa de Telegram Payments
- **PayPal**: Integración a través de API
- **Criptomonedas**: Pago en USDC a través de:
  - Red Tron
  - Red Ethereum

Cada método de pago tiene su propia configuración y manejo de errores.

---

## 🔒 Seguridad
- Todas las credenciales y tokens se manejan a través de variables de entorno.
- El archivo `.env` debe estar en `.gitignore`.
- Implementación de logging para monitoreo y debugging.
- Manejo seguro de claves privadas para criptomonedas.

---

## 🤝 Contribución
¡Las contribuciones son bienvenidas!
1. Haz un fork del repositorio.
2. Crea una rama para tu feature o fix: `git checkout -b mi-feature`.
3. Realiza tus cambios y haz commit: `git commit -m 'Agrega mi feature'`.
4. Haz push a tu rama: `git push origin mi-feature`.
5. Abre un Pull Request.

Por favor, sigue las buenas prácticas de Python y asegúrate de que tu código pase los tests antes de enviar un PR.

---

## 🛡️ Licencia
Este proyecto está bajo la licencia MIT.
