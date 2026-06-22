# Phân tích & Khuyến nghị Ứng dụng AI Agent trong Khoa học Máy tính

Dự án trực quan hóa dữ liệu khảo sát ý kiến người lao động và đánh giá của chuyên gia về khả năng/mong muốn tự động hóa các tác vụ thuộc lĩnh vực Khoa học Máy tính (CS). Dự án phục vụ bài tập cá nhân (20% điểm số) môn học **Trực quan hóa dữ liệu**.

---

## 🚀 Tính năng nổi bật của dự án
1.  **Tiền xử lý dữ liệu chuẩn hóa (ETL)**: Lọc chuyên sâu nhóm ngành CS, tính toán chỉ số Tác động Kinh tế (ROI) thực tế của tự động hóa dựa trên lương và số lượng việc làm.
2.  **7 biểu đồ tương tác cao cấp (Plotly)**: 
    *   *Opportunity Gap*: Khả năng công nghệ vs. Mong muốn nhân viên (Scatter).
    *   *Skill Treemap*: Phân cấp nhóm kỹ năng cần hỗ trợ AI Agent.
    *   *Tug of War*: Giằng co giữa Động lực và Rào cản tự động hóa (Lưỡng cực).
    *   *LLM Substitution*: Tương quan Pearson giữa thói quen dùng LLM và mong muốn TĐH.
    *   *Perception vs Reality*: Thái độ chung về AI đối chiếu với đánh giá thực tế (Boxplot).
    *   *Complexity Violin*: Ảnh hưởng của độ phức tạp/chuyên môn sâu đến mong muốn TĐH.
    *   *ROI Prioritization*: Định giá quỹ lương bị ảnh hưởng để xếp thứ tự đầu tư (Bubble).
3.  **Web Dashboard tương tác (Streamlit)**: Giao diện hiện đại, phông chữ chuẩn Việt hóa, tích hợp bộ lọc Occupation động để cập nhật toàn bộ biểu đồ tức thì.

---

## 📁 Cấu trúc thư mục dự án
*   `eda.py`: Khám phá dữ liệu thô ban đầu trong terminal.
*   `preprocess.py`: Làm sạch, gộp dữ liệu và xuất các file sạch `cs_tasks_cleaned.csv`, `cs_workers_cleaned.csv`.
*   `visualize.py`: Script vẽ 7 biểu đồ tương tác Plotly và lưu thành các file HTML độc lập.
*   `app.py`: Giao diện ứng dụng Web Dashboard (Streamlit).
*   `report.md`: Báo cáo nháp bằng định dạng Markdown.
*   `requirements.txt`: Danh sách các thư viện Python phụ thuộc.
*   `.gitignore`: Tệp cấu hình loại trừ các file cache và file tạm thời khi tải lên GitHub.

---

## 🛠️ Hướng dẫn cài đặt và sử dụng

### Bước 1: Nhân bản kho lưu trữ (Clone repository)
```bash
git clone <URL_KHO_LƯU_TRỮ_GITHUB_CỦA_BẠN>
cd <TÊN_THƯ_MỤC_DỰ_ÁN>
```

### Bước 2: Cài đặt các thư viện yêu cầu
```bash
pip install -r requirements.txt
```

### Bước 3: Chạy quy trình tiền xử lý và phân tích
1.  **Chạy tiền xử lý dữ liệu**:
    ```bash
    python preprocess.py
    ```
2.  **Khởi chạy Web Dashboard tương tác (Streamlit)**:
    ```bash
    streamlit run app.py
    ```

---

## 🎓 Thành viên thực hiện
*   Họ và tên: VÕ THỊ THU THẢO
*   Môn học: Trực quan hóa dữ liệu
