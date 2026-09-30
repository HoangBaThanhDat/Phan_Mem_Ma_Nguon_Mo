from flask import Flask, request, url_for, jsonify, abort
from markupsafe import escape

app = Flask(__name__)

# 1. List BOOKS >= 4 cuốn, đầy đủ: id, title, author, year, category, available
BOOKS = [
    {"id": 1, "title": "Flask Căn Bản", "author": "An", "year": 2023, "category": "Lập trình", "available": True},
    {"id": 2, "title": "Python Nâng Cao", "author": "Bình", "year": 2022, "category": "Lập trình", "available": False},
    {"id": 3, "title": "Toán Rời Rạc", "author": "Cường", "year": 2021, "category": "Toán học", "available": True},
    {"id": 4, "title": "Mạng Máy Tính", "author": "Dũng", "year": 2024, "category": "Hệ thống", "available": True}
]

# Hàm hỗ trợ: Menu chung dùng url_for (Yêu cầu 6, 7)
def menu_chung():
    return f"<a href='{url_for('index')}'>Trang chủ</a> | <a href='{url_for('books')}'>Danh sách sách</a> | <a href='{url_for('api_books')}'>API Sách</a><hr>"

# 2. Trang chủ (/): Tổng số đầu sách, số sách sẵn sàng
@app.route('/')
def index():
    tong_so = len(BOOKS)
    san_sang = sum(1 for b in BOOKS if b['available'])
    return f"{menu_chung()}Tổng số đầu sách: {tong_so}<br>Số sách sẵn sàng cho mượn: {san_sang}"

# 3. /books: bảng sách, link chi tiết, lọc category=Lập trình kèm thanh liên kết
@app.route('/books')
def books():
    # Xử lý lọc
    category = request.args.get('category')
    danh_sach = [b for b in BOOKS if b['category'] == category] if category else BOOKS

    # Thanh liên kết lọc (Dùng url_for và escape)
    cats = set(b['category'] for b in BOOKS)
    thanh_loc = f"<a href='{url_for('books')}'>Tất cả</a>"
    for c in cats:
        thanh_loc += f" | <a href='{url_for('books', category=c)}'>{escape(c)}</a>"

    # Hiển thị bảng
    html = f"{menu_chung()}Lọc theo thể loại: {thanh_loc}<br><br><table border='1'>"
    html += "<tr><th>ID</th><th>Tên sách</th><th>Tác giả</th><th>Năm</th><th>Thể loại</th><th>Sẵn sàng</th></tr>"
    for b in danh_sach:
        link = url_for('book_detail', book_id=b['id'])
        html += f"<tr><td>{b['id']}</td><td><a href='{link}'>{escape(b['title'])}</a></td><td>{escape(b['author'])}</td><td>{b['year']}</td><td>{escape(b['category'])}</td><td>{b['available']}</td></tr>"
    html += "</table>"
    return html

# 4. /books/<int:book_id>: chi tiết; 404 "Không có sách với ID = ..."
@app.route('/books/<int:book_id>')
def book_detail(book_id):
    book = next((b for b in BOOKS if b['id'] == book_id), None)
    if not book:
        abort(404, description=f"Không có sách với ID = {escape(book_id)}")
    
    return f"{menu_chung()}<b>Chi tiết sách:</b><br>ID: {book['id']}<br>Tiêu đề: {escape(book['title'])}<br>Tác giả: {escape(book['author'])}<br>Năm: {book['year']}<br>Thể loại: {escape(book['category'])}<br>Sẵn sàng: {book['available']}"

# 5. /api/books và /api/books/<int:book_id>: JSON; không tồn tại -> {"error": ...} với mã 404
@app.route('/api/books')
def api_books():
    return jsonify(BOOKS)

@app.route('/api/books/<int:book_id>')
def api_book_detail(book_id):
    book = next((b for b in BOOKS if b['id'] == book_id), None)
    if not book:
        return jsonify({"error": f"Không có sách với ID = {book_id}"}), 404
    return jsonify(book)

# 6. Trang 404 tuỳ biến, có menu chung
@app.errorhandler(404)
def page_not_found(e):
    # Trả về JSON nếu là đường dẫn API
    if request.path.startswith('/api/'):
        return jsonify({"error": "Endpoint không tồn tại"}), 404
    
    # Trả về HTML với menu chung
    msg = e.description if e.description != e.name else "Đường dẫn không tồn tại"
    return f"{menu_chung()}<h2>Lỗi 404</h2><p>{msg}</p>", 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)