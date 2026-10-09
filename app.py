import streamlit as st
from pypdf import PdfReader

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="centered"
)

st.title("📄 AI Resume Analyzer")
st.write("Analyze your resume against a job description.")

SKILLS = [
    "python", "java", "sql", "machine learning",
    "deep learning", "nlp", "data analysis",
    "pandas", "numpy", "tensorflow", "pytorch",
    "streamlit", "html", "css", "javascript",
    "git", "communication", "problem solving",
    "excel", "power bi", "aws", "azure",
    "data visualization", "statistics", "scikit-learn",
    "natural language processing", "data science"
]

def extract_resume_text(uploaded_file):
    if uploaded_file.name.lower().endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        return "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

    return uploaded_file.getvalue().decode(
        "utf-8", errors="ignore"
    )

resume = st.file_uploader(
    "Upload your resume",
    type=["pdf", "txt"]
)

job_description = st.text_area(
    "Paste the Job Description",
    height=180
)

if st.button("Analyze Resume", type="primary"):
    if resume is None:
        st.warning("Please upload your resume.")
    elif not job_description.strip():
        st.warning("Please enter a job description.")
    else:
        try:
            resume_text = extract_resume_text(resume)

            if not resume_text.strip():
                st.error(
                    "No readable text found. Try a text-based PDF or TXT file."
                )
            else:
                resume_lower = resume_text.lower()
                job_lower = job_description.lower()

                required_skills = [
                    skill for skill in SKILLS
                    if skill in job_lower
                ]

                if not required_skills:
                    st.warning(
                        "No recognized skills found in the job description."
                    )
                else:
                    matched = [
                        skill for skill in required_skills
                        if skill in resume_lower
                    ]

                    missing = [
                        skill for skill in required_skills
                        if skill not in resume_lower
                    ]

                    score = round(
                        len(matched) / len(required_skills) * 100
                    )

                    st.success("Resume analysis completed!")

                    st.metric("Skill Match Score", f"{score}%")

                    st.progress(score / 100)

                    st.subheader("✅ Matching Skills")
                    if matched:
                        st.write(", ".join(matched))
                    else:
                        st.write("No matching skills found.")

                    st.subheader("📌 Skills to Improve")
                    if missing:
                        st.write(", ".join(missing))
                    else:
                        st.write("All detected skills matched!")

                    st.subheader("📊 Analysis Summary")
                    st.write(
                        f"Required skills detected: {len(required_skills)}"
                    )
                    st.write(f"Matching skills: {len(matched)}")
                    st.write(f"Missing skills: {len(missing)}")

                    with st.expander("View extracted resume text"):
                        st.text(resume_text[:10000])

                    st.caption(
                        "This is a basic keyword-based skill match, "
                        "not a complete AI assessment of resume quality."
                    )

        except Exception as error:
            st.error(f"Could not read the file: {error}")
