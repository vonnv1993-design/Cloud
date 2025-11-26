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
        transition: all 0.2s ease;
    }
    .deliverable-item:hover {
        background: #f3f4f6;
    }
    .deliverable-completed {
        background: #ecfdf5;
        border-left-color: #10b981;
        opacity: 0.8;
    }
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-top: 4px solid;
    }
    .overdue-warning {
        background: #fef2f2;
        border: 2px solid #ef4444;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    div[data-testid="stExpander"] {
        border: none;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-radius: 0.75rem;
        margin: 0.75rem 0;
    }
    div[data-testid="stExpander"][aria-expanded="true"] {
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

# Helper functions
def get_status_info(status):
    info = {
        'completed': {'label': 'Hoàn thành', 'color': '#10b981', 'icon': '✅', 'bg': '#ecfdf5'},
        'in-progress': {'label': 'Đang thực hiện', 'color': '#f59e0b', 'icon': '⏳', 'bg': '#fffbeb'},
        'upcoming': {'label': 'Sắp tới', 'color': '#3b82f6', 'icon': '📅', 'bg': '#eff6ff'},
        'overdue': {'label': 'Quá hạn', 'color': '#ef4444', 'icon': '⚠️', 'bg': '#fef2f2'}
    }
    return info.get(status, info['upcoming'])

def update_statuses():
    if 'milestones' not in st.session_state:
        return
    
    today = datetime.now()
    for m in st.session_state.milestones:
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
    return (deadline - datetime.now()).days

def calculate_milestone_progress(milestone):
    if 'deliverables' not in milestone:
        return milestone.get('progress', 0)
    
    total = len(milestone['deliverables'])
    if total == 0:
        return 0
    
    completed = sum(1 for d in milestone['deliverables'] if d.get('completed', False))
    return int((completed / total) * 100)

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
            'original_days': 30,
            'deadline': contract + timedelta(days=30),
            'original_deadline': contract + timedelta(days=30),
            'status': 'upcoming',
            'progress': 0,
            'extensions': [],
            'contact': {
                'name': 'Nguyễn Văn An',
                'role': 'Trưởng phòng Thiết kế',
                'phone': '0912-345-678',
                'email': 'an.nguyen@company.com'
            },
            'deliverables': [
                {'text': 'Bản vẽ thiết kế kỹ thuật tổng thể hệ thống', 'completed': False, 'note': ''},
                {'text': 'Mô tả chi tiết kiến trúc hệ thống và các thành phần', 'completed': False, 'note': ''},
                {'text': 'Danh mục thiết bị, phần cứng và phần mềm', 'completed': False, 'note': ''},
                {'text': 'Tài liệu kỹ thuật đặc tả hệ thống', 'completed': False, 'note': ''},
                {'text': 'Phương án triển khai và tích hợp', 'completed': False, 'note': ''}
            ]
        },
        {
            'id': 2,
            'name': 'Kế hoạch Triển khai Lắp đặt & Cài đặt',
            'days': 60,
            'original_days': 60,
            'deadline': contract + timedelta(days=60),
            'original_deadline': contract + timedelta(days=60),
            'status': 'upcoming',
            'progress': 0,
            'extensions': [],
            'contact': {
                'name': 'Trần Thị Bình',
                'role': 'Trưởng phòng Triển khai',
                'phone': '0923-456-789',
                'email': 'binh.tran@company.com'
            },
            'deliverables': [
                {'text': 'Kế hoạch chi tiết lắp đặt thiết bị phần cứng', 'completed': False, 'note': ''},
                {'text': 'Kế hoạch cài đặt và cấu hình phần mềm hệ thống', 'completed': False, 'note': ''},
                {'text': 'Lịch trình triển khai từng giai đoạn', 'completed': False, 'note': ''},
                {'text': 'Danh sách nhân lực và phân công công việc', 'completed': False, 'note': ''},
                {'text': 'Kế hoạch kiểm tra và nghiệm thu từng bước', 'completed': False, 'note': ''},
                {'text': 'Phương án xử lý rủi ro và dự phòng', 'completed': False, 'note': ''}
            ]
        },
        {
            'id': 3,
            'name': 'Kế hoạch Chuyển đổi Hệ thống',
            'days': 100,
            'original_days': 100,
            'deadline': contract + timedelta(days=100),
            'original_deadline': contract + timedelta(days=100),
            'status': 'upcoming',
            'progress': 0,
            'extensions': [],
            'contact': {
                'name': 'Lê Văn Cường',
                'role': 'Chuyên gia Chuyển đổi số',
                'phone': '0934-567-890',
                'email': 'cuong.le@company.com'
            },
            'deliverables': [
                {'text': 'Kế hoạch chuyển đổi dữ liệu từ hệ thống cũ', 'completed': False, 'note': ''},
                {'text': 'Phương án đào tạo người dùng', 'completed': False, 'note': ''},
                {'text': 'Quy trình vận hành hệ thống mới', 'completed': False, 'note': ''},
                {'text': 'Kế hoạch song song vận hành 2 hệ thống', 'completed': False, 'note': ''},
                {'text': 'Tiêu chí đánh giá và nghiệm thu chuyển đổi', 'completed': False, 'note': ''},
                {'text': 'Kế hoạch hỗ trợ sau chuyển đổi', 'completed': False, 'note': ''}
            ]
        },
        {
            'id': 4,
            'name': 'Hoàn thành & Sẵn sàng Cung cấp Dịch vụ',
            'days': 150,
            'original_days': 150,
            'deadline': contract + timedelta(days=150),
            'original_deadline': contract + timedelta(days=150),
            'status': 'upcoming',
            'progress': 0,
            'extensions': [],
            'contact': {
                'name': 'Phạm Thị Dung',
                'role': 'Giám đốc Dự án',
                'phone': '0945-678-901',
                'email': 'dung.pham@company.com'
            },
            'deliverables': [
                {'text': 'Hệ thống được triển khai đầy đủ và vận hành ổn định', 'completed': False, 'note': ''},
                {'text': 'Hoàn tất kiểm thử tổng thể (System Testing)', 'completed': False, 'note': ''},
                {'text': 'Hoàn tất kiểm thử chấp nhận người dùng (UAT)', 'completed': False, 'note': ''},
                {'text': 'Tài liệu vận hành và bảo trì hệ thống', 'completed': False, 'note': ''},
                {'text': 'Chương trình đào tạo người dùng đã hoàn thành', 'completed': False, 'note': ''},
                {'text': 'Biên bản nghiệm thu và bàn giao hệ thống', 'completed': False, 'note': ''},
                {'text': 'Hệ thống sẵn sàng đưa vào sử dụng chính thức', 'completed': False, 'note': ''}
            ]
        }
    ]

