
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
- Triển khai production: đặt `DEBUG=False`, cấu hình `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` (khớp domain/cổng reverse proxy, ví dụ `http://localhost:8080`), cập nhật `SECRET_KEY` và `DATABASES` cho môi trường thật.

## Triển khai production (không Docker: systemd + Nginx)

Phù hợp khi chạy trên 1 máy chủ Ubuntu/Debian và muốn quản lý bằng `systemd`.

1) Cài đặt gói hệ thống  
```bash
sudo apt update
sudo apt install -y python3-venv python3-pip nginx \
  build-essential libpq-dev libcairo2 libpango-1.0-0 libpangocairo-1.0-0 \
  libgdk-pixbuf-2.0-0 libffi-dev shared-mime-info fontconfig
```

2) Chuẩn bị mã nguồn  
- Ví dụ dùng đường dẫn `/opt/qlkt` và user chạy service là `www-data` (tùy chỉnh theo môi trường).  
- Sửa `qlkt/settings.py` cho production: `DEBUG=False`, `ALLOWED_HOSTS=["ten-mien-hoac-ip"]`, `CSRF_TRUSTED_ORIGINS=["https://ten-mien-hoac-ip"]`, cập nhật `SECRET_KEY` và `DATABASES` (SQLite có thể giữ nguyên, khuyến khích PostgreSQL).

3) Thiết lập virtualenv và phụ thuộc  
```bash
cd /opt/qlkt
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt gunicorn
python manage.py migrate
python manage.py collectstatic --noinput
```

4) Tạo service `systemd` cho Gunicorn (ví dụ `/etc/systemd/system/qlkt.service`)  
```ini
[Unit]
Description=Gunicorn for QLKT
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/qlkt
Environment="PATH=/opt/qlkt/.venv/bin"
Environment="DJANGO_SETTINGS_MODULE=qlkt.settings"
RuntimeDirectory=qlkt
ExecStart=/opt/qlkt/.venv/bin/gunicorn qlkt.wsgi:application --bind unix:/run/qlkt/qlkt.sock --workers 3
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
Sau đó bật service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now qlkt.service
```

5) Cấu hình Nginx (ví dụ `/etc/nginx/sites-available/qlkt` rồi symlink sang `sites-enabled`)  
```nginx
upstream qlkt {
    server unix:/run/qlkt/qlkt.sock;
}

server {
    listen 80;
    server_name example.com;  # đổi sang domain/IP của bạn

    client_max_body_size 50M;

    location /static/ {
        alias /opt/qlkt/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, max-age=2592000";
    }

    location / {
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://qlkt;
    }
}
```
Kiểm tra và reload:
```bash
sudo nginx -t && sudo systemctl reload nginx
```

6) Tạo tài khoản admin:
```bash
sudo -u www-data /opt/qlkt/.venv/bin/python /opt/qlkt/manage.py createsuperuser
```

## Triển khai bằng Docker Compose + Nginx reverse proxy

Phù hợp khi muốn môi trường đóng gói sẵn. Yêu cầu Docker Engine và Docker Compose plugin.

1) Kiểm tra lại `qlkt/settings.py`: đặt `DEBUG=False`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` (ví dụ `http://localhost:8080`), `SECRET_KEY` và cấu hình DB (mặc định compose dùng SQLite qua bind mount `db.sqlite3`; nếu muốn PostgreSQL hãy cập nhật settings và thêm dịch vụ DB riêng).

2) Build và chạy:
```bash
docker compose build
docker compose up -d
```
Truy cập: `http://localhost:8080` (Nginx reverse proxy tới Gunicorn trên container web).

3) Quản trị container:
```bash
# Xem log
docker compose logs -f web

# Tạo superuser
docker compose exec web python manage.py createsuperuser

# Dừng dịch vụ
docker compose down
```

Mặc định static được collect vào volume `static_volume` và Nginx phục vụ tại `/static/`. Cổng host đang map 8080→80 trong container (`http://localhost:8080`). DB SQLite được bind mount từ file `db.sqlite3` trong thư mục dự án. Nếu chuyển sang Postgres, thêm service Postgres trong `docker-compose.yml`, cập nhật biến kết nối trong `qlkt/settings.py`, và chạy lại `docker compose up -d --build`.
