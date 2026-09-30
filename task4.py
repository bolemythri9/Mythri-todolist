import streamlit as st
from datetime import date


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Mythri - To-Do List",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: #f7f9fc;
    }

    /* Main title */
    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        color: #6b7280;
        font-size: 17px;
        margin-bottom: 25px;
    }

    /* Statistics cards */
    .stat-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #e5e7eb;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }

    .stat-number {
        font-size: 28px;
        font-weight: 700;
    }

    .stat-label {
        color: #6b7280;
        font-size: 14px;
    }

    /* Task card */
    .task-card {
        background-color: white;
        padding: 18px;
        border-radius: 14px;
        border: 1px solid #e5e7eb;
        margin-bottom: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    }

    .completed-task {
        color: #9ca3af;
        text-decoration: line-through;
    }

    .pending-task {
        color: #111827;
        font-weight: 600;
    }

    .priority-high {
        color: #dc2626;
        font-weight: 600;
    }

    .priority-medium {
        color: #d97706;
        font-weight: 600;
    }

    .priority-low {
        color: #16a34a;
        font-weight: 600;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# SESSION STATE
# =========================================================

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "task_id" not in st.session_state:
    st.session_state.task_id = 0


# =========================================================
# FUNCTIONS
# =========================================================

def add_task(title, priority, category, due_date):

    title = title.strip()

    if not title:
        return False

    st.session_state.task_id += 1

    task = {
        "id": st.session_state.task_id,
        "title": title,
        "priority": priority,
        "category": category,
        "due_date": due_date,
        "completed": False
    }

    st.session_state.tasks.append(task)

    return True


def toggle_task(task_id):

    for task in st.session_state.tasks:

        if task["id"] == task_id:
            task["completed"] = not task["completed"]
            break


def delete_task(task_id):

    st.session_state.tasks = [
        task
        for task in st.session_state.tasks
        if task["id"] != task_id
    ]


def delete_completed():

    st.session_state.tasks = [
        task
        for task in st.session_state.tasks
        if not task["completed"]
    ]


def get_statistics():

    total = len(st.session_state.tasks)

    completed = sum(
        task["completed"]
        for task in st.session_state.tasks
    )

    pending = total - completed

    return total, completed, pending


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("⚙️ Task Controls")

    st.write("Manage and filter your tasks.")

    st.divider()

    st.subheader("🔎 Search")

    search = st.text_input(
        "Search tasks",
        placeholder="Search by task name..."
    )

    st.subheader("📌 Filter")

    status_filter = st.selectbox(
        "Status",
        ["All", "Pending", "Completed"]
    )

    priority_filter = st.selectbox(
        "Priority",
        ["All", "High", "Medium", "Low"]
    )

    st.divider()

    if st.button(
        "🗑️ Clear Completed",
        use_container_width=True
    ):
        delete_completed()
        st.rerun()


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">✅ TaskFlow</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Organize your tasks. Stay focused. Get things done.'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# STATISTICS
# =========================================================

total, completed, pending = get_statistics()

if total > 0:
    progress = completed / total
else:
    progress = 0


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-number">{total}</div>
            <div class="stat-label">Total Tasks</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-number">{pending}</div>
            <div class="stat-label">Pending</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-number">{completed}</div>
            <div class="stat-label">Completed</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col4:

    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-number">{progress * 100:.0f}%</div>
            <div class="stat-label">Progress</div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.write("")


# =========================================================
# PROGRESS BAR
# =========================================================

if total > 0:

    st.write("### 📊 Overall Progress")

    st.progress(progress)

    st.write(
        f"{completed} of {total} tasks completed"
    )


st.write("")


# =========================================================
# ADD TASK SECTION
# =========================================================

st.subheader("➕ Add New Task")

with st.container(border=True):

    col1, col2 = st.columns([3, 1])

    with col1:

        task_title = st.text_input(
            "Task",
            placeholder="Example: Complete Python assignment",
            label_visibility="collapsed"
        )

    with col2:

        priority = st.selectbox(
            "Priority",
            ["Medium", "High", "Low"],
            label_visibility="collapsed"
        )


    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:

        category = st.selectbox(
            "Category",
            [
                "Study",
                "Work",
                "Personal",
                "Project",
                "Other"
            ]
        )

    with col2:

        due_date = st.date_input(
            "Due Date",
            value=date.today()
        )

    with col3:

        st.write("")

        add_button = st.button(
            "Add Task",
            type="primary",
            use_container_width=True
        )


    if add_button:

        if add_task(
            task_title,
            priority,
            category,
            due_date
        ):

            st.success("Task added successfully!")

            st.rerun()

        else:

            st.error(
                "Please enter a task before adding it."
            )


# =========================================================
# TASK LIST
# =========================================================

st.subheader("📋 My Tasks")


# Apply filters

filtered_tasks = []

for task in st.session_state.tasks:

    # Search filter
    if search:

        if search.lower() not in task["title"].lower():
            continue

    # Status filter
    if status_filter == "Pending" and task["completed"]:
        continue

    if status_filter == "Completed" and not task["completed"]:
        continue

    # Priority filter
    if (
        priority_filter != "All"
        and task["priority"] != priority_filter
    ):
        continue

    filtered_tasks.append(task)


# =========================================================
# DISPLAY TASKS
# =========================================================

if not st.session_state.tasks:

    st.info(
        "📝 No tasks yet. Add your first task above!"
    )


elif not filtered_tasks:

    st.warning(
        "No tasks match your current filters."
    )


else:

    for task in filtered_tasks:

        with st.container(border=True):

            col1, col2, col3 = st.columns(
                [0.5, 5, 1]
            )

            # Checkbox
            with col1:

                checked = st.checkbox(
                    "",
                    value=task["completed"],
                    key=f"check_{task['id']}"
                )

                if checked != task["completed"]:

                    toggle_task(task["id"])

                    st.rerun()


            # Task information
            with col2:

                if task["completed"]:

                    st.markdown(
                        f"""
                        <div class="completed-task">
                            <h4>✓ {task["title"]}</h4>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                else:

                    st.markdown(
                        f"""
                        <div class="pending-task">
                            <h4>{task["title"]}</h4>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                # Task details

                priority_class = (
                    "priority-high"
                    if task["priority"] == "High"
                    else
                    "priority-medium"
                    if task["priority"] == "Medium"
                    else
                    "priority-low"
                )

                st.markdown(
                    f"""
                    <span class="{priority_class}">
                        ● {task["priority"]}
                    </span>
                    &nbsp;&nbsp;
                    🏷️ {task["category"]}
                    &nbsp;&nbsp;
                    📅 {task["due_date"]}
                    """,
                    unsafe_allow_html=True
                )


            # Delete button
            with col3:

                if st.button(
                    "🗑️ Delete",
                    key=f"delete_{task['id']}"
                ):

                    delete_task(task["id"])

                    st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "TaskFlow • Built with Python and Streamlit"
)