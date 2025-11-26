import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict

# Page configuration
st.set_page_config(
    page_title="Quản lý Tiến độ Dự án",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #64748b;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border-left: 4px solid;
        height: 100%;
    }
    .milestone-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 5px solid;
    }
    .deliverable-item {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 3px solid;
    }
    .team-member-card {
        background: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .status-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }
    .progress-container {
        background: #e2e8f0;
        height: 12px;
        border-radius: 9999px;
        overflow: hidden;
        margin: 0.75rem 0;
    }
    .progress-bar {
        height: 100%;
        transition: width 0.5s ease;
        border-radius: 9999px;
    }
    .timeline-item {
        position: relative;
        padding-left: 2rem;
        padding-bottom: 2rem;
        border-left: 2px solid #e2e8f0;
    }
    .timeline-dot {
        position: absolute;
        left: -8px;
        width: 16px;
        height: 16px;
        border-radius: 50%;
        border: 3px solid white;
        box-shadow: 0 0 0 2px;
    }
    .info-box {
        background: #f1f5f9;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3b82f6;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.team_members = [
        {
            'id': 'tm1',
            'name': 'Nguyễn Văn An',
            'role': 'Project Manager',
            'email': 'an.nguyen@company.com',
            'avatar': '👨‍💼',
            'skills': ['Quản lý dự án', 'Lập kế hoạch', 'Quản lý rủi ro']
        },
        {
            'id': 'tm2',
            'name': 'Trần Thị Bình',
            'role': 'Tech Lead',
            'email': 'binh.tran@company.com',
            'avatar': '👩‍💻',
            'skills': ['Kiến trúc hệ thống', 'Backend', 'Database']
        },
        {
            'id': 'tm3',
            'name': 'Lê Văn Cường',
            'role': 'Senior Designer',
            'email': 'cuong.le@company.com',
            'avatar': '🎨',
            'skills': ['UI/UX Design', 'Prototyping', 'Design System']
        },
        {
            'id': 'tm4',
            'name': 'Phạm Thị Dung',
            'role': 'Full-stack Developer',
            'email': 'dung.pham@company.com',
            'avatar': '💻',
            'skills': ['React', 'Node.js', 'Python']
        },
        {
            'id': 'tm5',
            'name': 'Hoàng Văn Em',
            'role': 'QA Engineer',
            'email': 'em.hoang@company.com',
            'avatar': '🔍',
            'skills': ['Testing', 'Automation', 'Quality Assurance']
        },
        {
            'id': 'tm6',
            'name': 'Đặng Thị Phương',
            'role': 'Business Analyst',
            'email': 'phuong.dang@company.com',
            'avatar': '📊',
            'skills': ['Phân tích nghiệp vụ', 'Requirements', 'Documentation']
        },
    ]
    
    st.session_state.milestones = [
        {
            'id': 'm1',
            'name': 'Khởi động Dự án',
            'description': 'Lập kế hoạch chi tiết, phân tích yêu cầu nghiệp vụ và xác định phạm vi dự án',
            'status': 'completed',
            'start_date': '2024-01-01',
            'end_date': '2024-01-15',
            'progress': 100,
            'budget': 50000000,
            'actual_cost': 48000000,
            'assigned_members': ['tm1', 'tm6'],
            'phase_leader': 'tm1',
            'priority': 'high',
            'deliverables': [
                {
                    'id': 'd1',
                    'name': 'Tài liệu Yêu cầu Nghiệp vụ (BRD)',
                    'description': 'Mô tả chi tiết các yêu cầu nghiệp vụ và mục tiêu dự án',
                    'status': 'completed',
                    'due_date': '2024-01-08',
                    'completed_date': '2024-01-07',
                    'assignee': 'tm6'
                },
                {
                    'id': 'd2',
                    'name': 'Kế hoạch Dự án Chi tiết',
                    'description': 'Timeline, resource allocation, và risk management plan',
                    'status': 'completed',
                    'due_date': '2024-01-12',
                    'completed_date': '2024-01-12',
                    'assignee': 'tm1'
                },
                {
                    'id': 'd3',
                    'name': 'Ma trận Phân tích Rủi ro',
                    'description': 'Xác định và đánh giá các rủi ro tiềm ẩn',
                    'status': 'completed',
                    'due_date': '2024-01-15',
                    'completed_date': '2024-01-14',
                    'assignee': 'tm1'
                },
            ],
        },
        {
            'id': 'm2',
            'name': 'Thiết kế Hệ thống',
            'description': 'Thiết kế kiến trúc hệ thống, database schema và giao diện người dùng',
            'status': 'completed',
            'start_date': '2024-01-16',
            'end_date': '2024-02-15',
            'progress': 100,
            'budget': 80000000,
            'actual_cost': 82000000,
            'assigned_members': ['tm2', 'tm3', 'tm6'],
            'phase_leader': 'tm2',
            'priority': 'high',
            'deliverables': [
                {
                    'id': 'd4',
                    'name': 'Thiết kế Kiến trúc Hệ thống',
                    'description': 'System architecture diagram, tech stack selection',
                    'status': 'completed',
                    'due_date': '2024-01-30',
                    'completed_date': '2024-01-29',
                    'assignee': 'tm2'
                },
                {
                    'id': 'd5',
                    'name': 'Wireframe và Mockup UI/UX',
                    'description': 'Thiết kế giao diện người dùng và user flow',
                    'status': 'completed',
                    'due_date': '2024-02-05',
                    'completed_date': '2024-02-06',
                    'assignee': 'tm3'
                },
                {
                    'id': 'd6',
                    'name': 'Tài liệu Thiết kế Kỹ thuật',
                    'description': 'Chi tiết technical specifications và API design',
                    'status': 'completed',
                    'due_date': '2024-02-15',
                    'completed_date': '2024-02-15',
                    'assignee': 'tm2'
                },
            ],
        },
        {
            'id': 'm3',
            'name': 'Phát triển Backend',
            'description': 'Xây dựng API, business logic, và tích hợp database',
            'status': 'in-progress',
            'start_date': '2024-02-16',
            'end_date': '2024-04-30',
            'progress': 68,
            'budget': 150000000,
            'actual_cost': 95000000,
            'assigned_members': ['tm2', 'tm4'],
            'phase_leader': 'tm2',
            'priority': 'high',
            'deliverables': [
                {
                    'id': 'd7',
                    'name': 'API Authentication & Authorization',
                    'description': 'Hệ thống đăng nhập, phân quyền người dùng',
                    'status': 'completed',
                    'due_date': '2024-03-01',
                    'completed_date': '2024-03-01',
                    'assignee': 'tm4'
                },
                {
                    'id': 'd8',
                    'name': 'API Quản lý Dữ liệu Core',
                    'description': 'CRUD operations cho các entities chính',
                    'status': 'completed',
                    'due_date': '2024-03-25',
                    'completed_date': '2024-03-24',
                    'assignee': 'tm2'
                },
                {
                    'id': 'd9',
                    'name': 'Tích hợp Third-party Services',
                    'description': 'Payment gateway, email service, cloud storage',
                    'status': 'in-progress',
                    'due_date': '2024-04-15',
                    'completed_date': None,
                    'assignee': 'tm4'
                },
                {
                    'id': 'd10',
                    'name': 'Unit Testing Backend',
                    'description': 'Test coverage >= 80% cho backend code',
                    'status': 'in-progress',
                    'due_date': '2024-04-30',
                    'completed_date': None,
                    'assignee': 'tm2'
                },
            ],
        },
        {
            'id': 'm4',
            'name': 'Phát triển Frontend',
            'description': 'Xây dựng giao diện người dùng và tích hợp với backend API',
            'status': 'in-progress',
            'start_date': '2024-03-01',
            'end_date': '2024-05-15',
            'progress': 52,
            'budget': 120000000,
            'actual_cost': 55000000,
            'assigned_members': ['tm3', 'tm4'],
            'phase_leader': 'tm3',
            'priority': 'high',
            'deliverables': [
                {
                    'id': 'd11',
                    'name': 'Các Trang Chính của Ứng dụng',
                    'description': 'Dashboard, profile, main features pages',
                    'status': 'completed',
                    'due_date': '2024-03-30',
                    'completed_date': '2024-03-30',
                    'assignee': 'tm3'
                },
                {
                    'id': 'd12',
                    'name': 'Tích hợp API với UI',
                    'description': 'Kết nối frontend với backend APIs',
                    'status': 'in-progress',
                    'due_date': '2024-04-20',
                    'completed_date': None,
                    'assignee': 'tm4'
                },
                {
                    'id': 'd13',
                    'name': 'Responsive Design Implementation',
                    'description': 'Mobile, tablet và desktop optimization',
                    'status': 'in-progress',
                    'due_date': '2024-05-05',
                    'completed_date': None,
                    'assignee': 'tm3'
                },
                {
                    'id': 'd14',
                    'name': 'Performance Optimization',
                    'description': 'Load time < 2s, code splitting, lazy loading',
                    'status': 'not-started',
                    'due_date': '2024-05-15',
                    'completed_date': None,
                    'assignee': 'tm4'
                },
            ],
        },
        {
            'id': 'm5',
            'name': 'Kiểm thử và QA',
            'description': 'Testing tổng thể, bug fixing và quality assurance',
            'status': 'delayed',
            'start_date': '2024-04-15',
            'end_date': '2024-05-31',
            'progress': 25,
            'budget': 60000000,
            'actual_cost': 18000000,
            'assigned_members': ['tm5', 'tm4'],
            'phase_leader': 'tm5',
            'priority': 'critical',
            'deliverables': [
                {
                    'id': 'd15',
                    'name': 'Test Cases và Test Scenarios',
                    'description': 'Viết test cases cho tất cả features',
                    'status': 'in-progress',
                    'due_date': '2024-04-25',
                    'completed_date': None,
                    'assignee': 'tm5'
                },
                {
                    'id': 'd16',
                    'name': 'Integration Testing',
                    'description': 'Test tích hợp giữa các modules',
                    'status': 'not-started',
                    'due_date': '2024-05-10',
                    'completed_date': None,
                    'assignee': 'tm5'
                },
                {
                    'id': 'd17',
                    'name': 'User Acceptance Testing (UAT)',
                    'description': 'Testing với end users và stakeholders',
                    'status': 'not-started',
                    'due_date': '2024-05-25',
                    'completed_date': None,
                    'assignee': 'tm5'
                },
                {
                    'id': 'd18',
                    'name': 'Bug Fixing và Regression Testing',
                    'description': 'Sửa lỗi và verify không ảnh hưởng features khác',
                    'status': 'not-started',
                    'due_date': '2024-05-31',
                    'completed_date': None,
                    'assignee': 'tm4'
                },
            ],
        },
        {
            'id': 'm6',
            'name': 'Deployment và Go-live',
            'description': 'Triển khai lên production environment và monitoring',
            'status': 'not-started',
            'start_date': '2024-06-01',
            'end_date': '2024-06-15',
            'progress': 0,
            'budget': 40000000,
            'actual_cost': 0,
            'assigned_members': ['tm2', 'tm1'],
            'phase_leader': 'tm2',
            'priority': 'high',
            'deliverables': [
                {
                    'id': 'd19',
                    'name': 'Cấu hình Production Environment',
                    'description': 'Setup servers, domain, SSL certificates',
                    'status': 'not-started',
                    'due_date': '2024-06-05',
                    'completed_date': None,
                    'assignee': 'tm2'
                },
                {
                    'id': 'd20',
                    'name': 'Data Migration',
                    'description': 'Migrate dữ liệu từ staging sang production',
                    'status': 'not-started',
                    'due_date': '2024-06-08',
                    'completed_date': None,
                    'assignee': 'tm2'
                },
                {
                    'id': 'd21',
                    'name': 'Production Deployment',
                    'description': 'Deploy application lên production',
                    'status': 'not-started',
                    'due_date': '2024-06-12',
                    'completed_date': None,
                    'assignee': 'tm2'
                },
                {
                    'id': 'd22',
                    'name': 'Monitoring và Post-launch Support',
                    'description': 'Setup monitoring tools và support plan',
                    'status': 'not-started',
                    'due_date': '2024-06-15',
                    'completed_date': None,
                    'assignee': 'tm1'
                },
            ],
        },
    ]

