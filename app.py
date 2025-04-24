from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from transformers import pipeline

# Initialize FastAPI app
app = FastAPI()

# Serve static files (index.html and styles.css)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_index():
    return FileResponse("static/index.html")

# Initialize the summarizer model
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# Input model for the request
class TextRequest(BaseModel):
    text: str

# Summarize endpoint
@app.post("/summarize/")
async def summarize(request: TextRequest):
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    try:
        summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
        return {"summary": summary[0]['summary_text']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
