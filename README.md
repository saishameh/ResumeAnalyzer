# Resume Analyzer

A Python tool that extracts text from resume PDFs and analyzes them using Google's Gemini AI to provide comprehensive resume insights.

## Features

- Extract text from PDF resumes using direct extraction and OCR fallback
- Analyze resumes with Google's Gemini AI model
- Option to compare resume against specific job descriptions
- Generate structured analysis including:
  - Overall assessment
  - Key skills
  - Strengths
  - Areas for improvement
  - Skill development recommendations
  - Job fit analysis
  - Job description alignment (optional)
- Save analysis results to a text file

## Prerequisites

- Python 3.7+
- Google API Key for Gemini AI

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/resume-analyzer.git
   cd resume-analyzer
   ```

2. Install required packages:
   ```
   pip install pdfplumber pytesseract pdf2image google-generativeai python-dotenv
   ```

3. Create a `.env` file in the project directory with your Google API key:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## Usage

Run the script:
```
python resume_analyzer.py
```

Follow the prompts:
1. Enter the path to the resume PDF
2. Choose whether to analyze against a job description
3. If yes, paste the job description
4. View the analysis results
5. Choose whether to save the analysis to a file
