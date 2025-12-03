
# Device-And-Operation-Management-For-IT-Department

Ứng dụng Django quản lý thiết bị, công văn và nghiệp vụ xử lý kỹ thuật cho bộ phận CNTT.

## Cài đặt nhanh

1) Tạo môi trường ảo
```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

2) Cài thư viện
```bash
pip install -r requirements.txt
```

3) Cấu hình cơ sở dữ liệu  
Mặc định dùng SQLite (`db.sqlite3`). Nếu muốn PostgreSQL, cập nhật `DATABASES` trong `qlkt/settings.py` rồi chạy migrate.

4) Tạo bảng & dữ liệu mẫu
```bash
python manage.py migrate
python manage.py seed_all    # hoặc seed_data, seed_equipment, seed_documents, seed_operations
```

5) Chạy server
```bash
python manage.py runserver 0.0.0.0:8000
```
Truy cập admin: `http://127.0.0.1:8000/admin`

## Ghi chú
- Kiểm tra quyền thực thi của file `setup.sh` nếu muốn chạy tập lệnh tự động.
- Nếu dùng PostgreSQL, đảm bảo service đang chạy và thông tin kết nối đúng.
- Dữ liệu seed được viết bằng tiếng Việt, sát với nghiệp vụ CNTT (nhân sự, thiết bị, công văn, yêu cầu xử lý).

## Khắc phục sự cố
- Lỗi kết nối DB: kiểm tra `DATABASES` và service PostgreSQL/SQLite file path.
- Lỗi migrate/seed: xóa file `db.sqlite3` (nếu dùng SQLite) và chạy lại `migrate` + `seed_all`.
- Thiếu thư viện: đảm bảo đã kích hoạt đúng môi trường ảo trước khi `pip install`.

Triển khai production với Gunicorn/Nginx: tham khảo hướng dẫn chuẩn cho Django + Postgres + Nginx + Gunicorn.
