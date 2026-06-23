#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import logging
import sys
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

logger = logging.getLogger(__name__)

class HotWheelsScraper:
    def __init__(self):
        self.url = "https://creations.mattel.com/en-ch/collections/hot-wheels-collectors"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    async def fetch_products(self):
        """Получение товаров с сайта"""
        try:
            logger.info(f"🌐 Загрузка сайта: {self.url}")
            
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument(f'user-agent={self.headers["User-Agent"]}')
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            try:
                driver.get(self.url)
                
                wait = WebDriverWait(driver, 30)
                wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "product")))
                
                await asyncio.sleep(3)
                
                html = driver.page_source
            finally:
                driver.quit()
            
            soup = BeautifulSoup(html, 'lxml')
            products = []
            
            product_elements = soup.find_all('div', class_='product')
            logger.info(f"🔍 Найдено элементов товаров: {len(product_elements)}")
            
            for element in product_elements:
                try:
                    name_elem = element.find('h2', class_='product-name')
                    price_elem = element.find('span', class_='price')
                    status_elem = element.find('span', class_='status')
                    url_elem = element.find('a', class_='product-link')
                    
                    if name_elem and price_elem:
                        name = name_elem.get_text(strip=True)
                        price = price_elem.get_text(strip=True)
                        status = status_elem.get_text(strip=True) if status_elem else "In Stock"
                        url = url_elem['href'] if url_elem else self.url
                        
                        product_id = hash(name + price) % ((sys.maxsize + 1) * 2)
                        
                        product = {
                            'product_id': str(product_id),
                            'name': name,
                            'price': price,
                            'status': status,
                            'url': url if url.startswith('http') else self.url + url,
                            'timestamp': datetime.now().isoformat()
                        }
                        products.append(product)
                        logger.debug(f"✅ Товар добавлен: {name}")
                
                except Exception as e:
                    logger.warning(f"⚠️ Ошибка при парсинге товара: {str(e)}")
                    continue
            
            logger.info(f"✅ Получено товаров: {len(products)}")
            return products
            
        except Exception as e:
            logger.error(f"❌ Ошибка при загрузке сайта: {str(e)}")
            return []