# Helper functions
def get_status_config(status):
    """Get color and icon configuration for status"""
    configs = {
        'completed': {
            'label': 'Hoàn thành',
            'color': '#22c55e',
            'bg_color': '#dcfce7',
            'border_color': '#22c55e',
            'icon': '✅'
        },
        'in-progress': {
            'label': 'Đang thực hiện',
            'color': '#f59e0b',
            'bg_color': '#fef3c7',
            'border_color': '#f59e0b',
            'icon': '⏳'
        },
        'delayed': {
            'label': 'Trễ tiến độ',
            'color': '#ef4444',
            'bg_color': '#fee2e2',
            'border_color': '#ef4444',
            'icon': '⚠️'
        },
        'not-started': {
            'label': 'Chưa bắt đầu',
            'color': '#3b82f6',
            'bg_color': '#dbeafe',
            'border_color': '#3b82f6',
            'icon': '⭕'
        }
    }
    return configs.get(status, configs['not-started'])

def get_priority_config(priority):
    """Get configuration for priority level"""
    configs = {
        'critical': {'label': 'Khẩn cấp', 'color': '#dc2626', 'icon': '🔥'},
        'high': {'label': 'Cao', 'color': '#ea580c', 'icon': '⬆️'},
        'medium': {'label': 'Trung bình', 'color': '#f59e0b', 'icon': '➡️'},
        'low': {'label': 'Thấp', 'color': '#22c55e', 'icon': '⬇️'}
    }
    return configs.get(priority, configs['medium'])

