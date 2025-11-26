import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Quản lý Tiến độ Dự án",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e40af;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .contract-info {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 1rem;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .milestone-card {
        background: white;
        border-radius: 1rem;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 6px solid;
        transition: transform 0.2s;
    }
    .milestone-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .status-completed {
        border-left-color: #10b981;
        background: linear-gradient(to right, #ecfdf5 0%, white 100%);
    }
    .status-in-progress {
        border-left-color: #f59e0b;
        background: linear-gradient(to right, #fffbeb 0%, white 100%);
    }
    .status-upcoming {
        border-left-color: #3b82f6;
        background: linear-gradient(to right, #eff6ff 0%, white 100%);
    }
    .status-overdue {
        border-left-color: #ef4444;
        background: linear-gradient(to right, #fef2f2 0%, white 100%);
    }
    .milestone-header {
        display: flex;
        justify-content: space-between;
        align-items: start;
        margin-bottom: 1rem;
    }
    .milestone-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.5rem;
    }
    .milestone-days {
        font-size: 2rem;
        font-weight: 700;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .deliverable-box {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 3px solid #cbd5e1;
    }
    .deliverable-title {
        font-weight: 600;
        color: #334155;
        margin-bottom: 0.25rem;
    }
    .status-badge {
        display: inline-block;
        padding: 0.375rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 600;
    }
    .badge-completed {
        background: #d1fae5;
        color: #065f46;
    }
    .badge-in-progress {
        background: #fef3c7;
        color: #92400e;
    }
    .badge-upcoming {
        background: #dbeafe;
        color: #1e40af;
    }
    .badge-overdue {
        background: #fee2e2;
        color: #991b1b;
    }
    .progress-container {
        background: #e2e8f0;
        height: 20px;
        border-radius: 9999px;
        overflow: hidden;
        margin: 1rem 0;
    }
    .progress-bar {
        height: 100%;
        transition: width 0.5s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        font-size: 0.75rem;
    }
    .timeline-container {
        position: relative;
        padding: 2rem 0;
    }
    .timeline-line {
        position: absolute;
        left: 50%;
        top: 0;
        bottom: 0;
        width: 4px;
        background: #e2e8f0;
        transform: translateX(-50%);
    }
    .timeline-item {
        position: relative;
        margin: 2rem 0;
        display: flex;
        align-items: center;
    }
    .timeline-dot {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        border: 4px solid white;
        box-shadow: 0 0 0 4px;
        z-index: 1;
    }
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    .stat-label {
        color: #64748b;
        font-size: 0.875rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    .contact-person {
        background: #f1f5f9;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .contact-avatar {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        color: white;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'contract_date' not in st.session_state:
    st.session_state.contract_date = datetime(2024, 10, 31)

if 'milestones' not in st.session_state:
    contract_date = st.session_state.contract_date
    st.session_state.milestones = [
        {
            'id': 1,
            'name': 'Hồ sơ Thiết kế Kỹ thuật Chi tiết',
            'days': 30,
            'deadline': contract_date + timedelta(days=30),
            'status': 'completed',
            'progress': 100,
            'contact_person': {
                'name': 'Nguyễn Văn An',
                'role': 'Trưởng phòng Thiết kế',
                'phone': '0912-345-678',
                'email': 'an.nguyen@company.com'
            },
            'deliverables': [
                'Bản vẽ thiết kế kỹ thuật tổng thể hệ thống',
                'Mô tả chi tiết kiến trúc hệ thống và các thành phần',
                'Danh mục thiết bị, phần cứng và phần mềm',
                'Tài liệu kỹ thuật đặc tả hệ thống',
                'Phương án triển khai và tích hợp'
            ]
        },
        {
            'id': 2,
            'name': 'Kế hoạch Triển khai Lắp đặt & Cài đặt',
            'days': 60,
            'deadline': contract_date + timedelta(days=60),
            'status': 'in-progress',
            'progress': 65,
            'contact_person': {
                'name': 'Trần Thị Bình',
                'role': 'Trưởng phòng Triển khai',
                'phone': '0923-456-789',
                'email': 'binh.tran@company.com'
            },
            'deliverables': [
                'Kế hoạch chi tiết lắp đặt thiết bị phần cứng',
                'Kế hoạch cài đặt và cấu hình phần mềm hệ thống',
                'Lịch trình triển khai từng giai đoạn',
                'Danh sách nhân lực và phân công công việc',
                'Kế hoạch kiểm tra và nghiệm thu từng bước',
                'Phương án xử lý rủi ro và dự phòng'
            ]
        },
        {
            'id': 3,
            'name': 'Kế hoạch Chuyển đổi Hệ thống',
            'days': 100,
            'deadline': contract_date + timedelta(days=100),
            'status': 'upcoming',
            'progress': 0,
            'contact_person': {
                'name': 'Lê Văn Cường',
                'role': 'Chuyên gia Chuyển đổi số',
                'phone': '0934-567-890',
                'email': 'cuong.le@company.com'
            },
            'deliverables': [
                'Kế hoạch chuyển đổi dữ liệu từ hệ thống cũ',
                'Phương án đào tạo người dùng',
                'Quy trình vận hành hệ thống mới',
                'Kế hoạch song song vận hành 2 hệ thống',
                'Tiêu chí đánh giá và nghiệm thu chuyển đổi',
                'Kế hoạch hỗ trợ sau chuyển đổi'
            ]
        },
        {
            'id': 4,
            'name': 'Hoàn thành & Sẵn sàng Cung cấp Dịch vụ',
            'days': 150,
            'deadline': contract_date + timedelta(days=150),
            'status': 'upcoming',
            'progress': 0,
            'contact_person': {
                'name': 'Phạm Thị Dung',
                'role': 'Giám đốc Dự án',
                'phone': '0945-678-901',
                'email': 'dung.pham@company.com'
            },
            'deliverables': [
                'Hệ thống được triển khai đầy đủ và vận hành ổn định',
                'Hoàn tất kiểm thử tổng thể (System Testing)',
                'Hoàn tất kiểm thử chấp nhận người dùng (UAT)',
                'Tài liệu vận hành và bảo trì hệ thống',
                'Chương trình đào tạo người dùng đã hoàn thành',
                'Biên bản nghiệm thu và bàn giao hệ thống',
                'Hệ thống sẵn sàng đưa vào sử dụng chính thức'
            ]
        }
    ]

# Helper functions
def get_status_config(status):
    configs = {
        'completed': {
            'label': 'Hoàn thành',
            'color': '#10b981',
            'bg': '#d1fae5',
            'icon': '✅',
            'class': 'completed'
        },
        'in-progress': {
            'label': 'Đang thực hiện',
            'color': '#f59e0b',
            'bg': '#fef3c7',
            'icon': '⏳',
            'class': 'in-progress'
        },
        'upcoming': {
            'label': 'Sắp tới',
            'color': '#3b82f6',
            'bg': '#dbeafe',
            'icon': '📅',
            'class': 'upcoming'
        },
        'overdue': {
            'label': 'Quá hạn',
            'color': '#ef4444',
            'bg': '#fee2e2',
            'icon': '⚠️',
            'class': 'overdue'
        }
    }
    return configs.get(status, configs['upcoming'])

def calculate_days_remaining(deadline):
    today = datetime.now()
    delta = deadline - today
    return delta.days

def get_overall_progress():
    total_progress = sum(m['progress'] for m in st.session_state.milestones)
    return total_progress / len(st.session_state.milestones)

def update_milestone_status():
    """Update milestone status based on current date"""
    today = datetime.now()
    for milestone in st.session_state.milestones:
        if milestone['progress'] >= 100:
            milestone['status'] = 'completed'
        elif today > milestone['deadline'] and milestone['progress'] < 100:
            milestone['status'] = 'overdue'
        elif today >= milestone['deadline'] - timedelta(days=milestone['days']):
            milestone['status'] = 'in-progress'
        else:
            milestone['status'] = 'upcoming'

# Update statuses
update_milestone_status()

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Cấu hình Dự án")
    
    # Contract date
    st.markdown("#### 📅 Ngày Ký Hợp đồng")
    contract_date = st.date_input(
        "Ngày hiệu lực",
        value=st.session_state.contract_date,
        help="Ngày hợp đồng có hiệu lực"
    )
    
    if contract_date != st.session_state.contract_date.date():
        st.session_state.contract_date = datetime.combine(contract_date, datetime.min.time())
        # Recalculate all deadlines
        for milestone in st.session_state.milestones:
            milestone['deadline'] = st.session_state.contract_date + timedelta(days=milestone['days'])
        st.rerun()
    
    st.markdown("---")
    
    # Quick stats
    st.markdown("### 📊 Thống kê")
    completed_count = len([m for m in st.session_state.milestones if m['status'] == 'completed'])
    in_progress_count = len([m for m in st.session_state.milestones if m['status'] == 'in-progress'])
    
    st.metric("Hoàn thành", f"{completed_count}/{len(st.session_state.milestones)}")
    st.metric("Đang thực hiện", in_progress_count)
    st.metric("Tiến độ tổng thể", f"{get_overall_progress():.1f}%")
    
    st.markdown("---")
    
    # Filter options
    st.markdown("### 🔍 Bộ lọc")
    show_completed = st.checkbox("Hiển thị milestone đã hoàn thành", value=True)
    show_deliverables = st.checkbox("Hiển thị chi tiết deliverables", value=True)
    
    st.markdown("---")
    
    # Project info
    st.markdown("### ℹ️ Thông tin Dự án")
    st.markdown("""
    **Tên dự án:** Triển khai Hệ thống  
    **Bên A:** Đơn vị Khách hàng  
    **Bên B:** Đơn vị Cung cấp  
    **Loại hợp đồng:** Triển khai & Vận hành
    """)

# Main content
st.markdown('<div class="main-title">📋 QUẢN LÝ TIẾN ĐỘ DỰ ÁN</div>', unsafe_allow_html=True)

# Contract info banner
days_since_contract = (datetime.now() - st.session_state.contract_date).days
st.markdown(f"""
<div class="contract-info">
    <h2 style="margin: 0; font-size: 1.5rem;">📜 Hợp đồng có hiệu lực</h2>
    <div style="font-size: 3rem; font-weight: 700; margin: 1rem 0;">
        {st.session_state.contract_date.strftime('%d/%m/%Y')}
    </div>
    <div style="font-size: 1.25rem; opacity: 0.9;">
        🕐 Đã trôi qua: <strong>{days_since_contract}</strong> ngày
    </div>
</div>
""", unsafe_allow_html=True)

# Overall progress
st.markdown("### 📈 Tiến độ Tổng thể")
overall_progress = get_overall_progress()
progress_color = '#10b981' if overall_progress >= 75 else '#f59e0b' if overall_progress >= 50 else '#ef4444'

st.markdown(f"""
<div class="progress-container" style="height: 30px;">
    <div class="progress-bar" style="width: {overall_progress}%; background: {progress_color};">
        {overall_progress:.1f}%
    </div>
</div>
""", unsafe_allow_html=True)

# Statistics cards
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stat-card" style="border-top: 4px solid #10b981;">
        <div class="stat-label">Đã hoàn thành</div>
        <div class="stat-number" style="color: #10b981;">{completed_count}</div>
        <div style="font-size: 0.875rem; color: #64748b;">milestone</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card" style="border-top: 4px solid #f59e0b;">
        <div class="stat-label">Đang thực hiện</div>
        <div class="stat-number" style="color: #f59e0b;">{in_progress_count}</div>
        <div style="font-size: 0.875rem; color: #64748b;">milestone</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    upcoming_count = len([m for m in st.session_state.milestones if m['status'] == 'upcoming'])
    st.markdown(f"""
    <div class="stat-card" style="border-top: 4px solid #3b82f6;">
        <div class="stat-label">Sắp tới</div>
        <div class="stat-number" style="color: #3b82f6;">{upcoming_count}</div>
        <div style="font-size: 0.875rem; color: #64748b;">milestone</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    total_days = max([m['days'] for m in st.session_state.milestones])
    st.markdown(f"""
    <div class="stat-card" style="border-top: 4px solid #8b5cf6;">
        <div class="stat-label">Tổng thời gian</div>
        <div class="stat-number" style="color: #8b5cf6;">{total_days}</div>
        <div style="font-size: 0.875rem; color: #64748b;">ngày</div>
    </div>
    """, unsafe_allow_html=True)

# Timeline visualization
st.markdown("---")
st.markdown("### 📊 Biểu đồ Timeline")

# Create Gantt chart
fig = go.Figure()

for idx, milestone in enumerate(st.session_state.milestones):
    status_config = get_status_config(milestone['status'])
    start_date = st.session_state.contract_date
    end_date = milestone['deadline']
    
    fig.add_trace(go.Bar(
        x=[milestone['days']],
        y=[milestone['name']],
        orientation='h',
        name=milestone['name'],
        marker=dict(
            color=status_config['color'],
            line=dict(color=status_config['color'], width=2)
        ),
        hovertemplate=f"""
        <b>{milestone['name']}</b><br>
        Thời hạn: {milestone['days']} ngày<br>
        Deadline: {end_date.strftime('%d/%m/%Y')}<br>
        Tiến độ: {milestone['progress']}%<br>
        <extra></extra>
        """,
        showlegend=False
    ))

fig.update_layout(
    title="Lịch trình Thực hiện Dự án",
    xaxis_title="Số ngày kể từ ngày ký hợp đồng",
    yaxis_title="",
    height=400,
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(size=12),
    hovermode='closest'
)

fig.update_xaxis(showgrid=True, gridwidth=1, gridcolor='#e2e8f0')
fig.update_yaxis(showgrid=False)

st.plotly_chart(fig, use_container_width=True)

# Milestone cards
st.markdown("---")
st.markdown("### 📋 Chi tiết Milestone")

# Filter milestones
display_milestones = st.session_state.milestones
if not show_completed:
    display_milestones = [m for m in display_milestones if m['status'] != 'completed']

for milestone in display_milestones:
    status_config = get_status_config(milestone['status'])
    days_remaining = calculate_days_remaining(milestone['deadline'])
    
    # Determine urgency color
    if days_remaining < 0:
        urgency_color = '#ef4444'
        urgency_text = f"Quá hạn {abs(days_remaining)} ngày"
    elif days_remaining < 7:
        urgency_color = '#f59e0b'
        urgency_text = f"Còn {days_remaining} ngày"
    else:
        urgency_color = '#10b981'
        urgency_text = f"Còn {days_remaining} ngày"
    
    st.markdown(f"""
    <div class="milestone-card status-{status_config['class']}">
        <div class="milestone-header">
            <div style="flex: 1;">
                <div class="milestone-title">
                    {status_config['icon']} Milestone {milestone['id']}: {milestone['name']}
                </div>
                <div style="display: flex; gap: 1rem; align-items: center; margin-bottom: 1rem;">
                    <span class="status-badge badge-{status_config['class']}">
                        {status_config['label']}
                    </span>
                    <span style="color: #64748b; font-size: 0.875rem;">
                        📅 Deadline: <strong>{milestone['deadline'].strftime('%d/%m/%Y')}</strong>
                    </span>
                    <span style="color: {urgency_color}; font-size: 0.875rem; font-weight: 600;">
                        ⏰ {urgency_text}
                    </span>
                </div>
            </div>
            <div class="milestone-days" style="background: {status_config['bg']}; color: {status_config['color']};">
                {milestone['days']}<br>
                <span style="font-size: 0.875rem;">ngày</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Progress bar
    st.markdown(f"""
        <div style="margin: 1rem 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="font-weight: 600; color: #334155;">Tiến độ hoàn thành</span>
                <span style="font-weight: 700; color: {status_config['color']};">{milestone['progress']}%</span>
            </div>
            <div class="progress-container">
                <div class="progress-bar" style="width: {milestone['progress']}%; background: {status_config['color']};">
                    {milestone['progress']}%
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Contact person
    contact = milestone['contact_person']
    st.markdown(f"""
        <div class="contact-person">
            <div class="contact-avatar">{contact['name'][0]}</div>
            <div style="flex: 1;">
                <div style="font-weight: 700; color: #1e293b; margin-bottom: 0.25rem;">
                    👤 Đầu mối: {contact['name']}
                </div>
                <div style="font-size: 0.875rem; color: #64748b;">
                    {contact['role']}
                </div>
                <div style="font-size: 0.75rem; color: #64748b; margin-top: 0.25rem;">
                    📞 {contact['phone']} | 📧 {contact['email']}
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Deliverables
    if show_deliverables:
        st.markdown("""
            <div style="margin-top: 1rem;">
                <div style="font-weight: 700; color: #1e293b; margin-bottom: 0.75rem; font-size: 1.1rem;">
                    📦 Nội dung Bàn giao:
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        for idx, deliverable in enumerate(milestone['deliverables'], 1):
            st.markdown(f"""
            <div class="deliverable-box">
                <div class="deliverable-title">
                    {idx}. {deliverable}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Add progress update controls
    with st.expander("🔧 Cập nhật tiến độ"):
        col1, col2 = st.columns([3, 1])
        with col1:
            new_progress = st.slider(
                "Điều chỉnh tiến độ",
                0, 100, milestone['progress'],
                key=f"progress_{milestone['id']}"
            )
        with col2:
            if st.button("Cập nhật", key=f"update_{milestone['id']}"):
                milestone['progress'] = new_progress
                update_milestone_status()
                st.success("Đã cập nhật!")
                st.rerun()

# Summary section
st.markdown("---")
st.markdown("### 📊 Tổng kết")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📅 Các Mốc Quan Trọng")
    for milestone in st.session_state.milestones:
        status_config = get_status_config(milestone['status'])
        st.markdown(f"""
        <div style="background: white; padding: 1rem; margin: 0.5rem 0; border-radius: 0.5rem; 
                    border-left: 4px solid {status_config['color']}; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
            <div style="font-weight: 600; color: #1e293b; margin-bottom: 0.25rem;">
                {status_config['icon']} {milestone['name']}
            </div>
            <div style="font-size: 0.875rem; color: #64748b;">
                📅 {milestone['deadline'].strftime('%d/%m/%Y')} ({milestone['days']} ngày)
            </div>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("#### 📈 Biểu đồ Tiến độ")
    
    # Progress pie chart
    progress_data = {
        'Trạng thái': [],
        'Số lượng': []
    }
    
    status_counts = {}
    for milestone in st.session_state.milestones:
        status = get_status_config(milestone['status'])['label']
        status_counts[status] = status_counts.get(status, 0) + 1
    
    for status, count in status_counts.items():
        progress_data['Trạng thái'].append(status)
        progress_data['Số lượng'].append(count)
    
    df_progress = pd.DataFrame(progress_data)
    
    fig_pie = px.pie(
        df_progress,
        values='Số lượng',
        names='Trạng thái',
        color='Trạng thái',
        color_discrete_map={
            'Hoàn thành': '#10b981',
            'Đang thực hiện': '#f59e0b',
            'Sắp tới': '#3b82f6',
            'Quá hạn': '#ef4444'
        }
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    fig_pie.update_layout(height=300, showlegend=True)
    
    st.plotly_chart(fig_pie, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: #f8fafc; border-radius: 1rem; margin-top: 2rem;">
    <p style="margin: 0; color: #64748b; font-size: 0.875rem;">
        💼 <strong>Công cụ Quản lý Tiến độ Dự án</strong>
    </p>
    <p style="margin: 0.5rem 0 0 0; color: #94a3b8; font-size: 0.75rem;">
        Theo dõi milestone, deliverable và đầu mối một cách trực quan | Powered by Streamlit
    </p>
</div>
""", unsafe_allow_html=True)
