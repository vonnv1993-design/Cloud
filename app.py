"""
Streamlit app: VNA Private Cloud - Simple Project Milestone Manager
- Prepopulated milestones based on contract signing date 2025-10-31
- Features: view milestones, assign owners, edit deliverables, mark complete, color-coded Gantt/timeline, export CSV

Requirements (requirements.txt):
streamlit
pandas
plotly

Deploy: upload this file + requirements.txt to Streamlit Cloud or run locally: `streamlit run streamlit_vna_private_cloud.py`
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="VNA Private Cloud - Milestone Manager", layout="wide")

CONTRACT_START_DEFAULT = datetime(2025, 10, 31)

# ---------- Helpers ----------
def default_milestones(start_date):
    """Return a DataFrame with prepopulated milestones relative to start_date."""
    data = [
        {
            "id": 1,
            "milestone": "Hồ sơ thiết kế kỹ thuật chi tiết (HLD/LLD)",
            "days_from_start": 30,
            "due_date": start_date + timedelta(days=30),
            "deliverables": "Hồ sơ thiết kế kỹ thuật chi tiết; Tài liệu HLD; Tài liệu LLD",
            "owner": "Ban CNTT / Đối tác",
            "status": "Not Started",
        },
        {
            "id": 2,
            "milestone": "Kế hoạch triển khai lắp đặt, cài đặt hệ thống",
            "days_from_start": 60,
            "due_date": start_date + timedelta(days=60),
            "deliverables": "Kế hoạch triển khai; Checklists triển khai; Bản vẽ bố trí",
            "owner": "Đối tác / Ban CNTT",
            "status": "Not Started",
        },
        {
            "id": 3,
            "milestone": "Kế hoạch chuyển đổi hệ thống (Migration plan)",
            "days_from_start": 100,
            "due_date": start_date + timedelta(days=100),
            "deliverables": "Kế hoạch migration; Kịch bản rollback; Kế hoạch kiểm thử",
            "owner": "Ban CNTT / CQĐV",
            "status": "Not Started",
        },
        {
            "id": 4,
            "milestone": "Hoàn thiện triển khai và sẵn sàng cung cấp dịch vụ",
            "days_from_start": 150,
            "due_date": start_date + timedelta(days=150),
            "deliverables": "Hệ thống đã triển khai, kiểm thử; Biên bản nghiệm thu; Bàn giao vận hành",
            "owner": "Đối tác / Ban CNTT",
            "status": "Not Started",
        },
    ]
    return pd.DataFrame(data)


def compute_status(row, today=None):
    if today is None:
        today = datetime.now()
    if row.get("completed_date") is not None and pd.notna(row.get("completed_date")):
        return "Completed"
    due = row["due_date"]
    if due >= today + timedelta(days=7):
        return "On Track"
    if due >= today:
        return "At Risk"
    return "Delayed"


def status_color_map(status):
    return {
        "Completed": "green",
        "On Track": "blue",
        "At Risk": "orange",
        "Delayed": "red",
        "Not Started": "gray",
    }.get(status, "gray")


# ---------- App State Init ----------
if "contract_start" not in st.session_state:
    st.session_state.contract_start = CONTRACT_START_DEFAULT

if "milestones_df" not in st.session_state:
    st.session_state.milestones_df = default_milestones(st.session_state.contract_start)
    st.session_state.milestones_df["completed_date"] = pd.NaT

# ---------- Sidebar controls ----------
st.sidebar.header("Cấu hình dự án")
start_input = st.sidebar.date_input("Ngày ký Hợp đồng / Ngày hiệu lực", value=st.session_state.contract_start.date())

if start_input != st.session_state.contract_start.date():
    st.session_state.contract_start = datetime.combine(start_input, datetime.min.time())
    # regenerate default due dates but preserve any existing custom fields by merging
    base_df = default_milestones(st.session_state.contract_start)
    old = st.session_state.milestones_df.set_index("id")
    base_df = base_df.set_index("id")
    for col in ["deliverables", "owner", "status", "completed_date"]:
        if col in old.columns:
            base_df[col] = old[col]
    base_df = base_df.reset_index()
    st.session_state.milestones_df = base_df

st.sidebar.markdown("---")
if st.sidebar.button("Thêm milestone mẫu (ví dụ)"):
    df = st.session_state.milestones_df
    new_id = int(df["id"].max()) + 1
    new_row = {
        "id": new_id,
        "milestone": f"Milestone bổ sung {new_id}",
        "days_from_start": 30,
        "due_date": st.session_state.contract_start + timedelta(days=30),
        "deliverables": "",
        "owner": "",
        "status": "Not Started",
        "completed_date": pd.NaT,
    }
    st.session_state.milestones_df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

st.sidebar.markdown("---")
if st.sidebar.button("Reset về mặc định"):
    st.session_state.milestones_df = default_milestones(st.session_state.contract_start)
    st.session_state.milestones_df["completed_date"] = pd.NaT

st.sidebar.markdown("\n\nExport / Import")
if st.sidebar.download_button("Tải CSV hiện tại", st.session_state.milestones_df.to_csv(index=False), file_name="milestones.csv"):
    pass

uploaded = st.sidebar.file_uploader("Import CSV (milestones) để cập nhật", type=["csv"]) 
if uploaded is not None:
    try:
        df_up = pd.read_csv(uploaded, parse_dates=["due_date", "completed_date"], dayfirst=True)
        st.session_state.milestones_df = df_up
        st.sidebar.success("Import thành công")
    except Exception as e:
        st.sidebar.error(f"Lỗi khi import: {e}")

# ---------- Main layout ----------
st.title("VNA Private Cloud — Milestone Manager (Streamlit)")
st.markdown("Ứng dụng đơn giản để quản lý các milestone chính, giao nhiệm vụ, và theo dõi tiến độ dự án.")

col1, col2 = st.columns((2, 3))

with col1:
    st.subheader("Danh sách Milestone")
    df = st.session_state.milestones_df.copy()
    # compute dynamic status
    today = datetime.now()
    df["status_dynamic"] = df.apply(lambda r: compute_status(r, today=today) if pd.isna(r.get("completed_date")) else "Completed", axis=1)

    # interactive edit per row
    for i, row in df.iterrows():
        exp = st.expander(f"{row['milestone']} — Hạn: {row['due_date'].date()} — Trạng thái: {row['status_dynamic']}")
        with exp:
            c1, c2 = st.columns([3, 2])
            with c1:
                new_m = st.text_input(f"Tiêu đề {row['id']}", value=row['milestone'], key=f"m_{row['id']}")
                new_d = st.text_area(f"Deliverables {row['id']}", value=row['deliverables'], key=f"d_{row['id']}")
            with c2:
                new_owner = st.text_input(f"Owner {row['id']}", value=row['owner'], key=f"o_{row['id']}")
                new_due = st.date_input(f"Due date {row['id']}", value=row['due_date'].date(), key=f"due_{row['id']}")
                status_sel = st.selectbox(f"Trạng thái {row['id']}", options=["Not Started","On Track","At Risk","Delayed","Completed"], index=0, key=f"s_{row['id']}")
                if status_sel == "Completed":
                    comp_date = st.date_input(f"Ngày hoàn thành {row['id']}", value=(row['completed_date'].date() if pd.notna(row['completed_date']) else today.date()), key=f"c_{row['id']}")
                else:
                    comp_date = None
            # apply changes back to session_state
            st.session_state.milestones_df.loc[st.session_state.milestones_df['id'] == row['id'], 'milestone'] = new_m
            st.session_state.milestones_df.loc[st.session_state.milestones_df['id'] == row['id'], 'deliverables'] = new_d
            st.session_state.milestones_df.loc[st.session_state.milestones_df['id'] == row['id'], 'owner'] = new_owner
            st.session_state.milestones_df.loc[st.session_state.milestones_df['id'] == row['id'], 'due_date'] = pd.to_datetime(new_due)
            st.session_state.milestones_df.loc[st.session_state.milestones_df['id'] == row['id'], 'status'] = status_sel
            if comp_date:
                st.session_state.milestones_df.loc[st.session_state.milestones_df['id'] == row['id'], 'completed_date'] = pd.to_datetime(comp_date)
            else:
                st.session_state.milestones_df.loc[st.session_state.milestones_df['id'] == row['id'], 'completed_date'] = pd.NaT

    st.markdown("---")
    if st.button("Thêm Milestone mới ở cuối"):
        df2 = st.session_state.milestones_df
        new_id = int(df2['id'].max()) + 1
        new_row = {
            'id': new_id,
            'milestone': f'New milestone {new_id}',
            'days_from_start': 0,
            'due_date': datetime.now(),
            'deliverables': '',
            'owner': '',
            'status': 'Not Started',
            'completed_date': pd.NaT,
        }
        st.session_state.milestones_df = pd.concat([df2, pd.DataFrame([new_row])], ignore_index=True)
        st.experimental_rerun()

with col2:
    st.subheader("Gantt / Timeline")
    gantt_df = st.session_state.milestones_df.copy()
    gantt_df['start'] = pd.to_datetime(st.session_state.contract_start)
    gantt_df['finish'] = pd.to_datetime(gantt_df['due_date'])
    gantt_df['status_dynamic'] = gantt_df.apply(lambda r: compute_status(r, today=today) if pd.isna(r.get('completed_date')) else 'Completed', axis=1)
    color_map = {s: status_color_map(s) for s in gantt_df['status_dynamic'].unique()}

    fig = px.timeline(
        gantt_df,
        x_start='start',
        x_end='finish',
        y='milestone',
        color='status_dynamic',
        hover_data=['deliverables', 'owner'],
        color_discrete_map=color_map,
    )
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Bảng tóm tắt")
    summary = st.session_state.milestones_df.copy()
    summary['due_date'] = pd.to_datetime(summary['due_date']).dt.date
    summary['completed_date'] = pd.to_datetime(summary['completed_date']).dt.date
    summary['status_dynamic'] = summary.apply(lambda r: compute_status(r, today=today) if pd.isna(r.get('completed_date')) else 'Completed', axis=1)
    st.dataframe(summary[['id','milestone','owner','due_date','completed_date','status_dynamic','deliverables']])

# ---------- Footer / Help ----------
st.markdown("---")
st.caption("Hướng dẫn: Thay đổi ngày ký hợp đồng ở thanh bên để cập nhật mốc thời hạn. Sử dụng nút export để tải CSV. Triển khai nhanh trên Streamlit Cloud hoặc chạy local bằng `streamlit run`.")


# End of file