def get_member_by_id(member_id):
    """Get team member by ID"""
    return next((m for m in st.session_state.team_members if m['id'] == member_id), None)

def format_currency(amount):
    """Format currency in VND"""
    return f"{amount:,.0f} VNĐ"

def calculate_date_progress(start_date, end_date):
    """Calculate time-based progress"""
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    today = datetime.now()
    
    if today < start:
        return 0
    elif today > end:
        return 100
    else:
        total_days = (end - start).days
        elapsed_days = (today - start).days
        return (elapsed_days / total_days * 100) if total_days > 0 else 0

def get_milestone_health(milestone):
    """Determine milestone health status"""
    date_progress = calculate_date_progress(milestone['start_date'], milestone['end_date'])
    actual_progress = milestone['progress']
    
    if actual_progress >= date_progress:
        return 'healthy'
    elif actual_progress >= date_progress - 20:
        return 'at-risk'
    else:
        return 'critical'

# Sidebar
with st.sidebar:
    st.markdown("### 🎯 Bộ lọc và Cài đặt")
    
    # Filter by status
    st.markdown("#### Trạng thái")
    status_filter = st.multiselect(
        "Lọc theo trạng thái",
        options=['completed', 'in-progress', 'delayed', 'not-started'],
        format_func=lambda x: get_status_config(x)['label'],
        default=['in-progress', 'delayed']
    )
    
    # Filter by team member
    st.markdown("#### Thành viên")
    member_options = [m['id'] for m in st.session_state.team_members]
    member_filter = st.multiselect(
        "Lọc theo thành viên",
        options=member_options,
        format_func=lambda x: get_member_by_id(x)['name'] if get_member_by_id(x) else x
    )
    
    # View options
    st.markdown("#### Hiển thị")
    show_completed = st.checkbox("Hiển thị milestone đã hoàn thành", value=True)
    show_budget = st.checkbox("Hiển thị thông tin ngân sách", value=True)
    show_timeline_chart = st.checkbox("Hiển thị biểu đồ timeline", value=True)
    
    st.markdown("---")
    st.markdown("### 📊 Thống kê nhanh")
    
    total_budget = sum(m['budget'] for m in st.session_state.milestones)
    total_actual = sum(m['actual_cost'] for m in st.session_state.milestones)
    
    st.metric("Tổng ngân sách", format_currency(total_budget))
    st.metric("Chi phí thực tế", format_currency(total_actual))
    st.metric("Chênh lệch", format_currency(total_budget - total_actual), 
              delta=f"{((total_budget - total_actual) / total_budget * 100):.1f}%")

