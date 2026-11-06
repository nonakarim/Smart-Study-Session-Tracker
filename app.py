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

