"""
Тестовый бот для мессенджера MAX с интерактивными кнопками и умными ответами на текст.
Использует библиотеку maxapi для работы с API мессенджера MAX.
"""

import asyncio
import logging
import os
from typing import Optional

from maxapi import Bot, Dispatcher, F
from maxapi.types import (
    MessageCreated,
    MessageCallback,
    Command,
    CallbackButton,
    BotStarted,
)
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
# Токен берется из переменной окружения MAX_BOT_TOKEN
bot = Bot()
dp = Dispatcher()

# --- Конфигурация клавиатур ---

def get_main_menu_keyboard() -> InlineKeyboardBuilder:
    """Создает главное меню с основными разделами."""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        CallbackButton(text="📋 Услуги", payload="menu_services"),
        CallbackButton(text="💰 Цены", payload="menu_prices"),
    )
    builder.row(
        CallbackButton(text="📞 Контакты", payload="menu_contacts"),
        CallbackButton(text="ℹ️ О боте", payload="menu_about"),
    )
    
    return builder

def get_services_keyboard() -> InlineKeyboardBuilder:
    """Создает меню услуг."""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        CallbackButton(text="🚀 Разработка", payload="service_dev"),
        CallbackButton(text="🎨 Дизайн", payload="service_design"),
    )
    builder.row(
        CallbackButton(text="📈 Маркетинг", payload="service_marketing"),
        CallbackButton(text="⬅️ Назад", payload="back_to_main"),
    )
    
    return builder

def get_prices_keyboard() -> InlineKeyboardBuilder:
    """Создает меню цен."""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        CallbackButton(text="📦 Тарифы", payload="prices_tariffs"),
        CallbackButton(text="💳 Оплата", payload="prices_payment"),
    )
    builder.row(
        CallbackButton(text="⬅️ Назад", payload="back_to_main"),
    )
    
    return builder

def get_contacts_keyboard() -> InlineKeyboardBuilder:
    """Создает меню контактов."""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        CallbackButton(text="📧 Написать на почту", payload="contact_email"),
        CallbackButton(text="📱 Позвонить", payload="contact_phone"),
    )
    builder.row(
        CallbackButton(text="⬅️ Назад", payload="back_to_main"),
    )
    
    return builder

# --- Обработчики событий ---

@dp.bot_started()
async def on_bot_started(event: BotStarted):
    """Обработчик события запуска бота."""
    logger.info(f"Бот запущен пользователем: {event.chat_id}")
    
    text = (
        "👋 Привет! Я тестовый бот для мессенджера MAX!\n\n"
        "Я умею:\n"
        "• Отвечать на текстовые сообщения\n"
        "• Работать с интерактивными кнопками\n"
        "• Понимать команды\n\n"
        "Нажмите кнопку ниже, чтобы начать 👇"
    )
    
    await event.bot.send_message(
        chat_id=event.chat_id,
        text=text,
        attachments=[get_main_menu_keyboard().as_markup()]
    )

@dp.message_created(Command('start'))
async def on_start(event: MessageCreated):
    """Обработчик команды /start."""
    logger.info(f"Команда /start от пользователя: {event.chat_id}")
    
    text = (
        "🚀 Бот перезапущен!\n\n"
        "Выберите раздел из меню ниже:"
    )
    
    await event.message.answer(
        text=text,
        attachments=[get_main_menu_keyboard().as_markup()]
    )

@dp.message_created(Command('menu'))
async def on_menu(event: MessageCreated):
    """Показать главное меню."""
    await event.message.answer(
        text="📋 Главное меню:",
        attachments=[get_main_menu_keyboard().as_markup()]
    )

@dp.message_created(Command('help'))
async def on_help(event: MessageCreated):
    """Справка по командам."""
    text = (
        "ℹ️ **Доступные команды:**\n\n"
        "/start - Запустить бота\n"
        "/menu - Показать главное меню\n"
        "/help - Эта справка\n"
        "/services - Список услуг\n"
        "/prices - Прайс-лист\n"
        "/contacts - Контакты\n"
        "/about - О боте\n\n"
        "Также вы можете просто писать сообщения - я пойму и отвечу! 💬"
    )
    
    await event.message.answer(text=text, parse_mode="Markdown")

