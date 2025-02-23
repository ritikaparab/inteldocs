from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import PyPDF2
import torch
from transformers import BertForQuestionAnswering, BertTokenizer
import logging
import os

# Suppress transformers warnings
logging.getLogger("transformers.modeling_utils").setLevel(logging.ERROR)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load pre-trained BERT model and tokenizer
model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

# In-memory storage for text and context
text_storage = {}  # Stores text extracted from PDFs
conversation_context = {}  # Stores conversation history per session

def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF file."""
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range(len(reader.pages)):
        text += reader.pages[page_num].extract_text()
    return text

def split_text_into_chunks(text, max_length=512):
    """Split text into smaller chunks, each containing up to max_length tokens."""
    tokens = tokenizer.tokenize(text)
    chunks = []
    
    # Split the tokens into chunks of max_length tokens
    for i in range(0, len(tokens), max_length - 2):  # -2 to account for special tokens
        chunk = tokens[i:i + max_length - 2]
        chunks.append(tokenizer.convert_tokens_to_string(chunk))
    
    return chunks

def answer_question(question, context):
    """Answer a question based on the provided context using BERT."""
    inputs = tokenizer(question, context, return_tensors='pt', truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    answer_start = torch.argmax(outputs.start_logits)
    answer_end = torch.argmax(outputs.end_logits) + 1
    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs['input_ids'][0][answer_start:answer_end]))
    return answer

def answer_question_in_chunks(question, context):
    """Answer a question based on context split into chunks."""
    chunks = split_text_into_chunks(context)
    answers = []
    
    for chunk in chunks:
        answer = answer_question(question, chunk)
        answers.append(answer)
    
    # Combine the answers from each chunk (you could further process these answers if needed)
    return ' '.join(answers)

@app.route('/')
def home():
    """Serve the frontend index.html file."""
    return send_from_directory('../frontend', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    """Handle PDF upload and extract text."""
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    pdf_file = request.files['file']
    if pdf_file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        text = extract_text_from_pdf(pdf_file)
        text_storage[pdf_file.filename] = text
        print(f"File '{pdf_file.filename}' uploaded successfully.")  # Log success
        return jsonify({"status": "success", "filename": pdf_file.filename})
    except Exception as e:
        print(f"Error processing file: {e}")  # Log errors
        return jsonify({"error": "Error processing file"}), 500

@app.route('/ask', methods=['POST'])
def ask_question():
    """Handle user questions and provide answers."""
    data = request.json
    print(f"Received data: {data}")  # Log the received data to inspect its structure
    
    try:
        filename = data['filename']
    except KeyError:
        return jsonify({"error": "Missing 'filename' in request"}), 400
    
    question = data['question']
    session_id = data.get('session_id', 'default')

    if filename not in text_storage:
        return jsonify({"error": "File not found"}), 404

    context = text_storage[filename]  # Use the entire text as context
    answer = answer_question_in_chunks(question, context)

    # Update conversation context for follow-up questions
    if session_id not in conversation_context:
        conversation_context[session_id] = context
    else:
        conversation_context[session_id] += " " + answer

    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(debug=True)
