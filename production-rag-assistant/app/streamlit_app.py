from __future__ import annotations

import requests
import streamlit as st

API_BASE = st.sidebar.text_input("API URL", value="http://localhost:8000")

st.title("Production RAG Assistant")
st.caption("Upload documents, reindex, then ask grounded questions.")

uploaded = st.file_uploader("Upload PDF, DOCX, or Markdown", type=["pdf", "docx", "md", "txt"])
if uploaded and st.button("Upload"):
    files = {"file": (uploaded.name, uploaded.getvalue(), uploaded.type or "application/octet-stream")}
    resp = requests.post(f"{API_BASE}/upload", files=files, timeout=60)
    st.json(resp.json())

if st.button("Reindex"):
    resp = requests.post(f"{API_BASE}/reindex", timeout=300)
    st.json(resp.json())

question = st.text_area("Question", placeholder="What are the SOC2 control requirements?")
if st.button("Ask") and question.strip():
    resp = requests.post(f"{API_BASE}/ask", data={"question": question}, timeout=300)
    data = resp.json()
    st.subheader("Answer")
    st.write(data.get("answer", ""))
    st.subheader("Citations")
    for citation in data.get("citations", []):
        st.markdown(
            f"- **{citation['source']}** (page: {citation.get('page')})  \n"
            f"  id: `{citation['id']}`  \n"
            f"  snippet: {citation['snippet']}"
        )
