import os
import uuid
import time
import json
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import PyPDF2
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# It's a good practice to have an upload folder, and create it if it doesn't exist.
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'resume-analyzer'})


@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({'error': 'No resume file provided'}), 400

    file = request.files['resume']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.endswith('.pdf'):
        # Use a unique filename to avoid conflicts
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)

        try:
            # Extract text from PDF
            pdf_text = ''
            with open(filepath, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                
                # Check if PDF is readable
                if len(pdf_reader.pages) == 0:
                    return jsonify({'error': 'PDF file appears to be empty or corrupted'}), 400
                
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text.strip():  # Only add non-empty pages
                            pdf_text += f"\n--- Page {page_num + 1} ---\n"
                            pdf_text += page_text
                    except Exception as e:
                        print(f"Error extracting text from page {page_num + 1}: {e}")
                        continue
                
                # If no text was extracted, try alternative methods
                if not pdf_text.strip():
                    print("No text extracted with PyPDF2, trying alternative methods...")
                    
                    # Method 1: Try with different extraction parameters
                    for page in pdf_reader.pages:
                        try:
                            page_text = page.extract_text(visitor_text=lambda text, cm, tm, fontDict, fontSize: text)
                            if page_text.strip():
                                pdf_text += page_text + "\n"
                        except:
                            continue
                    
                    # Method 2: Try extracting text from annotations and forms
                    if not pdf_text.strip():
                        print("Trying to extract from annotations and forms...")
                        for page in pdf_reader.pages:
                            try:
                                if hasattr(page, 'get_contents'):
                                    contents = page.get_contents()
                                    if contents:
                                        pdf_text += str(contents) + "\n"
                            except:
                                continue
                    
                    # Method 3: Try extracting from page objects directly
                    if not pdf_text.strip():
                        print("Trying to extract from page objects...")
                        for page in pdf_reader.pages:
                            try:
                                if hasattr(page, 'get_object'):
                                    page_obj = page.get_object()
                                    if isinstance(page_obj, dict) and '/Contents' in page_obj:
                                        contents = page_obj['/Contents']
                                        if contents:
                                            pdf_text += str(contents) + "\n"
                            except:
                                continue
                
                # If still no text, try one more fallback method
                if not pdf_text.strip():
                    print("Trying final fallback method...")
                    try:
                        # Try to extract any readable text, even if fragmented
                        for page in pdf_reader.pages:
                            try:
                                # Try different text extraction methods
                                page_text = ""
                                
                                # Method 1: Standard extraction
                                try:
                                    page_text = page.extract_text()
                                except:
                                    pass
                                
                                # Method 2: Extract with different parameters
                                if not page_text.strip():
                                    try:
                                        page_text = page.extract_text(visitor_text=lambda text, cm, tm, fontDict, fontSize: text if text.strip() else "")
                                    except:
                                        pass
                                
                                # Method 3: Try to get any text from the page
                                if not page_text.strip():
                                    try:
                                        if hasattr(page, '_objects'):
                                            for obj in page._objects:
                                                if hasattr(obj, 'get_data'):
                                                    data = obj.get_data()
                                                    if isinstance(data, str) and len(data) > 10:
                                                        page_text += data + " "
                                    except:
                                        pass
                                
                                if page_text.strip():
                                    pdf_text += page_text + "\n"
                                    
                            except Exception as e:
                                print(f"Error in fallback extraction: {e}")
                                continue
                    except Exception as e:
                        print(f"Error in final fallback: {e}")
                
                # If still no text, return a more helpful error
                if not pdf_text.strip():
                    return jsonify({
                        'error': 'Could not extract text from this PDF. This might be because:\n1. The PDF contains only scanned images\n2. The PDF is password protected\n3. The PDF has an unusual format\n\nPlease try with a different PDF file or ensure the PDF contains selectable text.'
                    }), 400

            # Clean up the saved file - add a small delay and retry logic
            try:
                time.sleep(0.1)  # Small delay to ensure file handle is released
                os.remove(filepath)
            except PermissionError:
                # If still locked, try again after a longer delay
                time.sleep(0.5)
                try:
                    os.remove(filepath)
                except:
                    pass  # If we still can't delete, continue anyway

            if not pdf_text.strip():
                return jsonify({'error': 'Could not extract text from PDF. The PDF might be image-based or empty.'}), 400

            
            # Call the API to get JSON from text
            api_key = os.getenv('API_KEY')
            if not api_key:
                return jsonify({'error': 'API key not found. Please set the API_KEY environment variable.'}), 500

            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}"
                },
                json={
                    "model": "gryphe/mythomax-l2-13b", # A capable model for this task
                    "messages": [
                        {
                            "role": "system",
                            "content": """You are an expert resume parser. Extract ALL information from the resume text and convert it into a comprehensive structured JSON format. 

REQUIRED FIELDS:
- name: Full name
- contact_information: {email, phone, linkedin, address (if available)}
- summary: Professional summary/objective (2-3 sentences)
- experience: Array of objects with {company, role, duration, location, responsibilities (array of strings), achievements (array of strings)}
- education: Array of objects with {institution, degree, graduation_year, cgpa/percentage, field_of_study}
- skills: Array of strings (technical skills, soft skills, tools, languages)
- certifications: Array of strings (professional certifications)
- awards: Array of strings (awards, honors, recognitions)
- projects: Array of objects with {name, description, technologies, duration}
- languages: Array of strings (spoken languages)
- interests: Array of strings (if mentioned)

EXTRACTION RULES:
1. Extract ALL skills mentioned, including technical tools, programming languages, frameworks
2. Get complete work experience with detailed responsibilities and achievements
3. Include all education details including GPA/percentage if mentioned
4. Extract any projects, internships, or volunteer work
5. Include certifications, awards, and recognitions
6. Extract soft skills and personal attributes
7. If information is missing, use empty arrays or empty strings
8. Be thorough and comprehensive in extraction

Return ONLY valid JSON, no other text."""
                        },
                        {
                            "role": "user",
                            "content": pdf_text
                        }
                    ]
                }
            )

            if response.status_code == 200:
                try:
                    response_data = response.json()
                    api_response = response_data['choices'][0]['message']['content']

                    # Try to parse the response as JSON, if it fails, use the raw text
                    try:
                        parsed_json = json.loads(api_response.strip())
                    except json.JSONDecodeError:
                        # If it's not valid JSON, create a simple JSON structure
                        parsed_json = {"raw_resume_text": api_response}

                    # Return JSON response directly
                    return jsonify({
                        'success': True,
                        'data': parsed_json
                    })

                except (KeyError, IndexError) as e:
                    return jsonify({'error': 'Failed to parse API response', 'details': str(e)}), 500
            else:
                return jsonify({'error': 'API call failed', 'status_code': response.status_code, 'details': response.text}), response.status_code

        except Exception as e:
            # Clean up file in case of error
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': 'An error occurred', 'details': str(e)}), 500

    return jsonify({'error': 'Invalid file type. Please upload a PDF.'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
