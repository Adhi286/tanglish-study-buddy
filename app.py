import time
import streamlit as st
import pandas as pd
from buddy.agent import chat
from buddy import memory, skills

st.set_page_config(
    page_title="Tanglish Study Buddy",
    page_icon="📚",
    layout="wide"
)

# Sidebar controls & information
with st.sidebar:
    st.header("⚙️ Settings")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    # Display Exam Countdowns
    st.header("⏳ Exam Countdowns")
    try:
        countdowns = skills.exam_countdown()
        if countdowns and not countdowns.startswith("No exam dates"):
            st.markdown(countdowns)
        else:
            st.info("No exam dates saved yet.")
    except Exception:
        st.info("No exam dates set.")

    st.divider()

    # Display Saved Memories
    st.header("🧠 Saved Memories")
    try:
        data = memory.load()
        if data:
            for k, v in data.items():
                st.caption(f"**{k}**: {v}")
        else:
            st.info("No memories stored.")
    except Exception:
        st.info("No saved memories found.")

st.title("📚 Tanglish Study Buddy")
st.caption("Learn & revise complex concepts with clear Tanglish explanations.")

# Tabs for Chat vs Interactive Tools
tab_chat, tab_lab = st.tabs(["💬 Chat Buddy", "⏱️ Study Lab"])

# ---------------------------------------------------------
# TAB 1: CHAT INTERFACE
# ---------------------------------------------------------
with tab_chat:
    # Initialize session state chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display prior chat messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Process new user input
    if prompt := st.chat_input("Enna topic puriyala? Type here..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            with st.spinner("Yosichutu irukken..."):
                try:
                    response = chat(st.session_state.messages)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

# ---------------------------------------------------------
# TAB 2: STUDY LAB & TIMER
# ---------------------------------------------------------
with tab_lab:
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.subheader("📊 Dynamic Hours Split")
        daily_hrs = st.slider("Select Available Study Hours Today:", min_value=1.0, max_value=10.0, value=4.0, step=0.5)
        
        # Calculate split dynamically from saved exams
        exams = skills._exams() if hasattr(skills, "_exams") else []
        if exams:
            weights = [1 / max(days, 1) for _, _, days in exams]
            total_w = sum(weights)
            
            chart_data = []
            for (name, _, _), w in zip(exams, weights):
                allocated = round((daily_hrs * w / total_w), 2)
                chart_data.append({"Subject": name, "Hours": allocated})
            
            df = pd.DataFrame(chart_data)
            st.bar_chart(df, x="Subject", y="Hours", color="#4CAF50")
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("Save exam dates in chat first (e.g., 'CN exam on Nov 15') to see the calculated study split!")

    with col2:
        st.subheader("⏱️ Focus Pomodoro Timer")
        timer_mins = st.number_input("Timer Duration (minutes):", min_value=1, max_value=120, value=25)
        
        if st.button("🚀 Start Timer", type="primary", use_container_width=True):
            seconds = timer_mins * 60
            progress_bar = st.progress(1.0)
            status_text = st.empty()
            
            for s in range(seconds, -1, -1):
                mins_left, secs_left = divmod(s, 60)
                status_text.metric("Time Remaining", f"{mins_left:02d}:{secs_left:02d}")
                progress_bar.progress(s / seconds)
                time.sleep(1)
            
            st.success("🎉 Time's up! Nalla break eduthuko!")
            st.balloons()
