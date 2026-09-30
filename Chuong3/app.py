from flask import Flask, request, url_for

app = Flask(__name__)

# BƯỚC 3: Thêm dữ liệu mẫu cho MiniBlog
POSTS = [
    {
        "id": 1,
        "title": "Chào Flask",
        "author": "an",
        "content": "Flask là một micro-framework...",
        "created": "2026-09-01",
    },
    {
        "id": 2,
        "title": "Định tuyến trong Flask",
        "author": "bình",
        "content": "Nội dung bài viết về routing trong Flask...",
        "created": "2026-09-05",
    },
    {
        "id": 3,
        "title": "Giấy phép BSD của Flask",
        "author": "an",
        "content": "Nội dung bài viết về giấy phép mã nguồn mở...",
        "created": "2026-09-10",
    }
]

# Hàm tìm kiếm bài viết theo ID
def find_post(post_id):
    """Tìm một bài viết dựa vào post_id hoặc None nếu không có."""
    for post in POSTS:
        if post["id"] == post_id:
            return post
    return None

# Ví dụ 1: Giao diện Trang chủ (đã gộp và sử dụng url_for để tạo link)
@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    # Sử dụng url_for để tự động sinh đường dẫn an toàn đến hàm gioi_thieu
    return f"<a href='/'>Trang chủ</a> | <a href='{url_for('gioi_thieu')}'>Giới thiệu</a>"

# Ví dụ 2: Trang giới thiệu
@app.route("/gioi-thieu")
@app.route("/about")
def gioi_thieu():
    return "Xin chào, đây là trang giới thiệu!"

# Ví dụ 3: Biến trên URL
@app.route("/user/<username>")
def user_profile(username):
    return f"Xin chào, {username}!"

# Bài 4 - Cách 1: Bắt buộc phải có dấu chấm (vd: /square/5.0)
@app.route("/square/<float:x>")
def square(x):
    return f"{x}^2 = {x**2}"

# Bài 4 - Cách 2: Tự ép kiểu thủ công (vd: /square2/5)
@app.route("/square2/<x>")
def square2(x):
    return f"({float(x)})^2 = {float(x) ** 2}"

# BÀI MỚI 1: Nhận chuỗi số và tính tổng
@app.route("/sum/<strs>")
def tong(strs):
    # Ví dụ nhận vào: 1,2,3 -> Tính ra: 6
    numbers = strs.split(",")
    total = sum(float(num) for num in numbers)
    return f"Tổng của {strs} là: {total}"

# BÀI MỚI 2: Đọc tham số Query String (Tính toán cộng/trừ)
@app.route("/tinh-toan")
def tinh_toan():
    # Lấy và tự động ép URL sang số thực
    a = request.args.get("a", type=float)
    b = request.args.get("b", type=float)
    op = request.args.get("op")
    
    # Kiểm tra an toàn
    if a is None or b is None:
        return "Vui lòng truyền tham số là số hợp lệ (ví dụ: ?a=5&b=10&op=add)"

    # Xử lý phép tính
    if op == "add":
        return f"{a} + {b} = {a + b}"
    elif op == "sub":
        return f"{a} - {b} = {a - b}"
    else:
        return "Vui lòng truyền đúng phép tính (op=add hoặc op=sub)"

# ĐOẠN NÀY BẮT BUỘC PHẢI NẰM Ở CUỐI FILE
if __name__ == "__main__":
    app.run(debug=True, port=5000)