#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import logging
from datetime import datetime
from dotenv import load_dotenv
import asyncio

# Загружаем переменные окружения
load_dotenv('.env')

from scraper import HotWheelsScraper
from telegram_notifier import TelegramNotifier
from database import Database

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/monitor.log', encoding='utf-8'),
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
        logger.info("Hot Wheels Monitor initialized")

    async def check_for_updates(self):
        """Проверка обновлений на сайте"""
        try:
            logger.info(f"Checking for updates... [{datetime.now().strftime('%H:%M:%S')}]")
            
            current_products = await self.scraper.fetch_products()
            
            if not current_products:
                logger.warning("Could not get products from site")
                return
            
            logger.info(f"Found products: {len(current_products)}")
            
            previous_products = self.db.get_all_products()
            previous_ids = {p['product_id'] for p in previous_products}
            current_ids = {p['product_id'] for p in current_products}
            
            new_products = [p for p in current_products if p['product_id'] not in previous_ids]
            if new_products:
                logger.info(f"Found new products: {len(new_products)}")
                for product in new_products:
                    self.db.add_product(product)
                    await self.notifier.send_notification(
                        f"NEW PRODUCT!\n\n"
                        f"Name: {product['name']}\n"
                        f"Price: {product['price']}\n"
                        f"Status: {product['status']}\n"
                        f"Link: {product['url']}",
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
                            logger.info(f"Price changed: {current_product['name']}")
                            await self.notifier.send_notification(
                                f"PRICE CHANGED!\n\n"
                                f"Product: {current_product['name']}\n"
                                f"Old price: {previous_product['price']}\n"
                                f"New price: {current_product['price']}\n"
                                f"Link: {current_product['url']}",
                                product_type="price_change"
                            )
                        
                        if previous_product['status'] != current_product['status']:
                            if previous_product['status'] == "Sold Out" and current_product['status'] == "In Stock":
                                logger.info(f"Product back in stock: {current_product['name']}")
                                await self.notifier.send_notification(
                                    f"PRODUCT BACK IN STOCK!\n\n"
                                    f"Product: {current_product['name']}\n"
                                    f"Price: {current_product['price']}\n"
                                    f"Link: {current_product['url']}",
                                    product_type="status_change"
                                )
                        
                        self.db.update_product(current_product)
            
            logger.info("Check completed")
            
        except Exception as e:
            logger.error(f"Error during check: {str(e)}")
            await self.notifier.send_notification(
                f"ERROR IN MONITOR!\n\nError: {str(e)}",
                product_type="error"
            )

    async def run(self):
        """Запуск мониторинга"""
        check_interval = int(os.getenv('CHECK_INTERVAL', 60))
        logger.info(f"Check interval: {check_interval} seconds")
        
        try:
            while True:
                await self.check_for_updates()
                logger.info(f"Next check in {check_interval} sec...")
                await asyncio.sleep(check_interval)
        except KeyboardInterrupt:
            logger.info("Monitoring stopped")
        except Exception as e:
            logger.error(f"Critical error: {str(e)}")

if __name__ == "__main__":
    os.makedirs('logs', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    
    monitor = HotWheelsMonitor()
    try:
        asyncio.run(monitor.run())
    except Exception as e:
        logger.error(f"Failed to start monitor: {str(e)}")
        sys.exit(1)