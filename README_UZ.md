# ClickUp Webhook Integration - Uzbek Dokumentatsiyasi

## Loyiha haqida

Bu loyiha ClickUp task management tizimi bilan Telegram bot orqali integratsiya qilish uchun yaratilgan. Asosiy maqsad - ClickUp'da vazifalar o'zgarganda brokerlarga avtomatik xabar yuborish.

## Loyiha tuzilishi

```
clickup/
├── app.py                      # Asosiy ilova fayli (entry point)
├── config/                     # Konfiguratsiya modullari
│   ├── __init__.py
│   └── settings.py             # Sozlamalar va environment variables
├── core/                       # Asosiy funksionallik
│   ├── __init__.py
│   ├── clickup_client.py       # ClickUp API klienti
│   ├── dispatcher.py           # Webhook event dispatcher
│   ├── logging_config.py       # Logging sozlamalari
│   ├── telegram_bot.py         # Telegram bot funksiyalari
│   └── webhook_manager.py      # Webhook boshqaruvi
├── clickup/                     # ClickUp event handlerlari
│   ├── __init__.py
│   └── savdo/
│       ├── __init__.py
│       └── when_broker_set/    # Broker field o'zgarganda handlerlar
│           ├── __init__.py
│           ├── components.py   # Message va keyboard yaratish
│           └── when_broker_set.py  # Event handlerlar
├── clickup_sdk/                # ClickUp SDK (ichki kutubxona)
├── utils/                      # Utility funksiyalar
│   └── get_curstom_field_value.py
├── logs/                       # Log fayllari (avtomatik yaratiladi)
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables namunasi
└── README_UZ.md               # Bu dokumentatsiya
```

## O'rnatish va ishga tushirish

### 1. Talablar

- Python 3.8 yoki yuqori versiya
- ClickUp API token
- Telegram Bot token
- ClickUp Team ID

### 2. O'rnatish

```bash
# Repositoryni klon qiling
git clone <repository_url>
cd clickup

# Virtual environment yarating (tavsiya etiladi)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows

# Dependencies o'rnating
pip install -r requirements.txt
```

### 3. Sozlamalar

`.env.example` faylini `.env` nomiga ko'chiring va kerakli ma'lumotlarni kiriting:

```bash
cp .env.example .env
```

`.env` faylini tahrirlang:

```env
# ClickUp API Configuration
CLICKUP_API_TOKEN=pk_your_clickup_token_here
TEAM_ID=your_team_id_here

# Telegram Bot Configuration
BOT_TOKEN=your_telegram_bot_token_here

# Webhook Configuration
WEBHOOK_SECRET=your_webhook_secret_here  # Ixtiyoriy
WEBHOOK_ENDPOINT=https://clickup.venu.uz/clickup-webhook
WEBHOOK_PATH=/clickup-webhook

# Server Configuration
SERVER_HOST=0.0.0.0
SERVER_PORT=3000

# Logging Configuration
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR
LOG_DIR=logs
```

### 4. Ishga tushirish

```bash
python app.py
```

Ilova ishga tushganda quyidagi ma'lumotlar ko'rsatiladi:

- Server manzili va port
- Ro'yxatdan o'tgan eventlar
- Webhook holati

## Qanday ishlaydi?

### 1. Webhook sozlamalari

Ilova ishga tushganda avtomatik ravishda:

1. Mavjud webhooklarni o'chiradi
2. Yangi webhook yaratadi
3. Quyidagi eventlarni kuzatadi:
   - `taskCreated` - Vazifa yaratilganda
   - `taskUpdated` - Vazifa yangilanganda
   - `taskStatusUpdated` - Vazifa statusi o'zgarganda
   - `taskDeleted` - Vazifa o'chirilganda

### 2. Broker field handleri

ClickUp'da taskning "Broker" custom fieldiga qiymat qo'yilganda:

1. **Event qabul qilinadi**: `taskUpdated` eventi keladi
2. **Filter tekshiriladi**: `custom_field_set` filteri "Broker" fieldini tekshiradi
3. **Broker ma'lumotlari olinadi**:
   - Broker task ID olinadi
   - Broker taskdan `telegram_id` custom field olinadi
