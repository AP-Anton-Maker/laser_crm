import os
import csv
import zipfile
import shutil
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.config import settings
from db.models import Client, Order

class BackupService:
    @staticmethod
    async def create_full_backup(db: AsyncSession) -> str:
        """
        Создает временную папку, выгружает таблицы в CSV, 
        копирует SQLite файл, упаковывает в ZIP и возвращает путь к архиву.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = f"./data/temp_backup_{timestamp}"
        os.makedirs(backup_dir, exist_ok=True)
        
        # 1. Экспорт клиентов в CSV
        clients_csv_path = os.path.join(backup_dir, "clients.csv")
        stmt_clients = select(Client)
        result_clients = await db.execute(stmt_clients)
        clients = result_clients.scalars().all()
        
        with open(clients_csv_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Name", "VK ID", "Phone", "LTV", "Cashback", "Created At"])
            for c in clients:
                writer.writerow([c.id, c.name, c.vk_id, c.phone, c.ltv, c.cashback_balance, c.created_at])
                
        # 2. Экспорт заказов в CSV
        orders_csv_path = os.path.join(backup_dir, "orders.csv")
        stmt_orders = select(Order)
        result_orders = await db.execute(stmt_orders)
        orders = result_orders.scalars().all()
        
        with open(orders_csv_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Client ID", "Description", "Status", "Price", "Cost Price", "Created At"])
            for o in orders:
                writer.writerow([o.id, o.client_id, o.description, o.status.value, o.price, o.cost_price, o.created_at])
                
        # 3. Копирование файла базы данных
        # Парсим путь к файлу БД. Например, sqlite+aiosqlite:///./laser_crm.sqlite3 -> ./laser_crm.sqlite3
        db_filepath = settings.DATABASE_URL.split("///")[-1]
        db_backup_path = os.path.join(backup_dir, "database.sqlite3")
        
        if os.path.exists(db_filepath):
            shutil.copy2(db_filepath, db_backup_path)
            
        # 4. Создание ZIP-архива
        zip_filename = f"./data/laser_crm_backup_{timestamp}.zip"
        os.makedirs("./data", exist_ok=True) # Гарантируем, что папка data существует
        
        with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(clients_csv_path, arcname="clients.csv")
            zipf.write(orders_csv_path, arcname="orders.csv")
            if os.path.exists(db_backup_path):
                zipf.write(db_backup_path, arcname="database.sqlite3")
                
        # 5. Очистка временных файлов
        shutil.rmtree(backup_dir)
        
        return zip_filename
