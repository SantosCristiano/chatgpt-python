import pdfplumber
import openai

# Function to extract text from PDF using pdfplumber
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Function to interact with ChatGPT-4 API
def analyze_with_chatgpt(text):
    openai.api_key = 'your_openai_api_key'
    response = openai.Completion.create(
        engine="text-davinci-004",
        prompt=text,
        max_tokens=50  # Adjust based on your requirement
    )
    return response.choices[0].text.strip()

# Example usage
pdf_path = 'sample.pdf'
pdf_text = extract_text_from_pdf(pdf_path)
analysis_result = analyze_with_chatgpt(pdf_text)
print(analysis_result)
