#!/bin/bash
source .venv/bin/activate
# Xóa các file migrations trừ __init__.py
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# Tạo lại migrations và migrate
python manage.py makemigrations
python manage.py migrate

# Seed dữ liệu
python manage.py seed_data
python manage.py seed_equipment
python manage.py seed_documents
python manage.py seed_operations
# Tạo superuser (custom command sẽ xử lý)
python manage.py createsu --username red --password 1234xyza

# Chạy server
python manage.py runserver 8001