# Main content
st.markdown('<div class="main-header">📊 Quản lý Tiến độ Dự án</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Theo dõi milestone, deliverable và phân công nhân sự một cách trực quan</div>', unsafe_allow_html=True)

# Key metrics
st.markdown("### 📈 Tổng quan")
col1, col2, col3, col4 = st.columns(4)

total_milestones = len(st.session_state.milestones)
completed_milestones = len([m for m in st.session_state.milestones if m['status'] == 'completed'])
in_progress_milestones = len([m for m in st.session_state.milestones if m['status'] == 'in-progress'])
delayed_milestones = len([m for m in st.session_state.milestones if m['status'] == 'delayed'])

with col1:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #64748b;">
        <div style="font-size: 0.875rem; color: #64748b; font-weight: 600;">TỔNG SỐ GIAI ĐOẠN</div>
        <div style="font-size: 2.5rem; font-weight: 700; color: #1e293b; margin: 0.5rem 0;">{total_milestones}</div>
        <div style="font-size: 0.75rem; color: #64748b;">milestone</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    completion_rate = (completed_milestones / total_milestones * 100) if total_milestones > 0 else 0
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #22c55e;">
        <div style="font-size: 0.875rem; color: #16a34a; font-weight: 600;">ĐÃ HOÀN THÀNH</div>
        <div style="font-size: 2.5rem; font-weight: 700; color: #22c55e; margin: 0.5rem 0;">{completed_milestones}</div>
        <div style="font-size: 0.75rem; color: #16a34a;">({completion_rate:.1f}%)</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #f59e0b;">
        <div style="font-size: 0.875rem; color: #d97706; font-weight: 600;">ĐANG THỰC HIỆN</div>
        <div style="font-size: 2.5rem; font-weight: 700; color: #f59e0b; margin: 0.5rem 0;">{in_progress_milestones}</div>
        <div style="font-size: 0.75rem; color: #d97706;">đang triển khai</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #ef4444;">
        <div style="font-size: 0.875rem; color: #dc2626; font-weight: 600;">TRỄ TIẾN ĐỘ</div>
        <div style="font-size: 2.5rem; font-weight: 700; color: #ef4444; margin: 0.5rem 0;">{delayed_milestones}</div>
        <div style="font-size: 0.75rem; color: #dc2626;">cần chú ý</div>
    </div>
    """, unsafe_allow_html=True)

# Timeline visualization
if show_timeline_chart:
    st.markdown("---")
    st.markdown("### 📅 Timeline Dự án")
    
    # Create Gantt chart data
    gantt_data = []
    for milestone in st.session_state.milestones:
        status_config = get_status_config(milestone['status'])
        gantt_data.append({
            'Task': milestone['name'],
            'Start': milestone['start_date'],
            'Finish': milestone['end_date'],
            'Status': status_config['label'],
            'Progress': milestone['progress']
        })
    
    df_gantt = pd.DataFrame(gantt_data)
    
    # Create Gantt chart
    fig = px.timeline(
        df_gantt,
        x_start='Start',
        x_end='Finish',
        y='Task',
        color='Status',
        color_discrete_map={
            'Hoàn thành': '#22c55e',
            'Đang thực hiện': '#f59e0b',
            'Trễ tiến độ': '#ef4444',
            'Chưa bắt đầu': '#3b82f6'
        },
        hover_data=['Progress']
    )
    
    fig.update_layout(
        height=400,
        xaxis_title="Thời gian",
        yaxis_title="",
        showlegend=True,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Progress overview
st.markdown("---")
st.markdown("### 🎯 Tiến độ Chi tiết")

# Filter milestones
filtered_milestones = st.session_state.milestones

if status_filter:
    filtered_milestones = [m for m in filtered_milestones if m['status'] in status_filter]

if member_filter:
    filtered_milestones = [m for m in filtered_milestones 
                          if any(member in m['assigned_members'] for member in member_filter)]

if not show_completed:
    filtered_milestones = [m for m in filtered_milestones if m['status'] != 'completed']

# Display milestones
for milestone in filtered_milestones:
    status_config = get_status_config(milestone['status'])
    priority_config = get_priority_config(milestone['priority'])
    phase_leader = get_member_by_id(milestone['phase_leader'])
    health = get_milestone_health(milestone)
    
    with st.expander(
        f"{status_config['icon']} {milestone['name']} - {status_config['label']} ({milestone['progress']}%)",
        expanded=(milestone['status'] in ['in-progress', 'delayed'])
    ):
        # Milestone header info
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"**📝 Mô tả:** {milestone['description']}")
            
            col_info1, col_info2, col_info3 = st.columns(3)
            with col_info1:
                st.markdown(f"""
                <div style="margin: 0.5rem 0;">
                    <div style="font-size: 0.75rem; color: #64748b;">📅 Thời gian</div>
                    <div style="font-weight: 600;">{milestone['start_date']} → {milestone['end_date']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_info2:
                st.markdown(f"""
                <div style="margin: 0.5rem 0;">
                    <div style="font-size: 0.75rem; color: #64748b;">🎯 Ưu tiên</div>
                    <div style="font-weight: 600; color: {priority_config['color']};">
                        {priority_config['icon']} {priority_config['label']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_info3:
                if phase_leader:
                    st.markdown(f"""
                    <div style="margin: 0.5rem 0;">
                        <div style="font-size: 0.75rem; color: #64748b;">👤 Đầu mối</div>
                        <div style="font-weight: 600;">{phase_leader['avatar']} {phase_leader['name']}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        with col2:
            # Health indicator
            health_colors = {
                'healthy': '#22c55e',
                'at-risk': '#f59e0b',
                'critical': '#ef4444'
            }
            health_labels = {
                'healthy': 'Đúng tiến độ',
                'at-risk': 'Cần theo dõi',
                'critical': 'Nguy hiểm'
            }
            
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem; background: {health_colors[health]}20; 
                        border-radius: 0.5rem; border: 2px solid {health_colors[health]};">
                <div style="font-size: 0.75rem; color: #64748b;">HEALTH STATUS</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: {health_colors[health]};">
                    {health_labels[health]}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Progress bar
        st.markdown(f"""
        <div style="margin: 1rem 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="font-weight: 600;">Tiến độ hoàn thành</span>
                <span style="font-weight: 700; color: {status_config['color']};">{milestone['progress']}%</span>
            </div>
            <div class="progress-container">
                <div class="progress-bar" style="width: {milestone['progress']}%; background: {status_config['color']};"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Budget info
        if show_budget:
            budget_col1, budget_col2, budget_col3 = st.columns(3)
            with budget_col1:
                st.metric("Ngân sách", format_currency(milestone['budget']))
            with budget_col2:
                st.metric("Chi phí thực tế", format_currency(milestone['actual_cost']))
            with budget_col3:
                variance = milestone['budget'] - milestone['actual_cost']
                st.metric("Chênh lệch", format_currency(variance),
                         delta=f"{(variance / milestone['budget'] * 100):.1f}%")
        
        # Team members
        st.markdown("---")
        st.markdown("**👥 Đội ngũ thực hiện:**")
        
        member_cols = st.columns(len(milestone['assigned_members']))
        for idx, member_id in enumerate(milestone['assigned_members']):
            member = get_member_by_id(member_id)
            if member:
                with member_cols[idx]:
                    is_leader = member_id == milestone['phase_leader']
                    st.markdown(f"""
                    <div class="team-member-card">
                        <div style="font-size: 2rem;">{member['avatar']}</div>
                        <div style="flex: 1;">
                            <div style="font-weight: 600;">
                                {member['name']}
                                {' 🏆' if is_leader else ''}
                            </div>
                            <div style="font-size: 0.75rem; color: #64748b;">{member['role']}</div>
                            {f'<div style="font-size: 0.7rem; color: #22c55e; font-weight: 600;">Leader</div>' if is_leader else ''}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Deliverables
        st.markdown("---")
        st.markdown("**✅ Deliverables:**")
        
        # Deliverables summary
        total_deliverables = len(milestone['deliverables'])
        completed_deliverables = len([d for d in milestone['deliverables'] if d['status'] == 'completed'])
        
        st.markdown(f"""
        <div class="info-box">
            <strong>Tổng quan:</strong> {completed_deliverables}/{total_deliverables} deliverables đã hoàn thành 
            ({(completed_deliverables/total_deliverables*100):.0f}%)
        </div>
        """, unsafe_allow_html=True)
        
        for deliverable in milestone['deliverables']:
            deliv_status = get_status_config(deliverable['status'])
            assignee = get_member_by_id(deliverable['assignee'])
            
            st.markdown(f"""
            <div class="deliverable-item" style="border-left-color: {deliv_status['border_color']}; 
                                                  background: {deliv_status['bg_color']};">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div style="flex: 1;">
                        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                            <span style="font-size: 1.2rem;">{deliv_status['icon']}</span>
                            <span style="font-weight: 600; font-size: 1rem;">{deliverable['name']}</span>
                        </div>
                        <div style="font-size: 0.875rem; color: #64748b; margin-bottom: 0.5rem;">
                            {deliverable['description']}
                        </div>
                        <div style="display: flex; gap: 1rem; font-size: 0.75rem; color: #64748b;">
                            <span>📅 Hạn: <strong>{deliverable['due_date']}</strong></span>
                            {f"<span>✅ Hoàn thành: <strong>{deliverable['completed_date']}</strong></span>" if deliverable['completed_date'] else ""}
                            {f"<span>👤 Phụ trách: <strong>{assignee['avatar']} {assignee['name']}</strong></span>" if assignee else ""}
                        </div>
                    </div>
                    <div>
                        <span class="status-badge" style="background: {deliv_status['bg_color']}; 
                                                           color: {deliv_status['color']}; 
                                                           border: 1px solid {deliv_status['border_color']};">
                            {deliv_status['label']}
                        </span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Team overview section
st.markdown("---")
st.markdown("### 👥 Đội ngũ Dự án")

# Team statistics
team_stats = []
for member in st.session_state.team_members:
    assigned_milestones = [m for m in st.session_state.milestones if member['id'] in m['assigned_members']]
    leading_milestones = [m for m in st.session_state.milestones if m['phase_leader'] == member['id']]
    
    assigned_deliverables = []
    for milestone in st.session_state.milestones:
        assigned_deliverables.extend([d for d in milestone['deliverables'] if d['assignee'] == member['id']])
    
    completed_deliverables = len([d for d in assigned_deliverables if d['status'] == 'completed'])
    
    team_stats.append({
        'member': member,
        'assigned_count': len(assigned_milestones),
        'leading_count': len(leading_milestones),
        'deliverables_count': len(assigned_deliverables),
        'completed_deliverables': completed_deliverables
    })

# Display team members in grid
cols = st.columns(3)
for idx, stat in enumerate(team_stats):
    member = stat['member']
    with cols[idx % 3]:
        st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-radius: 0.75rem; 
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 1rem; height: 100%;">
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                <div style="font-size: 3rem;">{member['avatar']}</div>
                <div style="flex: 1;">
                    <div style="font-weight: 700; font-size: 1.1rem; margin-bottom: 0.25rem;">
                        {member['name']}
                        {' 🏆' if stat['leading_count'] > 0 else ''}
                    </div>
                    <div style="font-size: 0.875rem; color: #64748b;">{member['role']}</div>
                </div>
            </div>
            
            <div style="background: #f8fafc; padding: 0.75rem; border-radius: 0.5rem; margin-bottom: 0.75rem;">
                <div style="font-size: 0.75rem; color: #64748b; margin-bottom: 0.25rem;">Tham gia</div>
                <div style="font-weight: 700; font-size: 1.25rem;">{stat['assigned_count']} milestone</div>
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem;">
                <div style="background: #fef3c7; padding: 0.5rem; border-radius: 0.5rem; text-align: center;">
                    <div style="font-size: 0.7rem; color: #92400e;">Đầu mối</div>
                    <div style="font-weight: 700; color: #d97706;">{stat['leading_count']}</div>
                </div>
                <div style="background: #dcfce7; padding: 0.5rem; border-radius: 0.5rem; text-align: center;">
                    <div style="font-size: 0.7rem; color: #166534;">Hoàn thành</div>
                    <div style="font-weight: 700; color: #16a34a;">{stat['completed_deliverables']}/{stat['deliverables_count']}</div>
                </div>
            </div>
            
            <div style="margin-top: 0.75rem;">
                <div style="font-size: 0.75rem; color: #64748b; margin-bottom: 0.25rem;">Kỹ năng</div>
                <div style="display: flex; flex-wrap: wrap; gap: 0.25rem;">
                    {''.join([f'<span style="font-size: 0.7rem; padding: 0.125rem 0.5rem; background: #e0e7ff; color: #4338ca; border-radius: 9999px;">{skill}</span>' for skill in member['skills']])}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Charts and Analytics
st.markdown("---")
st.markdown("### 📊 Phân tích và Báo cáo")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    # Status distribution
    st.markdown("#### Phân bổ theo Trạng thái")
    status_counts = {}
    for milestone in st.session_state.milestones:
        status = get_status_config(milestone['status'])['label']
        status_counts[status] = status_counts.get(status, 0) + 1
    
    fig_status = go.Figure(data=[go.Pie(
        labels=list(status_counts.keys()),
        values=list(status_counts.values()),
        hole=.4,
        marker_colors=['#22c55e', '#f59e0b', '#ef4444', '#3b82f6']
    )])
    fig_status.update_layout(height=300, showlegend=True)
    st.plotly_chart(fig_status, use_container_width=True)

with chart_col2:
    # Progress by milestone
    st.markdown("#### Tiến độ theo Milestone")
    milestone_names = [m['name'] for m in st.session_state.milestones]
    milestone_progress = [m['progress'] for m in st.session_state.milestones]
    
    fig_progress = go.Figure(data=[
        go.Bar(
            x=milestone_progress,
            y=milestone_names,
            orientation='h',
            marker_color=['#22c55e' if p == 100 else '#f59e0b' if p > 50 else '#ef4444' 
                         for p in milestone_progress]
        )
    ])
    fig_progress.update_layout(
        height=300,
        xaxis_title="Tiến độ (%)",
        yaxis_title="",
        showlegend=False
    )
    st.plotly_chart(fig_progress, use_container_width=True)

# Budget analysis
st.markdown("#### 💰 Phân tích Ngân sách")
budget_col1, budget_col2 = st.columns(2)

with budget_col1:
    # Budget vs Actual
    milestone_names = [m['name'] for m in st.session_state.milestones]
    budgets = [m['budget'] for m in st.session_state.milestones]
    actuals = [m['actual_cost'] for m in st.session_state.milestones]
    
    fig_budget = go.Figure(data=[
        go.Bar(name='Ngân sách', x=milestone_names, y=budgets, marker_color='#3b82f6'),
        go.Bar(name='Chi phí thực tế', x=milestone_names, y=actuals, marker_color='#22c55e')
    ])
    fig_budget.update_layout(
        barmode='group',
        height=300,
        xaxis_title="",
        yaxis_title="Số tiền (VNĐ)"
    )
    st.plotly_chart(fig_budget, use_container_width=True)

with budget_col2:
    # Cost efficiency
    st.markdown("**Chi tiết Chi phí:**")
    for milestone in st.session_state.milestones:
        variance = milestone['budget'] - milestone['actual_cost']
        efficiency = (variance / milestone['budget'] * 100) if milestone['budget'] > 0 else 0
        color = '#22c55e' if variance >= 0 else '#ef4444'
        
        st.markdown(f"""
        <div style="background: white; padding: 0.75rem; border-radius: 0.5rem; 
                    border-left: 4px solid {color}; margin: 0.5rem 0;">
            <div style="font-weight: 600; margin-bottom: 0.25rem;">{milestone['name']}</div>
            <div style="display: flex; justify-content: space-between; font-size: 0.875rem;">
                <span>Chênh lệch:</span>
                <span style="color: {color}; font-weight: 700;">{format_currency(variance)} ({efficiency:.1f}%)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #64748b;">
    <p style="margin: 0; font-size: 0.875rem;">
        💡 <strong>Công cụ Quản lý Tiến độ Dự án</strong> | 
        Theo dõi milestone, deliverable và nhân sự một cách hiệu quả
    </p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.75rem;">
        Powered by Streamlit • Cập nhật theo thời gian thực
    </p>
</div>
""", unsafe_allow_html=True)