@dp.message_created(Command('services'))
async def on_services(event: MessageCreated):
    """Показать услуги."""
    await event.message.answer(
        text="📋 **Наши услуги:**\n\n"
        "• 🚀 Разработка сайтов и приложений\n"
        "• 🎨 Графический и веб-дизайн\n"
        "• 📈 Маркетинг и продвижение\n\n"
        "Выберите интересующую услугу:",
        parse_mode="Markdown",
        attachments=[get_services_keyboard().as_markup()]
    )

@dp.message_created(Command('prices'))
async def on_prices(event: MessageCreated):
    """Показать цены."""
    text = (
        "💰 **Наши цены:**\n\n"
        "• 🚀 Разработка: от 50 000 ₽\n"
        "• 🎨 Дизайн: от 20 000 ₽\n"
        "• 📈 Маркетинг: от 30 000 ₽\n\n"
        "Уточните детали у менеджера!"
    )
    
    await event.message.answer(
        text=text,
        parse_mode="Markdown",
        attachments=[get_prices_keyboard().as_markup()]
    )

@dp.message_created(Command('contacts'))
async def on_contacts(event: MessageCreated):
    """Показать контакты."""
    text = (
        "📞 **Контакты:**\n\n"
        "📧 Email: info@maxbot.ru\n"
        "📱 Телефон: +7 (999) 123-45-67\n"
        "📍 Адрес: г. Москва, ул. Примерная, д. 1\n\n"
        "Выберите способ связи:"
    )
    
    await event.message.answer(
        text=text,
        parse_mode="Markdown",
        attachments=[get_contacts_keyboard().as_markup()]
    )

@dp.message_created(Command('about'))
async def on_about(event: MessageCreated):
    """О боте."""
    text = (
        "ℹ️ **О боте:**\n\n"
        "Это тестовый бот для мессенджера MAX, созданный на библиотеке `maxapi`.\n\n"
        "• Версия: 1.0.0\n"
        "• Создан: 2026\n"
        "• Технологии: Python, maxapi, asyncio\n\n"
        "Бот поддерживает:\n"
        "✅ Интерактивные кнопки\n"
        "✅ Умные ответы на текст\n"
        "✅ Команды\n"
        "✅ Обработку callback-запросов"
    )
    
    await event.message.answer(text=text, parse_mode="Markdown")

# --- Обработчики текстовых сообщений ---

@dp.message_created(F.message.body.text.lower() == "привет")
@dp.message_created(F.message.body.text.lower() == "здравствуйте")
@dp.message_created(F.message.body.text.lower() == "hello")
@dp.message_created(F.message.body.text.lower() == "hi")
async def on_greeting(event: MessageCreated):
    """Ответ на приветствия."""
    text = (
        "👋 Привет! Рад вас видеть!\n\n"
        "Чем могу помочь? Выберите раздел из меню или напишите свой вопрос."
    )
    
    await event.message.answer(
        text=text,
        attachments=[get_main_menu_keyboard().as_markup()]
    )

@dp.message_created(F.message.body.text.lower().contains("цена") | F.message.body.text.lower().contains("стоимость") | F.message.body.text.lower().contains("сколько стоит"))
async def on_price_request(event: MessageCreated):
    """Ответ на запросы о ценах."""
    text = (
        "💰 **Наши цены:**\n\n"
        "• 🚀 Разработка: от 50 000 ₽\n"
        "• 🎨 Дизайн: от 20 000 ₽\n"
        "• 📈 Маркетинг: от 30 000 ₽\n\n"
        "Точная стоимость зависит от задачи. Хотите узнать подробнее?"
    )
    
    await event.message.answer(
        text=text,
        parse_mode="Markdown",
        attachments=[get_prices_keyboard().as_markup()]
    )

