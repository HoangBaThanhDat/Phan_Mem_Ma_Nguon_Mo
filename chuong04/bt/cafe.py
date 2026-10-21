from flask import Flask, render_template, request, abort
from datetime import datetime

app = Flask(__name__)

@app.template_filter('vnd')
def vnd_format(value):
    try:
        return f"{int(value):,}".replace(",", ".") + " đ"
    except (ValueError, TypeError):
        return str(value) + " đ"

@app.template_filter('title_vi')
def title_vi(s):
    return ' '.join(word.capitalize() for word in str(s).split())

SHOP = {
    "name": "Cà Phê Thành Đạt",
    "address": "12 Lê Lợi, Huế",
    "phone": "0234 3888 999",
    "open": 7,
    "close": 22
}

PROMOTIONS = [
    "Giảm 10% cho sinh viên",
    "Mua 2 tặng 1 vào thứ Hai"
]

# Danh sách đủ 7 món theo yêu cầu các bài trước
MENU = [
    {"id": 1, "name": "cà phê đen", "price": 20000, "available": True},
    {"id": 2, "name": "cà phê sữa", "price": 25000, "available": True},
    {"id": 3, "name": "bạc xỉu", "price": 28000, "available": True},
    {"id": 4, "name": "trà sen vàng", "price": 45000, "available": True},
    {"id": 5, "name": "freeze trà xanh", "price": 55000, "available": False},
    {"id": 6, "name": "phindi hạnh nhân", "price": 45000, "available": True},
    {"id": 7, "name": "trà thanh đào", "price": 45000, "available": True}
]

@app.route('/')
def index():
    gio_param = request.args.get('gio')
    try:
        gio = int(gio_param) if gio_param is not None else datetime.now().hour
    except ValueError:
        gio = datetime.now().hour

    is_open = SHOP['open'] <= gio < SHOP['close']
    total_items = len(MENU)
    avg_price = sum(item['price'] for item in MENU) / total_items if total_items > 0 else 0

    return render_template(
        'index.html', 
        shop=SHOP, 
        promotions=PROMOTIONS, 
        gio=gio, 
        is_open=is_open, 
        total_items=total_items, 
        avg_price=avg_price
    )

@app.route('/menu')
def menu():
    # Lấy tham số page từ URL (mặc định là trang 1)
    page_param = request.args.get('page', 1)
    try:
        page = int(page_param)
    except ValueError:
        abort(404)  # Nếu nhập chữ (VD: abc) -> Báo lỗi 404

    PER_PAGE = 3  # Mỗi trang 3 món theo yêu cầu slide
    total_items = len(MENU)
    total_pages = (total_items + PER_PAGE - 1) // PER_PAGE

    # Nếu trang yêu cầu nhỏ hơn 1 hoặc vượt quá tổng số trang -> Báo lỗi 404
    if page < 1 or page > total_pages:
        abort(404)

    # Cắt danh sách món cho trang hiện tại
    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    current_menu = MENU[start:end]

    return render_template(
        'menu.html', 
        shop=SHOP, 
        menu=current_menu, 
        page=page, 
        pages=total_pages, 
        endpoint='menu'
    )

@app.route('/contact')
def contact():
    return render_template('contact.html', shop=SHOP)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', shop=SHOP), 404

if __name__ == '__main__':
    app.run(debug=True)