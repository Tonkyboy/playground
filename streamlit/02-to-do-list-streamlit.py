# Code With Alex
import streamlit as st
# pip install streamlit

priority_order = {"Must": 0, "Should": 1, "Could": 2}
color = {"Must": "red", "Should": "orange", "Could": "green"}

st.title("My Tasks")

if "tasks_data" not in st.session_state:
    st.session_state.tasks_data = []

with st.form("add_task_form", clear_on_submit=True):
    col1, col2, col3 = st.columns([3, 1, 1])

    with col1:
        new_task = st.text_input("Task", label_visibility="collapsed", placeholder="Task")
    with col2:
        priority = st.selectbox("Priority", options=list(priority_order.keys()), label_visibility="collapsed")
    with col3:
        add_clicked = st.form_submit_button("Add")

    if add_clicked and new_task.strip() != "":
        st.session_state.tasks_data.append((priority, new_task))

st.session_state.tasks_data.sort(key=lambda item: priority_order[item[0]])

for i, (task_priority, task_text) in enumerate(st.session_state.tasks_data):
    task_col, delete_col = st.columns([5, 1])
    with task_col:
        st.markdown(f":{color[task_priority]}[**[{task_priority}]** {task_text}]")
    with delete_col:
        if st.button("🗑️", key=f"delete_{i}"):
            st.session_state.tasks_data.pop(i)
            st.rerun()

# streamlit run filename.py
