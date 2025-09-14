from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from resume_parser import parse_resume
import os
import tempfile

app = FastAPI(title="Alumni Resume Parser with Llama 3", version="1.0")

@app.post("/parse-resume/")
async def parse_resume_endpoint(file: UploadFile = File(...)):
    # Validate file type
    if not file.filename.endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files allowed")

    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename[-4:]) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        result = parse_resume(tmp_path)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing resume: {str(e)}")
    finally:
        os.unlink(tmp_path)  # Clean up temp file

@app.get("/")
def root():
    return {"message": "Welcome to Alumni Resume Parser with Llama 3! POST /parse-resume/ with a PDF or DOCX"}