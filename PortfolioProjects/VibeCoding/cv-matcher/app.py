import streamlit as st
import pandas as pd
from io import BytesIO

from matcher import extract_text_from_bytes, batch_score

st.set_page_config(page_title="CV Matcher", layout='wide')
st.title('CV Matcher — compare many CVs to a job description')

st.markdown('Upload a job description (paste or file) and multiple CV files. The app will score each CV and show a percentage match.')

job_text = st.text_area('Job description (paste text here)', height=200)
job_file = st.file_uploader('Or upload a job description file (optional)', type=['txt','pdf','docx'], key='job')
if job_file is not None and not job_text:
    job_text = extract_text_from_bytes(job_file.read(), job_file.name)

cv_files = st.file_uploader('Upload CVs (multiple)', type=['txt','pdf','docx'], accept_multiple_files=True)

if st.button('Run matching'):
    if not job_text:
        st.error('Please provide a job description (paste text or upload a file).')
    elif not cv_files:
        st.error('Please upload one or more CV files.')
    else:
        with st.spinner('Scoring CVs...'):
            cvs = []
            for f in cv_files:
                try:
                    b = f.read()
                    text = extract_text_from_bytes(b, f.name)
                except Exception:
                    text = ''
                cvs.append((f.name, text))
            results = batch_score(job_text, cvs)
            df = pd.DataFrame(results)
            st.subheader('Results')
            st.dataframe(df)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button('Download CSV', data=csv, file_name='cv_scores.csv', mime='text/csv')

            for r in results:
                with st.expander(f"{r['name']} — {r['combined_percent']}%"):
                    st.write(f"Embedding score: {r['embedding_score']}%")
                    st.write(f"Keyword overlap: {r['keyword_overlap']}%")
