import streamlit as st
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Quản lý Tiến độ Dự án",
    page_icon="📋",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e40af;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 1rem;
        margin-bottom: 2rem;
    }
    .contract-banner {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
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
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 6px solid;
        transition: all 0.3s ease;
    }
    .milestone-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.15);
    }
    .status-completed { border-left-color: #10b981; background: linear-gradient(to right, #ecfdf5, white); }
    .status-in-progress { border-left-color: #f59e0b; background: linear-gradient(to right, #fffbeb, white); }
    .status-upcoming { border-left-color: #3b82f6; background: linear-gradient(to right, #eff6ff, white); }
    .status-overdue { border-left-color: #ef4444; background: linear-gradient(to right, #fef2f2, white); }
    
    .progress-bar-container {
        background: #e5e7eb;
        height: 24px;
        border-radius: 12px;
        overflow: hidden;
        margin: 1rem 0;
    }
    .progress-bar-fill {
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        font-size: 0.875rem;
        transition: width 0.5s ease;
    }
    .deliverable-item {
        background: #f9fafb;
        padding: 0.75rem;
        margin: 0.5rem 0;
        border-radius: 0.5rem;
        border-left: 3px solid #9ca3af;
    }
    .contact-box {
        background: #f3f4f6;
        padding: 1rem;
        border-radius: 0.75rem;
        margin: 1rem 0;
    }
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-top: 4px solid;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions (DEFINE BEFORE USING)
def get_status_info(status):
    info = {
        'completed': {'label': 'Hoàn thành', 'color': '#10b981', 'icon': '✅'},
        'in-progress': {'label': 'Đang thực hiện', 'color': '#f59e0b', 'icon': '⏳'},
        'upcoming': {'label': 'Sắp tới', 'color': '#3b82f6', 'icon': '📅'},
        'overdue': {'label': 'Quá hạn', 'color': '#ef4444', 'icon': '⚠️'}
    }
    return info.get(status, info['upcoming'])

def update_statuses():
    """Update milestone status based on current date"""
    if 'milestones' not in st.session_state:
        return
    
    today = datetime.now()
    for m in st.session_state.milestones:
        # Safety check
        if 'deadline' not in m or 'progress' not in m:
            continue
            
        if m['progress'] >= 100:
            m['status'] = 'completed'
        elif today > m['deadline'] and m['progress'] < 100:
            m['status'] = 'overdue'
        elif today >= m['deadline'] - timedelta(days=m['days']):
            m['status'] = 'in-progress'
        else:
            m['status'] = 'upcoming'

def days_until(deadline):
    """Calculate days until deadline"""
    return (deadline - datetime.now()).days

# Initialize session state
if 'contract_date' not in st.session_state:
    st.session_state.contract_date = datetime(2025, 10, 31)

if 'milestones' not in st.session_state:
    contract = st.session_state.contract_date
    st.session_state.milestones = [
        {
            'id': 1,
            'name': 'Hồ sơ Thiết kế Kỹ thuật Chi tiết',
            'days': 30,
            'deadline': contract + timedelta(days=30),
            'status': 'upcoming',
            'progress': 0,
            'contact': {
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
            'deadline': contract + timedelta(days=60),
            'status': 'upcoming',
            'progress': 0,
            'contact': {
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
            'deadline': contract + timedelta(days=100),
            'status': 'upcoming',
            'progress': 0,
            'contact': {
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
            'deadline': contract + timedelta(days=150),
            'status': 'upcoming',
            'progress': 0,
            'contact': {
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

# NOW update statuses after initialization
update_statuses()

# Header
st.markdown('<div class="main-header">📋 QUẢN LÝ TIẾN ĐỘ DỰ ÁN</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Cấu hình")
    
    contract_date = st.date_input(
        "📅 Ngày Ký Hợp đồng",
        value=st.session_state.contract_date,
        help="Ngày hợp đồng có hiệu lực"
    )
    
    if contract_date != st.session_state.contract_date.date():
        st.session_state.contract_date = datetime.combine(contract_date, datetime.min.time())
        for m in st.session_state.milestones:
            m['deadline'] = st.session_state.contract_date + timedelta(days=m['days'])
        update_statuses()
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("### 📊 Thống kê")
    total = len(st.session_state.milestones)
    completed = len([m for m in st.session_state.milestones if m.get('status') == 'completed'])
    in_progress = len([m for m in st.session_state.milestones if m.get('status') == 'in-progress'])
    
    st.metric("Tổng số", total)
    st.metric("Hoàn thành", completed)
    st.metric("Đang làm", in_progress)
    
    avg_progress = sum(m.get('progress', 0) for m in st.session_state.milestones) / total if total > 0 else 0
    st.metric("Tiến độ TB", f"{avg_progress:.0f}%")
    
    st.markdown("---")
    
    show_completed = st.checkbox("Hiện milestone đã xong", value=True)
    show_deliverables = st.checkbox("Hiện chi tiết deliverables", value=True)

# Contract info banner
days_passed = (datetime.now() - st.session_state.contract_date).days
st.markdown(f"""
<div class="contract-banner">
    <h2 style="margin:0;">📜 Hợp đồng Hiệu lực</h2>
    <div style="font-size:3rem;font-weight:700;margin:1rem 0;">
        {st.session_state.contract_date.strftime('%d/%m/%Y')}
    </div>
    <div style="font-size:1.25rem;">
        🕐 Đã qua: <strong>{days_passed}</strong> ngày
    </div>
</div>
""", unsafe_allow_html=True)

# Overall progress
st.markdown("### 📈 Tiến độ Tổng thể")
overall = sum(m.get('progress', 0) for m in st.session_state.milestones) / len(st.session_state.milestones)
color = '#10b981' if overall >= 75 else '#f59e0b' if overall >= 50 else '#ef4444'

st.markdown(f"""
<div class="progress-bar-container" style="height:30px;">
    <div class="progress-bar-fill" style="width:{overall}%;background:{color};">
        {overall:.1f}%
    </div>
</div>
""", unsafe_allow_html=True)

# Stats
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stat-card" style="border-top-color:#10b981;">
        <div style="font-size:0.875rem;color:#64748b;font-weight:600;">HOÀN THÀNH</div>
        <div style="font-size:2.5rem;font-weight:700;color:#10b981;">{completed}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card" style="border-top-color:#f59e0b;">
        <div style="font-size:0.875rem;color:#64748b;font-weight:600;">ĐANG LÀM</div>
        <div style="font-size:2.5rem;font-weight:700;color:#f59e0b;">{in_progress}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    upcoming = len([m for m in st.session_state.milestones if m.get('status') == 'upcoming'])
    st.markdown(f"""
    <div class="stat-card" style="border-top-color:#3b82f6;">
        <div style="font-size:0.875rem;color:#64748b;font-weight:600;">SẮP TỚI</div>
        <div style="font-size:2.5rem;font-weight:700;color:#3b82f6;">{upcoming}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    max_days = max(m.get('days', 0) for m in st.session_state.milestones)
    st.markdown(f"""
    <div class="stat-card" style="border-top-color:#8b5cf6;">
        <div style="font-size:0.875rem;color:#64748b;font-weight:600;">TỔNG THỜI GIAN</div>
        <div style="font-size:2.5rem;font-weight:700;color:#8b5cf6;">{max_days}</div>
    </div>
    """, unsafe_allow_html=True)

# Timeline chart
st.markdown("---")
st.markdown("### 📊 Biểu đồ Timeline")

fig = go.Figure()
for m in st.session_state.milestones:
    status = get_status_info(m.get('status', 'upcoming'))
    fig.add_trace(go.Bar(
        x=[m.get('days', 0)],
        y=[m.get('name', '')],
        orientation='h',
        marker_color=status['color'],
        hovertemplate=f"<b>{m.get('name', '')}</b><br>Thời hạn: {m.get('days', 0)} ngày<br>Deadline: {m.get('deadline', datetime.now()).strftime('%d/%m/%Y')}<br>Tiến độ: {m.get('progress', 0)}%<extra></extra>",
        showlegend=False
    ))

fig.update_layout(
    xaxis_title="Số ngày kể từ ký hợp đồng",
    yaxis_title="",
    height=400,
    plot_bgcolor='white',
    paper_bgcolor='white'
)
st.plotly_chart(fig, use_container_width=True)

# Milestone cards
st.markdown("---")
st.markdown("### 📋 Chi tiết Milestone")

display = [m for m in st.session_state.milestones if show_completed or m.get('status') != 'completed']

for m in display:
    status = get_status_info(m.get('status', 'upcoming'))
    days_left = days_until(m.get('deadline', datetime.now()))
    
    urgency_color = '#ef4444' if days_left < 0 else '#f59e0b' if days_left < 7 else '#10b981'
    urgency_text = f"Quá hạn {abs(days_left)} ngày" if days_left < 0 else f"Còn {days_left} ngày"
    
    st.markdown(f"""
    <div class="milestone-card status-{m.get('status', 'upcoming')}">
        <div style="display:flex;justify-content:space-between;align-items:start;">
            <div style="flex:1;">
                <div style="font-size:1.5rem;font-weight:700;color:#1e293b;margin-bottom:0.5rem;">
                    {status['icon']} Milestone {m.get('id', 0)}: {m.get('name', '')}
                </div>
                <div style="display:flex;gap:1rem;margin-bottom:1rem;">
                    <span style="background:{status['color']}20;color:{status['color']};padding:0.25rem 0.75rem;border-radius:9999px;font-size:0.875rem;font-weight:600;">
                        {status['label']}
                    </span>
                    <span style="color:#64748b;font-size:0.875rem;">
                        📅 <strong>{m.get('deadline', datetime.now()).strftime('%d/%m/%Y')}</strong>
                    </span>
                    <span style="color:{urgency_color};font-size:0.875rem;font-weight:600;">
                        ⏰ {urgency_text}
                    </span>
                </div>
            </div>
            <div style="background:{status['color']}20;color:{status['color']};padding:1rem;border-radius:0.5rem;text-align:center;font-size:2rem;font-weight:700;">
                {m.get('days', 0)}<br><span style="font-size:0.875rem;">ngày</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Progress
    progress = m.get('progress', 0)
    st.markdown(f"""
        <div style="margin:1rem 0;">
            <div style="display:flex;justify-content:space-between;margin-bottom:0.5rem;">
                <span style="font-weight:600;">Tiến độ</span>
                <span style="font-weight:700;color:{status['color']};">{progress}%</span>
            </div>
            <div class="progress-bar-container">
                <div class="progress-bar-fill" style="width:{progress}%;background:{status['color']};">
                    {progress}%
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Contact
    c = m.get('contact', {})
    st.markdown(f"""
        <div class="contact-box">
            <div style="font-weight:700;color:#1e293b;margin-bottom:0.5rem;">
                👤 Đầu mối: {c.get('name', 'N/A')}
            </div>
            <div style="font-size:0.875rem;color:#64748b;">{c.get('role', 'N/A')}</div>
            <div style="font-size:0.75rem;color:#64748b;margin-top:0.5rem;">
                📞 {c.get('phone', 'N/A')} | 📧 {c.get('email', 'N/A')}
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Deliverables
    if show_deliverables and 'deliverables' in m:
        st.markdown('<div style="margin-top:1rem;font-weight:700;color:#1e293b;">📦 Nội dung Bàn giao:</div>', unsafe_allow_html=True)
        for idx, d in enumerate(m.get('deliverables', []), 1):
            st.markdown(f'<div class="deliverable-item">{idx}. {d}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Update progress
    with st.expander("🔧 Cập nhật tiến độ"):
        new_progress = st.slider("Tiến độ mới", 0, 100, m.get('progress', 0), key=f"progress_{m.get('id', 0)}")
        if st.button("Cập nhật", key=f"btn_{m.get('id', 0)}"):
            m['progress'] = new_progress
            update_statuses()
            st.success("✅ Đã cập nhật!")
            st.rerun()

# Summary
st.markdown("---")
st.markdown("### 📊 Tổng kết")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📅 Lịch trình")
    for m in st.session_state.milestones:
        status = get_status_info(m.get('status', 'upcoming'))
        st.markdown(f"""
        <div style="background:white;padding:1rem;margin:0.5rem 0;border-radius:0.5rem;border-left:4px solid {status['color']};box-shadow:0 1px 3px rgba(0,0,0,0.1);">
            <div style="font-weight:600;">{status['icon']} {m.get('name', '')}</div>
            <div style="font-size:0.875rem;color:#64748b;">📅 {m.get('deadline', datetime.now()).strftime('%d/%m/%Y')} ({m.get('days', 0)} ngày)</div>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("#### 📈 Phân bố Trạng thái")
    status_data = {}
    for m in st.session_state.milestones:
        status = get_status_info(m.get('status', 'upcoming'))['label']
        status_data[status] = status_data.get(status, 0) + 1
    
    if status_data:
        fig_pie = px.pie(
            values=list(status_data.values()),
            names=list(status_data.keys()),
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
<div style="text-align:center;padding:2rem;background:#f8fafc;border-radius:1rem;">
    <p style="margin:0;color:#64748b;">💼 <strong>Công cụ Quản lý Tiến độ Dự án</strong></p>
    <p style="margin:0.5rem 0 0 0;color:#94a3b8;font-size:0.875rem;">Powered by Streamlit</p>
</div>
""", unsafe_allow_html=True)
