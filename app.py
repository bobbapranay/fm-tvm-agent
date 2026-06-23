import streamlit as st
from agents.orchestrator import answer_query

st.set_page_config(page_title="FM TVM Solver", page_icon="💰")

st.title("💰 FM TVM Solver")
st.caption("Time Value of Money agent: PV, FV, i, n, rate conversions, force of interest, and equation of value.")

with st.expander("Rules used by this app"):
    st.write("""
    - Cash inflows are positive.
    - Cash outflows are negative.
    - All cashflows are valued at a clearly stated focal date.
    - Every answer follows: Given, Formula, Substitution, Final Answer.
    """)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Ask me a TVM question, for example: Find the present value of ₹10,000 due in 3 years at 8% effective annual interest."
        }
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask a TVM question...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = answer_query(prompt)

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
