from fastapi import FastAPI, UploadFile, File
import pdfplumber
import io 
app = FastAPI()

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    # Your code to handle the uploaded file
    # For example, you can save the file to disk
    # with open(file.filename, "wb") as f:
    #     f.write(file.file.read())
    # return {"filename": file.filename}
    file_content = await file.read()

    file_object = io.BytesIO(file_content)

    with pdfplumber.open(file_object) as pdf:
        # Extract text from each page
        extracted_text = []
        for page in pdf.pages:
            extracted_text.append(page.extract_text())

    return {"text": extracted_text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
