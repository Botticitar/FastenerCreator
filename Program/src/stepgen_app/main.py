from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os

from stepgen_app import ScrewRequest, WasherRequest, StepGenerator

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