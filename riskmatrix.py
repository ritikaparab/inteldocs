import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from tkinter import Tk, filedialog
import fitz  # PyMuPDF for PDF extraction
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

# Function to analyze data using Gemini
def analyze_pdf_data(pdf_text):
    query = f"""
    Analyze the following document and extract structured risk assessment data:
    {pdf_text}
    Provide structured data including transaction details, risk levels, and potential anomalies.
    """
    response = model.generate_content(query)
    return response.text  # Assuming structured output needs further processing

# Open file dialog to select PDF
Tk().withdraw()
pdf_path = filedialog.askopenfilename(title="Select a PDF file", filetypes=[("PDF Files", "*.pdf")])

if pdf_path:
    print("✅ PDF selected successfully. Extracting text...")
    pdf_text = extract_text_from_pdf(pdf_path)
    
    if pdf_text:
        print("✅ PDF extracted successfully. Analyzing data...")
        structured_data = analyze_pdf_data(pdf_text)
        
        # Convert structured text to DataFrame (this part assumes correct structured format)
        # Placeholder: Replace with actual parsing logic
        data = {
            "Transaction ID": ["TXN1001", "TXN1002", "TXN1003", "TXN1004", "TXN1005"],
            "Probability": [0.9, 0.7, 0.5, 0.8, 0.3],
            "Impact": [100000, 50000, 20000, 80000, 10000],
            "Risk Level": ["High", "Medium", "Low", "High", "Low"]
        }
        df = pd.DataFrame(data)

        # Risk Matrix Visualization
        plt.figure(figsize=(8, 6))
        sns.scatterplot(x=df["Probability"], y=df["Impact"], hue=df["Risk Level"], size=df["Impact"], sizes=(20, 400), palette="coolwarm")
        plt.xlabel("Probability")
        plt.ylabel("Impact")
        plt.title("Risk Matrix Visualization")
        plt.grid(True)
        plt.show()

        # Bubble Chart
        plt.figure(figsize=(8, 6))
        plt.scatter(df["Probability"], df["Impact"], s=df["Impact"] / 300, c=np.where(df["Risk Level"] == "High", 'red', np.where(df["Risk Level"] == "Medium", 'orange', 'green')))
        plt.xlabel("Probability")
        plt.ylabel("Impact")
        plt.title("Bubble Chart - Risk Analysis")
        plt.grid(True)
        plt.show()

        # Forecasting Graph
        df.sort_values(by="Probability", inplace=True)
        plt.figure(figsize=(8, 6))
        sns.lineplot(x=df["Probability"], y=df["Impact"], marker="o", label="Trend")
        plt.xlabel("Probability")
        plt.ylabel("Impact")
        plt.title("Forecasting Graph")
        plt.grid(True)
        plt.legend()
        plt.show()

        # Decision Tree (Basic Flowchart Representation)
        from sklearn.tree import DecisionTreeClassifier
        from sklearn import tree

        X = df[["Probability", "Impact"]]
        y = df["Risk Level"]
        clf = DecisionTreeClassifier()
        clf.fit(X, y)
        
        plt.figure(figsize=(10, 6))
        tree.plot_tree(clf, feature_names=["Probability", "Impact"], class_names=df["Risk Level"].unique(), filled=True)
        plt.title("Decision Tree for Risk Prediction")
        plt.show()
    else:
        print("❌ Error: No text found in the PDF.")
else:
    print("❌ No file selected. Please select a PDF file.")
