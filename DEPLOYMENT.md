# Deployment Guide

## Production Deployment Checklist

### 1. Environment Setup

- [ ] Set up production environment variables
- [ ] Configure API keys securely
- [ ] Set up proper logging
- [ ] Configure CORS for production domains

### 2. Backend Services

#### Resume Analyzer Service
- [ ] Deploy to production server (e.g., AWS EC2, DigitalOcean)
- [ ] Use production WSGI server (Gunicorn)
- [ ] Set up reverse proxy (Nginx)
- [ ] Configure SSL certificates
- [ ] Set up monitoring and logging

#### Resume Builder Service
- [ ] Deploy to production server
- [ ] Use production WSGI server (Gunicorn)
- [ ] Set up reverse proxy (Nginx)
- [ ] Configure SSL certificates
- [ ] Set up monitoring and logging

### 3. Frontend

- [ ] Build production bundle: `npm run build`
- [ ] Deploy to CDN or static hosting (Vercel, Netlify, AWS S3)
- [ ] Configure environment variables for production API endpoints
- [ ] Set up proper caching headers

### 4. Database (if needed)

- [ ] Set up production database
- [ ] Configure connection pooling
- [ ] Set up backups
- [ ] Configure monitoring

### 5. Security

- [ ] Enable HTTPS
- [ ] Configure CORS properly
- [ ] Set up rate limiting
- [ ] Implement API authentication if needed
- [ ] Secure API keys and secrets

### 6. Monitoring

- [ ] Set up application monitoring (e.g., Sentry)
- [ ] Configure uptime monitoring
- [ ] Set up log aggregation
- [ ] Configure alerting

## Production Commands

### Backend Services with Gunicorn

```bash
# Resume Analyzer
cd backend-resume-anaalyser
gunicorn -w 4 -b 0.0.0.0:5001 main:app

# Resume Builder
cd backend-tailured-resume-builder
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Frontend Build

```bash
cd front-end
npm run build
```

## Environment Variables for Production

### Resume Analyzer
```bash
API_KEY=your_production_openrouter_api_key
FLASK_ENV=production
```

### Resume Builder
```bash
OPENROUTER_API_KEY=your_production_openrouter_api_key
FLASK_ENV=production
```

### Frontend
```bash
VITE_API_ANALYZER_URL=https://your-domain.com:5001
VITE_API_BUILDER_URL=https://your-domain.com:5000
```

## Docker Deployment (Optional)

Create Dockerfiles for containerized deployment:

```dockerfile
# Backend Dockerfile example
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## Load Balancing

For high traffic, consider:
- Load balancer (AWS ALB, Nginx)
- Multiple backend instances
- Database connection pooling
- CDN for static assets
