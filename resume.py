import json
import re

def parse_resume(resume_text):
    # Define regular expressions for extracting different sections of the resume
    sections = {
        "name": re.compile(r"^\s*([A-Z][a-z]+\s[A-Z][a-z]+)\s*$", re.MULTILINE),
        "contact_info": re.compile(r"Email:\s([^\s]+)\s+Mobile:\s([\+\d\-]+)", re.MULTILINE),
        "skills": re.compile(r"SKILLS\s+([\s\S]+?)\s+PROJECTS", re.MULTILINE),
        "projects": re.compile(r"PROJECTS\s+([\s\S]+?)\s+CERTIFICATES", re.MULTILINE),
        "certificates": re.compile(r"CERTIFICATES\s+([\s\S]+?)\s+EDUCATION", re.MULTILINE),
        "education": re.compile(r"EDUCATION\s+([\s\S]+)", re.MULTILINE),
    }

    # Extract sections using regular expressions
    extracted = {}
    for section, regex in sections.items():
        match = regex.search(resume_text)
        if match:
            extracted[section] = match.group(1).strip()

    # Further parse the extracted sections
    if "contact_info" in extracted:
        email, mobile = extracted["contact_info"].split()
        extracted["contact_info"] = {"email": email, "mobile": mobile}

    if "skills" in extracted:
        skills = [skill.strip() for skill in extracted["skills"].split(",")]
        extracted["skills"] = skills

    if "projects" in extracted:
        projects = extracted["projects"].split("II. ")
        project_list = []
        for project in projects:
            project_lines = project.strip().split("\n")
            title = project_lines[0].replace("I.", "").strip()
            tools_and_libs = project_lines[1].replace("Tools and Library Used: ", "").strip()
            description = " ".join(project_lines[2:])
            project_list.append({
                "title": title,
                "tools_and_libraries": tools_and_libs,
                "description": description
            })
        extracted["projects"] = project_list

    if "certificates" in extracted:
        certificates = [cert.strip() for cert in extracted["certificates"].split("\n")]
        extracted["certificates"] = certificates

    if "education" in extracted:
        education_lines = extracted["education"].split("\n")
        education_list = []
        for i in range(0, len(education_lines), 2):
            institution = education_lines[i].strip()
            details = education_lines[i + 1].strip()
            education_list.append({"institution": institution, "details": details})
        extracted["education"] = education_list

    return json.dumps(extracted, indent=4)

# Example resume text
resume_text = """
Sanchit Chopra
Linkedin: sanchit-chopra-29367a24a/
Github:SanchitChopra123

Email: choprasanchit23@gmail.com
Mobile: +91-7710545003

SKILLS
Python, SQL, C++, Pandas, NumPy, Jupyter, IntelliJ Idea, Linux, Data Structures and Algorithms, Problem-Solving, Scripting in Python, Problem-Solving Skills, Team Player, Project Management, Adaptability

PROJECTS
I. Book Management System
Tools and Library Used: Python, SQL, Tkinter, PIL, pymysql
Developed a system to organize and track books with easy cataloging and inventory monitoring.
Implemented OTP authentication for secure access.
Used Tkinter for the GUI, PIL for image processing, and pymysql for database connectivity.
Features include adding, updating, deleting, and searching book records.

II. Voice Calculator (Basic)
Tools and Library Used: Python, Tkinter, SpeechRecognition, pyttsx3, PIL
Created a voice-activated calculator for hands-free basic arithmetic operations.
Utilized SpeechRecognition for voice input and pyttsx3 for voice output.
Designed an intuitive interface with Tkinter.
Implemented arithmetic functions and enhanced the interface with PIL for image handling.

CERTIFICATES
Introduction to Hardware and Operating Systems (July, 2023)
Object Oriented Programming using Python (April, 2023)
The Bits and Bytes of Computer Networking (Nov, 2023)

EDUCATION
Lovely Professional University Punjab
Computer Science and Engineering — CGPA: 7.15
Cambridge International School Kariha
12th with Science — Percentage: 77%
Cambridge International School Kariha
10th — percentage: 86%
"""

# Parse the resume text
parsed_resume = parse_resume(resume_text)
print(parsed_resume)
