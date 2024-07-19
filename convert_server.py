from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import os

class ConvertRequest(BaseModel):
    input_file: str
    output_dir: str

app = FastAPI()

@app.post("/convert")
async def convert(request: ConvertRequest):
    input_file = request.input_file
    output_dir = request.output_dir

    if not os.path.isfile(input_file):
        raise HTTPException(status_code=400, detail="Input file does not exist")

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = os.path.join(output_dir, base_name + '.docx')

    libreoffice_path = "/usr/bin/libreoffice"
    command = [
        libreoffice_path,
        '--headless',
        '--convert-to', 'docx',
        input_file,
        '--outdir', output_dir
    ]

    subprocess.run(command, check=True)

    if not os.path.isfile(output_file):
        raise HTTPException(status_code=500, detail="Failed to convert file")

    return {"output_file": output_file}
