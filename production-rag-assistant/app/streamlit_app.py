from __future__ import annotations

import requests
import streamlit as st

st.set_page_config(page_title='Production RAG Assistant', layout='wide')
st.title('📚 Production RAG Assistant')
st.caption('Interactive Ask-My-Docs app with grounded citations.')

api = st.sidebar.text_input('API URL', 'http://localhost:8000')

uploaded = st.file_uploader('Upload .md or .txt docs', type=['md', 'txt'])
if uploaded and st.button('Upload file'):
    files = {'file': (uploaded.name, uploaded.getvalue(), 'text/plain')}
    res = requests.post(f'{api}/upload', files=files, timeout=30)
    st.success(res.json())

if st.button('Reindex documents'):
    res = requests.post(f'{api}/reindex', timeout=60)
    st.info(res.json())

question = st.text_area('Ask a question', placeholder='What is the incident response SLA?')
if st.button('Ask') and question.strip():
    res = requests.post(f'{api}/ask', data={'question': question}, timeout=60)
    if res.status_code >= 400:
        st.error(res.text)
    else:
        body = res.json()
        st.subheader('Answer')
        st.write(body['answer'])
        st.subheader('Citations')
        for c in body['citations']:
            st.markdown(f"- **{c['source']}** (`{c['id']}`)  \n{c['snippet']}")
