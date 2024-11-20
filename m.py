from transformers import pipeline
from PyPDF2 import PdfReader
from pymongo import MongoClient
import json

# Function to extract text from each page of the PDF
def extract_text_from_pdf(pdf_path):
    pdf_reader = PdfReader(pdf_path)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to summarize the extracted text in chunks to avoid long processing time
def summarize_text(text, max_length=150, min_length=50, chunk_size=1000):
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    
    # Break the text into chunks
    text_chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    summary = ""
    
    # Summarize each chunk separately
    for chunk in text_chunks:
        chunk_summary = summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)
        summary += chunk_summary[0]['summary_text'] + " "
    
    return summary.strip()

# Store the summary in MongoDB
def store_summary_in_mongodb(pdf_name, summary):
    # Connect to MongoDB (adjust host and port if necessary)
    client = MongoClient("mongodb://localhost:27017/")
    db = client["pdf_summaries"]  # Database name
    collection = db["summaries"]  # Collection name
    
    # Create the data to insert
    data = {
        "pdf_name": pdf_name,
        "summary": summary
    }
    
    # Insert the data into the collection
    collection.insert_one(data)
    print("Summary successfully stored in MongoDB.")

# Path to your PDF file
pdf_path = r"C:\Users\U.B.A Yadav\OneDrive\Desktop\Resume.pdf"
pdf_name = "Resume.pdf"

# Extract and summarize
text = extract_text_from_pdf(pdf_path)
summary = summarize_text(text)

# Store the summary in MongoDB
store_summary_in_mongodb(pdf_name, summary)
