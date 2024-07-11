import PyPDF2

def extract_text(file_path):
    text = ""
    try:
        if file_path.endswith('.pdf'):
            with open(file_path, 'rb') as file:

                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text()

        else:
            raise ValueError("Unsupported file format. Please select a PDF file.")
    except Exception as e:

        print(f"Error extracting text from file: {str(e)}")
        return None
    return text
