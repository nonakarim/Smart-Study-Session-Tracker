import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

if "sessions" not in st.session_state:
    st.session_state.sessions= []

st.title("⏱️ Smart Study Session Tracker")
st.divider()
tab1, tab2, tab3, tab4= st.tabs(["Add a study session",
                                 "Session history",
                                 "Dashboard",
                                 "Productivity analysis"
                                 ])
with tab1:
    subjects= ["Python", "C++", "Math", "English", "Science"]

    with st.form(" "):
        stu_name= st.text_input("Student Name")
        subject= st.selectbox("Subject", subjects)
        duration= st.number_input("Study duration in minutes",
                                   min_value=1, 
                                   max_value=300
                                )
        difficulty= st.radio("Difficulty", 
                             ["Easy",
                              "Medium",
                              "Hard"
                              ])
        date= st.date_input("Session date")
        notes= st.text_area("Notes")

        save= st.form_submit_button("Save Session", type="primary", width= "stretch")

        if save:
            st.session_state.sessions.append({"Student Name": stu_name, 
                                            "Subject": subject, 
                                            "Duration": duration,
                                            "Difficulty": difficulty,
                                            "Date": date
                                            })

with tab2:
    st.table(st.session_state.sessions)

with tab3:
    if len(st.session_state.sessions) == 0:
        st.info("Add a study session to generate the info.")
    else:
        total_duration= 0
        max_duration= 0
        max_duration_subj= ""
        duration_sum= 0
        for duration in st.session_state.sessions:
            total_duration += duration.get("Duration")

            if duration.get("Duration") > max_duration:
                max_duration= duration.get("Duration")
                max_duration_subj= duration.get("Subject")

        average_duration= total_duration / len(st.session_state.sessions)

        col1, col2, col3, col4= st.columns(4)
        with col1:
            st.metric(label= "Total study hours", value= total_duration)
        with col2:
            st.metric(label= "Number of sessions", value= len(st.session_state.sessions))
        with col3:
            st.metric(label= "Most studied subject", value= max_duration_subj)
        with col4:
            st.metric(label= "Average session duration", value= average_duration)

with tab4:
    if len(st.session_state.sessions) == 0:
            st.info("Add a study session to generate the chart.")
    else:
        #Bar Chart
        raw_df = pd.DataFrame(st.session_state.sessions)
        
        subject_chart_df = raw_df.groupby("Subject")["Duration"].sum().reset_index()
        
        st.bar_chart(
            data=subject_chart_df,
            x="Subject",
            y="Duration",
            color="#FF4B4B" 
        )

        #Pie Chart
        subjects = ["Python", "C++", "Math", "English", "Science"]
        durations = [0, 0, 0, 0, 0]

        for i in st.session_state.sessions:
            match i.get("Subject"):
                case "Python":
                    durations[0] += i.get("Duration")
                case "C++":
                    durations[1] += i.get("Duration")
                case "Math":
                    durations[2] += i.get("Duration")
                case "English":
                    durations[3] += i.get("Duration")
                case "Science":
                    durations[4] += i.get("Duration")                   
                
        fig, ax = plt.subplots()
        ax.pie(durations, labels=subjects, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")

        st.pyplot(fig)

        #Message

        if total_duration < 120:
            st.info("Keep going!")
        elif total_duration <= 300:
            st.info("Good progress!")
        else:
            st.info("Study champion!")
        
