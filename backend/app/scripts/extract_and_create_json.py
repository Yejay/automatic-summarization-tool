import os
import re
import json
import unicodedata
from pypdf import PdfReader

def extract_text(file_path):
    with open(file_path, 'rb') as file:
        pdf = PdfReader(file)
        text = ""
        total_pages = len(pdf.pages)
        for page_num in range(total_pages):
            page = pdf.pages[page_num]
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def clean_text(text):
    lines = text.splitlines()
    cleaned_lines = [line.strip() for line in lines if line.strip()]
    combined_lines = []
    for i in range(len(cleaned_lines)):
        if i > 0 and cleaned_lines[i][0].islower():
            combined_lines[-1] += " " + cleaned_lines[i]
        else:
            combined_lines.append(cleaned_lines[i])
    filtered_lines = [line for line in combined_lines if not is_reference(line)]
    normalized_text = "\n".join(filtered_lines)
    normalized_text = unicodedata.normalize("NFKD", normalized_text)
    return normalized_text

def is_reference(line):
    patterns = [
        r"^\[\d+\]", r"^\d+\.", r"^\(\d+\)", r"\(\d{4}\)", r"^\d{4}", r"\d{4}\)$",
        r"et al\., \d{4}", r"\[\d{4}\]", r"doi:.*$", r"http[s]?://\S+",
    ]
    for pattern in patterns:
        if re.search(pattern, line):
            return True
    return False

def save_text_to_file(text, output_path):
    with open(output_path, "w", encoding="utf-8") as text_file:
        text_file.write(text)

def main():
    input_dir = "../../../test_data/"
    output_dir = "../../../output/"
    output_json_path = os.path.join(output_dir, "studies.json")
    abstracts_dir = os.path.join(output_dir, "abstracts/")
    texts_dir = os.path.join(output_dir, "texts/")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if not os.path.exists(abstracts_dir):
        os.makedirs(abstracts_dir)
    if not os.path.exists(texts_dir):
        os.makedirs(texts_dir)
    
    abstracts = {
        "study1": "abstract1_for_study1.txt",
        "study2": "abstract2_for_study2.txt",
        "study3": "abstract3_for_study3.txt",
        "study4": "abstract4_for_study4.txt",
        "study5": "abstract5_for_study5.txt",
        "study6": "abstract6_for_study6.txt",
        "study7": "abstract7_for_study7.txt",
        "study8": "abstract8_for_study8.txt"
    }
    
    studies = []
    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_dir, filename)
            study_id = filename.replace(".pdf", "")
            text = extract_text(pdf_path)
            cleaned_text = clean_text(text)
            
            text_file_path = os.path.join(texts_dir, f"{study_id}.txt")
            save_text_to_file(cleaned_text, text_file_path)
            
            abstract_file_name = abstracts.get(study_id, None)
            abstract_file_path = os.path.join(abstracts_dir, abstract_file_name) if abstract_file_name else None
            
            if abstract_file_path and not os.path.exists(abstract_file_path):
                print(f"Warnung: Abstract-Datei für {study_id} nicht gefunden.")
                abstract_file_path = None
            
            study_data = {
                "id": study_id,
                "text_file": text_file_path,
                "abstract_file": abstract_file_path
            }
            studies.append(study_data)
            print(f"Text von {pdf_path} wurde erfolgreich extrahiert und bereinigt.")
    
    save_json(studies, output_json_path)
    print(f"Studieninformationen wurden erfolgreich in {output_json_path} gespeichert.")

def save_json(data, output_path):
    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()