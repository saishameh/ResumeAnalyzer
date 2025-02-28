import pdfplumber
import pytesseract
from pdf2image import convert_from_path
import os
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
import google.generativeai as genai
from dotenv import load_dotenv

def extract_text_from_pdf(pdf_path):
    """
    Extract text from PDF using direct extraction and OCR as fallback
    """
    text = ""
    # text extraction first
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        # return it
        if text.strip():
            print("Successfully extracted text directly from PDF.")
            return text.strip()
    except Exception as e:
        print(f"Direct text extraction failed: {e}")
    
    # Fallback to OCR for image-based PDFs
    print("Falling back to OCR for image-based PDF...")
    try:
        images = convert_from_path(pdf_path)
        for i, image in enumerate(images):
            print(f"Processing page {i+1} with OCR...")
            page_text = pytesseract.image_to_string(image)
            text += page_text + "\n"
        return text.strip()
    except Exception as e:
        print(f"OCR failed: {e}")
        return ""

def analyze_resume(resume_text, job_description=None):
    """
    Analyze resume text using Gemini API
    """
    if not resume_text:
        return {"error": "Resume text is empty. Please check PDF extraction."}
    
    model = genai.GenerativeModel("gemini-2.0-flash")
    
    # Structured prompt with clear instructions
    prompt = f"""
    # Resume Analysis Task
    
    ## Context
    You are an experienced HR professional with technical expertise. Your task is to provide a comprehensive analysis of the candidate's resume.
    
    ## Resume Text
    ```
    {resume_text}
    ```
    
    ## Analysis Requirements
    Please structure your response with the following sections:
    
    1. **Overall Assessment**: Provide a brief summary of the candidate's profile (2-3 sentences)
    2. **Key Skills**: List the most relevant technical and soft skills identified in the resume
    3. **Strengths**: Identify 3-5 notable strengths based on the resume
    4. **Areas for Improvement**: Suggest 2-3 areas where the candidate could improve
    5. **Skill Development Recommendations**: Recommend specific courses or certifications that would enhance the candidate's profile (2-3 recommendations)
    6. **Job Fit Analysis**: Assess which roles this candidate would be most suitable for based on their experience and skills
    """
    
    # Add job description comparison if provided
    if job_description:
        prompt += f"""
    7. **Job Description Alignment**:
       - Job Description: {job_description}
       - Alignment score (0-10)
       - Matching qualifications
       - Missing qualifications
       - Overall fit assessment
    """
    
    try:
        response = model.generate_content(prompt)
        analysis = response.text.strip()
        return analysis
    except Exception as e:
        return f"Error generating analysis: {e}"

def main():
    # Load environment variables
    load_dotenv()
    
    # Configure Gemini API
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in environment variables.")
        print("Please create a .env file with your Google API key (GOOGLE_API_KEY=your_key_here)")
        return
    
    genai.configure(api_key=api_key)
    
    # Get file path from user
    pdf_path = input("Enter the path to the resume PDF: ").strip()
    # if not os.path.exists(pdf_path):
    #     print(f"Error: File not found at {pdf_path}")
    #     return
    
    # Extract text from PDF
    print(f"Extracting text from {pdf_path}...")
    resume_text = extract_text_from_pdf(pdf_path)
    
    if not resume_text:
        print("Error: Could not extract text from the PDF. Please check the file.")
        return
    
    print("\nSuccessfully extracted text from resume.")
    
    # Ask if user wants to include a job description
    include_job = input("\nDo you want to analyze against a specific job description? (y/n): ")
    job_description = None
    if include_job.lower() == 'y':
        job_description = input("Paste the job description here: ")
    
    # Analyze resume
    print("\nAnalyzing resume...")
    analysis = analyze_resume(resume_text, job_description)
    
    # Print analysis
    print("\n=== RESUME ANALYSIS ===\n")
    print(analysis)
    
    # Option to save analysis
    save_option = input("\nDo you want to save this analysis to a file? (y/n): ")
    if save_option.lower() == 'y':
        output_file = input("Enter filename to save analysis (default: resume_analysis.txt): ") or "resume_analysis.txt"
        with open(output_file, 'w') as f:
            f.write(analysis)
        print(f"Analysis saved to {output_file}")

if __name__ == "__main__":
    main()