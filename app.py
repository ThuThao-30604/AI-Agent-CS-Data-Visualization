"""
Streamlit Application: Dashboard Trực quan hóa ứng dụng AI Agent trong Khoa học máy tính
Chạy ứng dụng bằng lệnh: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import ast

# 1. Cấu hình trang tối ưu cho giao diện rộng (Wide mode) và Premium Look
st.set_page_config(
    page_title="AI Agent in CS - Analysis Dashboard",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS để tối ưu hóa thẩm mỹ (Typography, Gradient, Cards, Borders)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Be+Vietnam+Pro:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: "Be Vietnam Pro", system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    .main-title {
        font-family: "Be Vietnam Pro", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
        background: linear-gradient(135deg, #FF0080 0%, #7928CA 50%, #00DFD8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.8rem;
        line-height: 1.3;
        margin-bottom: 0.5rem;
    }
    
    .section-header {
        font-family: "Be Vietnam Pro", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
        color: #1E293B;
        font-weight: 600;
        font-size: 1.8rem;
        border-left: 5px solid #FF0080;
        padding-left: 10px;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: #CBD5E1;
    }
    
    .custom-alert {
        background-color: #EFF6FF;
        border-left: 4px solid #3B82F6;
        color: #1E40AF;
        padding: 15px;
        border-radius: 8px;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Đọc dữ liệu sạch
@st.cache_data
def load_data():
    try:
        tasks = pd.read_csv("cs_tasks_cleaned.csv")
        workers = pd.read_csv("cs_workers_cleaned.csv")
    except:
        # Dự phòng nếu file nằm ở thư mục tuyệt đối
        tasks = pd.read_csv("d:/TQH/cs_tasks_cleaned.csv")
        workers = pd.read_csv("d:/TQH/cs_workers_cleaned.csv")
        
    # Làm sạch dữ liệu chống lỗi NaN vẽ biểu đồ
    tasks["Economic_Impact_USD"] = tasks["Economic_Impact_USD"].fillna(0)
    tasks["Economic_Impact_Millions"] = tasks["Economic_Impact_Millions"].fillna(0).clip(lower=0)
    tasks["Occupation Mean Annual Wage"] = tasks["Occupation Mean Annual Wage"].fillna(0)
    tasks["Occupation Employment"] = tasks["Occupation Employment"].fillna(0)
    
    return tasks, workers

tasks_raw, workers_raw = load_data()

# =========================================================================
# THANH BỘ LỌC BÊN TRÁI (SIDEBAR FILTERS)
# =========================================================================
st.sidebar.image("https://img.icons8.com/clouds/200/code.png", width=120)
st.sidebar.markdown("### 🔍 Bộ lọc Dữ liệu")

# Lựa chọn vị trí công việc (Occupation Filter)
all_occupations = list(tasks_raw["Occupation (O*NET-SOC Title)"].unique())
selected_occupation = st.sidebar.selectbox(
    "Chọn Vị trí Công việc:",
    options=["Tất cả ngành CS"] + all_occupations
)

# Lọc dữ liệu dựa trên lựa chọn của người dùng
if selected_occupation == "Tất cả ngành CS":
    tasks_df = tasks_raw.copy()
    workers_df = workers_raw.copy()
else:
    tasks_df = tasks_raw[tasks_raw["Occupation (O*NET-SOC Title)"] == selected_occupation].copy()
    workers_df = workers_raw[workers_raw["Occupation"] == selected_occupation].copy()

# Thông tin tác giả sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 🎓 Thông tin dự án")
st.sidebar.markdown("**Môn học**: Trực quan hóa dữ liệu")
st.sidebar.markdown("**Chủ đề**: Phân tích ứng dụng AI Agent trong Khoa học máy tính")
st.sidebar.markdown("**Công cụ**: Python, Streamlit, Plotly")

# =========================================================================
# PHẦN THÂN TRANG (MAIN CONTENT)
# =========================================================================
st.markdown('<div class="main-title">Phân tích & Khuyến nghị ứng dụng AI Agent trong Khoa học Máy tính</div>', unsafe_allow_html=True)
st.markdown("Dashboard tương tác phân tích khoảng cách công nghệ, nhu cầu nhân sự và cơ hội kinh tế để thiết kế AI Agent tối ưu cho nhóm ngành CS.")

# 4 chỉ số KPI tổng quan (Metrices Row)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
        <div class="metric-card">
            <span style="color: #64748B; font-size: 0.85rem; font-weight: 600; text-transform: uppercase;">Số nhiệm vụ CS</span>
            <h2 style="color: #1E293B; margin: 5px 0 0 0; font-family: 'Be Vietnam Pro'; font-size: 2rem;">{tasks_df['Task ID'].nunique()}</h2>
        </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
        <div class="metric-card">
            <span style="color: #64748B; font-size: 0.85rem; font-weight: 600; text-transform: uppercase;">Số lao động phản hồi</span>
            <h2 style="color: #1E293B; margin: 5px 0 0 0; font-family: 'Be Vietnam Pro'; font-size: 2rem;">{workers_df['User ID'].nunique()}</h2>
        </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
        <div class="metric-card">
            <span style="color: #64748B; font-size: 0.85rem; font-weight: 600; text-transform: uppercase;">Mong muốn TĐH TB</span>
            <h2 style="color: #10B981; margin: 5px 0 0 0; font-family: 'Be Vietnam Pro'; font-size: 2rem;">{tasks_df['Avg_Automation_Desire'].mean():.2f}/5.0</h2>
        </div>
    """, unsafe_allow_html=True)
