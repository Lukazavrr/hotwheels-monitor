#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
from telegram import Bot
from telegram.error import TelegramError
import asyncio

logger = logging.getLogger(__name__)

class TelegramNotifier:
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_ids = [
            int(os.getenv('TELEGRAM_CHAT_ID_1')),
            int(os.getenv('TELEGRAM_CHAT_ID_2'))
        ]
        self.bot = Bot(token=self.bot_token)
        logger.info(f"✅ Telegram Notifier инициализирован для {len(self.chat_ids)} чатов")

    async def send_notification(self, message, product_type="info"):
        """Отправка уведомления в Telegram"""
        try:
            emojis = {
                "new": "🆕",
                "price_change": "💰",
                "status_change": "📈",
                "error": "❌",
                "info": "ℹ️"
            }
            emoji = emojis.get(product_type, "ℹ️")
            
            formatted_message = f"{emoji}\n" + message
            
            tasks = []
            for chat_id in self.chat_ids:
                try:
                    task = self.bot.send_message(
                        chat_id=chat_id,
                        text=formatted_message,
                        parse_mode='HTML',
                        disable_web_page_preview=True
                    )
                    tasks.append(task)
                    logger.info(f"📤 Сообщение отправлено в чат {chat_id}")
                except TelegramError as e:
                    logger.error(f"❌ Ошибка при отправке в чат {chat_id}: {str(e)}")
            
            if tasks:
                await asyncio.gather(*tasks)
            
        except Exception as e:
            logger.error(f"❌ Ошибка в TelegramNotifier: {str(e)}")

    async def test_connection(self):
        """Тестирование подключения к Telegram"""
        try:
            me = await self.bot.get_me()
            logger.info(f"✅ Telegram бот подключен: {me.username}")
            
            for chat_id in self.chat_ids:
                await self.send_notification(
                    "✅ Hot Wheels Monitor запущен и готов к работе!\n\n"
                    "Буду отслеживать:\n"
                    "🆕 Новые товары\n"
                    "💰 Изменения цены\n"
                    "📈 Появление товаров в наличии",
                    product_type="info"
                )
            
            return True
        except Exception as e:
            logger.error(f"❌ Ошибка подключения к Telegram: {str(e)}")
            return False