"""
Preprocessing Script: Tiền xử lý và gộp dữ liệu
Tệp tin này dùng để làm sạch, gộp dữ liệu và tính toán các chỉ số kinh tế phái sinh cho nhóm ngành CS.
"""

import pandas as pd
import numpy as np
import os

def preprocess_data(data_dir="d:/TQH"):
    print("Bắt đầu tiền xử lý dữ liệu...")
    
    # 1. Đọc dữ liệu
    try:
        desires = pd.read_csv(os.path.join(data_dir, "domain_worker_desires.csv"))
        metadata = pd.read_csv(os.path.join(data_dir, "domain_worker_metadata.csv"))
        expert = pd.read_csv(os.path.join(data_dir, "expert_rated_technological_capability.csv"))
        tasks = pd.read_csv(os.path.join(data_dir, "task_statement_with_metadata.csv"))
    except Exception as e:
        print(f"Lỗi đọc file: {e}. Thử đọc thư mục hiện tại...")
        desires = pd.read_csv("domain_worker_desires.csv")
        metadata = pd.read_csv("domain_worker_metadata.csv")
        expert = pd.read_csv("expert_rated_technological_capability.csv")
        tasks = pd.read_csv("task_statement_with_metadata.csv")

    # 2. Định nghĩa danh sách các ngành nghề Khoa học Máy tính (CS)
    cs_occupations = [
        "Computer Programmers",
        "Computer Systems Engineers/Architects",
        "Computer Network Support Specialists",
        "Computer User Support Specialists",
        "Computer and Information Systems Managers",
        "Information Technology Project Managers"
    ]
    
    print(f"Lọc dữ liệu cho {len(cs_occupations)} ngành nghề Khoa học Máy tính...")
    
    # Lọc desires và metadata theo nhóm ngành CS
    desires_cs = desires[desires["Occupation (O*NET-SOC Title)"].isin(cs_occupations)].copy()
    metadata_cs = metadata[metadata["Occupation (O*NET-SOC Title)"].isin(cs_occupations)].copy()
    
    print(f"- Số bản ghi mong muốn (Desires) thuộc CS: {desires_cs.shape[0]}")
    print(f"- Số lao động (Workers) thuộc CS: {metadata_cs.shape[0]}")

    # ==========================================
    # PHẦN A: TẠO DỮ LIỆU CẤP ĐỘ NHÂN SỰ (Worker-level)
    # ==========================================
    # Gộp desires và metadata theo User ID để phân tích đặc trưng cá nhân
    workers_merged = pd.merge(
        desires_cs,
        metadata_cs,
        on="User ID",
        how="inner",
        suffixes=("_desire", "_meta")
    )
    # Xử lý các cột trùng tên sau khi merge
    if "Occupation (O*NET-SOC Title)_desire" in workers_merged.columns:
        workers_merged.rename(columns={"Occupation (O*NET-SOC Title)_desire": "Occupation"}, inplace=True)
        if "Occupation (O*NET-SOC Title)_meta" in workers_merged.columns:
            workers_merged.drop(columns=["Occupation (O*NET-SOC Title)_meta"], inplace=True)
    
    # Lưu tệp nhân sự sạch
    workers_merged.to_csv("cs_workers_cleaned.csv", index=False)
    print(f"- Đã lưu file nhân sự sạch: cs_workers_cleaned.csv ({workers_merged.shape[0]} dòng)")

    # ==========================================
    # PHẦN B: TẠO DỮ LIỆU CẤP ĐỘ NHIỆM VỤ (Task-level)
    # ==========================================
    # 1. Tính toán giá trị mong muốn tự động hóa trung bình cho mỗi Task ID từ góc nhìn Worker
    # Lưu ý: Một Task có thể được đánh giá bởi nhiều Worker khác nhau, ta lấy trung bình
    task_desire_avg = desires_cs.groupby("Task ID").agg(
        Avg_Automation_Desire=("Automation Desire Rating", "mean"),
        Count_Worker_Ratings=("Automation Desire Rating", "count"),
        # Lấy trung bình các lý do mong muốn tự động hóa (True/False -> tỉ lệ)
        Reason_FreeTime=("Reasons for Automation Desire - Free Time", lambda x: x.astype(bool).mean()),
        Reason_Repetitive=("Reasons for Automation Desire - Repetitive", lambda x: x.astype(bool).mean()),
        Reason_HumanError=("Reasons for Automation Desire - Human Error", lambda x: x.astype(bool).mean()),
        Reason_Stress=("Reasons for Automation Desire - Stress", lambda x: x.astype(bool).mean()),
        Reason_Difficulty=("Reasons for Automation Desire - Difficulty", lambda x: x.astype(bool).mean()),
        Reason_Scale=("Reasons for Automation Desire - Scale", lambda x: x.astype(bool).mean()),
        # Lấy trung bình lý do muốn giữ quyền kiểm soát của con người
        Reason_Physical=("Reasons for Human Agency - Physical", lambda x: x.astype(bool).mean()),
        Reason_Control=("Reasons for Human Agency - Control", lambda x: x.astype(bool).mean()),
        Reason_DomainKnowledge=("Reasons for Human Agency - Domain Knowledge", lambda x: x.astype(bool).mean()),
        Reason_Empathy=("Reasons for Human Agency - Empathy", lambda x: x.astype(bool).mean()),
        Reason_QualityOversight=("Reasons for Human Agency - Quality Oversight", lambda x: x.astype(bool).mean()),
        Reason_Dynamic=("Reasons for Human Agency - Dynamic", lambda x: x.astype(bool).mean()),
        Reason_Ethical=("Reasons for Human Agency - Ethical", lambda x: x.astype(bool).mean())
    ).reset_index()

    # 2. Tính toán giá trị khả năng tự động hóa công nghệ từ chuyên gia
    task_expert_avg = expert.groupby("Task ID").agg(
        Avg_Automation_Capacity=("Automation Capacity Rating", "mean"),
        Avg_Expert_Physical=("Physical Action Requirement", "mean"),
        Avg_Expert_Uncertainty=("Involved Uncertainty", "mean"),
        Avg_Expert_DomainExp=("Domain Expertise Requirement", "mean"),
        Avg_Expert_Interpersonal=("Interpersonal Communication Requirement", "mean"),
        Avg_Expert_AgencyScale=("Human Agency Scale Rating", "mean")
    ).reset_index()

    # 3. Gộp tất cả thông tin vào bảng tasks
    # Lọc tasks thuộc CS (tránh lấy task ngành khác)
    tasks_cs = tasks[tasks["Occupation (O*NET-SOC Title)"].isin(cs_occupations)].copy()
    
    # Merge tuần tự
    tasks_merged = pd.merge(tasks_cs, task_desire_avg, on="Task ID", how="inner")
    tasks_merged = pd.merge(tasks_merged, task_expert_avg, on="Task ID", how="inner")
    
    # Clean cột lương và việc làm để tránh giá trị NaN
    tasks_merged["Occupation Mean Annual Wage"] = tasks_merged["Occupation Mean Annual Wage"].fillna(0)
    tasks_merged["Occupation Employment"] = tasks_merged["Occupation Employment"].fillna(0)

    # 4. Tính toán Chỉ số Tác động Kinh tế (ROI Score)
    # ROI Score = Quỹ lương năm của tác vụ chịu ảnh hưởng = Employment * Mean Annual Wage * (Desire / 5) * (Capacity / 5)
    # Chia cho 1,000,000 để có giá trị theo triệu USD
    tasks_merged["Economic_Impact_USD"] = (
        tasks_merged["Occupation Employment"] *
        tasks_merged["Occupation Mean Annual Wage"] *
        (tasks_merged["Avg_Automation_Desire"] / 5.0) *
        (tasks_merged["Avg_Automation_Capacity"] / 5.0)
    ).fillna(0)
    tasks_merged["Economic_Impact_Millions"] = (tasks_merged["Economic_Impact_USD"] / 1_000_000).fillna(0)
    
    # Lưu tệp nhiệm vụ sạch
    tasks_merged.to_csv("cs_tasks_cleaned.csv", index=False)
    print(f"- Đã lưu file nhiệm vụ sạch: cs_tasks_cleaned.csv ({tasks_merged.shape[0]} dòng)")
    print("Hoàn thành tiền xử lý dữ liệu thành công!")

if __name__ == "__main__":
    preprocess_data()
