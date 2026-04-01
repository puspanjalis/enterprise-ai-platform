# production-rag-assistant

Interactive end-to-end RAG starter app with:
- FastAPI backend
- Streamlit front-end
- Document upload + reindex
- Grounded Q&A with citations

## Run locally
```bash
cd production-rag-assistant
pip install -r requirements.txt
uvicorn api.main:app --reload
```

In another terminal:
```bash
cd production-rag-assistant
streamlit run app/streamlit_app.py
```

## API
- `POST /upload`
- `POST /reindex`
- `POST /ask`
