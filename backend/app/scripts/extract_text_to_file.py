import os
import re
from pypdf import PdfReader

def extract_text(file_path):
    # Öffne die PDF-Datei
    with open(file_path, 'rb') as file:
        pdf = PdfReader(file)
        text = ""
        total_pages = len(pdf.pages)
        
        # Schleife durch jede Seite in der PDF
        for page_num in range(total_pages):
            page = pdf.pages[page_num]
            # Extrahiere den Text von der Seite
            page_text = page.extract_text()
            # Wenn die Seite Text enthält, füge ihn zum Gesamten hinzu
            if page_text:
                text += page_text + "\n"
    # Rückgabe des extrahierten Textes
    return text

def clean_text(text):
    # Entferne leere Zeilen und überflüssige Leerzeichen
    lines = text.splitlines()
    cleaned_lines = [line.strip() for line in lines if line.strip()]

    # Füge durch Zeilenumbrüche getrennte Wörter zusammen
    combined_lines = []
    for i in range(len(cleaned_lines)):
        if i > 0 and cleaned_lines[i][0].islower():
            combined_lines[-1] += " " + cleaned_lines[i]
        else:
            combined_lines.append(cleaned_lines[i])

    # Filtere typische Quellenangaben (z.B. numerische Listen, eckige Klammern)
    filtered_lines = [line for line in combined_lines if not is_reference(line)]

    return "\n".join(filtered_lines)

def is_reference(line):
    # Heuristik zur Identifizierung von Quellenangaben für verschiedene Zitierstile
    patterns = [
        r"^\[\d+\]",         # [1], [2], etc. (IEEE)
        r"^\d+\.",           # 1. 2. etc. (numerische Stile)
        r"^\(\d+\)",         # (1), (2), etc.
        r"\(\d{4}\)",        # (2020), (2019), etc. (APA)
        r"^\d{4}",           # 2020, 2019 am Anfang der Zeile
        r"\d{4}\)$",         # 2020), 2019) am Ende der Zeile
        r"et al\., \d{4}",   # et al., 2020 (Harvard)
        r"\[\d{4}\]",        # [2020], [2019] (Jahr in eckigen Klammern)
        r"doi:.*$",          # DOI-Links
        r"http[s]?://\S+",   # URLs
    ]
    for pattern in patterns:
        if re.search(pattern, line):
            return True
    return False

def save_text_to_file(text, output_path):
    # Speichere den Text in einer .txt Datei
    with open(output_path, "w", encoding="utf-8") as text_file:
        text_file.write(text)

def main():
    # Verzeichnis der PDF-Dateien
    input_dir = "../../../test_data/"
    # Verzeichnis zur Speicherung der Textdateien
    output_dir = "../../../test_data/"
    
    # Gehe alle Dateien im Verzeichnis durch
    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_dir, filename)
            txt_filename = filename.replace(".pdf", ".txt")
            output_path = os.path.join(output_dir, txt_filename)
            
            # Extrahiere Text aus der PDF
            text = extract_text(pdf_path)
            
            # Bereinige den Text
            cleaned_text = clean_text(text)
            
            # Speichere den bereinigten Text in einer .txt Datei (überschreibe, wenn vorhanden)
            save_text_to_file(cleaned_text, output_path)
            
            print(f"Text von {pdf_path} wurde erfolgreich in {output_path} gespeichert.")

if __name__ == "__main__":
    main()