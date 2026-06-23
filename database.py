#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sqlite3
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path='data/hotwheels.db'):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = None
        self.connect()

    def connect(self):
        """Подключение к БД"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            logger.info(f"✅ Подключение к БД: {self.db_path}")
        except Exception as e:
            logger.error(f"❌ Ошибка подключения к БД: {str(e)}")
            raise

    def init_database(self):
        """Инициализация таблиц БД"""
        try:
            cursor = self.conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    price TEXT NOT NULL,
                    status TEXT NOT NULL,
                    url TEXT NOT NULL,
                    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS price_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id TEXT NOT NULL,
                    old_price TEXT NOT NULL,
                    new_price TEXT NOT NULL,
                    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (product_id) REFERENCES products(product_id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS status_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id TEXT NOT NULL,
                    old_status TEXT NOT NULL,
                    new_status TEXT NOT NULL,
                    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (product_id) REFERENCES products(product_id)
                )
            ''')
            
            self.conn.commit()
            logger.info("✅ Таблицы БД инициализированы")
        except Exception as e:
            logger.error(f"❌ Ошибка инициализации БД: {str(e)}")
            raise

    def add_product(self, product):
        """Добавление нового товара"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO products 
                (product_id, name, price, status, url, first_seen, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                product['product_id'],
                product['name'],
                product['price'],
                product['status'],
                product['url'],
                datetime.now().isoformat(),
                datetime.now().isoformat()
            ))
            self.conn.commit()
            logger.info(f"✅ Товар добавлен: {product['name']}")
        except Exception as e:
            logger.error(f"❌ Ошибка при добавлении товара: {str(e)}")

    def update_product(self, product):
        """Обновление товара"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                UPDATE products SET price = ?, status = ?, last_updated = ?
                WHERE product_id = ?
            ''', (
                product['price'],
                product['status'],
                datetime.now().isoformat(),
                product['product_id']
            ))
            self.conn.commit()
            logger.debug(f"✅ Товар обновлен: {product['name']}")
        except Exception as e:
            logger.error(f"❌ Ошибка при обновлении товара: {str(e)}")

    def get_all_products(self):
        """Получение всех товаров"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT * FROM products')
            products = cursor.fetchall()
            return [dict(p) for p in products]
        except Exception as e:
            logger.error(f"❌ Ошибка при получении товаров: {str(e)}")
            return []

    def get_product_by_id(self, product_id):
        """Получение товара по ID"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT * FROM products WHERE product_id = ?', (product_id,))
            product = cursor.fetchone()
            return dict(product) if product else None
        except Exception as e:
            logger.error(f"❌ Ошибка при получении товара: {str(e)}")
            return None

    def close(self):
        """Закрытие соединения с БД"""
        if self.conn:
            self.conn.close()
            logger.info("✅ Соединение с БД закрыто")