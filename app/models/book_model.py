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
        """
        新增一筆書籍記錄。
        參數：
          - title (str): 書名
          - notes (str): 閱讀心得
          - rating (int): 評分 (1-5)
          - cover_image (str, optional): 封面圖片路徑
          - start_date (str, optional): 開始閱讀日期 (YYYY-MM-DD)
          - end_date (str, optional): 完讀日期 (YYYY-MM-DD)
        回傳：
          - 新增書籍的 ID (int)，若失敗則回傳 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO books (title, cover_image, start_date, end_date, notes, rating)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (title, cover_image, start_date, end_date, notes, rating))
            conn.commit()
            book_id = cursor.lastrowid
            return book_id
        except sqlite3.Error as e:
            print(f"資料庫錯誤 (create_book): {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_all_books():
        """
        取得所有書籍記錄，依建立時間降冪排序。
        回傳：
          - 書籍字典的列表 (list of dict)，若失敗則回傳空列表
        """
        try:
            conn = get_db_connection()
            books = conn.execute('SELECT * FROM books ORDER BY created_at DESC').fetchall()
            return [dict(book) for book in books]
        except sqlite3.Error as e:
            print(f"資料庫錯誤 (get_all_books): {e}")
            return []
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_book_by_id(book_id):
        """
        根據 ID 取得單筆書籍記錄。
        參數：
          - book_id (int): 書籍 ID
        回傳：
          - 書籍資料字典 (dict)，若找不到或失敗則回傳 None
        """
        try:
            conn = get_db_connection()
            book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
            return dict(book) if book else None
        except sqlite3.Error as e:
            print(f"資料庫錯誤 (get_book_by_id): {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def update_book(book_id, title, notes, rating, cover_image=None, start_date=None, end_date=None):
        """
        更新指定書籍記錄。
        參數：同 create_book，加上 book_id (int) 作為條件。
        回傳：
          - 成功為 True，失敗為 False
        """
        try:
            conn = get_db_connection()
            conn.execute('''
                UPDATE books
                SET title = ?, cover_image = ?, start_date = ?, end_date = ?, notes = ?, rating = ?
                WHERE id = ?
            ''', (title, cover_image, start_date, end_date, notes, rating, book_id))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"資料庫錯誤 (update_book): {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def delete_book(book_id):
        """
        刪除指定書籍記錄。
        參數：
          - book_id (int): 書籍 ID
        回傳：
          - 成功為 True，失敗為 False
        """
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"資料庫錯誤 (delete_book): {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()
