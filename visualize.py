"""
Visualization Script: Vẽ 7 biểu đồ tương tác độc đáo bằng Plotly
Tệp tin này dùng để chạy trên VS Code để tạo ra các file HTML tương tác.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import ast
import os

def generate_visualizations(data_dir="."):
    print("Bắt đầu vẽ biểu đồ...")
    
    # Đọc dữ liệu sạch
    try:
        tasks_df = pd.read_csv("cs_tasks_cleaned.csv")
        workers_df = pd.read_csv("cs_workers_cleaned.csv")
        
        # Làm sạch dữ liệu phòng thủ chống lại các giá trị NaN phát sinh lỗi vẽ biểu đồ
        tasks_df["Economic_Impact_USD"] = tasks_df["Economic_Impact_USD"].fillna(0)
        tasks_df["Economic_Impact_Millions"] = tasks_df["Economic_Impact_Millions"].fillna(0).clip(lower=0)
        tasks_df["Occupation Mean Annual Wage"] = tasks_df["Occupation Mean Annual Wage"].fillna(0)
        tasks_df["Occupation Employment"] = tasks_df["Occupation Employment"].fillna(0)
    except Exception as e:
        print(f"Lỗi đọc dữ liệu sạch: {e}. Vui lòng chạy preprocess.py trước.")
        return

    # Định nghĩa bảng màu Sleek & Premium
    color_palette = px.colors.qualitative.G10 # Bảng màu tinh tế, hiện đại
    bg_template = "plotly_white"

    # =========================================================================
    # BIỂU ĐỒ 1: Bản đồ Cơ hội & Khoảng cách công nghệ (Opportunity Gap)
    # =========================================================================
    print("1/7: Vẽ biểu đồ Opportunity Gap...")
    fig1 = px.scatter(
        tasks_df,
        x="Avg_Automation_Capacity",
        y="Avg_Automation_Desire",
        color="Occupation (O*NET-SOC Title)",
        hover_data={"Task ID": True, "Avg_Automation_Capacity": ":.2f", "Avg_Automation_Desire": ":.2f"},
        hover_name="Task",
        title="Bản đồ Cơ hội AI Agent: Khả năng Công nghệ vs. Mong muốn của con người",
        labels={
            "Avg_Automation_Capacity": "Đánh giá Khả năng Công nghệ (Expert Capacity Rating)",
            "Avg_Automation_Desire": "Mong muốn Tự động hóa (Worker Desire Rating)",
            "Occupation (O*NET-SOC Title)": "Ngành nghề CS"
        },
        color_discrete_sequence=color_palette,
        template=bg_template
    )
    # Thêm đường phân vùng (Quadrants) tại X=3 và Y=3
    fig1.add_shape(type="line", x0=3, y0=1, x1=3, y1=5, line=dict(color="red", width=1.5, dash="dash"))
    fig1.add_shape(type="line", x0=1, y0=3, x1=5, y1=3, line=dict(color="red", width=1.5, dash="dash"))
    # Thêm text chú thích cho các phân vùng
    fig1.add_annotation(x=4.2, y=4.5, text="Low-Hanging Fruits (Ưu tiên số 1)", showarrow=False, font=dict(color="green", size=11))
    fig1.add_annotation(x=1.8, y=4.5, text="Opportunity Gaps (Đầu tư R&D)", showarrow=False, font=dict(color="blue", size=11))
    fig1.add_annotation(x=4.2, y=1.5, text="Potential Resistance (Thận trọng)", showarrow=False, font=dict(color="orange", size=11))
    fig1.add_annotation(x=1.8, y=1.5, text="Human-Centric Core (Giữ nguyên)", showarrow=False, font=dict(color="gray", size=11))
    fig1.update_layout(
        xaxis=dict(range=[0.8, 5.2]),
        yaxis=dict(range=[0.8, 5.2]),
        legend=dict(yanchor="top", y=-0.2, xanchor="left", x=0, orientation="h")
    )
    fig1.write_html("1_opportunity_gap.html")


    # =========================================================================
    # BIỂU ĐỒ 2: Bản đồ Phân cấp Kỹ năng tổng quát (Skill-Hierarchy Treemap)
    # =========================================================================
    print("2/7: Vẽ biểu đồ Skill Treemap...")
    # Phân tách và giải nén cột Skill (dạng string list)
    skills_expanded = []
    for idx, row in tasks_df.iterrows():
        try:
            skill_list = ast.literal_eval(row["Skill (O*NET Work Activity)"])
        except:
            # Dự phòng nếu không parse được
            skill_str = row["Skill (O*NET Work Activity)"]
            if isinstance(skill_str, str):
                skill_list = [s.strip().replace("'", "").replace("[", "").replace("]", "") for s in skill_str.split(",")]
            else:
                skill_list = []
        
        for sk in skill_list:
            if sk:
                skills_expanded.append({
                    "Skill": sk,
                    "Occupation": row["Occupation (O*NET-SOC Title)"],
                    "Avg_Automation_Desire": row["Avg_Automation_Desire"],
                    "Task ID": row["Task ID"]
                })
    
    skills_df = pd.DataFrame(skills_expanded)
    # Group by Skill và Occupation để vẽ Treemap
    skills_grouped = skills_df.groupby(["Skill", "Occupation"]).agg(
        Count_Tasks=("Task ID", "count"),
        Avg_Desire=("Avg_Automation_Desire", "mean")
    ).reset_index()
    
    fig2 = px.treemap(
        skills_grouped,
        path=["Skill", "Occupation"],
        values="Count_Tasks",
        color="Avg_Desire",
        color_continuous_scale="RdYlBu_r", # Đỏ là mong muốn cao, Xanh là thấp
        title="Bản đồ Kỹ năng CS: Nhóm hoạt động nào cần AI Agent hỗ trợ nhiều nhất?",
        labels={
            "Count_Tasks": "Số lượng Nhiệm vụ",
            "Avg_Desire": "Mong muốn tự động hóa trung bình",
            "labels": "Nhóm Kỹ năng / Ngành nghề"
        },
        template=bg_template
    )
    fig2.write_html("2_skill_hierarchy.html")


    # =========================================================================
    # BIỂU ĐỒ 3: Giằng co giữa Động lực và Rào cản (Drivers vs. Barriers)
    # =========================================================================
    print("3/7: Vẽ biểu đồ Drivers vs Barriers...")
    # Lấy trung bình toàn bộ lý do của tất cả các Task CS
    drivers_cols = [
        "Reason_FreeTime", "Reason_Repetitive", "Reason_HumanError", 
        "Reason_Stress", "Reason_Difficulty", "Reason_Scale"
    ]
    barriers_cols = [
        "Reason_Physical", "Reason_Control", "Reason_DomainKnowledge", 
        "Reason_Empathy", "Reason_QualityOversight", "Reason_Dynamic", "Reason_Ethical"
    ]
    
    drivers_mean = tasks_df[drivers_cols].mean()
    barriers_mean = tasks_df[barriers_cols].mean()
    
    # Định dạng lại tên hiển thị
    drivers_labels = [c.replace("Reason_", "Tự động hóa để: ") for c in drivers_cols]
    barriers_labels = [c.replace("Reason_", "Giữ kiểm soát vì: ") for c in barriers_cols]
    
    # Biểu đồ cột ngang lưỡng cực (Tug of War)
    fig3 = go.Figure()
    # Add Drivers (cột dương bên phải)
    fig3.add_trace(go.Bar(
        y=drivers_labels,
        x=drivers_mean.values,
        name="Động lực Tự động hóa",
        orientation='h',
        marker=dict(color='#10B981'),
    ))
    # Add Barriers (cột âm bên trái để thể hiện sự đối nghịch)
    fig3.add_trace(go.Bar(
        y=barriers_labels,
        x=-barriers_mean.values,
        name="Rào cản / Muốn giữ quyền kiểm soát",
        orientation='h',
        marker=dict(color='#E11D48'),
    ))
    
    fig3.update_layout(
        title="Trận chiến Giằng co (Tug of War): Động lực vs Rào cản áp dụng AI Agent",
        xaxis=dict(
            title="Tỉ lệ phản hồi đồng ý (Trái: Rào cản | Phải: Động lực)",
            tickvals=[-1.0, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1.0],
            ticktext=["100%", "75%", "50%", "25%", "0%", "25%", "50%", "75%", "100%"]
        ),
        yaxis=dict(autorange="reversed"),
        barmode='overlay',
        template=bg_template
    )
    fig3.write_html("3_tug_of_war.html")


    # =========================================================================
    # BIỂU ĐỒ 4: Hồ sơ sử dụng LLM & Mong muốn tự động hóa (LLM Substitution Heatmap)
    # =========================================================================
    print("4/7: Vẽ biểu đồ LLM Usage correlation heatmap...")
    # Lấy các cột sử dụng LLM
    llm_cols = [
        "LLM Usage by Type - Information Access",
        "LLM Usage by Type - Edit",
        "LLM Usage by Type - Idea Generation",
        "LLM Usage by Type - Communication",
        "LLM Usage by Type - Analysis",
        "LLM Usage by Type - Decision",
        "LLM Usage by Type - Coding",
        "LLM Usage by Type - System Design",
        "LLM Usage by Type - Data Processing"
    ]
    
    # Chuyển đổi mức độ sử dụng thành điểm số để tính tương quan
    # "Daily" -> 4, "Weekly" -> 3, "Monthly" -> 2, "Never" -> 1 (hoặc NaN thành 1)
    freq_map = {"Daily": 4, "Weekly": 3, "Monthly": 2, "Never": 1}
    temp_df = workers_df[llm_cols + ["Automation Desire Rating"]].copy()
    for col in llm_cols:
        temp_df[col] = temp_df[col].map(freq_map).fillna(1)
        
    # Tính tương quan Pearson
    corr_matrix = temp_df.corr(method="pearson")
    # Lấy riêng tương quan của các kỹ năng LLM với mong muốn tự động hóa
    desire_corr = corr_matrix[["Automation Desire Rating"]].drop("Automation Desire Rating").sort_values(by="Automation Desire Rating", ascending=False)
    
    # Vẽ biểu đồ tương quan
    fig4 = px.bar(
        desire_corr,
        x="Automation Desire Rating",
        y=desire_corr.index,
        orientation="h",
        title="Mức độ tương quan: Kỹ năng sử dụng LLM nào kích thích mong muốn tự động hóa nhất?",
        labels={
            "Automation Desire Rating": "Hệ số Tương quan Pearson (r)",
            "y": "Kỹ năng sử dụng LLM hàng ngày"
        },
        color="Automation Desire Rating",
        color_continuous_scale="Blues",
        template=bg_template
    )
    fig4.update_layout(yaxis=dict(autorange="reversed"))
    fig4.write_html("4_llm_substitution.html")


    # =========================================================================
    # BIỂU ĐỒ 5: Nhận thức chung về AI vs. Mong muốn thực tế (Perception vs Reality)
    # =========================================================================
    print("5/7: Vẽ biểu đồ Perception vs Reality...")
    # Loại bỏ các dòng khuyết thái độ về công việc AI
    workers_attitude = workers_df.dropna(subset=["AI Tedious Work Attitude"])
    
    # Thống kê phân phối mong muốn tự động hóa theo từng thái độ
    fig5 = px.box(
        workers_attitude,
        x="AI Tedious Work Attitude",
        y="Automation Desire Rating",
        color="AI Tedious Work Attitude",
        title="Nhận thức vs. Thực tế: Thái độ chung về AI có tương đồng với Mong muốn Tự động hóa thực tế?",
        labels={
            "AI Tedious Work Attitude": "Mức độ đồng ý: 'AI có thể xử lý các công việc tẻ nhạt'",
            "Automation Desire Rating": "Mong muốn Tự động hóa tác vụ cụ thể (1-5)"
        },
        category_orders={
            "AI Tedious Work Attitude": ["Strongly agree", "Somewhat agree", "Neither agree nor disagree", "Somewhat disagree", "Strongly disagree"]
        },
        template=bg_template
    )
    fig5.write_html("5_perception_reality.html")


    # =========================================================================
    # BIỂU ĐỒ 6: Tác động của độ phức tạp tác vụ lên Mong muốn (Complexity Violin Plots)
    # =========================================================================
    print("6/7: Vẽ biểu đồ Complexity Violin...")
    # Làm tròn điểm đánh giá chuyên gia về độ phức tạp để phân loại
    tasks_df["Domain_Expertise_Category"] = tasks_df["Avg_Expert_DomainExp"].round().astype(int)
    
    fig6 = px.violin(
        tasks_df,
        x="Domain_Expertise_Category",
        y="Avg_Automation_Desire",
        color="Occupation (O*NET-SOC Title)",
        box=True, # Hiển thị cả box plot bên trong violin
        points="all", # Hiển thị tất cả điểm dữ liệu
        title="Tác động của yêu cầu kiến thức chuyên môn (Domain Expertise) lên Mong muốn tự động hóa",
        labels={
            "Domain_Expertise_Category": "Yêu cầu Kiến thức chuyên sâu (1: Rất thấp -> 5: Rất cao)",
            "Avg_Automation_Desire": "Mong muốn Tự động hóa trung bình",
            "Occupation (O*NET-SOC Title)": "Ngành nghề CS"
        },
        color_discrete_sequence=color_palette,
        template=bg_template
    )
    fig6.update_layout(
        legend=dict(yanchor="top", y=-0.25, xanchor="left", x=0, orientation="h"),
        legend_title_text='',
        margin=dict(b=100)
    )
    fig6.write_html("6_complexity_violin.html")


    # =========================================================================
    # BIỂU ĐỒ 7: Bản đồ nhiệt kinh tế & mức độ ưu tiên đầu tư (ROI Bubble Chart)
    # =========================================================================
    print("7/7: Vẽ biểu đồ ROI Bubble Chart...")
    fig7 = px.scatter(
        tasks_df,
        x="Avg_Automation_Desire",
        y="Avg_Automation_Capacity",
        size="Economic_Impact_Millions",
        color="Occupation (O*NET-SOC Title)",
        hover_name="Task",
        hover_data={
            "Task ID": True,
            "Economic_Impact_Millions": ":.2f",
            "Occupation Mean Annual Wage": ":,.0f",
            "Occupation Employment": ":,.0f"
        },
        size_max=60, # Tăng kích thước tối đa của bong bóng để nổi bật
        title="Bản đồ Ưu tiên Đầu tư AI Agent dựa trên Tác động Kinh tế (ROI)",
        labels={
            "Avg_Automation_Desire": "Mong muốn Tự động hóa trung bình (Worker)",
            "Avg_Automation_Capacity": "Khả năng Tự động hóa trung bình (Expert)",
            "Economic_Impact_Millions": "Quỹ lương tác động tiềm năng (Triệu USD)",
            "Occupation (O*NET-SOC Title)": "Ngành nghề CS"
        },
        color_discrete_sequence=color_palette,
        template=bg_template
    )
    fig7.update_layout(
        xaxis=dict(range=[0.8, 5.2]),
        yaxis=dict(range=[0.8, 5.2]),
        legend=dict(yanchor="top", y=-0.2, xanchor="left", x=0, orientation="h")
    )
    fig7.write_html("7_roi_prioritization.html")
    
    print("\n Đã vẽ xong 7 biểu đồ tương tác và lưu thành công dưới dạng HTML:")
    print(" - 1_opportunity_gap.html")
    print(" - 2_skill_hierarchy.html")
    print(" - 3_tug_of_war.html")
    print(" - 4_llm_substitution.html")
    print(" - 5_perception_reality.html")
    print(" - 6_complexity_violin.html")
    print(" - 7_roi_prioritization.html")

if __name__ == "__main__":
    generate_visualizations()
