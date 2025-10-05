from flask import Flask, request, render_template, jsonify, send_file
from flask_cors import CORS
import json
import os
import uuid
import requests
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT, TA_CENTER

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# OpenRouter API configuration
OPENROUTER_API_KEY = "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"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'resume-builder'})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_resume():
    try:
        data = request.get_json()
        
        if not data or 'resume' not in data:
            return jsonify({'error': 'No resume data provided'}), 400

        resume_data = data['resume']
        
        # Generate unique filename
        filename = f"resume_{uuid.uuid4()}.json"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save the resume data as JSON file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(resume_data, f, indent=2, ensure_ascii=False)

        return jsonify({'message': 'Resume data uploaded successfully', 'filename': filename}), 200

    except Exception as e:
        return jsonify({'error': f'Failed to upload resume data: {str(e)}'}), 500

@app.route('/generate', methods=['POST'])
def generate_resume():
    try:
        data = request.get_json()
        json_file = data.get('json_file')
        job_role = data.get('job_role')
        company = data.get('company')
        job_description = data.get('job_description', '')

        if not all([json_file, job_role, company]):
            return jsonify({'error': 'Missing required fields'}), 400

        # Read the JSON file
        json_path = os.path.join(app.config['UPLOAD_FOLDER'], json_file)
        with open(json_path, 'r') as f:
            resume_data = json.load(f)

        # Tailor the resume for the specific job
        tailored_resume = tailor_resume_for_job(resume_data, job_role, company, job_description)

        # Generate PDF
        pdf_path = generate_pdf(tailored_resume, f"resume_{uuid.uuid4()}")

        # Read the PDF file and convert to base64
        import base64
        try:
            with open(pdf_path, 'rb') as pdf_file:
                pdf_data = pdf_file.read()
                pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')
            
            # Verify PDF data
            if len(pdf_data) < 1000:  # PDF should be at least 1KB
                return jsonify({'error': 'Generated PDF is too small, may be corrupted'}), 500
            
            # Clean up the temporary PDF file
            try:
                os.remove(pdf_path)
            except:
                pass

            return jsonify({
                'message': 'Resume generated successfully',
                'pdf_data': pdf_base64,
                'filename': f'tailored-resume-{job_role.replace(" ", "-")}-{company.replace(" ", "-")}.pdf'
            }), 200
            
        except Exception as e:
            return jsonify({'error': f'Failed to read PDF file: {str(e)}'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_pdf(filename):
    try:
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': 'File not found'}), 404

def tailor_resume_for_job(resume_data, job_role, company, job_description=""):
    """Use AI to tailor the resume for the specific job role and company"""
    try:
        # Create the prompt for tailoring
        prompt = f"""
        I need you to tailor this resume for a {job_role} position at {company}.

        Job Description:
        {job_description if job_description else f"Looking for a {job_role} position at {company}"}

        Original resume data:
        {json.dumps(resume_data, indent=2)}

        Please analyze the job requirements for a {job_role} at {company} and modify the resume to:
        1. Highlight the most relevant experience and skills for this role
        2. Customize the professional summary to align with the job requirements
        3. Reorder experience bullets to emphasize relevant achievements
        4. Include only the most relevant skills for this position
        5. Keep all personal information and education the same

        Return the modified resume as JSON in the same format.
        """

        headers = {
            'Authorization': f'Bearer {OPENROUTER_API_KEY}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://your-app.com',
            'X-Title': 'Resume Tailoring App'
        }

        payload = {
            'model': 'anthropic/claude-3.5-sonnet',
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 2000,
            'temperature': 0.7
        }

        response = requests.post(f'{OPENROUTER_BASE_URL}/chat/completions', json=payload, headers=headers)

        if response.status_code == 200:
            result = response.json()
            tailored_content = result['choices'][0]['message']['content']

            # Try to extract JSON from the response
            try:
                # Find JSON in the response (Claude might add some text)
                json_start = tailored_content.find('{')
                json_end = tailored_content.rfind('}') + 1
                if json_start != -1 and json_end > json_start:
                    json_str = tailored_content[json_start:json_end]
                    return json.loads(json_str)
            except:
                pass
    except Exception as e:
        # Log error but don't crash the application
        pass

    # If AI tailoring fails, return original data
    return resume_data

def generate_latex_resume(resume_data):
    """Generate LaTeX content for the resume"""
    latex_template = """
\\documentclass[11pt,a4paper]{article}
\\usepackage[utf8]{inputenc}
\\usepackage[T1]{fontenc}
\\usepackage{geometry}
\\usepackage{setspace}
\\usepackage{xcolor}
\\usepackage{titlesec}
\\usepackage{enumitem}

\\geometry{
    left=0.75in,
    right=0.75in,
    top=0.5in,
    bottom=0.5in
}

\\definecolor{primary}{RGB}{0, 123, 255}
\\definecolor{textgray}{RGB}{102, 102, 102}

\\titleformat{\\section}{\\large\\bfseries\\color{primary}}{}{0em}{}[\\titlerule]
\\titlespacing{\\section}{0pt}{12pt}{6pt}

\\setlist[itemize]{leftmargin=*}

\\renewcommand{\\labelitemi}{●}

\\begin{document}

% Header
\\begin{center}
    \\Huge \\color{primary} \\textbf{ {name} } \\\\
    \\vspace{0.2cm}
    \\large \\color{textgray}
    {email} | {phone} | {linkedin} \\\\
    \\vspace{0.3cm}
\\end{center}

% Summary
\\section{Summary}
{summary}

% Experience
\\section{Professional Experience}
{experience_section}

% Education
\\section{Education}
{education_section}

% Skills
\\section{Skills}
{skills_section}

% Awards & Certifications
\\section{Awards & Certifications}
{awards_section}

\\end{document}
"""

    # Generate experience section
    experience_section = ""
    for exp in resume_data.get('experience', []):
        experience_section += f"""
\\textbf{{{exp['role']}}} | {exp['company']} | {exp['duration']}
\\begin{itemize}
"""
        for resp in exp.get('responsibilities', []):
            experience_section += f"\\item {resp}\n"
        experience_section += "\\end{itemize}\n\\vspace{0.2cm}\n"

    # Generate education section
    education_section = ""
    for edu in resume_data.get('education', []):
        education_section += f"""
\\textbf{{{edu['degree']}}} | {edu['institution']} | {edu['graduation_year']}
"""
        if 'cgpa' in edu:
            education_section += f"CGPA: {edu['cgpa']}\n"
        if 'percentage' in edu:
            education_section += f"Percentage: {edu['percentage']}\n"
        education_section += "\\vspace{0.2cm}\n"

    # Generate skills section
    skills = resume_data.get('skills', [])
    skills_text = ', '.join(skills)
    skills_section = skills_text

    # Generate awards section
    awards_section = ""
    awards = resume_data.get('awards', [])
    if awards:
        for award in awards:
            awards_section += f"• {award}\n"

    certifications = resume_data.get('certifications', [])
    if certifications and any(certifications):
        if awards_section:
            awards_section += "\n"
        awards_section += "\\textbf{Certifications:}\n"
        for cert in certifications:
            if cert:
                awards_section += f"• {cert}\n"

    # Fill in the template
    latex_content = latex_template.format(
        name=resume_data.get('name', ''),
        email=resume_data.get('contact_information', {}).get('email', ''),
        phone=resume_data.get('contact_information', {}).get('phone', ''),
        linkedin=resume_data.get('contact_information', {}).get('linkedin', ''),
        summary=resume_data.get('summary', ''),
        experience_section=experience_section,
        education_section=education_section,
        skills_section=skills_section,
        awards_section=awards_section
    )

    return latex_content

def generate_pdf(resume_data, filename):
    """Generate PDF from resume data using ReportLab"""
    pdf_path = f"{filename}.pdf"

    # Create the PDF document
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=24,
        textColor=HexColor('#007BFF'),
        alignment=TA_CENTER,
        spaceAfter=12
    )

    section_header_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading1'],
        fontSize=14,
        textColor=HexColor('#007BFF'),
        spaceAfter=6,
        spaceBefore=12
    )

    normal_style = styles['Normal']
    contact_style = ParagraphStyle(
        'Contact',
        parent=styles['Normal'],
        fontSize=12,
        textColor=HexColor('#666666'),
        alignment=TA_CENTER,
        spaceAfter=12
    )

    # Build the content
    content = []

    # Header with name
    content.append(Paragraph(resume_data.get('name', ''), title_style))
    content.append(Spacer(1, 0.2 * inch))

    # Contact information
    contact_info = resume_data.get('contact_information', {})
    contact_text = f"{contact_info.get('email', '')} | {contact_info.get('phone', '')} | {contact_info.get('linkedin', '')}"
    content.append(Paragraph(contact_text, contact_style))
    content.append(Spacer(1, 0.3 * inch))

    # Summary
    content.append(Paragraph('Summary', section_header_style))
    content.append(Paragraph(resume_data.get('summary', ''), normal_style))
    content.append(Spacer(1, 0.2 * inch))

    # Experience
    content.append(Paragraph('Professional Experience', section_header_style))

    for exp in resume_data.get('experience', []):
        # Job title and company
        job_title = f"<b>{exp['role']}</b> | {exp['company']} | {exp['duration']}"
        content.append(Paragraph(job_title, normal_style))

        # Responsibilities as bullet points
        if exp.get('responsibilities'):
            bullet_items = [ListItem(Paragraph(resp, normal_style)) for resp in exp['responsibilities']]
            content.append(ListFlowable(bullet_items, bulletType='bullet', start='•'))
        content.append(Spacer(1, 0.2 * inch))

    # Education
    content.append(Paragraph('Education', section_header_style))

    for edu in resume_data.get('education', []):
        edu_text = f"<b>{edu['degree']}</b> | {edu['institution']} | {edu['graduation_year']}"
        content.append(Paragraph(edu_text, normal_style))

        if 'cgpa' in edu:
            content.append(Paragraph(f"CGPA: {edu['cgpa']}", normal_style))
        if 'percentage' in edu:
            content.append(Paragraph(f"Percentage: {edu['percentage']}", normal_style))

        content.append(Spacer(1, 0.2 * inch))

    # Skills
    content.append(Paragraph('Skills', section_header_style))
    skills = resume_data.get('skills', [])
    skills_text = ', '.join(skills)
    content.append(Paragraph(skills_text, normal_style))
    content.append(Spacer(1, 0.2 * inch))

    # Awards & Certifications
    content.append(Paragraph('Awards & Certifications', section_header_style))

    awards = resume_data.get('awards', [])
    for award in awards:
        content.append(Paragraph(f"• {award}", normal_style))

    certifications = resume_data.get('certifications', [])
    for cert in certifications:
        if cert:
            content.append(Paragraph(f"• {cert}", normal_style))

    # Build the PDF
    doc.build(content)
    return pdf_path

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
