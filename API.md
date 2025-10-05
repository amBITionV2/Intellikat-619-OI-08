# API Documentation

## Resume Analyzer Service (Port 5001)

### Health Check
```
GET /health
```
Returns service health status.

**Response:**
```json
{
  "status": "healthy",
  "service": "resume-analyzer"
}
```

### Upload and Analyze Resume
```
POST /upload
```
Uploads a resume PDF and extracts structured data.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `resume` (PDF file)

**Response:**
```json
{
  "success": true,
  "data": {
    "name": "John Doe",
    "contact_information": {
      "email": "john@example.com",
      "phone": "+1234567890",
      "linkedin": "linkedin.com/in/johndoe"
    },
    "summary": "Experienced software engineer...",
    "experience": [
      {
        "company": "Tech Corp",
        "role": "Software Engineer",
        "duration": "2020-2024",
        "responsibilities": ["Developed web applications", "Led team projects"]
      }
    ],
    "education": [
      {
        "institution": "University",
        "degree": "Bachelor of Computer Science",
        "graduation_year": "2019"
      }
    ],
    "skills": ["Python", "JavaScript", "React"],
    "awards": ["Employee of the Year"],
    "certifications": ["AWS Certified"]
  }
}
```

## Resume Builder Service (Port 5000)

### Health Check
```
GET /health
```
Returns service health status.

**Response:**
```json
{
  "status": "healthy",
  "service": "resume-builder"
}
```

### Upload Resume Data
```
POST /upload
```
Uploads structured resume data for processing.

**Request:**
- Content-Type: `application/json`
- Body: Resume data object

**Response:**
```json
{
  "message": "Resume data uploaded successfully",
  "filename": "resume_uuid.json"
}
```

### Generate Tailored Resume
```
POST /generate
```
Generates a tailored resume PDF for a specific job.

**Request:**
- Content-Type: `application/json`
- Body:
```json
{
  "json_file": "resume_uuid.json",
  "job_role": "Software Engineer",
  "company": "Tech Corp",
  "job_description": "Looking for a software engineer..."
}
```

**Response:**
```json
{
  "message": "Resume generated successfully",
  "pdf_data": "base64_encoded_pdf_data",
  "filename": "tailored-resume-software-engineer-tech-corp.pdf"
}
```

## Error Responses

All endpoints may return error responses in the following format:

```json
{
  "error": "Error message description"
}
```

Common HTTP status codes:
- `200` - Success
- `400` - Bad Request (invalid input)
- `500` - Internal Server Error