@dp.message_created(F.message.body.text.lower().contains("телефон") | F.message.body.text.lower().contains("контакт") | F.message.body.text.lower().contains("связаться"))
async def on_contact_request(event: MessageCreated):
    """Ответ на запросы о контактах."""
    text = (
        "📞 **Контакты для связи:**\n\n"
        "📧 Email: info@maxbot.ru\n"
        "📱 Телефон: +7 (999) 123-45-67\n"
        "📱 WhatsApp: +7 (999) 123-45-67\n"
        "📍 Адрес: г. Москва, ул. Примерная, д. 1\n\n"
        "Выберите удобный способ связи:"
    )
    
    await event.message.answer(
        text=text,
        parse_mode="Markdown",
        attachments=[get_contacts_keyboard().as_markup()]
    )

@dp.message_created(F.message.body.text.lower().contains("помощь") | F.message.body.text.lower().contains("ошибка") | F.message.body.text.lower().contains("проблема"))
async def on_help_request(event: MessageCreated):
    """Ответ на запросы о помощи."""
    text = (
        "🆘 **Помощь:**\n\n"
        "Если у вас возникли проблемы, вы можете:\n\n"
        "1. Написать нам на почту: info@maxbot.ru\n"
        "2. Позвонить: +7 (999) 123-45-67\n"
        "3. Описать проблему здесь, и я помогу!\n\n"
        "Что именно вас беспокоит?"
    )
    
    await event.message.answer(text=text)

@dp.message_created(F.message.body.text.lower().contains("купить") | F.message.body.text.lower().contains("заказать") | F.message.body.text.lower().contains("оформить"))
async def on_order_request(event: MessageCreated):
    """Ответ на запросы о заказе."""
    text = (
        "🛒 **Оформление заказа:**\n\n"
        "Отлично, что вы хотите заказать наши услуги!\n\n"
        "Пожалуйста, уточните:\n"
        "• Какой тип услуги вас интересует?\n"
        "• Есть ли у вас техническое задание?\n"
        "• Какие сроки вас устраивают?\n\n"
        "Или выберите услугу из меню ниже:"
    )
    
    await event.message.answer(
        text=text,
        attachments=[get_services_keyboard().as_markup()]
    )

@dp.message_created(F.message.body.text.lower().contains("кто ты") | F.message.body.text.lower().contains("информация") | F.message.body.text.lower().contains("о боте"))
async def on_about_request(event: MessageCreated):
    """Ответ на запросы о боте."""
    text = (
        "ℹ️ **Я - тестовый бот для мессенджера MAX!**\n\n"
        "Я создан на библиотеке `maxapi` и умею:\n"
        "• Отвечать на ваши вопросы\n"
        "• Работать с интерактивными кнопками\n"
        "• Понимать контекст диалога\n\n"
        "Попробуйте написать:\n"
        "/menu - главное меню\n"
        "/help - справка\n"
        "/services - услуги"
    )
    
    await event.message.answer(text=text, parse_mode="Markdown")

@dp.message_created(F.message.body.text)
async def on_default_text(event: MessageCreated):
    """Обработчик всех остальных текстовых сообщений."""
    text = event.message.body.text
    
    response = (
        f"🤔 Вы написали: «{text}»\n\n"
        "Я пока не совсем понял этот вопрос, но могу предложить:\n\n"
        "• Посмотреть меню услуг\n"
        "• Узнать цены\n"
        "• Связаться с менеджером\n\n"
        "Выберите что-нибудь из меню ниже 👇"
    )
    
    await event.message.answer(
        text=response,
        attachments=[get_main_menu_keyboard().as_markup()]
    )

# --- Обработчики callback-кнопок ---

@dp.message_callback(F.callback.payload == "menu_services")
async def callback_services(event: MessageCallback):
    """Обработка нажатия на кнопку 'Услуги'."""
    await event.answer(
        new_text="📋 **Наши услуги:**\n\n"
        "• 🚀 Разработка сайтов и приложений\n"
        "• 🎨 Графический и веб-дизайн\n"
        "• 📈 Маркетинг и продвижение\n\n"
        "Выберите интересующую услугу:",
        parse_mode="Markdown",
        new_reply_markup=get_services_keyboard().as_markup()
    )

