# -*- coding: utf-8 -*-
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import pandas as pd
import csv
import os
import tempfile
from datetime import datetime
from process_controller import NERProcessorController
import codecs

app = FastAPI()
process_controller = NERProcessorController()

def preprocess_bytes(content):
    try:
        decoded_content = content.decode('windows-1252').splitlines()
        return decoded_content
    except UnicodeDecodeError:
        print("Unicode replacement")
        return codecs.decode(content, 'windows-1252', 'ignore').splitlines()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    content = await file.read()

    content = preprocess_bytes(content)

    reader = csv.reader(content)
    rows = [row for row in reader]
    modified_rows = process_controller.process_sentence_list(rows, False)

    with tempfile.NamedTemporaryFile(delete=False, suffix='.csv', newline='', mode='w', encoding='windows-1252') as tmp_file:
        writer = csv.writer(tmp_file)
        writer.writerows(modified_rows)

    original_filename, extension = os.path.splitext(file.filename)

    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    new_filename = f'anonymized_{original_filename}_{current_datetime}.csv'

    tmp_file_path = tmp_file.name
    new_file_path = os.path.join(os.path.dirname(tmp_file_path), new_filename)
    os.rename(tmp_file_path, new_file_path)

    return FileResponse(new_file_path, filename=new_filename)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
