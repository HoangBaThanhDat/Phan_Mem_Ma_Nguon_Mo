from flask import Flask, render_template, request

app = Flask(__name__)

# Tùy chọn: Hàm làm gọn số (ví dụ 5.0 -> 5) để giao diện đẹp hơn
def format_num(n):
    if isinstance(n, float) and n.is_integer():
        return int(n)
    return n

@app.route("/")
def home():
    # 1. Lấy dữ liệu qua phương thức GET
    a_raw = request.args.get('a')
    b_raw = request.args.get('b')

    # 2. Xử lý giá trị a (Nếu trống thì bằng 0)
    if a_raw is None or a_raw == "":
        a = 0
    else:
        a = float(a_raw)

    # 3. Xử lý giá trị b (Nếu trống thì bằng 1 để tránh lỗi chia 0)
    if b_raw is None or b_raw == "":
        b = 1
    else:
        b = float(b_raw)

    # 4. Làm gọn số a và b để hiển thị đẹp hơn
    a = format_num(a)
    b = format_num(b)

    # 5. Tính toán cả 4 phép tính cùng lúc
    cong = format_num(a + b)
    tru = format_num(a - b)
    nhan = format_num(a * b)
    
    if b == 0:
        chia = "Không thể chia cho 0"
    else:
        # Làm tròn 4 chữ số thập phân cho phép chia
        chia = round(a / b, 4) if not (a/b).is_integer() else int(a / b)

    # 6. Trả kết quả về giao diện
    return render_template("math.html", a=a, b=b, cong=cong, tru=tru, nhan=nhan, chia=chia)

if __name__ == "__main__":
    app.run(debug=True)