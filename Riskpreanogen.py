import fitz  # PyMuPDF for PDF extraction
from tkinter import Tk, filedialog
import google.generativeai as genai

# Configure Google GenAI (Gemini)
genai.configure(api_key="AIzaSyAZw_IQd8zSxkxjQ2ni-dVZnHFQ48qUi2o")
model = genai.GenerativeModel("gemini-pro")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text() + "\n"
    return text.strip()

# Function to analyze risks & anomalies using Gemini
def analyze_risks(pdf_text):
    query = f"""
    Analyze the following document for potential risks and anomalies:

    {pdf_text}

    Identify key risk factors, unusual patterns, or anomalies. Provide recommendations for mitigating risks.
    """
    response = model.generate_content(query)
    return response.text

def main():
    print("=== Risk and Anomaly Analysis Tool ===")
    
    # Open file dialog to select PDF
    Tk().withdraw()  # Hide the root window
    pdf_path = filedialog.askopenfilename(title="Select a PDF file", filetypes=[("PDF Files", "*.pdf")])

    if pdf_path:
        print("\n✅ PDF selected successfully. Extracting text...")
        pdf_text = extract_text_from_pdf(pdf_path)
        
        if pdf_text:
            print("✅ PDF extracted successfully. Running AI analysis...\n")
            risk_report = analyze_risks(pdf_text)
            print("\n=== Risk Analysis Report ===")
            print(risk_report)
        else:
            print("❌ Error: No text found in the PDF.")
    else:
        print("❌ Error: No file selected.")

if __name__ == "__main__":
    main()
