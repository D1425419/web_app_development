import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app
from werkzeug.utils import secure_filename
from app.models.book_model import BookModel

# 建立 Blueprint，方便後續在 app.py 註冊
book_bp = Blueprint('book_bp', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@book_bp.route('/')
def index():
    """書單首頁"""
    books = BookModel.get_all_books()
    return render_template('index.html', books=books)

@book_bp.route('/books/create', methods=['GET'])
def create_book_form():
    """新增書籍頁面"""
    return render_template('form.html', mode='create')

@book_bp.route('/books/create', methods=['POST'])
def create_book():
    """建立書籍"""
    title = request.form.get('title')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    notes = request.form.get('notes')
    rating = request.form.get('rating')
    
    if not title or not notes or not rating:
        flash('書名、心得與評分為必填欄位', 'danger')
        return redirect(url_for('book_bp.create_book_form'))
        
    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            raise ValueError
    except ValueError:
        flash('評分必須為 1 到 5 之間的整數', 'danger')
        return redirect(url_for('book_bp.create_book_form'))

    cover_image_path = None
    if 'cover_image' in request.files:
        file = request.files['cover_image']
        if file and file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_dir = os.path.join(current_app.static_folder, 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            file.save(os.path.join(upload_dir, filename))
            cover_image_path = f'uploads/{filename}'

    book_id = BookModel.create_book(title, notes, rating, cover_image_path, start_date, end_date)
    if book_id:
        flash('書籍新增成功！', 'success')
        return redirect(url_for('book_bp.index'))
    else:
        flash('儲存時發生錯誤，請稍後再試。', 'danger')
        return redirect(url_for('book_bp.create_book_form'))

@book_bp.route('/books/<int:id>', methods=['GET'])
def book_detail(id):
    """書籍詳情"""
    book = BookModel.get_book_by_id(id)
    if not book:
        abort(404)
    return render_template('detail.html', book=book)

@book_bp.route('/books/<int:id>/edit', methods=['GET'])
def edit_book_form(id):
    """編輯書籍頁面"""
    book = BookModel.get_book_by_id(id)
    if not book:
        abort(404)
    return render_template('form.html', mode='edit', book=book)

@book_bp.route('/books/<int:id>/update', methods=['POST'])
def update_book(id):
    """更新書籍"""
    book = BookModel.get_book_by_id(id)
    if not book:
        abort(404)
        
    title = request.form.get('title')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    notes = request.form.get('notes')
    rating = request.form.get('rating')
    
    if not title or not notes or not rating:
        flash('書名、心得與評分為必填欄位', 'danger')
        return redirect(url_for('book_bp.edit_book_form', id=id))

    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            raise ValueError
    except ValueError:
        flash('評分必須為 1 到 5 之間的整數', 'danger')
        return redirect(url_for('book_bp.edit_book_form', id=id))

    cover_image_path = book['cover_image']
    if 'cover_image' in request.files:
        file = request.files['cover_image']
        if file and file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_dir = os.path.join(current_app.static_folder, 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            file.save(os.path.join(upload_dir, filename))
            cover_image_path = f'uploads/{filename}'
            
            # 刪除舊圖片
            if book['cover_image']:
                old_path = os.path.join(current_app.static_folder, book['cover_image'])
                if os.path.exists(old_path):
                    try:
                        os.remove(old_path)
                    except Exception:
                        pass

    success = BookModel.update_book(id, title, notes, rating, cover_image_path, start_date, end_date)
    if success:
        flash('書籍更新成功！', 'success')
        return redirect(url_for('book_bp.book_detail', id=id))
    else:
        flash('更新時發生錯誤，請稍後再試。', 'danger')
        return redirect(url_for('book_bp.edit_book_form', id=id))

@book_bp.route('/books/<int:id>/delete', methods=['POST'])
def delete_book(id):
    """刪除書籍"""
    book = BookModel.get_book_by_id(id)
    if not book:
        abort(404)
        
    # 刪除圖片檔案
    if book['cover_image']:
        old_path = os.path.join(current_app.static_folder, book['cover_image'])
        if os.path.exists(old_path):
            try:
                os.remove(old_path)
            except Exception:
                pass
                
    success = BookModel.delete_book(id)
    if success:
        flash('書籍已成功刪除！', 'success')
    else:
        flash('刪除時發生錯誤。', 'danger')
        
    return redirect(url_for('book_bp.index'))
