# Bài tập tổng hợp Chương 3

## 1. Kết quả lệnh `flask --app sodiem routes`
Endpoint               Methods    Rule
---------------------  ---------  ------------------------------------------
api_scores             DELETE, GET, PUT /api/students/<mssv>/scores/<course>
api_student_detail     GET        /api/students/<mssv>
api_students           GET        /api/students
export_csv             GET        /students/<mssv>/export
index                  GET        /
search_student         GET        /search
static                 GET        /static/<path:filename>
student_detail         GET        /students/<mssv>
student_list           GET        /students
sv_redirect            GET        /sv/<mssv>

## 2. Kết quả kiểm thử bằng curl
* `curl -i $B/sv/23T1020001` -> HTTP/1.1 301 MOVED PERMANENTLY, Location: /students/23T1020001
* `curl -i $B/students/23T1020001/export` -> HTTP/1.1 200 OK, Content-Type: text/csv; charset=utf-8, Content-Disposition: attachment; filename=diem_23T1020001.csv
* `curl "$B/api/students?lop=k47a&min_avg=7"` -> HTTP/1.1 200 OK, Trả về JSON danh sách sinh viên hợp lệ.
* `curl -i "$B/api/students?min_avg=abc"` -> HTTP/1.1 400 BAD REQUEST, Dữ liệu không hợp lệ.
* `curl -i $B/api/students/999` -> HTTP/1.1 404 NOT FOUND, Không tìm thấy.
* `curl -i -X PUT "$S/web?score=9"` -> HTTP/1.1 201 CREATED, Location: /api/students/23T1020005/scores/WEB
* `curl -i -X PUT "$S/WEB?score=7.5"` -> HTTP/1.1 200 OK, Cập nhật điểm thành công.
* `curl -i -X PUT "$S/WEB?score=11"` -> HTTP/1.1 400 BAD REQUEST, Điểm không hợp lệ.
* `curl -i -X DELETE $S/WEB` -> HTTP/1.1 204 NO CONTENT
* `curl -i -X POST $S/WEB` -> HTTP/1.1 405 METHOD NOT ALLOWED
* `curl -i -X POST $B/students` -> HTTP/1.1 405 METHOD NOT ALLOWED

## 3. Trả lời câu hỏi
* **Vì sao Câu 4 dùng 301 còn Câu 8 trả 201 kèm Location?**
  - Câu 4 dùng 301 (Moved Permanently) để báo cho trình duyệt biết URL rút gọn đã được chuyển hướng vĩnh viễn sang URL chi tiết, giúp trình duyệt tự động chuyển hướng.
  - Câu 8 dùng 201 (Created) vì phương thức PUT đã tạo ra một tài nguyên mới (điểm học phần mới chưa từng có). Header `Location` được kèm theo để chỉ ra đường dẫn của tài nguyên vừa được tạo.
* **Thêm điểm cho 23T1020005 rồi khởi động lại server, điểm đó còn không? Vì sao?**
  - Điểm đó **không còn**. Vì dữ liệu hiện tại chỉ được lưu tạm thời trong bộ nhớ RAM (biến dictionary `STUDENTS` trong mã nguồn Python). Khi khởi động lại server, chương trình sẽ chạy lại từ đầu và khởi tạo lại biến `STUDENTS` bằng dữ liệu gốc ghi trong code, mọi thay đổi trước đó sẽ bị mất do chưa được lưu vào cơ sở dữ liệu.