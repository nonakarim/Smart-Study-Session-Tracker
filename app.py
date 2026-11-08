import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

if "sessions" not in st.session_state:
    st.session_state.sessions = []

st.title("⏱️ Smart Study Session Tracker")
st.divider()

tab1, tab2, tab3, tab4 = st.tabs(["Add a study session", "Session history", "Dashboard", "Productivity analysis"])

subjects = ["Python", "C++", "Math", "English", "Science", "Social Studies", "Arabic"]

with tab1:
    with st.form(" "):
        stu_name = st.text_input("Student Name")
        subject = st.selectbox("Subject", subjects)
        duration = st.number_input("Study duration in minutes", min_value=1, max_value=300)
        difficulty = st.radio("Difficulty", ["Easy", "Medium", "Hard"])
        date = st.date_input("Session date")
        notes = st.text_area("Notes")
        save = st.form_submit_button("Save Session", type="primary", width="stretch")
        
        if save:
            st.session_state.sessions.append({
                "Student Name": stu_name,
                "Subject": subject,
                "Duration": duration,
                "Difficulty": difficulty,
                "Date": date,
                "Notes": notes
            })

# Pre-calculate data alignment across tabs if sessions exist
if len(st.session_state.sessions) > 0:
    raw_df = pd.DataFrame(st.session_state.sessions)
    # Ensure all subjects are represented in the data distribution, filling missing ones with 0
    duration_series = raw_df.groupby("Subject")["Duration"].sum().reindex(subjects, fill_value=0)
    durations = duration_series.tolist()
    
    total_duration = raw_df["Duration"].sum()
    average_duration = raw_df["Duration"].mean()
    total_hours = total_duration / 60
    
    max_duration_subj = duration_series.idxmax() if total_duration > 0 else ""

with tab3:
    if len(st.session_state.sessions) == 0:
        st.info("Add a study session to generate the info.")
    else:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label="Total study hours", value=f"{total_hours:.2f}")
        with col2:
            st.metric(label="Number of sessions", value=len(st.session_state.sessions))
        with col3:
            st.metric(label="Most studied subject", value=max_duration_subj)
        with col4:
            st.metric(label="Average session duration", value=f"{average_duration:.1f}m")

with tab4:
    if len(st.session_state.sessions) == 0:
        st.info("Add a study session to generate the chart.")
    else:
        # Bar Chart
        subject_chart_df = raw_df.groupby("Subject")["Duration"].sum().reset_index()
        st.bar_chart(data=subject_chart_df, x="Subject", y="Duration", color="#FF4B4B")
        
        # Pie Chart
        fig, ax = plt.subplots()
        ax.pie(durations, labels=subjects, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        st.pyplot(fig)
        
        # Message
        if total_duration < 120:
            st.info("Keep going!")
        elif total_duration <= 300:
            st.info("Good progress!")
        else:
            st.info("Study champion!")

with tab2:
    category = st.selectbox("Choose History table category", ["All Subjects"] + subjects)
    
    if len(st.session_state.sessions) == 0:
        st.info("No history recorded yet.")
    else:
        if category == "All Subjects":
            st.table(st.session_state.sessions)
        else:
            filtered_df = raw_df[raw_df["Subject"] == category]
            st.table(filtered_df.to_dict(orient="records"))
