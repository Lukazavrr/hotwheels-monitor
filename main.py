#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import logging
from datetime import datetime
from dotenv import load_dotenv
import asyncio

from scraper import HotWheelsScraper
from telegram_notifier import TelegramNotifier
from database import Database

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class HotWheelsMonitor:
    def __init__(self):
        self.scraper = HotWheelsScraper()
        self.notifier = TelegramNotifier()
        self.db = Database()
        self.db.init_database()
        logger.info("✅ Hot Wheels Monitor инициализирован")

    async def check_for_updates(self):
        """Проверка обновлений на сайте"""
        try:
            logger.info(f"🔍 Проверка обновлений... [{datetime.now().strftime('%H:%M:%S')}]")
            
            current_products = await self.scraper.fetch_products()
            
            if not current_products:
                logger.warning("⚠️ Не удалось получить товары с сайта")
                return
            
            logger.info(f"📦 Найдено товаров: {len(current_products)}")
            
            previous_products = self.db.get_all_products()
            previous_ids = {p['product_id'] for p in previous_products}
            current_ids = {p['product_id'] for p in current_products}
            
            new_products = [p for p in current_products if p['product_id'] not in previous_ids]
            if new_products:
                logger.info(f"🆕 Найдено новых товаров: {len(new_products)}")
                for product in new_products:
                    self.db.add_product(product)
                    await self.notifier.send_notification(
                        f"🆕 НОВЫЙ ТОВАР!\n\n"
                        f"Название: {product['name']}\n"
                        f"Цена: {product['price']}\n"
                        f"Статус: {product['status']}\n"
                        f"Ссылка: {product['url']}",
                        product_type="new"
                    )
            
            for current_product in current_products:
                if current_product['product_id'] in previous_ids:
                    previous_product = next(
                        (p for p in previous_products if p['product_id'] == current_product['product_id']),
                        None
                    )
                    
                    if previous_product:
                        if float(previous_product['price']) != float(current_product['price']):
                            logger.info(f"💰 Изменение цены: {current_product['name']}")
                            await self.notifier.send_notification(
                                f"💰 ИЗМЕНЕНИЕ ЦЕНЫ!\n\n"
                                f"Товар: {current_product['name']}\n"
                                f"Старая цена: {previous_product['price']}\n"
                                f"Новая цена: {current_product['price']}\n"
                                f"Ссылка: {current_product['url']}",
                                product_type="price_change"
                            )
                        
                        if previous_product['status'] != current_product['status']:
                            if previous_product['status'] == "Sold Out" and current_product['status'] == "In Stock":
                                logger.info(f"📈 Товар вернулся в наличие: {current_product['name']}")
                                await self.notifier.send_notification(
                                    f"📈 ТОВАР ВЕРНУЛСЯ В НАЛИЧИЕ!\n\n"
                                    f"Товар: {current_product['name']}\n"
                                    f"Цена: {current_product['price']}\n"
                                    f"Ссылка: {current_product['url']}",
                                    product_type="status_change"
                                )
                        
                        self.db.update_product(current_product)
            
            logger.info("✅ Проверка завершена")
            
        except Exception as e:
            logger.error(f"❌ Ошибка при проверке обновлений: {str(e)}")
            await self.notifier.send_notification(
                f"❌ ОШИБКА В МОНИТОРЕ!\n\nОшибка: {str(e)}",
                product_type="error"
            )

    async def run(self):
        """Запуск мониторинга"""
        check_interval = int(os.getenv('CHECK_INTERVAL', 60))
        logger.info(f"⏰ Интервал проверки: {check_interval} секунд")
        
        try:
            while True:
                await self.check_for_updates()
                logger.info(f"⏳ Следующая проверка через {check_interval} сек...")
                await asyncio.sleep(check_interval)
        except KeyboardInterrupt:
            logger.info("🛑 Мониторинг остановлен")
        except Exception as e:
            logger.error(f"❌ Критическая ошибка: {str(e)}")

if __name__ == "__main__":
    os.makedirs('logs', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    
    monitor = HotWheelsMonitor()
    try:
        asyncio.run(monitor.run())
    except Exception as e:
        logger.error(f"Не удалось запустить монитор: {str(e)}")
        sys.exit(1)