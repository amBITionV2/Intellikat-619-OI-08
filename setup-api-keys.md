# API Keys Setup

## Required API Keys

### 1. Resume Analyzer (backend-resume-anaalyser)
Create `backend-resume-anaalyser/.env`:
```
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### 2. Resume Builder (backend-tailured-resume-builder)  
Create `backend-tailured-resume-builder/.env`:
```
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

## Get API Keys

1. Go to https://openrouter.ai/
2. Sign up for free account
3. Get your API key
4. Add to both .env files

## Test API Keys

Run the test to verify:
```bash
# Test resume analyzer
curl http://localhost:5001/health

# Test resume builder  
curl http://localhost:5000/health
```

Both should return: `{"status": "healthy", "service": "..."}`