with col4:
    total_roi = tasks_df["Economic_Impact_Millions"].sum()
    st.markdown(f"""
        <div class="metric-card">
            <span style="color: #64748B; font-size: 0.85rem; font-weight: 600; text-transform: uppercase;">Quỹ lương tác động</span>
            <h2 style="color: #3B82F6; margin: 5px 0 0 0; font-family: 'Be Vietnam Pro'; font-size: 2rem;">${total_roi:,.1f} Tr USD</h2>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 4 Trang chuyển đổi (Tabs)
tab_overview, tab_opp_skills, tab_behavior, tab_roi = st.tabs([
    "🏠 Giới thiệu chung",
    "🎯 Cơ hội & Kỹ năng",
    "🧬 Hành vi & Sử dụng LLM",
    "💰 Định giá Kinh tế & Khuyến nghị"
])

# =========================================================================
# TAB 1: GIỚI THIỆU CHUNG (OVERVIEW)
# =========================================================================
with tab_overview:
    st.markdown('<div class="section-header">Giới thiệu Dự án</div>', unsafe_allow_html=True)
    col_intro_l, col_intro_r = st.columns([2, 1])
    with col_intro_l:
        st.write("""
            Dự án này phân tích khả năng tự động hóa và mong muốn của kỹ sư công nghệ đối với các tác vụ cụ thể trong lĩnh vực Khoa học Máy tính.
            Từ đó chỉ ra các "điểm nghẽn" và cơ hội để phát triển các thế hệ **AI Agent** (Tác nhân AI thông minh) giúp nâng cao năng suất lao động và mang lại lợi ích tài chính lớn nhất.
            
            Dữ liệu được tích hợp từ **O*NET** (Cơ sở dữ liệu nghề nghiệp của Bộ Lao động Mỹ) kết hợp với đánh giá thực tế của lập trình viên và các chuyên gia công nghệ AI hàng đầu.
        """)
        st.markdown("""
            <div class="custom-alert">
                💡 <b>Hướng dẫn sử dụng Dashboard:</b> Bạn có thể chọn lọc dữ liệu theo từng ngành nghề cụ thể (ví dụ: <i>Computer Programmers</i> hoặc <i>Information Technology Project Managers</i>) ở thanh bên trái. Toàn bộ biểu đồ và báo cáo phân tích sẽ tự động cập nhật tương ứng!
            </div>
        """, unsafe_allow_html=True)
    with col_intro_r:
        st.image("https://img.icons8.com/clouds/200/services.png", width=150)
        
    st.markdown('<div class="section-header">Mô tả tệp dữ liệu gốc</div>', unsafe_allow_html=True)
    col_desc_1, col_desc_2 = st.columns(2)
    with col_desc_1:
        st.markdown("""
            *   **domain_worker_desires.csv**: Phản hồi của người lao động ngành CS về mong muốn tự động hóa tác vụ.
            *   **domain_worker_metadata.csv**: Thông tin nhân khẩu học và thói quen sử dụng LLM của kỹ sư.
        """)
    with col_desc_2:
        st.markdown("""
            *   **expert_rated_technological_capability.csv**: Đánh giá khả năng tự động hóa của chuyên gia AI.
            *   **task_statement_with_metadata.csv**: Thống kê về mức lương, quy mô lao động và phân nhóm kỹ năng O*NET.
        """)

# =========================================================================
# TAB 2: CƠ HỘI & KỸ NĂNG (OPPORTUNITIES & SKILLS)
# =========================================================================
with tab_opp_skills:
    bg_template = "plotly_white"
    color_palette = px.colors.qualitative.G10
    
    # 2.1 Opportunity Gap Chart
    st.markdown('<div class="section-header">1. Bản đồ Cơ hội & Khoảng cách công nghệ (Opportunity Gap)</div>', unsafe_allow_html=True)
    st.write("So sánh Khả năng Công nghệ của chuyên gia (Trục X) vs. Mong muốn của Lập trình viên (Trục Y) giúp định vị các nhóm tác vụ ưu tiên.")
    
    fig1 = px.scatter(
        tasks_df,
        x="Avg_Automation_Capacity",
        y="Avg_Automation_Desire",
        color="Occupation (O*NET-SOC Title)",
        hover_data={"Task ID": True, "Avg_Automation_Capacity": ":.2f", "Avg_Automation_Desire": ":.2f"},
        hover_name="Task",
        labels={
            "Avg_Automation_Capacity": "Đánh giá Khả năng Công nghệ (Expert Capacity)",
            "Avg_Automation_Desire": "Mong muốn Tự động hóa (Worker Desire)",
            "Occupation (O*NET-SOC Title)": "Ngành nghề CS"
        },
        color_discrete_sequence=color_palette,
        template=bg_template
    )
    fig1.add_shape(type="line", x0=3, y0=1, x1=3, y1=5, line=dict(color="red", width=1.5, dash="dash"))
    fig1.add_shape(type="line", x0=1, y0=3, x1=5, y1=3, line=dict(color="red", width=1.5, dash="dash"))
    fig1.add_annotation(x=4.2, y=4.5, text="Low-Hanging Fruits (Ưu tiên số 1)", showarrow=False, font=dict(color="green", size=12))
    fig1.add_annotation(x=1.8, y=4.5, text="Opportunity Gaps (Đầu tư R&D)", showarrow=False, font=dict(color="blue", size=12))
    fig1.add_annotation(x=4.2, y=1.5, text="Potential Resistance (Thận trọng)", showarrow=False, font=dict(color="orange", size=12))
    fig1.add_annotation(x=1.8, y=1.5, text="Human-Centric Core (Giữ nguyên)", showarrow=False, font=dict(color="gray", size=12))
    fig1.update_layout(xaxis=dict(range=[0.8, 5.2]), yaxis=dict(range=[0.8, 5.2]))
    st.plotly_chart(fig1, use_container_width=True)
    
    # 2.2 Skill Treemap & Complexity Violin Plot
    st.markdown('<div class="section-header">2. Phân tích Phân cấp Kỹ năng & Độ phức tạp tác vụ</div>', unsafe_allow_html=True)
    col_skill, col_violin = st.columns(2)
    
    with col_skill:
        st.markdown("#### Bản đồ Kỹ năng cần AI Agent hỗ trợ")
        # Phân tách và giải nén cột Skill (dạng string list)
        skills_expanded = []
        for idx, row in tasks_df.iterrows():
            try:
                skill_list = ast.literal_eval(row["Skill (O*NET Work Activity)"])
            except:
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
        
        if skills_expanded:
            skills_df = pd.DataFrame(skills_expanded)
            skills_grouped = skills_df.groupby(["Skill", "Occupation"]).agg(
                Count_Tasks=("Task ID", "count"),
                Avg_Desire=("Avg_Automation_Desire", "mean")
            ).reset_index()
            
            fig2 = px.treemap(
                skills_grouped,
                path=["Skill", "Occupation"],
                values="Count_Tasks",
                color="Avg_Desire",
                color_continuous_scale="RdYlBu_r",
                labels={"Count_Tasks": "Số lượng tác vụ", "Avg_Desire": "Mong muốn TĐH TB"},
                template=bg_template
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.write("Không đủ dữ liệu kỹ năng.")
            
    with col_violin:
        st.markdown("#### Yêu cầu Chuyên môn vs. Mong muốn Tự động hóa")
        tasks_df["Domain_Expertise_Category"] = tasks_df["Avg_Expert_DomainExp"].round().astype(int)
        fig6 = px.violin(
            tasks_df,
            x="Domain_Expertise_Category",
            y="Avg_Automation_Desire",
            color="Occupation (O*NET-SOC Title)",
            box=True,
            points="all",
            labels={
                "Domain_Expertise_Category": "Mức độ yêu cầu Chuyên môn sâu (1: Thấp -> 5: Cao)",
                "Avg_Automation_Desire": "Mong muốn tự động hóa"
            },
            color_discrete_sequence=color_palette,
            template=bg_template
        )
        fig6.update_layout(
            legend=dict(yanchor="top", y=-0.25, xanchor="left", x=0, orientation="h"),
            legend_title_text='',
            margin=dict(b=100)
        )
        st.plotly_chart(fig6, use_container_width=True)

# =========================================================================
# TAB 3: HÀNH VI & SỬ DỤNG LLM (BEHAVIOR & LLMS)
# =========================================================================
with tab_behavior:
    # 3.1 Tug of War (Drivers vs Barriers)
    st.markdown('<div class="section-header">3. Sự giằng co giữa Động lực và Rào cản (Drivers vs. Barriers)</div>', unsafe_allow_html=True)
    st.write("Tại sao lập trình viên muốn tự động hóa, và tại sao họ lại lo lắng giữ quyền kiểm soát?")
    
    drivers_cols = ["Reason_FreeTime", "Reason_Repetitive", "Reason_HumanError", "Reason_Stress", "Reason_Difficulty", "Reason_Scale"]
    barriers_cols = ["Reason_Physical", "Reason_Control", "Reason_DomainKnowledge", "Reason_Empathy", "Reason_QualityOversight", "Reason_Dynamic", "Reason_Ethical"]
    
    drivers_mean = tasks_df[drivers_cols].mean()
    barriers_mean = tasks_df[barriers_cols].mean()
    
    drivers_labels = [c.replace("Reason_", "Tự động hóa để: ") for c in drivers_cols]
    barriers_labels = [c.replace("Reason_", "Giữ kiểm soát vì: ") for c in barriers_cols]
    
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        y=drivers_labels,
        x=drivers_mean.values,
        name="Động lực Tự động hóa",
        orientation='h',
        marker=dict(color='#10B981'),
    ))
    fig3.add_trace(go.Bar(
        y=barriers_labels,
        x=-barriers_mean.values,
        name="Rào cản / Muốn giữ quyền kiểm soát",
        orientation='h',
        marker=dict(color='#E11D48'),
    ))
    fig3.update_layout(
        xaxis=dict(
            title="Tỉ lệ phản hồi đồng ý (Trái: Rào cản | Phải: Động lực)",
            tickvals=[-1.0, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1.0],
            ticktext=["100%", "75%", "50%", "25%", "0%", "25%", "50%", "75%", "100%"]
        ),
        yaxis=dict(autorange="reversed"),
        barmode='overlay',
        template=bg_template
    )
    st.plotly_chart(fig3, use_container_width=True)

    # 3.2 LLM Correlation vs. Perception Reality
    st.markdown('<div class="section-header">4. Hồ sơ sử dụng LLM & Thái độ nhận thức về AI</div>', unsafe_allow_html=True)
    col_llm, col_attitude = st.columns(2)
    
    with col_llm:
        st.markdown("#### Kỹ năng sử dụng LLM hàng ngày thúc đẩy Mong muốn tự động hóa")
        llm_cols = [
            "LLM Usage by Type - Information Access", "LLM Usage by Type - Edit",
            "LLM Usage by Type - Idea Generation", "LLM Usage by Type - Communication",
            "LLM Usage by Type - Analysis", "LLM Usage by Type - Decision",
            "LLM Usage by Type - Coding", "LLM Usage by Type - System Design",
            "LLM Usage by Type - Data Processing"
        ]
        
        freq_map = {"Daily": 4, "Weekly": 3, "Monthly": 2, "Never": 1}
        temp_df = workers_df[llm_cols + ["Automation Desire Rating"]].copy()
        for col in llm_cols:
            temp_df[col] = temp_df[col].map(freq_map).fillna(1)
            
        corr_matrix = temp_df.corr(method="pearson")
        # Handle cases where standard deviation is zero (returns NaN)
        desire_corr = corr_matrix[["Automation Desire Rating"]].drop("Automation Desire Rating").fillna(0).sort_values(by="Automation Desire Rating", ascending=False)
        
        fig4 = px.bar(
            desire_corr,
            x="Automation Desire Rating",
            y=desire_corr.index,
            orientation="h",
            labels={"Automation Desire Rating": "Hệ số tương quan (r)", "y": "Kỹ năng dùng LLM"},
            color="Automation Desire Rating",
            color_continuous_scale="Blues",
            template=bg_template
        )
        fig4.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig4, use_container_width=True)
        
    with col_attitude:
        st.markdown("#### Nhận thức về việc AI xử lý việc tẻ nhạt vs. Mong muốn thực tế")
        workers_attitude = workers_df.dropna(subset=["AI Tedious Work Attitude"])
        if not workers_attitude.empty:
            fig5 = px.box(
                workers_attitude,
                x="AI Tedious Work Attitude",
                y="Automation Desire Rating",
                color="AI Tedious Work Attitude",
                category_orders={
                    "AI Tedious Work Attitude": ["Strongly agree", "Somewhat agree", "Neither agree nor disagree", "Somewhat disagree", "Strongly disagree"]
                },
                labels={"AI Tedious Work Attitude": "Nhận thức", "Automation Desire Rating": "Mong muốn tác vụ cụ thể"},
                template=bg_template
            )
            fig5.update_layout(showlegend=False)
            st.plotly_chart(fig5, use_container_width=True)
        else:
            st.write("Không đủ dữ liệu khảo sát thái độ.")

# =========================================================================
# TAB 4: ĐỊNH GIÁ KINH TẾ & KHUYẾN NGHỊ (ROI & RECOMMENDATIONS)
# =========================================================================
with tab_roi:
    # 4.1 ROI Bubble Chart
    st.markdown('<div class="section-header">5. Bản đồ Ưu tiên Đầu tư AI Agent dựa trên ROI</div>', unsafe_allow_html=True)
    st.write("Biểu đồ bong bóng thể hiện tiềm năng tài chính của tự động hóa. Bong bóng càng lớn đại diện cho quỹ lương tác động khi triển khai AI Agent càng cao.")
    
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
        size_max=60,
        labels={
            "Avg_Automation_Desire": "Mong muốn TĐH TB (Worker)",
            "Avg_Automation_Capacity": "Khả năng TĐH TB (Expert)",
            "Economic_Impact_Millions": "Quỹ lương tác động (Triệu USD)",
            "Occupation (O*NET-SOC Title)": "Ngành nghề CS"
        },
        color_discrete_sequence=color_palette,
        template=bg_template
    )
    fig7.update_layout(
        xaxis=dict(range=[0.8, 5.2]),
        yaxis=dict(range=[0.8, 5.2])
    )
    st.plotly_chart(fig7, use_container_width=True)

    # 4.2 Recommendations Section
    st.markdown('<div class="section-header">6. Lộ trình Khuyến nghị Xây dựng AI Agent</div>', unsafe_allow_html=True)
    
    col_rec1, col_rec2, col_rec3 = st.columns(3)
    with col_rec1:
        st.markdown("""
            <div style="background-color: #F0FDF4; border: 1px solid #BBF7D0; padding: 20px; border-radius: 12px; height: 100%;">
                <h4 style="color: #166534; font-family: 'Be Vietnam Pro'; margin-top:0;">🚀 Ngắn hạn (Lập trình Co-pilot)</h4>
                <p style="font-size: 0.9rem; color: #1F2937;">Tập trung tự động hóa các tác vụ lặp đi lặp lại có mong muốn cao.</p>
                <ul style="font-size: 0.85rem; color: #4B5563; padding-left: 15px;">
                    <li><b>Unit Test Agent:</b> Sinh mã kiểm thử tự động.</li>
                    <li><b>Documentation Agent:</b> Tự viết tài liệu từ code nguồn.</li>
                </ul>
                <span style="font-size: 0.8rem; color: #166534; font-weight:bold;">Động lực: Tránh lặp việc & giảm lỗi.</span>
            </div>
        """, unsafe_allow_html=True)
        
    with col_rec2:
        st.markdown("""
            <div style="background-color: #EFF6FF; border: 1px solid #BFDBFE; padding: 20px; border-radius: 12px; height: 100%;">
                <h4 style="color: #1E40AF; font-family: 'Be Vietnam Pro'; margin-top:0;">📊 Trung hạn (DevOps & SysOps)</h4>
                <p style="font-size: 0.9rem; color: #1F2937;">Ứng dụng cho nhóm tác vụ hạ tầng và hệ thống lớn để đem lại ROI cao nhất.</p>
                <ul style="font-size: 0.85rem; color: #4B5563; padding-left: 15px;">
                    <li><b>Log Monitoring Agent:</b> Giám sát hệ thống và đề xuất sửa lỗi tự động.</li>
                    <li><b>IaC Config Agent:</b> Tạo cấu hình hạ tầng đám mây an toàn.</li>
                </ul>
                <span style="font-size: 0.8rem; color: #1E40AF; font-weight:bold;">Động lực: Quỹ lương chịu tác động lớn.</span>
            </div>
        """, unsafe_allow_html=True)
        
    with col_rec3:
        st.markdown("""
            <div style="background-color: #FFF7ED; border: 1px solid #FED7AA; padding: 20px; border-radius: 12px; height: 100%;">
                <h4 style="color: #9A3412; font-family: 'Be Vietnam Pro'; margin-top:0;">🛡️ Dài hạn (Project Co-pilot)</h4>
                <p style="font-size: 0.9rem; color: #1F2937;">Hỗ trợ lập kế hoạch và quản lý dự án công nghệ phức tạp.</p>
                <ul style="font-size: 0.85rem; color: #4B5563; padding-left: 15px;">
                    <li><b>Sprint Planning Agent:</b> Tự động ước lượng thời gian & phân chia tác vụ dự án.</li>
                </ul>
                <span style="font-size: 0.8rem; color: #9A3412; font-weight:bold;">Thiết kế: Human-in-the-loop để giám sát chất lượng.</span>
            </div>
        """, unsafe_allow_html=True)
