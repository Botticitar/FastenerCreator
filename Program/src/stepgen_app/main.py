from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
import os
import io
import zipfile

from stepgen_app import ScrewRequest, WasherRequest, AssemblyRequest, StepGenerator

app = FastAPI(title="Engineering STEP Generator")

@app.get("/")
def read_root():
    return {"status": "Server is running. Go to /docs for the GUI"}

#Bolt Endpoint
@app.post("/generate/screw")
async def create_screw(data: ScrewRequest):
    try:
        file_path = StepGenerator.screw(data)
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=500, detail="CAD generation failed")

        return FileResponse(
            path=file_path, 
            filename="generated_screw.step",
            media_type='application/step'
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Washer Endpoint
@app.post("/generate/washer")
async def create_washer(data: WasherRequest):
    try:
        file_path = StepGenerator.washer(data)
        
        return FileResponse(
            path=file_path, 
            filename="generated_washer.step",
            media_type='application/step'
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/generate/assembly")
async def generate_set(data: AssemblyRequest):
    s_path = StepGenerator.screw(data.screw)
    w_path = StepGenerator.washer(data.washer)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        zip_file.write(s_path, arcname="bolt.step")
        zip_file.write(w_path, arcname="washer.step")
    
    zip_buffer.seek(0)

    return StreamingResponse(
        zip_buffer, 
        media_type="application/x-zip-compressed",
        headers={"Content-Disposition": "attachment; filename=assembly.zip"}
    )