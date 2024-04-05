from pyoparser import ResumeParser

data = ResumeParser('./pyoparser/files/res/pdf/test_resume.pdf').get_extracted_data()
for key, value in data.items():
    print(f"{key}\t{value}")