4. **Xabar tayyorlanadi**: Task ma'lumotlaridan formatlangan xabar yaratiladi
5. **Telegramga yuboriladi**: Brokerning Telegram ID'siga xabar yuboriladi

### 3. Buxgalterga to'lov xabarnomasi

Status `pul tushishi kutilmoqda` ga o'tganda:

1. **Event qabul qilinadi**: `taskStatusUpdated` eventi keladi
2. **Filter tekshiriladi**: `status_changed(to_status="pul tushishi kutilmoqda")`
3. **Relationship o'qiladi**: Taskdagi `Bug'galter | Summa` custom fieldidan bog'langan task ID olinadi
4. **Buxgalter ma'lumoti**: Bog'langan taskdan `telegram_id` olinadi
5. **Message + button**: Summaga oid ma'lumotlar bilan xabar va inline keyboard generatsiya qilinadi
6. **Telegramga yuboriladi**: Buxgalterning Telegram'iga xabar boradi

Xabarda quyidagilar bo'ladi:

- Asosiy task nomi, statusi va listi
- Summa yozuvi nomi
- Kutilayotgan summa va dedlayn

Inline keyboard:

- `🔗 Taskni ochish` – asosiy task URL
- `📄 Summa kartochkasi` – relation task URL (agar mavjud bo'lsa)
- `✅ Pul qabul qilindi` – callback tugma

### 4. Xabar formati

Brokerlarga yuboriladigan xabar quyidagi ma'lumotlarni o'z ichiga oladi:

```
🆕 Yangi ish bor!

📌 Ish nomi: [Task nomi]
📊 Status: [Status]
📦 Soni: [Miqdor] ta
🏢 Firmamiz: [Firma nomi]
👤 Xaridor: [Xaridor companiya]
🤝 Hamkor: [Hamkor companiya]
💰 Hamkordan olinish narxi: [Narx] UZS
📤 Lot chiqishi: [Narx] UZS
📥 Lot qo'yilishi: [Narx] UZS
📅 Broker dedline: [Sana]
```

### 5. Inline keyboard

Har bir xabarda quyidagi tugmalar mavjud:

- **🔗 Taskni ochish** - ClickUp'da taskni ochadi
- **✅ Lot qo'yildi** - Callback tugmasi (keyingi versiyada ishlatiladi)

## Logging tizimi

Loyiha keng qamrovli logging tizimiga ega:

### Log fayllari

`logs/` papkasida quyidagi fayllar yaratiladi:

1. **app.log** - Barcha umumiy loglar (DEBUG, INFO, WARNING, ERROR)
2. **errors.log** - Faqat ERROR level loglar
3. **webhook.log** - Webhook eventlari bilan bog'liq loglar
4. **telegram.log** - Telegram bot operatsiyalari loglari

### Log rotation

- Har bir log fayli maksimal 10MB bo'lguncha o'sadi
- 10MB dan oshganda yangi fayl yaratiladi
- Eski fayllar saqlanadi (maksimal 5 ta backup)

### Log level'lar

Environment variable orqali o'zgartirish mumkin:

```env
LOG_LEVEL=DEBUG  # Eng batafsil ma'lumotlar
LOG_LEVEL=INFO   # Oddiy ish jarayoni (tavsiya etiladi)
LOG_LEVEL=WARNING  # Faqat ogohlantirishlar
LOG_LEVEL=ERROR  # Faqat xatolar
```

## Kod tuzilishi

### Config moduli (`config/`)

**settings.py** - Barcha sozlamalarni boshqaradi:

- Environment variables o'qish
- Sozlamalarni validatsiya qilish
- Default qiymatlar

### Core moduli (`core/`)

**clickup_client.py** - ClickUp API klienti:

- Singleton pattern orqali bitta instance
- Avtomatik initialization

**dispatcher.py** - Webhook event dispatcher:

- Global dispatcher instance
- Event handlerlarni boshqaradi

**logging_config.py** - Logging sozlamalari:

- File rotation
- Turli loggerlar (webhook, telegram)
- Formatlangan chiqishlar

**telegram_bot.py** - Telegram bot funksiyalari:

- Xabar yuborish
- Inline keyboard yaratish
- Error handling

**webhook_manager.py** - Webhook boshqaruvi:

- Webhook yaratish
- Webhook o'chirish
- Webhook ro'yxatini olish
- Avtomatik initialization

### ClickUp handlers (`clickup/`)

**when_broker_set.py** - Broker field handlerlari:

- `handle_broker_set` - Broker qo'yilganda
- `handle_broker_removed` - Broker olib tashlanganda
- `handle_broker_updated` - Broker yangilanganda

**components.py** - Helper funksiyalar:

- `create_broker_message` - Xabar yaratish
- `create_broker_keyboard` - Keyboard yaratish
- Formatlash funksiyalari (currency, number, date)

## Muhim eslatmalar

### ClickUp sozlamalari

1. **Custom Fields**: Quyidagi custom fieldlar mavjud bo'lishi kerak:

   - `Broker` - Relationship field (broker taskga bog'lash uchun)
   - `telegram_id` - Broker taskda (brokerning Telegram ID'si)
   - `🔢 miqdori` - Number field
   - `💵 lot chiqishi` - Currency field
   - `💸 lot qo'yilishi` - Currency field
   - `Firma` - Relationship field
   - `Xaridor companiya` - Relationship field
   - `Hamkor companiya` - Relationship field
   - `Hamkordan olinish narxi` - Currency field
   - `📅 broker dedline` - Date field

