"""
EDA Script: Khám phá Dữ liệu Tự động hóa ngành Khoa học Máy tính
Tệp tin này dùng để chạy trên VS Code để hiểu cấu trúc dữ liệu ban đầu.
"""

import pandas as pd
import os

def check_file(filename, path="."):
    filepath = os.path.join(path, filename)
    if not os.path.exists(filepath):
        # Dự phòng đường dẫn tuyệt đối nếu chạy ở thư mục khác
        filepath = os.path.join("d:/TQH", filename)
    
    print(f"\n==================================================")
    print(f"Báo cáo sơ bộ cho tệp tin: {filename}")
    print(f"==================================================")
    
    try:
        df = pd.read_csv(filepath)
        print(f"- Kích thước dữ liệu: {df.shape[0]} dòng, {df.shape[1]} cột")
        print("\n- Các cột dữ liệu và kiểu dữ liệu:")
        print(df.dtypes)
        
        null_counts = df.isnull().sum()
        if null_counts.sum() > 0:
            print("\n- Giá trị khuyết thiếu (Null/NaN) theo từng cột:")
            print(null_counts[null_counts > 0])
        else:
            print("\n- Không có giá trị khuyết thiếu.")
            
        print("\n- 2 dòng dữ liệu đầu tiên:")
        print(df.head(2))
        return df
    except Exception as e:
        print(f"Lỗi khi đọc file {filename}: {e}")
        return None

if __name__ == "__main__":
    print("Bắt đầu khám phá dữ liệu ban đầu...")
    
    # Đọc thử 4 file
    desires = check_file("domain_worker_desires.csv")
    metadata = check_file("domain_worker_metadata.csv")
    expert = check_file("expert_rated_technological_capability.csv")
    tasks = check_file("task_statement_with_metadata.csv")
    
    # Khảo sát riêng nhóm ngành CS
    if desires is not None:
        print("\n==================================================")
        print("PHÂN TÍCH NHÓM NGÀNH KHOA HỌC MÁY TÍNH (CS)")
        print("==================================================")
        occupations = desires['Occupation (O*NET-SOC Title)'].dropna().unique()
        
        # Tìm các ngành chứa từ khóa liên quan đến CS
        keywords = ['computer', 'programmer', 'software', 'network', 'information technology', 'systems analyst', 'web developer', 'database']
        cs_occupations = [occ for occ in occupations if any(keyword in occ.lower() for keyword in keywords)]
        
        print(f"Tổng số ngành nghề trong tập dữ liệu: {len(occupations)}")
        print(f"Phát hiện {len(cs_occupations)} ngành liên quan đến Khoa học Máy tính:")
        
        for occ in cs_occupations:
            tasks_count = desires[desires['Occupation (O*NET-SOC Title)'] == occ]['Task ID'].nunique()
            workers_count = desires[desires['Occupation (O*NET-SOC Title)'] == occ]['User ID'].nunique()
            print(f"  + {occ}:")
            print(f"    - Số lượng nhiệm vụ (Tasks): {tasks_count}")
            print(f"    - Số lượng người lao động (Workers): {workers_count}")
            
    print("\nHoàn thành bước EDA! Bạn có thể chạy tệp tin này bằng lệnh: `python eda.py` trong VS Code.")
