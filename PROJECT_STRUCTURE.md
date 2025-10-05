# JOBPLEXITY - Clean Project Structure

## 📁 Project Structure

```
JOBPLEXITY-5/
├── front-end/                          # React Frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── ui/                     # shadcn/ui components
│   │   │   └── PDFViewer.tsx          # PDF viewer modal
│   │   ├── services/
│   │   │   └── api.ts                 # API service layer
│   │   ├── utils/
│   │   │   ├── resumeParser.ts        # Resume extraction
│   │   │   └── resumeGenerator.ts     # Resume generation
│   │   └── pages/                     # React pages
│   └── package.json
├── backend-resume-anaalyser/          # Resume Analysis Backend
│   ├── main.py                        # Flask app for PDF analysis
│   ├── requirements.txt
│   └── .env
├── backend-tailured-resume-builder/   # Resume Generation Backend
│   ├── app.py                         # Flask app for PDF generation
│   ├── requirements.txt
│   └── .env
├── start-services-manual.bat          # Windows startup script
├── start-backends.sh                  # Linux/Mac startup script
├── test-complete-flow.html            # Complete flow test
├── README.md                          # Main documentation
└── PROJECT_STRUCTURE.md               # This file
```

## 🎯 Key Files

### **Frontend (React)**
- `front-end/src/services/api.ts` - Connects to both backends
- `front-end/src/utils/resumeParser.ts` - Handles resume extraction
- `front-end/src/utils/resumeGenerator.ts` - Handles resume generation
- `front-end/src/components/PDFViewer.tsx` - PDF display modal

### **Backend Services**
- `backend-resume-anaalyser/main.py` - AI-powered PDF analysis
- `backend-tailured-resume-builder/app.py` - AI-powered PDF generation

### **Startup & Testing**
- `start-services-manual.bat` - Start all services (Windows)
- `test-complete-flow.html` - Test complete flow in browser

## 🔄 Data Flow

1. **PDF Upload** → `backend-resume-anaalyser` → **JSON Data**
2. **JSON + Job Details** → `backend-tailured-resume-builder` → **PDF**
3. **PDF** → **Frontend Modal** → **View/Download**

## 🚀 Quick Start

1. **Start Services**: `.\start-services-manual.bat`
2. **Test Flow**: Open `test-complete-flow.html`
3. **Use App**: Go to http://localhost:5173

## 📋 Clean Structure Benefits

- ✅ **No redundant files** - Only essential files kept
- ✅ **Clear separation** - Frontend, backends, and tests
- ✅ **Single test file** - Complete flow testing
- ✅ **Consolidated docs** - All info in README.md
- ✅ **Easy to understand** - Clear file purposes