2. **Webhook endpoint**: Public URL bo'lishi kerak (ClickUp'ga yetib borishi uchun)

### Telegram bot

1. Bot token olish: [@BotFather](https://t.me/BotFather) orqali
2. Botni ishga tushirish shart emas (faqat token kerak)
3. Brokerlarning Telegram ID'lari ClickUp'da saqlanadi

## Muammolarni hal qilish

### Webhook ishlamayapti

1. `.env` faylida `WEBHOOK_ENDPOINT` to'g'ri URL ekanligini tekshiring
2. Server public internetga chiqadimi tekshiring
3. Loglarni ko'rib chiqing: `logs/webhook.log`

### Telegram xabarlar yuborilmayapti

1. `BOT_TOKEN` to'g'ri ekanligini tekshiring
2. Broker taskda `telegram_id` mavjudligini tekshiring
3. Loglarni ko'rib chiqing: `logs/telegram.log`

### ClickUp API xatolari

1. `CLICKUP_API_TOKEN` to'g'ri ekanligini tekshiring
2. Token permissions tekshiring
3. `logs/app.log` faylini ko'rib chiqing

## Rivojlantirish

### Yangi handler qo'shish

1. `clickup/` papkasida yangi modul yarating
2. `__init__.py` faylida import qiling
3. `@dispatcher.on()` dekoratori bilan handler yozing

Misol:

```python
from core.dispatcher import dispatcher
from clickup_sdk.webhook import WebhookEvent
from core.logging_config import get_logger

logger = get_logger(__name__)

@dispatcher.on("taskCreated")
async def handle_task_created(event: WebhookEvent):
    logger.info(f"New task created: {event.task_id}")
    # Sizning logikangiz
```

### Yangi custom field handleri

```python
from clickup_sdk.webhook import custom_field_set, WebhookEvent
from core.dispatcher import dispatcher

@dispatcher.on("taskUpdated", custom_field_set(field_name="YourField"))
async def handle_field_set(event: WebhookEvent):
    # Handler logikasi
    pass
```

## Xavfsizlik

1. **`.env` faylini git'ga qo'shmang** - `.gitignore` da mavjud
2. **Webhook secret** - Production'da ishlatish tavsiya etiladi
3. **HTTPS** - Production'da faqat HTTPS ishlatish
4. **Tokenlar** - Tokenlarni hech qachon kodga yozmang

## Yordam va qo'llab-quvvatlash

Muammo yoki savol bo'lsa:

1. Log fayllarini ko'rib chiqing
2. GitHub Issues oching
3. Kodga qarab tekshiring

## Versiya tarixi

- **v1.0.0** - Dastlabki versiya
  - Broker field handleri
  - Telegram integratsiyasi
  - Logging tizimi
  - Webhook management

## Muallif

Bu loyiha ClickUp va Telegram integratsiyasi uchun yaratilgan.

## Litsenziya

MIT License
