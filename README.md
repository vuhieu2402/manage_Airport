# Hệ thống Quản lý Xuất Nhập Cảnh

Hệ thống quản lý xuất nhập cảnh tại sân bay, cung cấp các chức năng quản lý bản ghi xuất nhập cảnh, tìm kiếm, lọc và báo cáo thống kê.

## Cấu trúc dự án

Dự án được chia làm hai phần chính:

- **Backend**: Xây dựng bằng Django và Django REST Framework
- **Frontend**: Xây dựng bằng Angular và Tailwind CSS

## Yêu cầu hệ thống

### Backend
- Python 3.10+
- Xem thêm tại `requirements-backend.txt`

### Frontend
- Node.js 18+
- Angular CLI 19.2+
- Xem thêm tại `requirements-frontend.txt`

## Cài đặt

### Backend

1. Tạo và kích hoạt môi trường ảo Python:
```bash
python -m venv venv
source venv/bin/activate  # Trên Linux/Mac
venv\Scripts\activate     # Trên Windows
```

2. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements-backend.txt
```

3. Di chuyển vào thư mục backend:
```bash
cd backend/manageAirport
```

4. Tạo database và chạy migration:
```bash
python manage.py migrate
```

5. Tạo tài khoản admin:
```bash
python manage.py createsuperuser
```

6. Chạy server:
```bash
python manage.py runserver
```

Backend sẽ chạy tại địa chỉ: http://127.0.0.1:8000/

### Frontend

1. Di chuyển vào thư mục frontend:
```bash
cd frontend
```

2. Cài đặt các thư viện:
```bash
npm install
```

3. Chạy ứng dụng:
```bash
ng serve
```

Frontend sẽ chạy tại địa chỉ: http://localhost:4200/

## Sử dụng

1. Truy cập giao diện quản trị Django: http://127.0.0.1:8000/admin/
2. Truy cập API Swagger UI: http://127.0.0.1:8000/swagger/
3. Truy cập ứng dụng web: http://localhost:4200/

## Tính năng chính

- Quản lý thông tin xuất nhập cảnh
- Tìm kiếm, lọc bản ghi
- Tạo mới, chỉnh sửa, xóa bản ghi
- Quản lý trạng thái xử lý
- Hỗ trợ lưu trữ thông tin bổ sung (thị thực, địa chỉ lưu trú, liên hệ)


