import os
import re
import PyPDF2
import docx
import pandas as pd
def find_emails(text):
    return re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
def find_phone_numbers(text):
    return re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', text)
def extract_pdf_data(pdf_path):
    text = ""
    emails = []
    phones = []
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
        emails = find_emails(text)
        phones = find_phone_numbers(text)
    return {"Emails": emails, "Phone Numbers": phones, "Text": text}
def extract_docx_data(docx_path):
    text = ""
    emails = []
    phones = []
    doc = docx.Document(docx_path)
    for paragraph in doc.paragraphs:
        text += paragraph.text
    emails = find_emails(text)
    phones = find_phone_numbers(text)
    return {"Emails": emails, "Phone Numbers": phones, "Text": text}
def process_files(directory):
    cv_info = []
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(directory, filename)
            cv_info.append(extract_pdf_data(pdf_path))
        elif filename.endswith(".docx"):
            docx_path = os.path.join(directory, filename)
            cv_info.append(extract_docx_data(docx_path))
    return cv_info
def save_to_excel(cv_info, output_path):
    df = pd.DataFrame(cv_info)
    df.to_excel(output_path, index=False)
#output section
#print("Hey there! Let's extract some info from CVs!")
#cv_folder = input("Could you please tell me where your CVs are? (just give me the folder path): ").strip()
#if not os.path.isdir(cv_folder):
#    print("Oops! That doesn't seem to be a valid folder. Please provide a valid folder path.")
#    exit()
#output_path = input("Alright, where would you like me to save the results? (give me the path with file name): ").strip()
#try:
def output_path(cv_info,output_path):
    cv_info = process_files(cv_folder)
    save_to_excel(cv_info, output_path)
#    print("hey! I've done it! The extracted info is saved at", output_path)
#except Exception as e:
#    print("Uh-oh! Something went wrong:", e)