@dp.message_callback(F.callback.payload == "menu_prices")
async def callback_prices(event: MessageCallback):
    """Обработка нажатия на кнопку 'Цены'."""
    await event.answer(
        new_text="💰 **Наши цены:**\n\n"
        "• 🚀 Разработка: от 50 000 ₽\n"
        "• 🎨 Дизайн: от 20 000 ₽\n"
        "• 📈 Маркетинг: от 30 000 ₽\n\n"
        "Уточните детали у менеджера!",
        parse_mode="Markdown",
        new_reply_markup=get_prices_keyboard().as_markup()
    )

@dp.message_callback(F.callback.payload == "menu_contacts")
async def callback_contacts(event: MessageCallback):
    """Обработка нажатия на кнопку 'Контакты'."""
    await event.answer(
        new_text="📞 **Контакты:**\n\n"
        "📧 Email: info@maxbot.ru\n"
        "📱 Телефон: +7 (999) 123-45-67\n"
        "📍 Адрес: г. Москва, ул. Примерная, д. 1\n\n"
        "Выберите способ связи:",
        parse_mode="Markdown",
        new_reply_markup=get_contacts_keyboard().as_markup()
    )

@dp.message_callback(F.callback.payload == "menu_about")
async def callback_about(event: MessageCallback):
    """Обработка нажатия на кнопку 'О боте'."""
    text = (
        "ℹ️ **О боте:**\n\n"
        "Это тестовый бот для мессенджера MAX, созданный на библиотеке `maxapi`.\n\n"
        "• Версия: 1.0.0\n"
        "• Создан: 2026\n"
        "• Технологии: Python, maxapi, asyncio\n\n"
        "Бот поддерживает:\n"
        "✅ Интерактивные кнопки\n"
        "✅ Умные ответы на текст\n"
        "✅ Команды\n"
        "✅ Обработку callback-запросов"
    )
    
    await event.answer(new_text=text, parse_mode="Markdown")

@dp.message_callback(F.callback.payload == "back_to_main")
async def callback_back_to_main(event: MessageCallback):
    """Обработка нажатия на кнопку 'Назад'."""
    text = "📋 **Главное меню:**\n\nВыберите раздел:"
    
    await event.answer(
        new_text=text,
        parse_mode="Markdown",
        new_reply_markup=get_main_menu_keyboard().as_markup()
    )

@dp.message_callback(F.callback.payload == "service_dev")
async def callback_service_dev(event: MessageCallback):
    """Обработка нажатия на кнопку 'Разработка'."""
    await event.answer(
        new_text="🚀 **Услуга: Разработка**\n\n"
        "Мы создаем:\n"
        "• Сайты любой сложности\n"
        "• Мобильные приложения\n"
        "• Веб-сервисы и платформы\n\n"
        "Стоимость: от 50 000 ₽\n"
        "Сроки: от 2 недель\n\n"
        "Хотите заказать? Напишите менеджеру!",
        parse_mode="Markdown",
        new_reply_markup=get_services_keyboard().as_markup()
    )

@dp.message_callback(F.callback.payload == "service_design")
async def callback_service_design(event: MessageCallback):
    """Обработка нажатия на кнопку 'Дизайн'."""
    await event.answer(
        new_text="🎨 **Услуга: Дизайн**\n\n"
        "Мы создаем:\n"
        "• Логотипы и айдентику\n"
        "• Веб-дизайн\n"
        "• Графику для соцсетей\n\n"
        "Стоимость: от 20 000 ₽\n"
        "Сроки: от 1 недели\n\n"
        "Хотите заказать? Напишите менеджеру!",
        parse_mode="Markdown",
        new_reply_markup=get_services_keyboard().as_markup()
    )

