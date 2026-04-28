import sqlite3
import os

# 根據專案結構，資料庫檔案放在專案根目錄的 instance/database.db
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'database.db')

def get_db_connection():
    """取得資料庫連線，若 instance 目錄不存在則自動建立"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

class BookModel:
    @staticmethod
    def create_book(title, notes, rating, cover_image=None, start_date=None, end_date=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO books (title, cover_image, start_date, end_date, notes, rating)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, cover_image, start_date, end_date, notes, rating))
        conn.commit()
        book_id = cursor.lastrowid
        conn.close()
        return book_id

    @staticmethod
    def get_all_books():
        conn = get_db_connection()
        books = conn.execute('SELECT * FROM books ORDER BY created_at DESC').fetchall()
        conn.close()
        return [dict(book) for book in books]

    @staticmethod
    def get_book_by_id(book_id):
        conn = get_db_connection()
        book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
        conn.close()
        return dict(book) if book else None

    @staticmethod
    def update_book(book_id, title, notes, rating, cover_image=None, start_date=None, end_date=None):
        conn = get_db_connection()
        conn.execute('''
            UPDATE books
            SET title = ?, cover_image = ?, start_date = ?, end_date = ?, notes = ?, rating = ?
            WHERE id = ?
        ''', (title, cover_image, start_date, end_date, notes, rating, book_id))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def delete_book(book_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
        conn.commit()
        conn.close()
        return True