# Update statuses
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
            days_diff = (m['deadline'] - m.get('original_deadline', m['deadline'])).days
            m['original_deadline'] = st.session_state.contract_date + timedelta(days=m['original_days'])
            m['deadline'] = m['original_deadline'] + timedelta(days=days_diff)
        update_statuses()
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("### 📊 Thống kê")
    total = len(st.session_state.milestones)
    completed = len([m for m in st.session_state.milestones if m.get('status') == 'completed'])
    in_progress = len([m for m in st.session_state.milestones if m.get('status') == 'in-progress'])
    overdue = len([m for m in st.session_state.milestones if m.get('status') == 'overdue'])
    
    total_deliverables = sum(len(m.get('deliverables', [])) for m in st.session_state.milestones)
    completed_deliverables = sum(
        sum(1 for d in m.get('deliverables', []) if d.get('completed', False))
        for m in st.session_state.milestones
    )
    
    st.metric("Tổng Milestone", total)
    st.metric("Hoàn thành", completed)
    st.metric("Đang làm", in_progress)
    st.metric("Quá hạn", overdue)
    st.metric("Deliverables", f"{completed_deliverables}/{total_deliverables}")
    
    avg_progress = sum(m.get('progress', 0) for m in st.session_state.milestones) / total if total > 0 else 0
    st.metric("Tiến độ TB", f"{avg_progress:.0f}%")
    
    st.markdown("---")
    
    show_completed = st.checkbox("Hiện milestone đã xong", value=True)

