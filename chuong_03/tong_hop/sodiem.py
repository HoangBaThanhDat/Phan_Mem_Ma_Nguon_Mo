from flask import Flask, request, url_for, jsonify, redirect, abort, make_response
from markupsafe import escape

app = Flask(__name__)
app.json.ensure_ascii = False

STUDENTS = {
    "23T1020001": {"name": "Nguyễn Văn An", "lop": "K47A", "scores": {"PMMNM": 8.5, "CSDL": 7.0, "MMT": 9.0}},
    "23T1020002": {"name": "Trần Thị Bình", "lop": "K47A", "scores": {"PMMNM": 6.0, "CSDL": 5.5, "MMT": 7.0}},
    "23T1020003": {"name": "Lê Hoàng Cường", "lop": "K47B", "scores": {"PMMNM": 9.5, "CSDL": 9.0}},
    "23T1020004": {"name": "Phạm Minh Dũng", "lop": "K47B", "scores": {"PMMNM": 4.0, "CSDL": 3.5, "MMT": 5.0}},
    "23T1020005": {"name": "Hoàng Thu Hà", "lop": "K47A", "scores": {}},
    "23T1020006": {"name": "Võ Quốc Khánh", "lop": "K47C", "scores": {"PMMNM": 7.5, "MMT": 8.0}}
}

def average(scores):
    if not scores:
        return None
    return round(sum(scores.values()) / len(scores), 2)

def rank(avg):
    if avg is None: return "Chưa có điểm"
    if avg >= 8.5: return "Giỏi"
    if avg >= 7.0: return "Khá"
    if avg >= 5.0: return "Trung bình"
    return "Yếu"

def student_summary(mssv):
    if mssv not in STUDENTS:
        return None
    info = STUDENTS[mssv]
    avg = average(info["scores"])
    return {
        "mssv": mssv,
        "name": info["name"],
        "lop": info["lop"],
        "scores": info["scores"],
        "average": avg,
        "rank": rank(avg)
    }

def layout(title, body):
    menu = f'''
        <a href="{url_for('index')}">Trang chủ</a> | 
        <a href="{url_for('student_list')}">Sinh viên</a> | 
        <a href="{url_for('search_student')}">Tìm kiếm</a>
    '''
    return f'''<!DOCTYPE html>
    <html>
    <head><title>{escape(title)}</title></head>
    <body>
        <nav>{menu}</nav><hr>
        {body}
    </body>
    </html>'''

@app.route('/')
def index():
    total_sv = len(STUDENTS)
    lops = set(s['lop'] for s in STUDENTS.values())
    body = f'''
        <h1>Tổng quan</h1>
        <p>Tổng số sinh viên: {total_sv}</p>
        <p>Số lớp: {len(lops)}</p>
        <ul>
            <li><a href="{url_for('student_list')}">Danh sách sinh viên (Web)</a></li>
            <li><a href="{url_for('api_students')}">Danh sách sinh viên (API)</a></li>
        </ul>
    '''
    return layout("Sổ điểm", body)

@app.route('/students')
def student_list():
    lop_filter = request.args.get('lop', '').upper()
    lops = sorted(list(set(s['lop'] for s in STUDENTS.values())))
    
    filter_links = [f'<a href="{url_for("student_list")}">Tất cả</a>']
    for l in lops:
        filter_links.append(f'<a href="{url_for("student_list", lop=l)}">{escape(l)}</a>')
    filter_html = " | ".join(filter_links)

    sv_list = [student_summary(m) for m in STUDENTS if not lop_filter or STUDENTS[m]['lop'].upper() == lop_filter]
    
    if not sv_list:
        return layout("Danh sách sinh viên", f'<p>{filter_html}</p><p>Không có sinh viên phù hợp.</p>')
    
    rows = ""
    for sv in sv_list:
        avg_str = sv['average'] if sv['average'] is not None else ""
        rows += f'''<tr>
            <td><a href="{url_for('student_detail', mssv=sv['mssv'])}">{escape(sv['mssv'])}</a></td>
            <td>{escape(sv['name'])}</td><td>{escape(sv['lop'])}</td>
            <td>{avg_str}</td><td>{escape(sv['rank'])}</td>
        </tr>'''
    
    body = f'<p>{filter_html}</p><table border="1"><tr><th>MSSV</th><th>Họ tên</th><th>Lớp</th><th>Điểm TB</th><th>Xếp loại</th></tr>{rows}</table>'
    return layout("Danh sách sinh viên", body)

