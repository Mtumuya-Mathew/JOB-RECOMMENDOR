import streamlit as st
#from components.recommendation import recommend_jobs
from components.resume_matching import display_recommended_jobs, extract_skills, extract_text_from_docx, extract_text_from_pdf, load_and_display_jobs, preprocess_text, recommend_jobs
from components.skills_gap import analyze_gap

# Initialize session state if not already initialized
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None  # 'job_seeker' or 'employer'

# First-time homepage for unauthenticated users
if not st.session_state.logged_in:
    options = "None"
    st.title("Welcome to the Job Market Application")
    st.write("Please login or register to access the features.")
    
    # Create Account / Login Button
    tab1, tab2 = st.tabs(["Registration", "Login"])

    # Registration Tab
    with tab1:
        st.header("Registration")
        with st.form("registration_form"):  # Form for registration
            username = st.text_input("Enter your username:")
            useremail = st.text_input("Enter your email:")
            userrole = st.selectbox("Choose your role: (Employer or Job Seeker)", ["Job Seeker", "Employer"])
            password = st.text_input("Enter your password:", type="password")
            submit_button = st.form_submit_button("Register")

            # Registration logic when form is submitted
            if submit_button:
                if username != "" and password != "":
                    st.session_state.logged_in = True
                    st.session_state.user_role = userrole.lower()  # Save user role (job_seeker or employer)
                    st.success(f"Registration successful! You are now logged in as a {userrole}.")
                else:
                    st.error("Please fill all fields correctly.")

    # Login Tab
    with tab2:
        st.header("Login")
        with st.form("login_form"):  # Form for login
            username = st.text_input("Enter your username:")
            password = st.text_input("Enter your password:", type="password")
            submit_button = st.form_submit_button("Login")

            # Login logic when form is submitted
            if submit_button:
                if username == "Mathew" and password == "pass123":  # For demo purposes
                    st.session_state.logged_in = True
                    st.session_state.user_role = "job_seeker"  # Default to job_seeker for now
                    st.success(f"Login successful! You are now logged in as a {st.session_state.user_role}.")
                else:
                    st.error("Invalid credentials.")

elif st.session_state.logged_in:
    # Dashboard Navigation for logged-in users
    st.sidebar.header("Dashboard")

    # Initialize `option` based on user role
    
    if st.session_state.user_role == "job_seeker":
        options = st.sidebar.selectbox("Choose an option", ["Job Recommendation", "Resume Screening", "Skills Gap Analysis"])
    elif st.session_state.user_role == "employer":
        options = st.sidebar.selectbox("Choose an option", ["Post a Job", "View applications"])
    # Job Recommendation Tab
    
if options == "Job Recommendation":
    st.title("Job Market Application")
    st.header("Job Recommendation System")

    tab1, tab2, tab3 = st.tabs(["Available Jobs", "Recommended jobs", "Your Skills"])

    # Tab 1: Available Jobs (will later pull from Adzuna API)
    with tab1:
        st.write("List of available jobs will appear here.")
        load_and_display_jobs("data/data job posts.csv")
        st.write("---")

    # Tab 2: Current Tab (Job recommendations from resume screening)
    with tab2:
        st.write("Here are your job recommendations:")
        
        if "recommended_jobs" not in st.session_state:
            st.session_state.recommended_jobs = []
        recommended_jobs = st.session_state.recommended_jobs 
        if "recommended_jobs" in st.session_state and st.session_state.recommended_jobs:
            display_recommended_jobs(recommended_jobs)
    # Tab 3: Your Skills
    with tab3:
        st.write("Here are your current skills:")

        if "parsed_skills" in st.session_state and st.session_state.parsed_skills:
            # Generate HTML for skill cards
            skill_cards = """
            <style>
            .skill-card {
                display: inline-block;
                margin: 5px;
                padding: 10px 15px;
                background-color: #f0f0f0;
                border-radius: 8px;
                box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
                font-size: 14px;
                color: #333;
                font-family: Arial, sans-serif;
            }
            </style>
            """
            for skill in st.session_state.parsed_skills:
                skill_cards += f"<div class='skill-card'>{skill}</div>"

            # Render the cards
            st.markdown(skill_cards, unsafe_allow_html=True)
        else:
            st.write("No skills available. Please upload your resume in the Resume Screening tab.")



elif options == "Resume Screening":
            st.header("Resume Screening")
            uploaded_file = st.file_uploader("Upload your resume:", type=["pdf", "docx"], key="resume_file_uploader")
            job_description = st.text_area("Paste the job description:")

            if st.button("Match Resume"):
                if uploaded_file is not None:
                 # Extract text from uploaded resume
                    if uploaded_file.type == "application/pdf":
                        extracted_text = extract_text_from_pdf(uploaded_file)
                    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                        extracted_text = extract_text_from_docx(uploaded_file)
                    else:
                        st.error("Unsupported file format.")
                        extracted_text = None

                    if extracted_text:
                        # Preprocess the extracted text
                        cleaned_text = preprocess_text(extracted_text)
                        # Extract skills from the text
                        parsed_skills = extract_skills(cleaned_text)
                        st.session_state.parsed_skills = parsed_skills  # Store parsed_skills in session state
                        st.write(f"Skills Extracted: {', '.join(parsed_skills)}")

                        # Call the recommend_jobs function with parsed skills
                        recommended_jobs = recommend_jobs(", ".join(parsed_skills))
                        st.session_state.recommended_jobs = recommended_jobs  # Store recommendations in session state
                        st.success("Resume matched! Check the Job Recommendation tab for suggestions.")
                    else:
                        st.error("Failed to extract text from the uploaded file.")
                else:
                    st.error("Please upload a resume.")
                

elif options == "Skills Gap Analysis":
            st.header("Skills Gap Analysis")
            user_skills = st.text_area("Enter your skills:")
            target_job = st.text_input("Enter your target job role:")
            if st.button("Analyze Skills Gap"):
                gap, recommendations = analyze_gap(user_skills, target_job)
                st.write("Skills Gap:", gap)
                st.write("Recommended Actions:", recommendations)

    # Employer Dashboard
elif st.session_state.user_role == "employer":
        if options == "Post a Job":
            st.title("Employer Dashboard")
            with st.form("post_job_form"):  # Form for posting a job
                job_title = st.text_input("Job Title")
                job_description = st.text_area("Job Description")
                skills_required = st.text_input("Skills Required")
                location = st.text_input("Location")
                salary = st.text_input("Salary")
                submit_button = st.form_submit_button("Post Job")

                if submit_button:
                    # Save job data to database (for now, display it)
                    st.write(f"Job Posted: {job_title}")
                    st.write(f"Description: {job_description}")
                    st.write(f"Skills: {skills_required}")
                    st.write(f"Location: {location}")
                    st.write(f"Salary: {salary}")