# Contract banner
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
    st.markdown(f"""
    <div class="stat-card" style="border-top-color:#ef4444;">
        <div style="font-size:0.875rem;color:#64748b;font-weight:600;">QUÁ HẠN</div>
        <div style="font-size:2.5rem;font-weight:700;color:#ef4444;">{overdue}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    upcoming = len([m for m in st.session_state.milestones if m.get('status') == 'upcoming'])
    st.markdown(f"""
    <div class="stat-card" style="border-top-color:#3b82f6;">
        <div style="font-size:0.875rem;color:#64748b;font-weight:600;">SẮP TỚI</div>
        <div style="font-size:2.5rem;font-weight:700;color:#3b82f6;">{upcoming}</div>
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

# Milestone cards - COLLAPSIBLE
st.markdown("---")
st.markdown("### 📋 Chi tiết Milestone")

display = [m for m in st.session_state.milestones if show_completed or m.get('status') != 'completed']

for m in display:
    status = get_status_info(m.get('status', 'upcoming'))
    days_left = days_until(m.get('deadline', datetime.now()))
    
    urgency_color = '#ef4444' if days_left < 0 else '#f59e0b' if days_left < 7 else '#10b981'
    urgency_text = f"Quá hạn {abs(days_left)} ngày" if days_left < 0 else f"Còn {days_left} ngày"
    
    # Summary header for expander
    completed_del = sum(1 for d in m.get('deliverables', []) if d.get('completed', False))
    total_del = len(m.get('deliverables', []))
    
    expander_label = f"{status['icon']} **Milestone {m.get('id', 0)}: {m.get('name', '')}** | {status['label']} | {m.get('progress', 0)}% | {completed_del}/{total_del} deliverables"
    
    with st.expander(expander_label, expanded=False):
        # Header info
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"""
            <div style="display:flex;gap:1rem;margin-bottom:1rem;">
                <span style="background:{status['color']}20;color:{status['color']};padding:0.5rem 1rem;border-radius:9999px;font-weight:600;">
                    {status['label']}
                </span>
                <span style="color:#64748b;">
                    📅 <strong>{m.get('deadline', datetime.now()).strftime('%d/%m/%Y')}</strong>
                </span>
                <span style="color:{urgency_color};font-weight:600;">
                    ⏰ {urgency_text}
                </span>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background:{status['bg']};color:{status['color']};padding:1rem;border-radius:0.5rem;text-align:center;">
                <div style="font-size:2rem;font-weight:700;">{m.get('days', 0)}</div>
                <div style="font-size:0.875rem;">ngày</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Progress bar
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
        
        # Edit timeline section
        with st.container():
            st.markdown("#### ⏱️ Cập nhật Thời gian")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                new_days = st.number_input(
                    "Số ngày thực hiện",
                    min_value=1,
                    max_value=365,
                    value=m.get('days', 30),
                    key=f"days_{m.get('id', 0)}"
                )
            
            with col2:
                new_deadline = st.date_input(
                    "Deadline mới",
                    value=m.get('deadline', datetime.now()),
                    key=f"deadline_{m.get('id', 0)}"
                )
            
            with col3:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("💾 Cập nhật thời gian", key=f"update_time_{m.get('id', 0)}", type="primary"):
                    m['days'] = new_days
                    m['deadline'] = datetime.combine(new_deadline, datetime.min.time())
                    update_statuses()
                    st.success("✅ Đã cập nhật thời gian!")
                    st.rerun()
        
        st.markdown("---")
        
        # Overdue warning
        if m.get('status') == 'overdue':
            st.markdown(f"""
            <div class="overdue-warning">
                <div style="font-size:1.25rem;font-weight:700;color:#dc2626;margin-bottom:0.5rem;">
                    ⚠️ Milestone đang Quá hạn!
                </div>
                <div style="color:#991b1b;">
                    Đã quá hạn: <strong>{abs(days_left)}</strong> ngày
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Extension history
            if m.get('extensions'):
                st.markdown("#### 📜 Lịch sử Gia hạn")
                for idx, ext in enumerate(m.get('extensions', []), 1):
                    st.markdown(f"""
                    <div style="background:#fffbeb;padding:0.75rem;border-radius:0.5rem;border-left:3px solid #f59e0b;margin:0.5rem 0;">
                        <div style="font-weight:600;color:#92400e;">Lần {idx}: {ext['date']}</div>
                        <div style="font-size:0.875rem;color:#78350f;margin-top:0.25rem;">
                            • Gia hạn: <strong>{ext['days']}</strong> ngày<br>
                            • Từ: {ext['old_deadline']} → {ext['new_deadline']}<br>
                            • Lý do: {ext['reason']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Contact info
        st.markdown("---")
        st.markdown("#### 👤 Thông tin Đầu mối")
        
        c = m.get('contact', {})
        col1, col2 = st.columns(2)
        
        with col1:
            new_name = st.text_input("Họ tên", value=c.get('name', ''), key=f"name_{m.get('id', 0)}")
            new_phone = st.text_input("Số điện thoại", value=c.get('phone', ''), key=f"phone_{m.get('id', 0)}")
        
        with col2:
            new_role = st.text_input("Vai trò", value=c.get('role', ''), key=f"role_{m.get('id', 0)}")
            new_email = st.text_input("Email", value=c.get('email', ''), key=f"email_{m.get('id', 0)}")
        
        if (new_name != c.get('name', '') or new_role != c.get('role', '') or 
            new_phone != c.get('phone', '') or new_email != c.get('email', '')):
            m['contact'] = {'name': new_name, 'role': new_role, 'phone': new_phone, 'email': new_email}
        
        # Deliverables with notes
        st.markdown("---")
        st.markdown("#### 📦 Nội dung Bàn giao")
        
        st.markdown(f"""
        <div style="background:#f1f5f9;padding:0.75rem;border-radius:0.5rem;margin:0.5rem 0;">
            <strong>Hoàn thành:</strong> {completed_del}/{total_del} ({(completed_del/total_del*100):.0f}%)
        </div>
        """, unsafe_allow_html=True)
        
        for idx, d in enumerate(m.get('deliverables', [])):
            col1, col2, col3 = st.columns([0.08, 0.52, 0.4])
            
            with col1:
                checked = st.checkbox(
                    "",
                    value=d.get('completed', False),
                    key=f"check_{m.get('id', 0)}_{idx}",
                    label_visibility="collapsed"
                )
                
                if checked != d.get('completed', False):
                    d['completed'] = checked
                    m['progress'] = calculate_milestone_progress(m)
                    update_statuses()
                    st.rerun()
            
            with col2:
                completed_class = "deliverable-completed" if d.get('completed', False) else ""
                check_icon = "✅" if d.get('completed', False) else "⬜"
                text_decoration = "text-decoration:line-through;opacity:0.6;" if d.get('completed', False) else ""
                
                st.markdown(f"""
                <div class="deliverable-item {completed_class}" style="{text_decoration}">
                    {check_icon} {idx + 1}. {d.get('text', '')}
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                note_value = st.text_input(
                    "Ghi chú",
                    value=d.get('note', ''),
                    key=f"note_{m.get('id', 0)}_{idx}",
                    placeholder="Thêm ghi chú...",
                    label_visibility="collapsed"
                )
                
                if note_value != d.get('note', ''):
                    d['note'] = note_value

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align:center;padding:2rem;background:#f8fafc;border-radius:1rem;">
    <p style="margin:0;color:#64748b;">💼 <strong>Công cụ Quản lý Tiến độ Dự án</strong></p>
    <p style="margin:0.5rem 0 0 0;color:#94a3b8;font-size:0.875rem;">Powered by Streamlit</p>
</div>
""", unsafe_allow_html=True)