@dp.message_callback(F.callback.payload == "service_marketing")
async def callback_service_marketing(event: MessageCallback):
    """Обработка нажатия на кнопку 'Маркетинг'."""
    await event.answer(
        new_text="📈 **Услуга: Маркетинг**\n\n"
        "Мы предлагаем:\n"
        "• Контекстную рекламу\n"
        "• SEO-продвижение\n"
        "• SMM и таргетинг\n\n"
        "Стоимость: от 30 000 ₽\n"
        "Сроки: от 1 месяца\n\n"
        "Хотите заказать? Напишите менеджеру!",
        parse_mode="Markdown",
        new_reply_markup=get_services_keyboard().as_markup()
    )

@dp.message_callback(F.callback.payload == "prices_tariffs")
async def callback_prices_tariffs(event: MessageCallback):
    """Обработка нажатия на кнопку 'Тарифы'."""
    await event.answer(
        new_text="💳 **Тарифы:**\n\n"
        "• 🥉 Базовый: 50 000 ₽\n"
        "• 🥈 Стандарт: 100 000 ₽\n"
        "• 🥇 Премиум: 200 000 ₽\n\n"
        "Выберите подходящий тариф или уточните детали у менеджера!",
        parse_mode="Markdown",
        new_reply_markup=get_prices_keyboard().as_markup()
    )

@dp.message_callback(F.callback.payload == "prices_payment")
async def callback_prices_payment(event: MessageCallback):
    """Обработка нажатия на кнопку 'Оплата'."""
    await event.answer(
        new_text="💳 **Способы оплаты:**\n\n"
        "• Банковская карта\n"
        "• Банковский перевод\n"
        "• Электронные деньги\n\n"
        "Оплата производится после подписания договора.",
        parse_mode="Markdown",
        new_reply_markup=get_prices_keyboard().as_markup()
    )

@dp.message_callback(F.callback.payload == "contact_email")
async def callback_contact_email(event: MessageCallback):
    """Обработка нажатия на кнопку 'Написать на почту'."""
    await event.answer(
        new_text="📧 **Напишите нам на почту:**\n\n"
        "info@maxbot.ru\n\n"
        "Мы ответим в течение 24 часов!",
        parse_mode="Markdown",
        new_reply_markup=get_contacts_keyboard().as_markup()
    )

@dp.message_callback(F.callback.payload == "contact_phone")
async def callback_contact_phone(event: MessageCallback):
    """Обработка нажатия на кнопку 'Позвонить'."""
    await event.answer(
        new_text="📞 **Позвоните нам:**\n\n"
        "+7 (999) 123-45-67\n\n"
        "Работаем с 9:00 до 18:00 (МСК)",
        parse_mode="Markdown",
        new_reply_markup=get_contacts_keyboard().as_markup()
    )

# --- Запуск бота ---

async def main():
    """Основная функция запуска бота."""
    logger.info("Запуск бота...")
    
    # Установить команды бота (появятся в меню)
    try:
        await bot.set_my_commands([
            {"name": "start", "description": "Запустить бота"},
            {"name": "menu", "description": "Показать главное меню"},
            {"name": "help", "description": "Справка"},
            {"name": "services", "description": "Список услуг"},
            {"name": "prices", "description": "Прайс-лист"},
            {"name": "contacts", "description": "Контакты"},
            {"name": "about", "description": "О боте"},
        ])
        logger.info("Команды бота установлены")
    except Exception as e:
        logger.error(f"Не удалось установить команды бота: {e}")
    
    # Запуск бота в режиме webhook (рекомендуется для продакшена)
    # Для локального тестирования можно использовать start_polling()
    
    webhook_url = os.getenv("MAX_WEBHOOK_URL")
    if webhook_url:
        logger.info(f"Запуск в режиме webhook: {webhook_url}")
        await bot.set_webhook(webhook_url)
        await dp.handle_webhook(bot=bot, host="0.0.0.0", port=8080)
    else:
        logger.info("Запуск в режиме polling (локальное тестирование)")
        logger.warning("Установите переменную окружения MAX_WEBHOOK_URL для работы через webhook")
        await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
