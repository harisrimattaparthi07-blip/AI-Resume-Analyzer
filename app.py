import streamlit as st

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="centered"
)

st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and check your skills.")

resume = st.file_uploader(
    "Upload your resume",
    type=["pdf", "txt"]
)

job_description = st.text_area(
    "Paste the Job Description here"
)

if st.button("Analyze Resume"):
    if resume is not None:
        st.success("Resume uploaded successfully!")
        st.write("Resume file:", resume.name)

        if job_description.strip():
            st.info("Your resume is ready for analysis!")
            st.write("Job description received.")
        else:
            st.warning("Please enter a job description.")
    else:
        st.warning("Please upload your resume first.")