@app.route('/students/<mssv>')
def student_detail(mssv):
    summary = student_summary(mssv)
    if not summary:
        abort(404, description=f"Không có sinh viên với MSSV = {mssv}.")
    
    rows = "".join([f"<tr><td>{escape(hp)}</td><td>{diem}</td></tr>" for hp, diem in summary['scores'].items()])
    avg_str = summary['average'] if summary['average'] is not None else "Chưa có điểm"
    
    body = f'''
        <h2>{escape(summary['name'])} - {escape(mssv)}</h2>
        <p>Lớp: <a href="{url_for('student_list', lop=summary['lop'])}">{escape(summary['lop'])}</a></p>
        <p>Điểm TB: {avg_str} - Xếp loại: {escape(summary['rank'])}</p>
        <table border="1"><tr><th>Học phần</th><th>Điểm</th></tr>{rows}</table>
        <p><a href="{url_for('export_csv', mssv=mssv)}">Tải bảng điểm (CSV)</a></p>
        <p>Link rút gọn: <a href="{url_for('sv_redirect', mssv=mssv)}">/sv/{escape(mssv)}</a></p>
    '''
    return layout(f"Chi tiết {summary['name']}", body)

@app.route('/sv/<mssv>')
def sv_redirect(mssv):
    return redirect(url_for('student_detail', mssv=mssv), code=301)

@app.route('/students/<mssv>/export')
def export_csv(mssv):
    summary = student_summary(mssv)
    if not summary:
        abort(404, description=f"Không có sinh viên với MSSV = {mssv}.")
    
    csv_content = "hoc_phan,diem\n" + "".join([f"{hp},{diem}\n" for hp, diem in summary['scores'].items()])
    response = make_response(csv_content)
    response.headers["Content-Type"] = "text/csv; charset=utf-8"
    response.headers["Content-Disposition"] = f"attachment; filename=diem_{mssv}.csv"
    return response

@app.route('/search')
def search_student():
    q = request.args.get('q', '')
    results = [(m, info['name']) for m, info in STUDENTS.items() if q.lower() in info['name'].lower() or q.lower() in m.lower()] if q else []
    
    res_html = f'<p>Tìm thấy {len(results)} kết quả cho "{escape(q)}":</p><ul>' + "".join([f'<li><a href="{url_for("student_detail", mssv=m)}">{escape(m)} - {escape(n)}</a></li>' for m, n in results]) + '</ul>' if q else ""
    
    body = f'''
        <form method="GET" action="{url_for('search_student')}">
            <input type="text" name="q" value="{escape(q)}" placeholder="Nhập tên hoặc MSSV">
            <button type="submit">Tìm kiếm</button>
        </form>
        {res_html}
    '''
    return layout("Tìm kiếm", body)

@app.route('/api/students')
def api_students():
    lop = request.args.get('lop', '').upper()
    min_avg_str = request.args.get('min_avg')
    min_avg = None
    
    if min_avg_str is not None:
        try:
            min_avg = float(min_avg_str)
        except ValueError:
            abort(400, description="Tham số min_avg phải là số.")

    result = [student_summary(m) for m in STUDENTS if (not lop or STUDENTS[m]['lop'].upper() == lop) and (min_avg is None or (student_summary(m)['average'] is not None and student_summary(m)['average'] >= min_avg))]
    return jsonify(result)

@app.route('/api/students/<mssv>')
def api_student_detail(mssv):
    summary = student_summary(mssv)
    if not summary: abort(404, description="Không tìm thấy sinh viên.")
    return jsonify(summary)

@app.route('/api/students/<mssv>/scores/<course>', methods=['GET', 'PUT', 'DELETE'])
def api_scores(mssv, course):
    if mssv not in STUDENTS: abort(404, description="Sinh viên không tồn tại.")
    course_upper = course.upper()
    scores = STUDENTS[mssv]['scores']
    
    if request.method == 'GET':
        if course_upper not in scores: abort(404, description="Học phần chưa có điểm.")
        return jsonify({"mssv": mssv, "course": course_upper, "score": scores[course_upper]})
    
    elif request.method == 'PUT':
        score_str = request.args.get('score')
        if score_str is None: abort(400, description="Thiếu tham số score.")
        try:
            score = float(score_str)
            if score < 0 or score > 10: raise ValueError
        except ValueError: abort(400, description="Điểm không hợp lệ.")
        
        is_new = course_upper not in scores
        scores[course_upper] = score
        res_data = {"mssv": mssv, "course": course_upper, "score": score, "average": average(scores)}
        
        if is_new:
            resp = jsonify(res_data)
            resp.status_code = 201
            resp.headers['Location'] = url_for('api_scores', mssv=mssv, course=course_upper)
            return resp
        return jsonify(res_data), 200

    elif request.method == 'DELETE':
        if course_upper not in scores: abort(404, description="Học phần chưa có điểm.")
        del scores[course_upper]
        return '', 204

@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(405)
def handle_error(error):
    titles = {400: "Dữ liệu không hợp lệ", 404: "Không tìm thấy", 405: "Phương thức không được hỗ trợ"}
    code = error.code
    title = titles.get(code, "Lỗi")
    
    if request.path.startswith('/api/'):
        return jsonify({"error": title, "detail": error.description}), code
    return layout(f"Lỗi {code}", f"<h1>{code} - {title}</h1><p>{escape(error.description)}</p>"), code

if __name__ == '__main__':
    app.run(debug=True, port=8000)