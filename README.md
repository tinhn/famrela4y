# 👨‍👩‍👧‍👦 Suy Luận Quan Hệ Gia Đình

## 📌 Giới thiệu

Dự án này là một ví dụ thực tiễn phục vụ mục đích **học tập**, **tham khảo**, và **mở rộng nghiên cứu** về các mối quan hệ trong gia đình. Được viết bằng ngôn ngữ **Python**, dự án sử dụng thư viện **NetworkX**, **cytoscape** để trực quan hóa các mối liên kết như cha mẹ – con cái, vợ chồng, anh chị em, và các mối quan hệ thông gia.


## 🔍 Các chức năng nổi bật

Dự án cung cấp các hàm suy luận tự động:

| Mối quan hệ              | Mô tả                                                                 |
|--------------------------|----------------------------------------------------------------------|
| 👴 Cháu nội / Cháu ngoại | Xác định mối quan hệ ông bà – cháu theo dòng nội hoặc dòng ngoại     |
| 🤝 Sui gia                | Tìm mối quan hệ giữa cha mẹ hai bên khi con cái kết hôn              |
| 💍 Vợ chồng               | Nhận diện các cặp vợ chồng từ dữ liệu đầu vào                        |
| 👨‍👧 Cha mẹ – Con cái      | Xây dựng liên kết giữa cha mẹ và con cái                             |
| 👨‍⚖️ Con rể, cha vợ, mẹ vợ | Suy luận quan hệ thông gia từ vợ chồng và cha mẹ                      |
| 👧👦 Anh chị em            | Xác định các cặp anh chị em ruột dựa trên cha mẹ chung               |

---
## 🧩 Cấu trúc dự án

Dự án gồm 2 phần chính:

### 1️⃣ `gen_data_demo.py`
- Tạo dữ liệu mẫu về các cá nhân, cặp vợ chồng, cha mẹ – con cái
- Dữ liệu được tổ chức rõ ràng, dễ mở rộng
- Phù hợp để thử nghiệm các hàm suy luận

### 2️⃣ `visualize_family.py`
- Xử lý dữ liệu và suy luận các mối quan hệ
- Trực quan hóa bằng thư viện `networkx`
- Hiển thị sơ đồ quan hệ gia đình dưới dạng đồ thị

---


## 📦 Đầu vào dữ liệu

Dữ liệu được tổ chức theo cấu trúc đơn giản và dễ hiểu:

```python
family_data = [
    {"spouse": ["Nguyễn Văn A", "Trần Thị B"]},
    {"spouse": ["Lê Văn C"], "children": ["Nguyễn Văn A"]},
    {"spouse": ["Phạm Thị D"], "children": ["Trần Thị B"]}
]
```

## ⚙️ Hướng dẫn chạy chương trình

### 1. Tạo dữ liệu mẫu
Bạn cần điều chỉnh lại một chút trước khi tạo dữ liệu mẫu bằng cách:
- Thay đổi hoặc bổ sung thông tin tại `person_info`:
```
person_info = {
    "Nguyễn Văn A":   {"gender": "Nam", "fam_order": 1},
    "Phạm Thị B":      {"gender": "Nữ", "fam_order": 1},
    "Nguyễn C":      {"gender": "Nam", "fam_order": 1},
    "Thị D":      {"gender": "Nữ", "fam_order": 2},   
    ...
}    
```
- Thay đổi hoặc bổ sung thông tin về vợ/chồng - con tại `families`: 
```
families = [
    {"spouse": ["Nguyễn Văn A", "Phạm Thị B"], "children": ["Nguyễn C", "Thị D", ...]},
    ...
]
```     
- Chạy lệnh sau để sinh dữ liệu
```bash
python3 gen_data_demo.py
```
Lệnh này sẽ tạo dữ liệu mẫu phục vụ cho việc trực quan hóa quan hệ gia đình.

### 2. Chạy chương trình trực quan hóa
```bash
python3 visualize_family.py
```
Chương trình sẽ khởi chạy một ứng dụng web hiển thị sơ đồ quan hệ gia đình.

### 3. Truy cập kết quả
Mở trình duyệt và truy cập địa chỉ: http://127.0.0.1:8050/ . Tại đây bạn sẽ thấy đồ thị quan hệ gia đình được trình bày trực quan và tương tác.

## 📈 Ứng dụng

- Phân tích phả hệ dòng họ
- Trực quan hóa mối quan hệ gia đình
- Hỗ trợ nghiên cứu nhân khẩu học, văn hóa – xã hội
- Làm nền tảng cho hệ thống hỏi đáp về quan hệ họ hàng
- Tích hợp vào chatbot hoặc trợ lý ảo

## 🚀 Hướng phát triển

- Hỗ trợ nhiều thế hệ hơn (ông cố, chắt…)
- Tích hợp sơ đồ cây trực quan
- Hỗ trợ dữ liệu không đầy đủ (suy luận từ dữ kiện thiếu)
- Xuất ra định dạng chuẩn như GEDCOM, GraphML, hoặc JSON

## 🤝 Dự án cộng đồng

Dự án được xây dựng với tinh thần mở, khuyến khích mọi người đóng góp, sử dụng lại, hoặc mở rộng theo nhu cầu riêng. Tất cả các hàm đều được viết rõ ràng, dễ hiểu, và có thể tái sử dụng trong các hệ thống khác.

## 📄 Giấy phép
Dự án được phát hành dưới giấy phép MIT License – bạn có thể sử dụng, chỉnh sửa, và phân phối lại với điều kiện ghi rõ nguồn. 
## 📬 Liên hệ & đóng góp
- Email: ngtinh@gmail.com
- GitHub: https://github.com/tinhn/famrela4y

Bạn có thể fork, mở issue, hoặc tạo pull request để đóng góp vào dự án.
